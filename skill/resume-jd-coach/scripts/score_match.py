#!/usr/bin/env python3
"""Deterministic scoring, rubric lock, multilingual negation-aware ATS audit, and round-diff engine for resume-jd-coach (v2.1).

Supports 4 native languages: Korean (ko), English (en), Simplified Chinese (zh), Japanese (ja).
Zero external dependencies (Python 3 Standard Library only).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CATEGORY_ORDER = ("must_have", "portfolio_impact", "preferred", "ats_framing")

CATEGORY_LABELS: dict[str, dict[str, Any]] = {
    "ko": {
        "must_have": "필수 자격 & 핵심 직무",
        "portfolio_impact": {
            "portfolio": "포트폴리오 증빙 & 성과",
            "resume_only": "직무 증빙 & 정량 성과",
        },
        "preferred": "우대 사항",
        "ats_framing": "JD 키워드 & 포지셔닝",
    },
    "en": {
        "must_have": "Must-Have & Core Duties",
        "portfolio_impact": {
            "portfolio": "Portfolio Proof & Impact",
            "resume_only": "Work Proof & Measurable Impact",
        },
        "preferred": "Preferred & Bonus",
        "ats_framing": "ATS Keywords & Role Framing",
    },
    "zh": {
        "must_have": "核心任职要求与主要职责",
        "portfolio_impact": {
            "portfolio": "作品集佐证与量化成果",
            "resume_only": "项目/工作佐证与量化成果",
        },
        "preferred": "加分项与优先条件",
        "ats_framing": "JD 关键词与岗位定位",
    },
    "ja": {
        "must_have": "必須要件・コア業務",
        "portfolio_impact": {
            "portfolio": "ポートフォリオ実績・定量成果",
            "resume_only": "職務実績・定量成果",
        },
        "preferred": "歓迎要件",
        "ats_framing": "JDキーワード・ポジション訴求",
    },
}

I18N: dict[str, dict[str, Any]] = {
    "ko": {
        "unit_pp": "%p",
        "sep": " · ",
        "doc_noun": {"portfolio": "이력서/포트폴리오", "resume_only": "이력서"},
        "default_target": "타깃 채용공고",
        "badges": {
            "PASS": "✅ **PASS** (지원 준비 완료)",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK** (합격선 도달 · 핵심 필수요건 위험 경고)",
            "REVISE": "🔁 **REVISE** (보완 후 재검토 필요)",
        },
        "status_badges": ("우수", "양호", "보강 필요", "취약"),
        "report_title": "# 채용공고 일치율 진단 — Round {round} ({target})",
        "overall_score": "- **종합 일치율:** **{score}%** / 합격 기준 **{threshold}%** — {badge}",
        "round_delta": "- **직전 라운드 대비 (Round {prev_r} → {curr_r}):** `{prev_s}% → {curr_s}% ({sign}{delta}{u})`",
        "gap_to_pass": "- **합격선까지 남은 점수:** `+{gap}{u}`",
        "proj_single": "- **표현·증빙 보강만으로 도달 가능 점수:** `{lo}%` (보강 가능 폭 `+{uplift}{u}`)",
        "proj_range": "- **정직한 도달 가능 점수 범위:** `{lo}%` (표현 보강 확실치) ~ `{hi}%` (유사·전이 역량 최대 `STRONG_PARTIAL` 반영 시)",
        "must_have_pct": "- **필수 자격(Must-Have) 충족률:** `{pct}%`",
        "ats_coverage": "- **ATS 핵심 키워드 커버리지:** `{matched}/{total}` (`{pct}%`)",
        "rubric_hash": "- **Rubric Lock Hash:** `{hash}`",
        "cat_heading": "## 영역별 상세 점수",
        "cat_table_header": "| 평가 영역 | 배점 비중 | 충족률 | 획득 점수 | Round Δ | 상태 |",
        "knockout_warn": "> **핵심 필수 요건(Knockout) 위험 감지 (`MISSING` 또는 `WEAK`):** 실제 보유 역량이라면 구체적 프로젝트 근거로 반드시 보강해 주세요.",
        "quote_audit_note": "> **원문 근거 자동 검증 참고:** `{ids}` 항목의 `evidence_quote`가 제출 문서 원문과 완전히 일치하지 않습니다. 원문 그대로 발췌했는지 재확인하세요.",
        "diff_heading": "## Round {prev_r} → Round {curr_r} 변화 요약",
        "improved_hdr": "- **개선/해결된 항목:**",
        "improved_none": "- **개선/해결된 항목:** 없음",
        "regressed_hdr": "- **⚠️ 점수 하락 항목 (의도치 않은 삭제 여부 확인):**",
        "stalled_hdr": "- **정체 항목 (보완 가능 항목 2라운드 이상 `<= PARTIAL` 유지):**",
        "stalled_line": "  - `{id}` {title} (`{grade}`, {streak}R, `{gap_type}`, 최대 `+{uplift}{u}`)",
        "priority_heading": "## 우선순위 보완 가이드 (직접 수정 포인트)",
        "gap_sections": [
            ("expression_gap", "🎯 표현·증빙 보강 (빠른 점수 상승 가능)"),
            ("transferable_gap", "🌉 유사·전이 역량 연결 필요"),
            ("true_gap", "🧭 실제 미보유 역량 점검 (창작·과장 금지)"),
        ],
        "stall_tag": " *(⚠️ {streak}R 정체)*",
        "item_line": "{idx}. **`{id}` {title}**{ko_tag}{stall_tag} — 현재 `{grade}` · 보완 시 최대 **`+{uplift}{u}`**",
        "evidence_present": "   - **현재 근거{src}:** \"{quote}\"",
        "evidence_missing": "   - **현재 근거:** 제출 문서에서 확인되지 않음",
        "revision_dir": "   - **수정 포인트:** {hint}",
        "ats_heading": "## JD 키워드 점검 (ATS 스캔)",
        "contra_warn": "> **문서 내 자기모순 키워드 경고 (ATS 점수 0점 처리):** {terms} 키워드가 '보유/스킬' 문맥과 '미경험/부정' 문맥에 동시에 등장하여 매칭 점수에서 제외되었습니다. 서류 신뢰도를 위해 실제 미보유 항목은 스킬란에서 제거하세요.",
        "missing_must": "- **필수 키워드 미반영:** {fmt}",
        "missing_pref": "- **우대 키워드 미반영:** {fmt}",
        "negated_note": "- *참고: {terms} 키워드는 미경험/부정 문맥에서만 확인되어 매칭에서 정확히 제외되었습니다.*",
        "ats_tip": "- *실제 경험·사용 사실이 있는 키워드만 구체적 프로젝트 맥락 안에 반영하세요. 근거 없는 스킬 나열은 `WEAK(0.25)` 상한이 적용됩니다.*",
        "mission_reach": "## 이번 라운드 핵심 미션 (최단 {threshold}% 돌파 TOP 3)",
        "mission_unreach": "## 최대 보강 가능 항목 (표현·유사경험 보강만으로 {threshold}% 단독 도달 어려움)",
        "gain_transferable": "유사경험 현실 상한 `+{cap}{u}` (FULL 기준 `+{full}{u}`)",
        "gain_full": "최대 `+{full}{u}`",
        "honest_fit_only": (
            "> **정직한 직무 적합도 안내:** 남은 미충족 항목이 모두 실제 미보유 역량(`true_gap`)입니다. "
            "표현 수정만으로 합격선을 인위적으로 맞추려 하기보다, 소규모 실전 포트폴리오 보강 또는 보유 강점이 더 잘 맞는 공고 병행 지원을 권장합니다."
        ),
        "honest_fit_capped": (
            "> **정직한 직무 적합도 안내:** 실제 미보유 역량(`true_gap`)으로 인해 표현·유사경험 보강을 모두 반영해도 최대 도달 가능 점수가 `{hi}%`(합격선 `{threshold}%` 미만)입니다. "
            "허위 창작 없이 현재 경력을 정리하는 한편, 보유 강점에 더 부합하는 공고 병행 지원이나 실전 역량 보강을 권장합니다."
        ),
        "honest_fit_knockout": (
            "> **정직한 직무 적합도 안내:** 다른 항목 보강으로 종합 점수는 `{hi}%`까지 올릴 수 있으나, 핵심 필수 요건(Knockout) 중 실제 미보유 역량(`true_gap`)이 존재합니다. "
            "허위 기재 없이 해당 요건의 실제 보완 가능성이나 대안 공고 병행 지원을 함께 검토하세요."
        ),
        "grace_offer_hdr": "> **보조 모드(Grace) 제안 (권장 시작: Tier {tier}):** {reasons}",
        "grace_offer_body": (
            "> 직접 더 다듬어 보셔도 좋고, 막히는 항목이 있다면 **1단계(질문+뼈대) / 2단계(사실 기반 표현 A·B안) / 3단계(특정 항목 공동 초안)** 중 원하시는 단계로 바로 보조해 드릴 수 있습니다."
        ),
        "grace_reason_stalled": "동일 보완 가능 항목이 2라운드 이상 정체됨: {names}",
        "grace_reason_low_gain": "직전 라운드 대비 점수 상승폭이 +3.0%p 미만 ({delta})",
        "cta_revise": "*위 포인트를 반영해 {doc}를 직접 수정하신 뒤 **Round {next_r}** 재평가를 요청해 주세요. 막히는 항목이 있으면 언제든 보조 모드(Grace 1~3단계)를 요청하실 수 있습니다.*",
        "cta_pass_risk": "*종합 점수는 합격선을 넘겼습니다. 다만 위 Knockout 필수요건 경고를 확인하신 뒤, 실제 보유 역량이라면 간단히 반영해 최종 재점검하시는 것을 권장합니다.*",
        "cta_pass": "*축하합니다! 잠금 루브릭 기준 합격선을 돌파했으며 핵심 Knockout 누락도 없습니다. 강점 항목을 면접 핵심 어필 포인트로 활용해 보세요.*",
        "cta_pass_regression_note": "*참고: 합격선을 넘겼지만 위 점수 하락 항목(`{ids}`)에 의도치 않은 삭제가 없는지 제출 전 한 번 더 확인하세요.*",
    },
    "en": {
        "unit_pp": "pp",
        "sep": " · ",
        "doc_noun": {"portfolio": "resume/portfolio", "resume_only": "resume"},
        "default_target": "Target JD",
        "badges": {
            "PASS": "✅ **PASS** (Ready to Apply)",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK** (Threshold Met · Knockout Requirement Risk)",
            "REVISE": "🔁 **REVISE** (Self-Revision Recommended)",
        },
        "status_badges": ("Strong", "Solid", "Needs Work", "Weak"),
        "report_title": "# JD Match Diagnostic — Round {round} ({target})",
        "overall_score": "- **Overall Match Score:** **{score}%** / Pass Threshold **{threshold}%** — {badge}",
        "round_delta": "- **Round-over-Round (Round {prev_r} → {curr_r}):** `{prev_s}% → {curr_s}% ({sign}{delta} {u})`",
        "gap_to_pass": "- **Gap to Pass:** `+{gap} {u}`",
        "proj_single": "- **Honest Reachable Score (Expression Fixes):** `{lo}%` (actionable uplift `+{uplift} {u}`)",
        "proj_range": "- **Honest Reachable Score Range:** `{lo}%` (expression fixes only) ~ `{hi}%` (incl. transferable skills capped at `STRONG_PARTIAL`)",
        "must_have_pct": "- **Must-Have Attainment:** `{pct}%`",
        "ats_coverage": "- **ATS Keyword Coverage:** `{matched}/{total}` (`{pct}%`)",
        "rubric_hash": "- **Rubric Lock Hash:** `{hash}`",
        "cat_heading": "## Category Breakdown",
        "cat_table_header": "| Category | Weight | Attainment | Earned / Max | Round Δ | Status |",
        "knockout_warn": "> **Critical Knockout Risk Detected (`MISSING` or `WEAK`):** High risk of automated/initial screening rejection unless substantiated with concrete work evidence.",
        "quote_audit_note": "> **Quote Verification Audit:** Item(s) `{ids}` had non-verbatim or paraphrased `evidence_quote` against candidate text.",
        "diff_heading": "## Round {prev_r} → Round {curr_r} Progress Summary",
        "improved_hdr": "- **Improved / Resolved:**",
        "improved_none": "- **Improved / Resolved:** None",
        "regressed_hdr": "- **⚠️ Regressed Items (check for accidental deletions):**",
        "stalled_hdr": "- **Stalled Actionable Items (2+ consecutive rounds `<= PARTIAL`):**",
        "stalled_line": "  - `{id}` {title} (`{grade}`, {streak} rounds, `{gap_type}`, max `+{uplift} {u}`)",
        "priority_heading": "## Priority Revision Guide (Coach-First)",
        "gap_sections": [
            ("expression_gap", "🎯 Expression & Evidence Fixes (Fastest Score Gains)"),
            ("transferable_gap", "🌉 Transferable Experience Bridging"),
            ("true_gap", "🧭 True Capability Gaps (Zero Fabrication)"),
        ],
        "stall_tag": " *(⚠️ {streak} rounds stalled)*",
        "item_line": "{idx}. **`{id}` {title}**{ko_tag}{stall_tag} — Current `{grade}` · Up to **`+{uplift} {u}`**",
        "evidence_present": "   - **Current Evidence{src}:** \"{quote}\"",
        "evidence_missing": "   - **Current Evidence:** Not found in submitted documents",
        "revision_dir": "   - **Revision Direction:** {hint}",
        "ats_heading": "## JD Keywords Audit (ATS Lexical Scan)",
        "contra_warn": "> **Self-Contradictory Keyword Warning (0 ATS Credit Awarded):** {terms} appeared in BOTH positive (skills/claims) and negative (unexperienced) sections of the document and were excluded from ATS credit. Remove unverified claims to protect credibility.",
        "missing_must": "- **Missing Must Keywords:** {fmt}",
        "missing_pref": "- **Missing Preferred Keywords:** {fmt}",
        "negated_note": "- *Note: {terms} appeared only inside negative/unexperienced phrasing and were correctly excluded.*",
        "ats_tip": "- *Include only verified terms inside real project context; bare skills-list stuffing is capped at `WEAK (0.25)`.*",
        "mission_reach": "## Next Round Fastest Path Mission (Top 3)",
        "mission_unreach": "## Highest-Impact Fixes (Threshold {threshold}% Unlikely Without True Gaps)",
        "gain_transferable": "realistic cap `+{cap} {u}` (full `+{full} {u}`)",
        "gain_full": "up to `+{full} {u}`",
        "honest_fit_only": (
            "> **Honest Role-Fit Advisory:** All remaining gaps are `true_gap` items (zero actionable wording gaps left). "
            "Rather than fabricating missing qualifications, consider building a small genuine proof artifact or targeting better-aligned postings."
        ),
        "honest_fit_capped": (
            "> **Honest Role-Fit Advisory:** Due to genuine capability gaps (`true_gap`), even resolving every actionable expression/transferable gap caps your honest reachable score at `{hi}%` (below the `{threshold}%` threshold). "
            "Polish your verified experience honestly, and consider targeting roles aligned with your current strengths alongside medium-term upskilling."
        ),
        "honest_fit_knockout": (
            "> **Honest Role-Fit Advisory:** Although fixing actionable gaps could raise your aggregate score to `{hi}%`, at least one hard Knockout requirement is a genuine `true_gap`. "
            "Never fabricate missing knockouts; weigh whether real-world upskilling or parallel better-aligned postings make stronger sense."
        ),
        "grace_offer_hdr": "> **Grace Assistance Available (Suggested: Tier {tier}):** {reasons}",
        "grace_offer_body": (
            "> Keep revising on your own, or opt in to **Tier 1 (Questions + Skeleton) / Tier 2 (Fact-Grounded Options A·B) / Tier 3 (Targeted Pair-Draft)** whenever you feel stuck."
        ),
        "grace_reason_stalled": "Actionable item(s) stalled for 2+ rounds: {names}",
        "grace_reason_low_gain": "Round-over-round gain below +3.0 pp ({delta})",
        "cta_revise": "*Revise your {doc} based on the pointers above and submit for **Round {next_r}** re-evaluation. Ask for Grace coaching anytime if you get stuck.*",
        "cta_pass_risk": "*You cleared the overall threshold, but please review the Knockout Risk warning above before submitting.*",
        "cta_pass": "*Congratulations! Your application passed the locked rubric threshold with zero knockout risks.*",
        "cta_pass_regression_note": "*Note: Although you passed the threshold, please double-check the regressed item(s) (`{ids}`) above to ensure no valuable proof was accidentally removed.*",
    },
    "zh": {
        "unit_pp": "pp",
        "sep": " · ",
        "doc_noun": {"portfolio": "简历/作品集", "resume_only": "简历"},
        "default_target": "目标岗位 JD",
        "badges": {
            "PASS": "✅ **PASS**（已达标，可投递）",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK**（总分已达线 · 存在核心一票否决风险）",
            "REVISE": "🔁 **REVISE**（建议针对性修改后复评）",
        },
        "status_badges": ("优秀", "良好", "待加强", "薄弱"),
        "report_title": "# 岗位匹配度诊断报告 — 第 {round} 轮 ({target})",
        "overall_score": "- **综合匹配度：** **{score}%** / 通过线 **{threshold}%** — {badge}",
        "round_delta": "- **较上一轮变化 (第 {prev_r} 轮 → 第 {curr_r} 轮)：** `{prev_s}% → {curr_s}% ({sign}{delta} {u})`",
        "gap_to_pass": "- **距离通过线还差：** `+{gap} {u}`",
        "proj_single": "- **仅优化表达与佐证可达分数：** `{lo}%`（可提升空间 `+{uplift} {u}`）",
        "proj_range": "- **诚实可达分数区间：** `{lo}%`（仅表达与佐证优化）~ `{hi}%`（含可迁移经验，按 `STRONG_PARTIAL` 上限保守估算）",
        "must_have_pct": "- **核心任职要求达成率：** `{pct}%`",
        "ats_coverage": "- **ATS 核心关键词覆盖率：** `{matched}/{total}`（`{pct}%`）",
        "rubric_hash": "- **评分标准锁定哈希 (Rubric Hash)：** `{hash}`",
        "cat_heading": "## 各维度得分明细",
        "cat_table_header": "| 评估维度 | 权重 | 达成率 | 得分 / 满分 | 轮次 Δ | 状态 |",
        "knockout_warn": "> **核心硬性门槛（Knockout）风险预警（`MISSING` 或 `WEAK`）：** 若您实际具备该能力，务必补充具体项目上下文与量化佐证，否则极易在初筛阶段被淘汰。",
        "quote_audit_note": "> **原文佐证自动核验提示：** `{ids}` 项的 `evidence_quote` 与提交材料原文存在偏差，请核对是否为原文逐字摘录。",
        "diff_heading": "## 第 {prev_r} 轮 → 第 {curr_r} 轮 改进追踪",
        "improved_hdr": "- **已提升 / 已达标项：**",
        "improved_none": "- **已提升 / 已达标项：** 无",
        "regressed_hdr": "- **⚠️ 分数回退项（请检查是否误删原有佐证）：**",
        "stalled_hdr": "- **连续停滞的可优化项（连续 2 轮及以上处于 `<= PARTIAL`）：**",
        "stalled_line": "  - `{id}` {title}（`{grade}`，连续 {streak} 轮，`{gap_type}`，最高 `+{uplift} {u}`）",
        "priority_heading": "## 优先修改指南（教练式诊断 · 鼓励自主润色）",
        "gap_sections": [
            ("expression_gap", "🎯 表达与佐证补强（最快提分区）"),
            ("transferable_gap", "🌉 相关 / 可迁移经验衔接"),
            ("true_gap", "🧭 真实能力缺口核查（严禁虚构经历）"),
        ],
        "stall_tag": " *（⚠️ 连续 {streak} 轮停滞）*",
        "item_line": "{idx}. **`{id}` {title}**{ko_tag}{stall_tag} — 当前 `{grade}` · 补强后最高 **`+{uplift} {u}`**",
        "evidence_present": "   - **当前材料佐证{src}：** \"{quote}\"",
        "evidence_missing": "   - **当前材料佐证：** 提交材料中未检索到相关证据",
        "revision_dir": "   - **修改方向：** {hint}",
        "ats_heading": "## JD 关键词扫描（ATS 词法核查）",
        "contra_warn": "> **材料内部自相矛盾警告（不计 ATS 匹配得分）：** {terms} 同时出现在“已掌握技能”与“未接触/暂无经验”语境中，系统已取消其匹配得分。为维护可信度，请从技能栏中移除未实际掌握的条目。",
        "missing_must": "- **缺失核心关键词：** {fmt}",
        "missing_pref": "- **缺失加分关键词：** {fmt}",
        "negated_note": "- *说明：{terms} 仅出现在“未接触/暂无经验”等否定语境中，系统已准确将其排除在匹配之外。*",
        "ats_tip": "- *请仅将真实用过的技术或方法融入具体项目描述中；脱离项目的技能清单堆砌（如仅写“了解/熟悉”）最高仅计 `WEAK (0.25)`。*",
        "mission_reach": "## 下一轮最快冲线任务（突破 {threshold}% TOP 3）",
        "mission_unreach": "## 最高收益补强项（仅靠表达与迁移优化恐难单独达到 {threshold}%）",
        "gain_transferable": "迁移上限 `+{cap} {u}`（满分参考 `+{full} {u}`）",
        "gain_full": "最高 `+{full} {u}`",
        "honest_fit_only": (
            "> **诚实人岗匹配建议：** 剩余未达标项均为真实能力缺口（`true_gap`），已无可通过话术润色提升的空间。"
            "切勿虚构经历强凑分数，建议补充真实小型实战作品，或优先投递与现有优势更契合的岗位。"
        ),
        "honest_fit_capped": (
            "> **诚实人岗匹配建议：** 受核心真实能力缺口（`true_gap`）限制，即使补齐全部可优化表达与迁移项，诚实可达上限仍为 `{hi}%`（低于通过线 `{threshold}%`）。"
            "建议在如实打磨现有优势的同时，优先匹配契合度更高的岗位并规划中长期能力补齐。"
        ),
        "honest_fit_knockout": (
            "> **诚实人岗匹配建议：** 尽管补强其余表达项可将总分提升至 `{hi}%`，但仍存在属于真实能力缺口（`true_gap`）的核心一票否决项（Knockout）。"
            "切勿虚构经历，建议同时评估契合度更高的岗位或先补齐核心实战能力。"
        ),
        "grace_offer_hdr": "> **可选分级辅导（Grace 模式 · 建议起点：第 {tier} 级）：** {reasons}",
        "grace_offer_body": (
            "> 您可以继续自主修改；若在某个模块卡壳，随时可开启 **第 1 级（启发式提问+框架）/ 第 2 级（基于事实的 A/B 表达方案）/ 第 3 级（指定段落联合起草+事实核对表）**。"
        ),
        "grace_reason_stalled": "同一可优化项连续停滞 2 轮及以上：{names}",
        "grace_reason_low_gain": "较上一轮提分幅度不足 +3.0 pp（{delta}）",
        "cta_revise": "*请参考以上修改方向自行润色{doc}，完成后提交进入 **第 {next_r} 轮** 同标准复评。如遇写作瓶颈，随时可申请 Grace 1~3 级辅导。*",
        "cta_pass_risk": "*综合得分已超过通过线，但投递前请务必核查上方 Knockout 核心门槛风险；若实际具备该经历，建议快速补充后复验。*",
        "cta_pass": "*恭喜！您的{doc}已在锁定评分标准下顺利通过阈值，且无核心 Knockout 缺失。可将高分优势项整理为面试重点案例。*",
        "cta_pass_regression_note": "*提示：虽然总分已达标，但投递前请确认上方回退项（`{ids}`）是否被误删，以免损失原有亮点。*",
    },
    "ja": {
        "unit_pp": "pt",
        "sep": "・",
        "doc_noun": {"portfolio": "履歴書・職務経歴書・ポートフォリオ", "resume_only": "履歴書・職務経歴書"},
        "default_target": "対象求人票",
        "badges": {
            "PASS": "✅ **PASS**（応募準備完了）",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK**（基準点到達・必須要件リスク警告）",
            "REVISE": "🔁 **REVISE**（改善後の再評価を推奨）",
        },
        "status_badges": ("優秀", "良好", "要補強", "不足"),
        "report_title": "# 求人マッチ度診断レポート — Round {round} ({target})",
        "overall_score": "- **総合マッチ率:** **{score}%** / 合格基準 **{threshold}%** — {badge}",
        "round_delta": "- **前回ラウンド比 (Round {prev_r} → {curr_r}):** `{prev_s}% → {curr_s}% ({sign}{delta}{u})`",
        "gap_to_pass": "- **合格基準までの不足分:** `+{gap}{u}`",
        "proj_single": "- **表現・実績補強のみで到達可能な見込み:** `{lo}%`（改善余地 `+{uplift}{u}`）",
        "proj_range": "- **現実的な到達可能スコア範囲:** `{lo}%`（表現・実績補強のみ）〜 `{hi}%`（類似・転用経験の上限 `STRONG_PARTIAL` 反映時）",
        "must_have_pct": "- **必須要件（Must-Have）充足率:** `{pct}%`",
        "ats_coverage": "- **ATS重要キーワード網羅率:** `{matched}/{total}`（`{pct}%`）",
        "rubric_hash": "- **評価基準ロックハッシュ (Rubric Hash):** `{hash}`",
        "cat_heading": "## 領域別スコア内訳",
        "cat_table_header": "| 評価領域 | 配点比重 | 充足率 | 獲得点 / 満点 | Round Δ | 状態 |",
        "knockout_warn": "> **重要必須要件（Knockout）リスク警告（`MISSING` または `WEAK`）:** 実務経験をお持ちの場合は、具体的な担当範囲・成果とともに必ず職務経歴書へ明記してください。",
        "quote_audit_note": "> **原文引用の自動検証メモ:** `{ids}` 項目の `evidence_quote` が提出書類の原文と完全一致していません。原文通り抜粋されているか再確認してください。",
        "diff_heading": "## Round {prev_r} → Round {curr_r} 変化サマリー",
        "improved_hdr": "- **改善・解決された項目:**",
        "improved_none": "- **改善・解決された項目:** なし",
        "regressed_hdr": "- **⚠️ スコア低下項目（意図しない削除がないか確認）:**",
        "stalled_hdr": "- **停滞中の改善可能項目（2回連続 `<= PARTIAL`）:**",
        "stalled_line": "  - `{id}` {title}（`{grade}`・{streak}回連続・`{gap_type}`・最大 `+{uplift}{u}`）",
        "priority_heading": "## 優先改善ガイド（コーチング指針・ご自身でのブラッシュアップ推奨）",
        "gap_sections": [
            ("expression_gap", "🎯 表現・実績の言語化補強（最短スコアアップ領域）"),
            ("transferable_gap", "🌉 類似・転用可能スキルの接続"),
            ("true_gap", "🧭 未経験・不足要件の正直な確認（虚偽記載厳禁）"),
        ],
        "stall_tag": " *（⚠️ {streak}回連続停滞）*",
        "item_line": "{idx}. **`{id}` {title}**{ko_tag}{stall_tag} — 現在 `{grade}`・補強時最大 **`+{uplift}{u}`**",
        "evidence_present": "   - **現在の記載根拠{src}:** \"{quote}\"",
        "evidence_missing": "   - **現在の記載根拠:** 提出書類内に該当記載なし",
        "revision_dir": "   - **改善ポイント:** {hint}",
        "ats_heading": "## 求人キーワード点検（ATS語彙スキャン）",
        "contra_warn": "> **書類内の自己矛盾キーワード警告（ATS加点対象外）:** {terms} が「保有スキル」と「未経験・否定」の両方の文脈に出現したため、ATS加点から除外しました。書類の信頼性を守るため、実務未経験の項目はスキル一覧から削除してください。",
        "missing_must": "- **未反映の必須キーワード:** {fmt}",
        "missing_pref": "- **未反映の歓迎キーワード:** {fmt}",
        "negated_note": "- *補足: {terms} は未経験・否定文脈のみで検出されたため、正しくマッチ対象外として処理されました。*",
        "ats_tip": "- *実務経験のある用語のみ具体的なプロジェクト文脈に織り込んでください。根拠のないスキル羅列は `WEAK (0.25)` が上限となります。*",
        "mission_reach": "## 次回ラウンド最優先ミッション（最短 {threshold}% 突破 TOP 3）",
        "mission_unreach": "## 最大改善可能項目（表現・類似経験の補強のみでは {threshold}% 到達困難）",
        "gain_transferable": "類似経験上限 `+{cap}{u}`（FULL基準 `+{full}{u}`）",
        "gain_full": "最大 `+{full}{u}`",
        "honest_fit_only": (
            "> **正直なポジション適合度のご案内:** 残る未充足項目はすべて未経験・未保有要件（`true_gap`）です。"
            "表現調整のみで無理に基準点を目指さず、小規模な実践アウトプットの追加や強みが活きる他求人の併願をおすすめします。"
        ),
        "honest_fit_capped": (
            "> **正直なポジション適合度のご案内:** 必須の未経験要件（`true_gap`）があるため、改善可能な表現・類似経験をすべて補強しても現実的な上限は `{hi}%`（合格基準 `{threshold}%` 未満）にとどまります。"
            "虚偽記載は行わず、強みを活かせる他求人の併願や中長期的な実務補完も併せてご検討ください。"
        ),
        "honest_fit_knockout": (
            "> **正直なポジション適合度のご案内:** 他の改善可能項目の補強により総合スコアは `{hi}%` まで伸ばせる見込みですが、必須要件（Knockout）に未経験項目（`true_gap`）が含まれています。"
            "虚偽記載は厳禁とし、他求人の併願や実務補完計画も併せてご検討ください。"
        ),
        "grace_offer_hdr": "> **段階的サポート（Graceモード・推奨開始: Tier {tier}）:** {reasons}",
        "grace_offer_body": (
            "> ご自身での修正を継続いただいても構いませんし、手が止まった項目があれば **Tier 1（深掘り質問＋構成テンプレート）/ Tier 2（事実ベースの表現案A・B）/ Tier 3（対象箇所の共同ドラフト＋事実確認チェックリスト）** で支援可能です。"
        ),
        "grace_reason_stalled": "改善可能な同一項目が2回連続で停滞: {names}",
        "grace_reason_low_gain": "前回ラウンド比の上昇幅が +3.0pt 未満（{delta}）",
        "cta_revise": "*上記ポイントを踏まえて{doc}をご自身で修正のうえ、**Round {next_r}** の再評価をご依頼ください。詰まった箇所があればいつでも Grace（1〜3段階）サポートをお呼びいただけます。*",
        "cta_pass_risk": "*総合スコアは合格基準を満たしていますが、応募前に上記の必須要件（Knockout）警告をご確認ください。実務経験がある場合は追記後の最終チェックをおすすめします。*",
        "cta_pass": "*おめでとうございます！ロック済み評価基準で合格ラインを突破し、必須要件（Knockout）の欠落もありません。高評価ポイントを面接での強みとしてご活用ください。*",
        "cta_pass_regression_note": "*補足: 合格基準は満たしていますが、スコア低下項目（`{ids}`）に意図しない削除がないか応募前にご確認ください。*",
    },
}

DEFAULT_WEIGHTS = {
    "must_have": Decimal("45"),
    "portfolio_impact": Decimal("25"),
    "preferred": Decimal("15"),
    "ats_framing": Decimal("15"),
}

GRADE_MULTIPLIERS: dict[str, Decimal] = {
    "FULL": Decimal("1.00"),
    "STRONG_PARTIAL": Decimal("0.75"),
    "PARTIAL": Decimal("0.50"),
    "WEAK": Decimal("0.25"),
    "MISSING": Decimal("0.00"),
}

GRADE_SEQUENCE = ("MISSING", "WEAK", "PARTIAL", "STRONG_PARTIAL", "FULL")
KNOCKOUT_RISK_GRADES = {"MISSING", "WEAK"}
VALID_GAP_TYPES = {"expression_gap", "transferable_gap", "true_gap"}
VALID_KEYWORD_TIERS = {"must": Decimal("2"), "preferred": Decimal("1")}
VALID_LANGUAGES = {"ko", "en", "zh", "ja"}
VALID_DOMAIN_MODES = {"portfolio", "resume_only"}

OVERLY_BROAD_ALIASES = {
    # Korean
    "자동화", "취득", "상실", "업무", "관리", "개발", "분석", "협업", "운영",
    # English
    "automation", "management", "development", "analysis", "operations", "design", "collaboration",
    # Simplified Chinese
    "自动化", "管理", "开发", "分析", "运营", "协作", "设计", "业务", "沟通",
    # Japanese
    "自動化", "開発", "運用", "設計", "業務", "対応", "連携", "推進",
}

HANGUL_OR_CJK_RE = re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\u30fc]")
UNSPACED_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\u30fc]")
PURE_HANGUL_RE = re.compile(r"^[\uac00-\ud7af\s]+$")
PURE_KATAKANA_RE = re.compile(r"^[\u30a0-\u30ff\u30fc\s]+$")
ASCII_ALNUM_RE = re.compile(r"[A-Za-z0-9]")
# Capture numeric value plus optional magnitude/percent unit suffix so "5K -> 5M" or "5千 -> 5万" cannot bypass strict quotes
NUM_TOKEN_RE = re.compile(r"\d+(?:\.\d+)?(?:[%％]|[KMBkmb](?![A-Za-z])|[천만억千万亿億])?")

HEADING_DECORATION_PREFIX_RE = re.compile(r"^[\s#■●◆◇▼▽▶▷★☆【\[]+")
BULLET_OR_NUMBERED_RE = re.compile(r"^([-•*·・▪]|(?:\d+|[①-⑩])[.)、])\s*")

NEGATED_HEADING_RE = re.compile(
    r"("
    # Korean
    r"아직\s*해\s*보지\s*않은|해보지\s*않은|미경험|미보유|부족한\s*부분|한계\s*및\s*미경험|"
    # English
    r"what\s+i\s+haven'?t\s+done|not\s+yet\s+experienced|missing\s+skills|skill\s+gaps|"
    r"skills\s+to\s+develop|currently\s+learning|areas\s+for\s+growth|gaps\s*(?:&|and)\s*limitations|"
    # Simplified Chinese
    r"尚未接触|暂未接触|暂无经验|尚无经验|待学习|待提升|技能短板|缺乏经验|未掌握|目前尚未掌握|不足之处|未涉及领域|"
    # Japanese
    r"未経験(?:の領域|スキル|項目)?|未習得|今後の課題|学習予定|不足しているスキル|経験のない領域|まだ経験がない|キャッチアップ中|今後の学習テーマ"
    r")",
    flags=re.IGNORECASE,
)

SECTION_RESET_HEADING_RE = re.compile(
    r"^(=== SOURCE:|"
    # Korean
    r"경력|학력|프로젝트|포트폴리오|기술\s*스택|사용\s*기술|요약|프로필|자격|관련\s*배경|"
    # English
    r"(?:work|professional)\s+experience|work\s+history|experience|employment|education|projects?|portfolio|"
    r"(?:technical\s+)?skills?|core\s+competencies|summary|profile|background|certifications?|"
    # Simplified Chinese
    r"工作经历|工作经验|项目经历|项目经验|教育背景|教育经历|专业技能|核心技能|技术栈|个人简介|自我评价|作品集|荣誉奖项|资格证书|基本信息|"
    # Japanese
    r"職務要約|職務経歴|業務経歴|プロジェクト|保有スキル|スキル|技術スタック|学歴|資格|自己PR|ポートフォリオ|主な実績|業務内容)",
    flags=re.IGNORECASE,
)

PREFIX_NEGATION_RE = re.compile(
    r"("
    # English
    r"no\s+(?:[A-Za-z-]+\s+){0,3}experience|no\s+exposure|0\s+years?(?:\s+of)?|"
    r"limited\s+(?:experience|exposure)|exposure\s+only|familiarity\s+only|"
    r"not\s+(?:yet\s+)?(?:experienced|used|familiar)|never\s+(?:used|worked|built|deployed)|"
    r"haven'?t\s+(?:used|worked|built)|have\s+not\s+(?:used|worked|built)|"
    r"unfamiliar\s+with|lack\s+of|without\s+(?:[A-Za-z-]+\s+){0,2}experience|do\s+not\s+have|don'?t\s+have|"
    r"currently\s+learning|theoretical\s+(?:knowledge|only)|zero\s+experience|"
    # Simplified Chinese
    r"未接触|尚未接触|暂未接触|暂无.{0,12}(?:经验|实战|实践|项目)?|尚无.{0,12}(?:经验|实战|实践)?|"
    r"无.{0,12}(?:经验|实战|实践)|不具备|没有.{0,12}(?:经验|使用|实战|实践|接触|做过)|"
    r"未曾(?:使用|接触|参与|负责|做过)|[未没]使用过|[未没]用过|没做过|未掌握|不熟悉|"
    r"缺乏.{0,10}(?:经验|实战|实践)?|仅停留在了解|仅了解概念|了解概念|"
    r"零经验|未在生产|尚未在生产|计划学习|正在入门|学习中|"
    # Korean / Japanese prefix forms
    r"미경험\s*[:：]|未経験\s*[:：]|未習得\s*[:：]"
    r")",
    flags=re.IGNORECASE,
)

SUFFIX_NEGATION_RE = re.compile(
    r"("
    # Korean
    r"미경험|미보유|경험\s*(?:이|은|는)?\s*없|해\s*보지\s*않|해보지\s*않|사용\s*(?:해\s*보지\s*)?않|"
    r"사용\s*안|다뤄\s*보지\s*않|적용\s*안|부재|없음|불가|아직\s*없|배우지\s*않|학습\s*예정|공부\s*중|이론만|"
    # Japanese (incl. Keigo ございません, general 経験なし, 学習中/勉強中/キャッチアップ中)
    r"未経験|未習得|実務経験(?:は|が)?(?:ありません|ございません|な[しく]|なし)|"
    r"使用経験(?:は|が)?(?:ありません|ございません|な[しく]|なし)|"
    r"開発経験(?:は|が)?(?:ありません|ございません|な[しく]|なし)|"
    r"運用経験(?:は|が)?(?:ありません|ございません|な[しく]|なし)|"
    r"経験(?:は|が)?(?:ありません|ございません|ない|無く|なく|なし|乏しく)|"
    r"触れたこと(?:は|が)?(?:ありません|ございません|な[いく])|"
    r"扱ったこと(?:は|が)?(?:ありません|ございません|な[いく])|"
    r"使ったこと(?:は|が)?(?:ありません|ございません|な[いく])|"
    r"携わって(?:おりません|いない|いません)|知識のみ|概念(?:の)?理解のみ|独学(?:の)?み|"
    r"これから学習|学習予定|学習中|勉強中|キャッチアップ中|未導入|未使用|実務では未使用|"
    r"本番(?:環境)?での(?:利用|運用|使用)経験(?:は|が)?(?:ありません|ございません|な[しく]|なし)|"
    # Chinese suffix forms
    r"经验不足|暂无实战|尚未掌握|未涉及|学习中"
    r")",
    flags=re.IGNORECASE,
)

LOCAL_NEGATION_RE = re.compile(
    f"(?:{PREFIX_NEGATION_RE.pattern})|(?:{SUFFIX_NEGATION_RE.pattern})",
    flags=re.IGNORECASE,
)

# Strictly unambiguous positive assertion predicates (never bare domain nouns like 構築/運用/开发/production)
POSITIVE_CLAUSE_MARKER_RE = re.compile(
    r"("
    # Japanese
    r"実務\s*\d+\s*年|実務経験あり|経験あり|主導し|担当いたし|担当し|構築いたし|導入し|"
    # Chinese
    r"熟悉|精通|熟练掌握|熟练使用|主导过|实务经验|\d+\s*年(?:以上)?(?:研发|开发|工作|实战)?经验|"
    # Korean
    r"실무\s*\d+\s*년|경험\s*보유|구축했|운영했|주도했|개발했|"
    # English
    r"\b(?:built|led|designed|developed|operated|managed|proficient|experienced)\b|\b\d+\+?\s*years?\b"
    r")",
    flags=re.IGNORECASE,
)

CLAUSE_SPLIT_RE = re.compile(
    r"[.;|。；！？]|"
    r"(?:이지만|지만|하지만|이며|이고|는데|반면|"
    r"\bbut\b|\bhowever\b|\balthough\b|\bthough\b|\bwhereas\b|\bwhile\b|\byet\b|"
    r"但是|不过|然而|只是|却|虽然|尽管|但(?!是)|而(?!且)|"
    r"ですが|ますが|けれど(?:も)?|しかし|一方で|ものの|ながら|(?<![い])ただ(?:し|、|，))",
    flags=re.IGNORECASE,
)

SOFT_LIST_COMMA_RE = re.compile(r"[,、，]")


def _nfkc(text: str) -> str:
    """Normalize full-width alphanumerics, punctuation, and half-width Katakana cleanly."""
    return unicodedata.normalize("NFKC", text)


def _dec(val: Any) -> Decimal:
    return Decimal(str(val))


def _round1(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def _round2(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _fmt1(val: Any) -> str:
    """Format number to 1 decimal place strictly using Decimal ROUND_HALF_UP (never IEEE Banker's Rounding)."""
    return f"{_round1(_dec(val)):.1f}"


def _category_label(cat: str, lang: str, domain_mode: str) -> str:
    entry = CATEGORY_LABELS[lang][cat]
    if isinstance(entry, dict):
        return entry[domain_mode]
    return entry


def _display_score_safe(exact_score: Decimal, threshold: Decimal) -> tuple[Decimal, bool]:
    """Round score to 1 decimal while preventing contradiction with pass/fail threshold."""
    passed = exact_score >= threshold
    rounded = _round1(exact_score)
    if not passed and rounded >= threshold:
        floored = exact_score.quantize(Decimal("0.1"), rounding=ROUND_DOWN)
        return floored, False
    return rounded, passed


def _dec_norm(val: Any) -> str:
    """Canonical Decimal string without trailing zeros or scientific notation (e.g., 80.0 == 80 -> '80')."""
    d = _dec(val).normalize()
    if d == d.to_integral_value():
        return str(d.to_integral_value())
    return format(d, "f")


def compute_rubric_hash(rubric: dict[str, Any]) -> str:
    """Compute canonical SHA-256 hash over locked rubric fields (excluding lock metadata)."""
    canonical = {
        "role_title": rubric.get("role_title", ""),
        "company": rubric.get("company", ""),
        "language": str(rubric.get("language", "ko")).lower(),
        "domain_mode": str(rubric.get("domain_mode", "portfolio")).lower(),
        "pass_threshold": _dec_norm(rubric.get("pass_threshold", 80.0)),
        "ats_lexical_share": _dec_norm(rubric.get("ats_lexical_share", 0.5)),
        "category_weights": {
            cat: _dec_norm(rubric.get("category_weights", DEFAULT_WEIGHTS).get(cat, DEFAULT_WEIGHTS[cat]))
            for cat in CATEGORY_ORDER
        },
        "categories": {
            cat: [
                {
                    "id": str(item["id"]),
                    "title": str(item["title"]),
                    "weight": _dec_norm(item.get("weight", 1)),
                    "is_knockout": bool(item.get("is_knockout", False)),
                }
                for item in rubric.get("categories", {}).get(cat, [])
            ]
            for cat in CATEGORY_ORDER
        },
        "keywords": [
            {
                "term": str(kw["term"]),
                "aliases": [str(a) for a in kw.get("aliases", [])],
                "tier": str(kw.get("tier", "must")).lower(),
                "linked_item_id": str(kw["linked_item_id"]) if kw.get("linked_item_id") else None,
            }
            for kw in rubric.get("keywords", [])
        ],
    }
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def validate_rubric(rubric: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Validate rubric schema and return (normalized_item_map, advisory_warnings)."""
    warnings: list[str] = []

    lang = str(rubric.get("language", "ko")).lower()
    if lang not in VALID_LANGUAGES:
        raise ValueError(f"Invalid language '{lang}'. Valid: {sorted(VALID_LANGUAGES)}")

    domain_mode = str(rubric.get("domain_mode", "portfolio")).lower()
    if domain_mode not in VALID_DOMAIN_MODES:
        raise ValueError(f"Invalid domain_mode '{domain_mode}'. Valid: {sorted(VALID_DOMAIN_MODES)}")

    threshold = _dec(rubric.get("pass_threshold", 80.0))
    if threshold <= Decimal("0") or threshold > Decimal("100"):
        raise ValueError(f"pass_threshold must be in (0, 100], got {threshold}")

    ats_share = _dec(rubric.get("ats_lexical_share", 0.5))
    if ats_share < Decimal("0") or ats_share > Decimal("1"):
        raise ValueError(f"ats_lexical_share must be in [0, 1], got {ats_share}")

    raw_weights = rubric.get("category_weights", DEFAULT_WEIGHTS)
    for cat in CATEGORY_ORDER:
        w = _dec(raw_weights.get(cat, DEFAULT_WEIGHTS[cat]))
        if w < Decimal("0"):
            raise ValueError(f"Category weight for '{cat}' cannot be negative: {w}")

    categories = rubric.get("categories")
    if not isinstance(categories, dict):
        raise ValueError("rubric.json must contain a 'categories' object.")

    unknown_cats = set(categories.keys()) - set(CATEGORY_ORDER)
    if unknown_cats:
        raise ValueError(f"Unknown categories in rubric.json: {sorted(unknown_cats)}")

    item_map: dict[str, dict[str, Any]] = {}
    for cat in CATEGORY_ORDER:
        items = categories.get(cat, [])
        if not isinstance(items, list):
            raise ValueError(f"Category '{cat}' must be a list of items.")
        for item in items:
            if not isinstance(item, dict) or "id" not in item or "title" not in item:
                raise ValueError(f"Every item in '{cat}' must have 'id' and 'title': {item}")
            item_id = str(item["id"]).strip()
            if not item_id:
                raise ValueError(f"Empty item id in category '{cat}'.")
            if item_id in item_map:
                raise ValueError(f"Duplicate item id '{item_id}' across rubric.")
            weight = _dec(item.get("weight", 1))
            if weight <= Decimal("0"):
                raise ValueError(f"Item '{item_id}' weight must be > 0, got {weight}")
            is_ko = bool(item.get("is_knockout", False))
            if is_ko and cat != "must_have":
                raise ValueError(f"Item '{item_id}' has is_knockout=true outside 'must_have'.")
            if is_ko and weight < Decimal("2"):
                raise ValueError(
                    f"KNOCKOUT_WEIGHT_ERROR: Knockout item '{item_id}' must have weight >= 2 (got {weight}) "
                    "so core screening gates cannot be artificially minimized."
                )
            item_map[item_id] = {
                "id": item_id,
                "category": cat,
                "title": str(item["title"]),
                "description": str(item.get("description", "")),
                "weight": weight,
                "is_knockout": is_ko,
            }

    keywords = rubric.get("keywords", [])
    if not isinstance(keywords, list):
        raise ValueError("'keywords' must be a list.")
    for kw in keywords:
        if not isinstance(kw, dict) or not str(kw.get("term", "")).strip():
            raise ValueError(f"Invalid keyword entry: {kw}")
        term = str(kw["term"]).strip()
        tier = str(kw.get("tier", "must")).lower()
        if tier not in VALID_KEYWORD_TIERS:
            raise ValueError(f"Keyword '{term}' has invalid tier '{tier}' (use 'must' or 'preferred').")
        linked = kw.get("linked_item_id")
        if linked and str(linked) not in item_map:
            raise ValueError(f"Keyword '{term}' references unknown linked_item_id '{linked}'.")
        for alias in kw.get("aliases", []):
            a_clean = _nfkc(str(alias)).strip()
            if a_clean.lower() in OVERLY_BROAD_ALIASES and a_clean.lower() != _nfkc(term).lower():
                warnings.append(
                    f"BROAD_ALIAS_WARNING: Keyword '{term}' uses overly broad alias '{a_clean}' which may cause false ATS matches."
                )

    if not item_map and not keywords:
        raise ValueError("Rubric has zero items and zero keywords.")

    return item_map, warnings


def _build_term_regex(term: str) -> re.Pattern[str]:
    cleaned = _nfkc(term).strip()
    if not cleaned:
        raise ValueError("Cannot build regex for empty keyword term.")

    has_cjk = bool(HANGUL_OR_CJK_RE.search(cleaned))
    tokens = re.split(r"\s+", cleaned)
    if has_cjk:
        core = r"\s*".join(re.escape(tok) for tok in tokens)
        if ASCII_ALNUM_RE.match(cleaned[0]):
            left = r"(?<![A-Za-z0-9])"
        elif PURE_HANGUL_RE.match(cleaned) and len(cleaned.replace(" ", "")) <= 2:
            # Prevent 1-2 char Hangul terms like "인사"/"취득" from matching inside unrelated words ("개인사정")
            left = r"(?<![\uac00-\ud7af])"
        elif PURE_KATAKANA_RE.match(cleaned) and len(cleaned.replace(" ", "")) <= 3:
            # Prevent short Katakana terms like "リース" from matching inside "リリース"
            left = r"(?<![\u30a0-\u30ff\u30fc])"
        else:
            left = ""

        if ASCII_ALNUM_RE.match(cleaned[-1]):
            right = r"(?![A-Za-z0-9+#])"
        elif PURE_KATAKANA_RE.match(cleaned) and len(cleaned.replace(" ", "")) <= 3:
            right = r"(?![\u30a0-\u30ff\u30fc])"
        else:
            right = ""
        return re.compile(f"{left}{core}{right}", flags=re.IGNORECASE)

    core = r"\s+".join(re.escape(tok) for tok in tokens)
    if cleaned.startswith("."):
        left = ""
    elif ASCII_ALNUM_RE.match(cleaned[0]):
        left = r"(?<![A-Za-z0-9])"
    else:
        left = r"(?<![A-Za-z0-9+#])"

    last_ch = cleaned[-1]
    if last_ch in ("+", "#"):
        right = r"(?![A-Za-z+#])"
    elif len(cleaned) == 1 and ASCII_ALNUM_RE.match(last_ch):
        right = r"(?![A-Za-z0-9+#&\-])"
    elif ASCII_ALNUM_RE.match(last_ch):
        right = r"(?![A-Za-z0-9+#])"
    else:
        right = r"(?![A-Za-z0-9])"
    return re.compile(f"{left}{core}{right}", flags=re.IGNORECASE)


def _compute_negated_line_flags(lines: list[str]) -> list[bool]:
    """Identify lines inside explicit negative-experience sections across ko/en/zh/ja."""
    flags: list[bool] = []
    in_negated_section = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            flags.append(in_negated_section)
            continue

        is_source_marker = stripped.startswith("=== SOURCE:")
        is_bullet_or_sentence = (
            (not is_source_marker)
            and (
                bool(BULLET_OR_NUMBERED_RE.match(stripped))
                or stripped.endswith((".", "。"))
                or any(p in stripped for p in (";", "；", ",", "，", "、"))
            )
        )
        heading_candidate = HEADING_DECORATION_PREFIX_RE.sub("", stripped).strip()
        is_heading_shape = is_source_marker or ((not is_bullet_or_sentence) and len(stripped) <= 55)

        if is_heading_shape and (not is_source_marker) and NEGATED_HEADING_RE.search(heading_candidate):
            in_negated_section = True
            flags.append(True)
            continue
        if in_negated_section and is_heading_shape:
            has_heading_glyph = bool(HEADING_DECORATION_PREFIX_RE.match(stripped))
            is_short_reset = len(heading_candidate) <= 22 or heading_candidate.endswith((":", "："))
            if (is_source_marker or has_heading_glyph or is_short_reset) and SECTION_RESET_HEADING_RE.search(heading_candidate):
                in_negated_section = False
        flags.append(in_negated_section)
    return flags


def _is_match_negated(line: str, start: int, end: int, line_in_neg_section: bool) -> bool:
    if line_in_neg_section:
        return True
    clause_left = max(0, start - 180)
    clause_right = min(len(line), end + 180)
    prefix = CLAUSE_SPLIT_RE.split(line[clause_left:start])[-1]
    suffix = CLAUSE_SPLIT_RE.split(line[end:clause_right])[0]

    # Guard left-hand prefix across soft commas ("," / "、" / "，"):
    # - A prior suffix-negation ("Spark未経験、Python実務3年") must NOT bleed right into Python,
    # - A positive predicate after comma ("Spark未経験、Python実務3年") resets prefix,
    # - A prefix-negation ("No experience with Airflow, Spark, or Kubernetes" / "暂未接触 Kubernetes，Spark") MUST govern the list!
    if SOFT_LIST_COMMA_RE.search(prefix):
        comma_parts = SOFT_LIST_COMMA_RE.split(prefix)
        before_last_comma = "".join(comma_parts[:-1])
        after_last_comma = comma_parts[-1]
        if SUFFIX_NEGATION_RE.search(before_last_comma) and not PREFIX_NEGATION_RE.search(before_last_comma):
            prefix = after_last_comma
        elif POSITIVE_CLAUSE_MARKER_RE.search(after_last_comma):
            prefix = after_last_comma

    # Guard right-hand suffix across soft commas ("," / "、" / "，"):
    # - A prefix-negation AFTER a comma ("Python 5 years, no experience with Spark" / "熟练掌握Java，暂未接触Kubernetes")
    #   must NOT negate the earlier positive token,
    # - An unambiguous positive assertion before a comma ("Python実務3年、Spark未経験") stops suffix-negation bleeding left!
    if SOFT_LIST_COMMA_RE.search(suffix):
        parts = SOFT_LIST_COMMA_RE.split(suffix, maxsplit=1)
        before_comma, after_comma = parts[0], parts[1]
        if POSITIVE_CLAUSE_MARKER_RE.search(before_comma) or PREFIX_NEGATION_RE.search(after_comma):
            suffix = before_comma

    if PREFIX_NEGATION_RE.search(prefix) or SUFFIX_NEGATION_RE.search(suffix):
        return True
    short_prefix = prefix[-24:]
    short_suffix = suffix[:24]
    return bool(LOCAL_NEGATION_RE.search(f"{short_prefix}{line[start:end]}{short_suffix}"))


def audit_ats_keywords(keywords: list[dict[str, Any]], candidate_text: str) -> dict[str, Any]:
    """Run deterministic ko/en/zh/ja NFKC-normalized, boundary-aware & negation-aware lexical keyword matching.

    Anti-stuffing policy: keywords appearing in BOTH positive and negative contexts (`contradictory_mention`)
    receive 0.0 ATS credit until the contradiction is resolved.
    """
    lines = [_nfkc(ln) for ln in candidate_text.splitlines()]
    neg_section_flags = _compute_negated_line_flags(lines)

    results: list[dict[str, Any]] = []
    total_w = Decimal("0")
    matched_w = Decimal("0")

    for kw in keywords:
        term = str(kw["term"]).strip()
        aliases = [str(a).strip() for a in kw.get("aliases", []) if str(a).strip()]
        tier = str(kw.get("tier", "must")).lower()
        linked_item_id = str(kw["linked_item_id"]) if kw.get("linked_item_id") else None
        weight = VALID_KEYWORD_TIERS[tier]
        total_w += weight

        matched_surface: str | None = None
        saw_negated = False

        for surface in [term, *aliases]:
            pattern = _build_term_regex(surface)
            for line, in_neg_sec in zip(lines, neg_section_flags):
                for m in pattern.finditer(line):
                    if _is_match_negated(line, m.start(), m.end(), in_neg_sec):
                        saw_negated = True
                    elif matched_surface is None:
                        matched_surface = m.group(0)

        is_contradictory = (matched_surface is not None) and saw_negated
        is_matched = (matched_surface is not None) and (not saw_negated)
        if is_matched:
            matched_w += weight

        results.append(
            {
                "term": term,
                "aliases": aliases,
                "tier": tier,
                "linked_item_id": linked_item_id,
                "weight": float(weight),
                "matched": is_matched,
                "matched_surface": matched_surface if is_matched else None,
                "negated_mention": (matched_surface is None) and saw_negated,
                "contradictory_mention": is_contradictory,
            }
        )

    ratio = (matched_w / total_w) if total_w > Decimal("0") else Decimal("1")
    return {
        "checked": True,
        "total_count": len(results),
        "matched_count": sum(1 for r in results if r["matched"]),
        "total_weight": total_w,
        "matched_weight": matched_w,
        "ratio": ratio,
        "coverage_pct": float(_round1(ratio * Decimal("100"))),
        "details": results,
    }


def _normalize_for_quote_check(text: str) -> str:
    """NFKC-normalize and preserve ASCII alnum, Hangul, Hanzi/Kanji, Hiragana, and Katakana."""
    norm = _nfkc(text).lower()
    return re.sub(r"[^0-9a-z\uac00-\ud7af\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\u30fc]+", " ", norm).strip()


QUOTE_UNIT_RE = re.compile(
    r"[0-9a-z]+|[\uac00-\ud7af]+|[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\u30fc]"
)


def _extract_quote_units(norm_text: str) -> list[str]:
    """Hybrid tokenizer: word tokens for ASCII/Hangul + character units for unspaced Hanzi/Kana."""
    return QUOTE_UNIT_RE.findall(norm_text)


def verify_quote_grounding(quote: str, candidate_text: str) -> bool:
    """Verify that a claimed evidence_quote actually appears in candidate_text (ko/en/zh/ja).

    Enforces:
      1. Minimum length >= 2 chars across all scripts (blocks 1-char particle/letter quotes),
      2. 100% numeric-token grounding (blocks metric fabrication such as '5千 -> 500万' or '2 -> 50'),
      3. Verbatim normalized substring match (whitespace-insensitive for unspaced CJK) OR strict
         contiguous n-gram overlap (en/ko: unigram >= 0.75 & bigram >= 0.55; zh/ja: unigram >= 0.80,
         bigram >= 0.65 & trigram >= 0.50).
    """
    norm_cand = _normalize_for_quote_check(candidate_text)
    if not norm_cand:
        return False
    compact_cand = re.sub(r"\s+", "", norm_cand)
    cand_nums = {m.lower() for m in NUM_TOKEN_RE.findall(_nfkc(candidate_text))}

    clauses = [c.strip() for c in re.split(r"\.{3}|…|\s+/\s+|\n+", quote) if c.strip()]
    if not clauses:
        return False

    cand_units_list = _extract_quote_units(norm_cand)
    cand_units = set(cand_units_list)
    cand_bigrams = {
        (cand_units_list[i], cand_units_list[i + 1]) for i in range(len(cand_units_list) - 1)
    }
    cand_trigrams = {
        (cand_units_list[i], cand_units_list[i + 1], cand_units_list[i + 2])
        for i in range(len(cand_units_list) - 2)
    }

    verified_clauses = 0
    non_empty_clauses = 0
    for clause in clauses:
        norm_clause = _normalize_for_quote_check(clause)
        if not norm_clause:
            continue
        non_empty_clauses += 1
        compact_clause = re.sub(r"\s+", "", norm_clause)

        # Reject trivial 1-char quotes across ALL scripts (e.g. "a", "의", "的", "の")
        if len(compact_clause) < 2:
            continue

        # 100% numeric+unit token grounding lock: blocks both digit and magnitude swaps ("5千->5万", "5K->5M")
        clause_nums = [m.lower() for m in NUM_TOKEN_RE.findall(_nfkc(clause))]
        if clause_nums and any(n not in cand_nums for n in clause_nums):
            continue

        if norm_clause in norm_cand:
            verified_clauses += 1
            continue
        is_cjk_clause = bool(UNSPACED_CJK_RE.search(norm_clause))
        if is_cjk_clause and compact_clause in compact_cand:
            verified_clauses += 1
            continue

        units = _extract_quote_units(norm_clause)
        if len(units) == 1:
            if len(units[0]) >= 2 and (units[0] in cand_units or units[0] in norm_cand):
                verified_clauses += 1
            continue

        meaningful = [u for u in units if len(u) >= 2 or UNSPACED_CJK_RE.match(u)]
        unigram_ratio = (
            sum(1 for u in meaningful if u in cand_units or (len(u) >= 2 and u in norm_cand)) / len(meaningful)
            if meaningful
            else 0.0
        )
        clause_bigrams = [(units[i], units[i + 1]) for i in range(len(units) - 1)]
        bigram_ratio = (
            sum(
                1
                for bg in clause_bigrams
                if bg in cand_bigrams
                or f"{bg[0]} {bg[1]}" in norm_cand
                or (
                    (UNSPACED_CJK_RE.match(bg[0]) or UNSPACED_CJK_RE.match(bg[1]))
                    and f"{bg[0]}{bg[1]}" in compact_cand
                )
            )
            / len(clause_bigrams)
            if clause_bigrams
            else 0.0
        )
        if is_cjk_clause and len(units) >= 4:
            clause_trigrams = [(units[i], units[i + 1], units[i + 2]) for i in range(len(units) - 2)]
            trigram_ratio = (
                sum(
                    1
                    for tg in clause_trigrams
                    if tg in cand_trigrams or "".join(tg) in compact_cand
                )
                / len(clause_trigrams)
                if clause_trigrams
                else 0.0
            )
            if unigram_ratio >= 0.80 and bigram_ratio >= 0.65 and trigram_ratio >= 0.50:
                verified_clauses += 1
        elif unigram_ratio >= 0.75 and bigram_ratio >= 0.55:
            verified_clauses += 1

    return non_empty_clauses > 0 and verified_clauses == non_empty_clauses


def evaluate_round(
    rubric: dict[str, Any],
    eval_data: dict[str, Any],
    candidate_text: str | None = None,
    history: dict[str, Any] | None = None,
    *,
    require_locked: bool = True,
    strict_quotes: bool = False,
    lang_override: str | None = None,
    domain_mode_override: str | None = None,
) -> dict[str, Any]:
    """Compute exact weighted score, uplifts, round diff, quote audit, and Grace recommendation."""
    item_map, rubric_warnings = validate_rubric(rubric)
    current_hash = compute_rubric_hash(rubric)

    stamped_hash = rubric.get("rubric_hash")
    if require_locked and not stamped_hash:
        raise ValueError(
            "RUBRIC_UNLOCKED_ERROR: rubric.json is missing 'rubric_hash'. "
            "Run --init-rubric <rubric.json> before evaluating Round 1."
        )
    if stamped_hash and stamped_hash != current_hash:
        raise ValueError(
            f"RUBRIC_TAMPERED_ERROR: rubric.json hash mismatch (stamped={stamped_hash}, computed={current_hash}). "
            "Do not alter locked rubric mid-session."
        )

    if history and history.get("rubric_hash") and history["rubric_hash"] != current_hash:
        raise ValueError(
            f"RUBRIC_DRIFT_ERROR: history.json hash ({history['rubric_hash']}) != rubric.json hash ({current_hash}). "
            "Start a new session if the target JD changed."
        )

    if eval_data.get("rubric_hash") and eval_data["rubric_hash"] != current_hash:
        raise ValueError(
            f"RUBRIC_HASH_MISMATCH: eval file hash ({eval_data['rubric_hash']}) != rubric hash ({current_hash})."
        )

    lang = (lang_override or str(rubric.get("language", "ko"))).lower()
    if lang not in VALID_LANGUAGES:
        raise ValueError(f"Invalid language '{lang}'. Valid: {sorted(VALID_LANGUAGES)}")
    domain_mode = (domain_mode_override or str(rubric.get("domain_mode", "portfolio"))).lower()
    if domain_mode not in VALID_DOMAIN_MODES:
        raise ValueError(f"Invalid domain_mode '{domain_mode}'. Valid: {sorted(VALID_DOMAIN_MODES)}")

    keywords = rubric.get("keywords", [])
    if keywords and candidate_text is None:
        raise ValueError(
            "CANDIDATE_TEXT_REQUIRED_ERROR: rubric.json defines ATS 'keywords', so --candidate-text is required "
            "to keep ats_framing category weights consistent across rounds."
        )

    eval_items_raw = eval_data.get("items")
    if not isinstance(eval_items_raw, list):
        raise ValueError("eval JSON must contain an 'items' list.")

    eval_by_id: dict[str, dict[str, Any]] = {}
    unverified_quotes: list[dict[str, str]] = []

    for entry in eval_items_raw:
        if not isinstance(entry, dict) or "id" not in entry or "grade" not in entry:
            raise ValueError(f"Every eval item must include 'id' and 'grade': {entry}")
        iid = str(entry["id"]).strip()
        if iid not in item_map:
            raise ValueError(f"Unknown item id '{iid}' in eval JSON (not in rubric.json).")
        if iid in eval_by_id:
            raise ValueError(f"Duplicate item id '{iid}' in eval JSON.")
        grade = str(entry["grade"]).strip().upper()
        if grade not in GRADE_MULTIPLIERS:
            raise ValueError(f"Invalid grade '{grade}' for item '{iid}'. Valid: {list(GRADE_MULTIPLIERS)}")
        evidence_quote = str(entry.get("evidence_quote", "")).strip()
        if grade != "MISSING" and not evidence_quote:
            raise ValueError(
                f"Anti-hallucination violation: item '{iid}' graded '{grade}' must include non-empty 'evidence_quote'."
            )
        quote_verified: bool | None = None
        if grade != "MISSING" and candidate_text is not None:
            quote_verified = verify_quote_grounding(evidence_quote, candidate_text)
            if not quote_verified:
                unverified_quotes.append({"id": iid, "evidence_quote": evidence_quote})

        gap_type = entry.get("gap_type")
        if grade == "FULL":
            gap_type_norm = None
        else:
            gap_type_norm = str(gap_type).strip().lower() if gap_type else "expression_gap"
            if gap_type_norm not in VALID_GAP_TYPES:
                raise ValueError(
                    f"Invalid gap_type '{gap_type_norm}' for item '{iid}'. Valid: {sorted(VALID_GAP_TYPES)}"
                )
        eval_by_id[iid] = {
            "id": iid,
            "grade": grade,
            "multiplier": GRADE_MULTIPLIERS[grade],
            "evidence_quote": evidence_quote,
            "quote_verified": quote_verified,
            "source": str(entry.get("source", "")).strip(),
            "gap_type": gap_type_norm,
            "action_hint": str(entry.get("action_hint", "")).strip(),
        }

    missing_eval_ids = sorted(set(item_map.keys()) - set(eval_by_id.keys()))
    if missing_eval_ids:
        raise ValueError(f"Eval JSON is missing rubric item(s): {missing_eval_ids}")

    if strict_quotes and unverified_quotes:
        bad_ids = [q["id"] for q in unverified_quotes]
        raise ValueError(
            f"QUOTE_VERIFICATION_ERROR: Non-verbatim or ungrounded evidence_quote detected for item(s): {bad_ids}."
        )

    if keywords and candidate_text is not None:
        ats_audit = audit_ats_keywords(keywords, candidate_text)
    else:
        ats_audit = {
            "checked": False,
            "total_count": 0,
            "matched_count": 0,
            "total_weight": Decimal("0"),
            "matched_weight": Decimal("0"),
            "ratio": Decimal("0"),
            "coverage_pct": None,
            "details": [],
        }

    raw_weights = {
        cat: _dec(rubric.get("category_weights", DEFAULT_WEIGHTS).get(cat, DEFAULT_WEIGHTS[cat]))
        for cat in CATEGORY_ORDER
    }
    cat_items: dict[str, list[dict[str, Any]]] = {cat: [] for cat in CATEGORY_ORDER}
    for meta in item_map.values():
        cat_items[meta["category"]].append(meta)

    active_cats: list[str] = []
    for cat in CATEGORY_ORDER:
        if cat == "ats_framing":
            if cat_items[cat] or (ats_audit["checked"] and ats_audit["total_weight"] > Decimal("0")):
                if raw_weights[cat] > Decimal("0"):
                    active_cats.append(cat)
        else:
            if cat_items[cat] and raw_weights[cat] > Decimal("0"):
                active_cats.append(cat)

    active_weight_sum = sum((raw_weights[c] for c in active_cats), Decimal("0"))
    if active_weight_sum <= Decimal("0"):
        raise ValueError("Active category weight sum must be > 0.")

    eff_weights: dict[str, Decimal] = {
        cat: ((raw_weights[cat] / active_weight_sum) * Decimal("100")) if cat in active_cats else Decimal("0")
        for cat in CATEGORY_ORDER
    }

    ats_lexical_share_cfg = _dec(rubric.get("ats_lexical_share", 0.5))

    category_results: dict[str, dict[str, Any]] = {}
    item_results: list[dict[str, Any]] = []
    total_exact = Decimal("0")

    for cat in CATEGORY_ORDER:
        items = cat_items[cat]
        w_eff = eff_weights[cat]
        label = _category_label(cat, lang, domain_mode)
        if cat not in active_cats:
            category_results[cat] = {
                "label": label,
                "label_ko": _category_label(cat, "ko", domain_mode),
                "active": False,
                "effective_weight": 0.0,
                "attainment_pct": None,
                "earned_points": 0.0,
                "max_points": 0.0,
                "item_count": 0,
            }
            continue

        item_weight_sum = sum((it["weight"] for it in items), Decimal("0"))
        if items:
            earned_item_w = sum((it["weight"] * eval_by_id[it["id"]]["multiplier"] for it in items), Decimal("0"))
            items_ratio = earned_item_w / item_weight_sum
        else:
            items_ratio = Decimal("0")

        if cat == "ats_framing":
            has_lex = ats_audit["checked"] and ats_audit["total_weight"] > Decimal("0")
            has_frame = bool(items)
            if has_lex and has_frame:
                lex_alpha = ats_lexical_share_cfg
                frame_beta = Decimal("1") - lex_alpha
                cat_ratio = frame_beta * items_ratio + lex_alpha * ats_audit["ratio"]
            elif has_lex:
                lex_alpha = Decimal("1")
                frame_beta = Decimal("0")
                cat_ratio = ats_audit["ratio"]
            else:
                lex_alpha = Decimal("0")
                frame_beta = Decimal("1")
                cat_ratio = items_ratio
        else:
            lex_alpha = Decimal("0")
            frame_beta = Decimal("1")
            cat_ratio = items_ratio

        earned_pts = w_eff * cat_ratio
        total_exact += earned_pts

        category_results[cat] = {
            "label": label,
            "label_ko": _category_label(cat, "ko", domain_mode),
            "active": True,
            "effective_weight": float(_round2(w_eff)),
            "effective_weight_exact": w_eff,
            "attainment_pct": float(_round1(cat_ratio * Decimal("100"))),
            "earned_points": float(_round2(earned_pts)),
            "earned_points_exact": earned_pts,
            "max_points": float(_round2(w_eff)),
            "item_count": len(items),
        }

        item_pool_pts = w_eff * frame_beta
        for it in items:
            ev = eval_by_id[it["id"]]
            max_item_pts = item_pool_pts * (it["weight"] / item_weight_sum) if item_weight_sum > 0 else Decimal("0")
            cur_item_pts = max_item_pts * ev["multiplier"]
            uplift_full = max_item_pts - cur_item_pts

            cur_idx = GRADE_SEQUENCE.index(ev["grade"])
            if cur_idx < len(GRADE_SEQUENCE) - 1:
                next_grade = GRADE_SEQUENCE[cur_idx + 1]
                uplift_step = max_item_pts * (GRADE_MULTIPLIERS[next_grade] - ev["multiplier"])
            else:
                next_grade = "FULL"
                uplift_step = Decimal("0")

            uplift_transferable_cap = (
                max(Decimal("0"), max_item_pts * Decimal("0.75") - cur_item_pts)
                if ev["gap_type"] == "transferable_gap"
                else Decimal("0")
            )

            item_results.append(
                {
                    "id": it["id"],
                    "category": cat,
                    "title": it["title"],
                    "is_knockout": it["is_knockout"],
                    "weight": float(it["weight"]),
                    "grade": ev["grade"],
                    "multiplier": float(ev["multiplier"]),
                    "max_points_pp": float(_round2(max_item_pts)),
                    "max_points_exact": max_item_pts,
                    "earned_points_pp": float(_round2(cur_item_pts)),
                    "earned_points_exact": cur_item_pts,
                    "uplift_to_full_pp": float(_round2(uplift_full)),
                    "uplift_to_full_exact": uplift_full,
                    "uplift_transferable_cap_pp": float(_round2(uplift_transferable_cap)),
                    "next_grade": next_grade,
                    "uplift_one_step_pp": float(_round2(uplift_step)),
                    "gap_type": ev["gap_type"],
                    "evidence_quote": ev["evidence_quote"],
                    "quote_verified": ev["quote_verified"],
                    "source": ev["source"],
                    "action_hint": ev["action_hint"],
                }
            )

        if cat == "ats_framing":
            kw_pool_pts = w_eff * lex_alpha
            for kw_detail in ats_audit["details"]:
                kw_w = _dec(kw_detail["weight"])
                kw_max = (
                    kw_pool_pts * (kw_w / ats_audit["total_weight"])
                    if ats_audit["total_weight"] > Decimal("0")
                    else Decimal("0")
                )
                kw_detail["uplift_pp"] = float(_round2(Decimal("0") if kw_detail["matched"] else kw_max))
                kw_detail["uplift_exact"] = Decimal("0") if kw_detail["matched"] else kw_max

    sum_item_uplifts = sum((r["uplift_to_full_exact"] for r in item_results), Decimal("0"))
    sum_kw_uplifts = sum((d.get("uplift_exact", Decimal("0")) for d in ats_audit["details"]), Decimal("0"))
    conservation_residual = abs((total_exact + sum_item_uplifts + sum_kw_uplifts) - Decimal("100"))
    if conservation_residual > Decimal("0.0001"):
        raise RuntimeError(f"Internal scoring conservation error: residual={conservation_residual}")

    threshold = _dec(rubric.get("pass_threshold", 80.0))
    threshold_display = _round1(threshold)
    display_score, passed_threshold = _display_score_safe(total_exact, threshold)

    knockout_risks = [
        {
            "id": r["id"],
            "title": r["title"],
            "grade": r["grade"],
            "gap_type": r["gap_type"],
            "action_hint": r["action_hint"],
        }
        for r in item_results
        if r["is_knockout"] and r["grade"] in KNOCKOUT_RISK_GRADES
    ]

    if passed_threshold and not knockout_risks:
        pass_status = "PASS"
    elif passed_threshold and knockout_risks:
        pass_status = "PASS_WITH_RISK"
    else:
        pass_status = "REVISE"

    # Display-consistent scoreboard gap (strictly satisfies display_score + gap_to_pass_display == threshold_display)
    if passed_threshold:
        gap_to_pass_display = Decimal("0.0")
    else:
        gap_to_pass_display = max(Decimal("0.1"), threshold_display - display_score)

    true_gap_ids = {r["id"] for r in item_results if r["gap_type"] == "true_gap"}
    expression_gap_ids = {r["id"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "expression_gap"}
    transferable_gap_ids = {r["id"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "transferable_gap"}

    expression_items_uplift = sum(
        (r["uplift_to_full_exact"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "expression_gap"),
        Decimal("0"),
    )
    transferable_capped_uplift = sum(
        (
            max(Decimal("0"), r["max_points_exact"] * Decimal("0.75") - r["earned_points_exact"])
            for r in item_results
            if r["grade"] != "FULL" and r["gap_type"] == "transferable_gap"
        ),
        Decimal("0"),
    )

    expression_ats_uplift = Decimal("0")
    transferable_ats_uplift = Decimal("0")
    for kw_detail in ats_audit["details"]:
        if (
            kw_detail["matched"]
            or kw_detail.get("negated_mention", False)
            or kw_detail.get("contradictory_mention", False)
        ):
            continue
        linked_id = kw_detail.get("linked_item_id")
        kw_u = kw_detail.get("uplift_exact", Decimal("0"))
        if linked_id:
            if linked_id in true_gap_ids:
                continue
            elif linked_id in transferable_gap_ids:
                transferable_ats_uplift += kw_u
            elif linked_id in expression_gap_ids or linked_id not in true_gap_ids:
                expression_ats_uplift += kw_u
        elif not true_gap_ids:
            expression_ats_uplift += kw_u

    projected_expression_only = min(Decimal("100"), total_exact + expression_items_uplift + expression_ats_uplift)
    projected_with_transferable = min(
        Decimal("100"), projected_expression_only + transferable_capped_uplift + transferable_ats_uplift
    )
    proj_expr_display = _round1(projected_expression_only)
    proj_trans_display = _round1(projected_with_transferable)
    actionable_expr_uplift_display = max(Decimal("0.0"), proj_expr_display - display_score)
    actionable_uplift_total = (
        expression_items_uplift + expression_ats_uplift + transferable_capped_uplift + transferable_ats_uplift
    )

    prior_rounds = list(history.get("rounds", [])) if history else []
    round_num = int(eval_data.get("round", len(prior_rounds) + 1))
    earlier_rounds = [r for r in prior_rounds if int(r["round"]) < round_num]
    later_rounds = [int(r["round"]) for r in prior_rounds if int(r["round"]) > round_num]
    prev_round = earlier_rounds[-1] if earlier_rounds else None

    grace_tier_used_current = eval_data.get("grace_tier_used")
    if grace_tier_used_current is not None:
        grace_tier_used_current = int(grace_tier_used_current)
        if grace_tier_used_current not in (1, 2, 3):
            raise ValueError(f"grace_tier_used must be 1, 2, or 3, got {grace_tier_used_current}")

    prev_items_map: dict[str, dict[str, Any]] = {}
    if prev_round:
        prev_items_map = {it["id"]: it for it in prev_round.get("items", [])}

    resolved_items: list[dict[str, Any]] = []
    improved_items: list[dict[str, Any]] = []
    regressed_items: list[dict[str, Any]] = []
    stalled_items: list[dict[str, Any]] = []
    actionable_stalled_items: list[dict[str, Any]] = []

    for r in item_results:
        mult = GRADE_MULTIPLIERS[r["grade"]]
        prev = prev_items_map.get(r["id"])
        if prev is None:
            streak = 1 if mult <= Decimal("0.50") else 0
            r["prev_grade"] = None
            r["stalled_streak"] = streak
        else:
            prev_grade = prev["grade"]
            prev_mult = GRADE_MULTIPLIERS[prev_grade]
            prev_streak = int(prev.get("stalled_streak", 1 if prev_mult <= Decimal("0.50") else 0))
            r["prev_grade"] = prev_grade

            if mult > prev_mult:
                delta_pts = _round2(r["earned_points_exact"] - _dec(prev.get("earned_points_pp", 0)))
                change = {
                    "id": r["id"],
                    "title": r["title"],
                    "from": prev_grade,
                    "to": r["grade"],
                    "delta_pp": float(delta_pts),
                }
                improved_items.append(change)
                if r["grade"] == "FULL":
                    resolved_items.append(change)
            elif mult < prev_mult:
                delta_pts = _round2(r["earned_points_exact"] - _dec(prev.get("earned_points_pp", 0)))
                regressed_items.append(
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "from": prev_grade,
                        "to": r["grade"],
                        "delta_pp": float(delta_pts),
                    }
                )

            if mult > Decimal("0.50"):
                streak = 0
            elif mult <= prev_mult:
                streak = prev_streak + 1
            else:
                streak = 1
            r["stalled_streak"] = streak

        if r["stalled_streak"] >= 2 and r["gap_type"] != "true_gap":
            stalled_entry = {
                "id": r["id"],
                "title": r["title"],
                "grade": r["grade"],
                "gap_type": r["gap_type"],
                "stalled_streak": r["stalled_streak"],
                "uplift_to_full_pp": r["uplift_to_full_pp"],
            }
            stalled_items.append(stalled_entry)
            actionable_stalled_items.append(stalled_entry)

    if prev_round:
        prev_total_exact = _dec(prev_round.get("total_score_exact", prev_round["total_score"]))
        prev_score_display = _dec(prev_round["total_score"])
        delta_score_exact = total_exact - prev_total_exact
        delta_score_display = _round1(display_score - prev_score_display)
        cat_deltas: dict[str, float | None] = {}
        prev_cats = prev_round.get("categories", {})
        for cat in CATEGORY_ORDER:
            if category_results[cat]["active"] and prev_cats.get(cat, {}).get("active"):
                c_delta = _round1(
                    _round1(category_results[cat]["earned_points_exact"])
                    - _round1(_dec(prev_cats[cat]["earned_points"]))
                )
                cat_deltas[cat] = float(c_delta)
            else:
                cat_deltas[cat] = None
    else:
        delta_score_exact = None
        delta_score_display = None
        prev_score_display = None
        cat_deltas = {cat: None for cat in CATEGORY_ORDER}

    t = I18N[lang]
    u = t["unit_pp"]
    has_actionable_headroom = (expression_items_uplift > Decimal("0")) or (transferable_capped_uplift > Decimal("0"))
    has_true_gap_knockout = any(kr.get("gap_type") == "true_gap" for kr in knockout_risks)
    # Emit honest_fit_advisory whenever true_gaps prevent reaching threshold OR zero actionable gaps remain
    honest_fit_advisory = (pass_status == "REVISE") and (
        (not has_actionable_headroom) or (projected_with_transferable < threshold) or has_true_gap_knockout
    )

    should_offer_grace = False
    grace_reasons: list[str] = []
    if pass_status == "REVISE" and round_num >= 2 and has_actionable_headroom:
        if actionable_stalled_items:
            should_offer_grace = True
            names = ", ".join(f"{it['id']}({it['title']})" for it in actionable_stalled_items[:3])
            grace_reasons.append(t["grace_reason_stalled"].format(names=names))
        if delta_score_exact is not None and delta_score_exact < Decimal("3.0"):
            should_offer_grace = True
            sp = " " if lang in ("en", "zh") else ""
            d_str = f"{delta_score_display:+.1f}{sp}{u}"
            grace_reasons.append(t["grace_reason_low_gain"].format(delta=d_str))

    prior_grace_tiers = [int(r["grace_tier_used"]) for r in earlier_rounds if r.get("grace_tier_used")]
    if grace_tier_used_current:
        prior_grace_tiers.append(grace_tier_used_current)
    max_prior_grace = max(prior_grace_tiers, default=0)
    max_actionable_streak = max((it["stalled_streak"] for it in actionable_stalled_items), default=0)

    if not should_offer_grace:
        suggested_tier = None
    elif max_prior_grace >= 2 or max_actionable_streak >= 4:
        suggested_tier = 3
    elif max_prior_grace >= 1 or max_actionable_streak >= 3 or round_num >= 4:
        suggested_tier = 2
    else:
        suggested_tier = 1

    grace_recommendation = {
        "should_offer": should_offer_grace,
        "suggested_tier": suggested_tier,
        "honest_fit_advisory": honest_fit_advisory,
        "has_actionable_headroom": has_actionable_headroom,
        "reasons": grace_reasons,
        "stalled_item_ids": [it["id"] for it in actionable_stalled_items],
    }

    gap_rank = {"expression_gap": 0, "transferable_gap": 1, "true_gap": 2, None: 3}
    top_priorities = sorted(
        [r for r in item_results if r["grade"] != "FULL"],
        key=lambda r: (
            0 if (r["is_knockout"] and r["grade"] in KNOCKOUT_RISK_GRADES) else 1,
            -r["uplift_to_full_pp"],
            gap_rank.get(r["gap_type"], 3),
            r["id"],
        ),
    )

    clean_categories = {}
    for cat, data in category_results.items():
        clean_categories[cat] = {k: v for k, v in data.items() if not k.endswith("_exact")}
        clean_categories[cat]["delta_points_pp"] = cat_deltas[cat]

    clean_items = [{k: v for k, v in r.items() if not k.endswith("_exact")} for r in item_results]
    clean_priorities = [{k: v for k, v in r.items() if not k.endswith("_exact")} for r in top_priorities]
    clean_kw_details = [{k: v for k, v in d.items() if not k.endswith("_exact")} for d in ats_audit["details"]]

    return {
        "session": {
            "company": rubric.get("company", ""),
            "role_title": rubric.get("role_title", ""),
            "language": lang,
            "domain_mode": domain_mode,
            "rubric_hash": current_hash,
        },
        "round": round_num,
        "grace_tier_used": grace_tier_used_current,
        "evaluated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pass_threshold": float(threshold_display),
        "total_score": float(display_score),
        "total_score_2dp": float(_round2(total_exact)),
        "total_score_exact": str(total_exact.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)),
        "pass_status": pass_status,
        "passed_threshold": passed_threshold,
        "gap_to_pass_pp": float(gap_to_pass_display),
        "must_have_attainment_pct": clean_categories["must_have"]["attainment_pct"],
        "projected_expression_only_score": float(proj_expr_display),
        "projected_with_transferable_cap": float(proj_trans_display),
        "projected_score_without_true_gaps": float(proj_trans_display),
        "actionable_expression_uplift_pp": float(actionable_expr_uplift_display),
        "actionable_transferable_cap_uplift_pp": float(_round1(transferable_capped_uplift)),
        "actionable_uplift_total_pp": float(_round1(actionable_uplift_total)),
        "missing_ats_uplift_pp": float(_round1(sum_kw_uplifts)),
        "knockout_risks": knockout_risks,
        "unverified_quotes": unverified_quotes,
        "rubric_warnings": rubric_warnings,
        "invalidated_subsequent_rounds": later_rounds,
        "categories": clean_categories,
        "ats_keywords": {
            "checked": ats_audit["checked"],
            "total_count": ats_audit["total_count"],
            "matched_count": ats_audit["matched_count"],
            "coverage_pct": ats_audit["coverage_pct"],
            "missing_must": [d for d in clean_kw_details if not d["matched"] and d["tier"] == "must"],
            "missing_preferred": [d for d in clean_kw_details if not d["matched"] and d["tier"] == "preferred"],
            "negated_mentions": [d for d in clean_kw_details if d.get("negated_mention")],
            "contradictory_mentions": [d for d in clean_kw_details if d.get("contradictory_mention")],
            "details": clean_kw_details,
        },
        "round_diff": {
            "has_previous": prev_round is not None,
            "previous_round": prev_round["round"] if prev_round else None,
            "previous_score": float(prev_score_display) if prev_score_display is not None else None,
            "delta_score_pp": float(delta_score_display) if delta_score_display is not None else None,
            "delta_score_exact_2dp": float(_round2(delta_score_exact)) if delta_score_exact is not None else None,
            "resolved_items": resolved_items,
            "improved_items": improved_items,
            "regressed_items": regressed_items,
            "stalled_items": stalled_items,
        },
        "grace_recommendation": grace_recommendation,
        "top_priorities": clean_priorities,
        "items": clean_items,
    }


def _category_status_badge(attainment: float, lang: str) -> str:
    strong, solid, needs_work, weak = I18N[lang]["status_badges"]
    if attainment >= 85.0:
        return strong
    if attainment >= 70.0:
        return solid
    if attainment >= 50.0:
        return needs_work
    return weak


def _format_kw_with_aliases(kw: dict[str, Any]) -> str:
    term = kw["term"]
    aliases = [a for a in kw.get("aliases", []) if a.lower() != term.lower()]
    if not aliases:
        return f"`{term}`"
    joined = "/".join(aliases)
    if joined.lower() == term.lower():
        return f"`{term}`"
    return f"`{term}` ({joined})"


def render_markdown_report(res: dict[str, Any]) -> str:
    """Render standardized native Markdown report (ko, en, zh, ja) with display-consistent rounding & locale units."""
    lang = res["session"].get("language", "ko")
    domain_mode = res["session"].get("domain_mode", "portfolio")
    t = I18N[lang]
    u = t["unit_pp"]
    sep = t["sep"]
    sp = " " if lang in ("en", "zh") else ""
    doc_noun = t["doc_noun"][domain_mode]
    company = res["session"]["company"]
    role = res["session"]["role_title"]
    header_target = sep.join(p for p in (company, role) if p) or t["default_target"]

    lines = [
        t["report_title"].format(round=res["round"], target=header_target),
        "",
        t["overall_score"].format(
            score=_fmt1(res["total_score"]),
            threshold=_fmt1(res["pass_threshold"]),
            badge=t["badges"][res["pass_status"]],
        ),
    ]
    if res["round_diff"]["has_previous"]:
        d = res["round_diff"]["delta_score_pp"]
        sign = "+" if d >= 0 else ""
        lines.append(
            t["round_delta"].format(
                prev_r=res["round_diff"]["previous_round"],
                curr_r=res["round"],
                prev_s=_fmt1(res["round_diff"]["previous_score"]),
                curr_s=_fmt1(res["total_score"]),
                sign=sign,
                delta=_fmt1(d),
                u=u,
            )
        )
    if res["pass_status"] == "REVISE":
        lines.append(t["gap_to_pass"].format(gap=_fmt1(res["gap_to_pass_pp"]), u=u))
        lo = _fmt1(res["projected_expression_only_score"])
        hi = _fmt1(res["projected_with_transferable_cap"])
        if lo == hi:
            lines.append(t["proj_single"].format(lo=lo, uplift=_fmt1(res["actionable_expression_uplift_pp"]), u=u))
        else:
            lines.append(t["proj_range"].format(lo=lo, hi=hi))
    if res["must_have_attainment_pct"] is not None:
        lines.append(t["must_have_pct"].format(pct=_fmt1(res["must_have_attainment_pct"])))
    if res["ats_keywords"]["checked"]:
        ak = res["ats_keywords"]
        lines.append(
            t["ats_coverage"].format(
                matched=ak["matched_count"],
                total=ak["total_count"],
                pct=_fmt1(ak["coverage_pct"]),
            )
        )
    lines.append(t["rubric_hash"].format(hash=res["session"]["rubric_hash"]))
    lines.append("")
    lines.extend(
        [
            t["cat_heading"],
            "",
            t["cat_table_header"],
            "| :--- | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    for cat in CATEGORY_ORDER:
        c = res["categories"][cat]
        if not c["active"]:
            continue
        delta_str = "—"
        if c["delta_points_pp"] is not None:
            dsign = "+" if c["delta_points_pp"] >= 0 else ""
            delta_str = f"{dsign}{_fmt1(c['delta_points_pp'])}{sp}{u}"
        status_txt = _category_status_badge(c["attainment_pct"], lang)
        lines.append(
            f"| {c['label']} (`{cat}`) | {_fmt1(c['effective_weight'])}% | "
            f"{_fmt1(c['attainment_pct'])}% | {_fmt1(c['earned_points'])} / {_fmt1(c['max_points'])} | {delta_str} | {status_txt} |"
        )
    lines.append("")

    if res["knockout_risks"]:
        lines.append("> [!WARNING]")
        lines.append(t["knockout_warn"])
        for kr in res["knockout_risks"]:
            lines.append(f"> - **`{kr['id']}` {kr['title']}** (`{kr['grade']}`{sep}`{kr['gap_type']}`): {kr['action_hint']}")
        lines.append("")

    if res["unverified_quotes"]:
        lines.append("> [!NOTE]")
        ids = ", ".join(q["id"] for q in res["unverified_quotes"])
        lines.append(t["quote_audit_note"].format(ids=ids))
        lines.append("")

    if res["round_diff"]["has_previous"]:
        rd = res["round_diff"]
        lines.append(t["diff_heading"].format(prev_r=rd["previous_round"], curr_r=res["round"]))
        lines.append("")
        if rd["improved_items"]:
            lines.append(t["improved_hdr"])
            for it in rd["improved_items"]:
                badge = " ✅" if it["to"] == "FULL" else ""
                lines.append(
                    f"  - `{it['id']}` {it['title']}: `{it['from']} → {it['to']}` (`+{_fmt1(it['delta_pp'])}{sp}{u}`){badge}"
                )
        else:
            lines.append(t["improved_none"])
        if rd["regressed_items"]:
            lines.append(t["regressed_hdr"])
            for it in rd["regressed_items"]:
                lines.append(
                    f"  - `{it['id']}` {it['title']}: `{it['from']} → {it['to']}` (`{_fmt1(it['delta_pp'])}{sp}{u}`)"
                )
        if rd["stalled_items"] and res["pass_status"] != "PASS":
            lines.append(t["stalled_hdr"])
            for it in rd["stalled_items"]:
                lines.append(
                    t["stalled_line"].format(
                        id=it["id"],
                        title=it["title"],
                        grade=it["grade"],
                        streak=it["stalled_streak"],
                        gap_type=it["gap_type"],
                        uplift=_fmt1(it["uplift_to_full_pp"]),
                        u=u,
                    )
                )
        lines.append("")

    if res["top_priorities"]:
        lines.append(t["priority_heading"])
        lines.append("")
        for gtype, heading in t["gap_sections"]:
            group = [p for p in res["top_priorities"] if p["gap_type"] == gtype]
            if not group:
                continue
            lines.append(f"### {heading}")
            lines.append("")
            for idx, item in enumerate(group, start=1):
                ko_tag = " **[KNOCKOUT]**" if item["is_knockout"] else ""
                show_stall = (
                    item["stalled_streak"] >= 2
                    and res["pass_status"] != "PASS"
                    and item["gap_type"] != "true_gap"
                )
                stall_tag = t["stall_tag"].format(streak=item["stalled_streak"]) if show_stall else ""
                lines.append(
                    t["item_line"].format(
                        idx=idx,
                        id=item["id"],
                        title=item["title"],
                        ko_tag=ko_tag,
                        stall_tag=stall_tag,
                        grade=item["grade"],
                        uplift=_fmt1(item["uplift_to_full_pp"]),
                        u=u,
                    )
                )
                if item["evidence_quote"]:
                    src = f" ({item['source']})" if item["source"] else ""
                    lines.append(t["evidence_present"].format(src=src, quote=item["evidence_quote"]))
                else:
                    lines.append(t["evidence_missing"])
                if item["action_hint"]:
                    lines.append(t["revision_dir"].format(hint=item["action_hint"]))
            lines.append("")

    if res["ats_keywords"]["checked"]:
        mm = res["ats_keywords"]["missing_must"]
        mp = res["ats_keywords"]["missing_preferred"]
        neg = res["ats_keywords"]["negated_mentions"]
        contra = res["ats_keywords"].get("contradictory_mentions", [])
        if mm or mp or contra:
            lines.append(t["ats_heading"])
            lines.append("")
            if contra:
                c_terms = ", ".join(f"`{k['term']}`" for k in contra)
                lines.append("> [!WARNING]")
                lines.append(t["contra_warn"].format(terms=c_terms))
                lines.append("")
            if mm:
                fmt = ", ".join(_format_kw_with_aliases(k) for k in mm)
                lines.append(t["missing_must"].format(fmt=fmt))
            if mp:
                fmt = ", ".join(_format_kw_with_aliases(k) for k in mp)
                lines.append(t["missing_pref"].format(fmt=fmt))
            if neg:
                neg_terms = ", ".join(f"`{k['term']}`" for k in neg)
                lines.append(t["negated_note"].format(terms=neg_terms))
            lines.append(t["ats_tip"])
            lines.append("")

    gr = res["grace_recommendation"]
    if res["pass_status"] == "REVISE":
        actionable_top3 = [p for p in res["top_priorities"] if p["gap_type"] != "true_gap"][:3]
        if actionable_top3:
            can_reach = _dec(res["projected_with_transferable_cap"]) >= _dec(res["pass_threshold"])
            mission_heading = (
                t["mission_reach"].format(threshold=_fmt1(res["pass_threshold"]))
                if can_reach
                else t["mission_unreach"].format(threshold=_fmt1(res["pass_threshold"]))
            )
            lines.append(mission_heading)
            lines.append("")
            for i, p in enumerate(actionable_top3, start=1):
                if p["gap_type"] == "transferable_gap" and p.get("uplift_transferable_cap_pp", 0) > 0:
                    gain_txt = t["gain_transferable"].format(
                        cap=_fmt1(p["uplift_transferable_cap_pp"]),
                        full=_fmt1(p["uplift_to_full_pp"]),
                        u=u,
                    )
                else:
                    gain_txt = t["gain_full"].format(full=_fmt1(p["uplift_to_full_pp"]), u=u)
                lines.append(f"{i}. **`{p['id']}` {p['title']}** (`{p['grade']}`{sep}{gain_txt})")
            lines.append("")
        if gr["honest_fit_advisory"]:
            if not gr.get("has_actionable_headroom", False):
                adv_text = t["honest_fit_only"]
            elif _dec(res["projected_with_transferable_cap"]) < _dec(res["pass_threshold"]):
                adv_text = t["honest_fit_capped"].format(
                    hi=_fmt1(res["projected_with_transferable_cap"]),
                    threshold=_fmt1(res["pass_threshold"]),
                )
            else:
                adv_text = t["honest_fit_knockout"].format(hi=_fmt1(res["projected_with_transferable_cap"]))
            lines.extend(["> [!IMPORTANT]", adv_text, ""])
        if gr["should_offer"]:
            lines.extend(
                [
                    "> [!TIP]",
                    t["grace_offer_hdr"].format(tier=gr["suggested_tier"], reasons=" / ".join(gr["reasons"])),
                    t["grace_offer_body"],
                    "",
                ]
            )
        elif not gr["honest_fit_advisory"]:
            lines.append(t["cta_revise"].format(doc=doc_noun, next_r=res["round"] + 1))
            lines.append("")
    elif res["pass_status"] == "PASS_WITH_RISK":
        lines.append(t["cta_pass_risk"])
        lines.append("")
    else:
        lines.append(t["cta_pass"].format(doc=doc_noun))
        if res["round_diff"]["regressed_items"]:
            reg_ids = ", ".join(it["id"] for it in res["round_diff"]["regressed_items"])
            lines.append(t["cta_pass_regression_note"].format(ids=reg_ids))
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def update_history(history_path: Path, result: dict[str, Any]) -> dict[str, Any]:
    """Persist round result idempotently; drops stale subsequent rounds if an earlier round is re-run."""
    if history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8-sig"))
    else:
        history = {
            "session": result["session"],
            "rubric_hash": result["session"]["rubric_hash"],
            "pass_threshold": result["pass_threshold"],
            "rounds": [],
        }

    cur_round = int(result["round"])
    rounds = [r for r in history.get("rounds", []) if int(r["round"]) < cur_round]
    rounds.append(
        {
            "round": cur_round,
            "evaluated_at": result["evaluated_at"],
            "total_score": result["total_score"],
            "total_score_2dp": result["total_score_2dp"],
            "total_score_exact": result["total_score_exact"],
            "pass_status": result["pass_status"],
            "grace_tier_used": result.get("grace_tier_used"),
            "categories": result["categories"],
            "items": [
                {
                    "id": it["id"],
                    "grade": it["grade"],
                    "earned_points_pp": it["earned_points_pp"],
                    "gap_type": it["gap_type"],
                    "stalled_streak": it["stalled_streak"],
                }
                for it in result["items"]
            ],
            "grace_recommended": result["grace_recommendation"]["should_offer"],
        }
    )
    rounds.sort(key=lambda r: int(r["round"]))
    history["rounds"] = rounds

    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return history


def init_rubric_command(rubric_path: Path) -> int:
    rubric = json.loads(rubric_path.read_text(encoding="utf-8-sig"))
    item_map, warnings = validate_rubric(rubric)
    rhash = compute_rubric_hash(rubric)
    rubric["rubric_hash"] = rhash
    rubric["locked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rubric_path.write_text(json.dumps(rubric, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {cat: len(rubric.get("categories", {}).get(cat, [])) for cat in CATEGORY_ORDER}
    summary = {
        "status": "RUBRIC_LOCKED",
        "rubric_path": str(rubric_path.resolve()),
        "rubric_hash": rhash,
        "language": str(rubric.get("language", "ko")).lower(),
        "domain_mode": str(rubric.get("domain_mode", "portfolio")).lower(),
        "pass_threshold": float(_round1(_dec(rubric.get("pass_threshold", 80.0)))),
        "total_items": len(item_map),
        "category_item_counts": counts,
        "keyword_count": len(rubric.get("keywords", [])),
        "warnings": warnings,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Deterministic rubric lock & multilingual match scorer for resume-jd-coach (v2.1).")
    parser.add_argument("--init-rubric", help="Validate and stamp rubric_hash onto rubric.json, then exit.")
    parser.add_argument("--rubric", help="Path to locked rubric.json.")
    parser.add_argument("--eval", dest="eval_path", help="Path to round_NN_eval.json.")
    parser.add_argument("--candidate-text", help="Path to consolidated plain-text candidate resume+portfolio.")
    parser.add_argument("--history", help="Path to session history.json (read prior rounds & append current).")
    parser.add_argument("--report-out", help="Optional path to write rendered Markdown coaching report.")
    parser.add_argument(
        "--lang",
        choices=["ko", "en", "zh", "ja"],
        help="Override report language (default from rubric.json or ko).",
    )
    parser.add_argument(
        "--domain-mode",
        choices=["portfolio", "resume_only"],
        help="Override portfolio_impact category label mode (portfolio vs resume_only).",
    )
    parser.add_argument(
        "--strict-quotes",
        action="store_true",
        help="Fail with non-zero exit code if any evidence_quote cannot be verified against --candidate-text.",
    )
    args = parser.parse_args()

    if args.init_rubric:
        return init_rubric_command(Path(args.init_rubric))

    if not args.rubric or not args.eval_path:
        parser.error("Provide either --init-rubric <path> OR both --rubric <path> and --eval <path>.")

    rubric_path = Path(args.rubric)
    eval_path = Path(args.eval_path)
    rubric = json.loads(rubric_path.read_text(encoding="utf-8-sig"))
    eval_data = json.loads(eval_path.read_text(encoding="utf-8-sig"))

    candidate_text = None
    if args.candidate_text:
        candidate_text = Path(args.candidate_text).read_text(encoding="utf-8-sig")

    history = None
    history_path = Path(args.history) if args.history else None
    if history_path and history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8-sig"))

    result = evaluate_round(
        rubric,
        eval_data,
        candidate_text=candidate_text,
        history=history,
        require_locked=True,
        strict_quotes=args.strict_quotes,
        lang_override=args.lang,
        domain_mode_override=args.domain_mode,
    )

    if history_path:
        update_history(history_path, result)

    if args.report_out:
        report_path = Path(args.report_out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_markdown_report(result), encoding="utf-8")
        result["report_path"] = str(report_path.resolve())

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
