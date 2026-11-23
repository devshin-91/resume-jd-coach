# Coaching Report & Round-Diff Template (`resume-jd-coach`)

Use this structure when presenting evaluation results to the user after running `score_match.py`.
Keep language **strictly aligned** with the session language (`ko`, `en`, `zh`, or `ja`) with **zero cross-language leakage** — `score_match.py --report-out` automatically renders native headers, tables, badges, warnings, and CTAs for all 4 languages.

---

## 1. Scoreboard Header (Always First)

```markdown
## 채용공고 일치율 진단 — Round {N} ({Company / Role})

- **종합 일치율:** **{total_score}%** / 합격 기준 **{pass_threshold}%** {status_badge}
  - *(Round 2+)* **직전 라운드 대비:** `{prev_score}% → {total_score}% ({delta_sign}{delta_score}%p)`
  - *(미달 시)* **합격선까지 남은 점수:** `+{gap_to_pass}%p`
  - *(미달 시)* **정직한 도달 가능 점수 범위:** `{projected_expression_only_score}%` (표현 보강 확실치) ~ `{projected_with_transferable_cap}%` (유사 역량 `STRONG_PARTIAL` 상한 반영 시)
- **필수 자격(Must-Have) 충족률:** `{must_have_pct}%`
- **ATS 핵심 키워드 커버리지:** `{matched_kw}/{total_kw}` ({ats_kw_pct}%)
```

Status badges:
- `PASS` → `✅ PASS (지원 준비 완료)`
- `PASS_WITH_RISK` → `⚠️ PASS_WITH_RISK (80% 도달 · 핵심 필수요건 위험 경고)`
- `REVISE` → `🔁 REVISE (보완 후 재검토 필요)`

---

## 2. Category Breakdown Table

| 평가 영역 | 배점 비중 | 현재 충족률 | 획득 점수 | Round Δ | 상태 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 필수 자격 & 핵심 직무 (`must_have`) | 45% | ...% | ... / 45.0 | +...%p | ... |
| 포트폴리오 증빙 & 성과 (`portfolio_impact`) | 25% | ...% | ... / 25.0 | +...%p | ... |
| 우대 사항 (`preferred`) | 15% | ...% | ... / 15.0 | +...%p | ... |
| JD 키워드 & 포지셔닝 (`ats_framing`) | 15% | ...% | ... / 15.0 | +...%p | ... |

*(If `knockout_risks` is non-empty, insert a prominent `> [!WARNING]` block right below the table listing each missing knockout requirement clearly.)*

---

## 3. Round-over-Round Progress Summary (Round 2+ Only)

- **해결/상승된 항목 (`Improved / Resolved`):** `항목명 (PARTIAL → FULL, +X.X%p)`
- **점수 하락 항목 (`Regressed` — 의도치 않은 삭제 여부 확인):** *(only if any)*
- **아직 미해결 항목 (`Still Open`):** count + highlight stalled items (`⚠️ 2라운드 연속 정체`)

---

## 4. Priority Revision Guide (Coach-First — Do NOT Rewrite!)

Sort by **highest `+X.X%p` uplift potential first**. Group or tag clearly by `gap_type`:

### 🎯 최우선 수정 포인트 (표현·증빙 보강으로 빠른 점수 상승 — `expression_gap`)
For each item:
1. **`[항목명]`** — 현재 `{GRADE}` → `FULL` 도달 시 **`+{uplift}%p`**
   - **공고 요구 맥락:** (1 sentence grounded in JD)
   - **현재 이력서/포트폴리오 진단:** (cite verbatim what was found or absent, e.g., "프로젝트 A에 기술 스택만 나열되어 있고 성과/본인 역할이 빠져 있음")
   - **직접 고칠 포인트:** (concrete, actionable coaching direction — *what* to surface, *where* to place it, *what evidence* convinces a hiring manager — **never write the final resume paragraph for them in default mode**)

### 🌉 유사 경험 연결 포인트 (`transferable_gap`)
- Explain how to honestly bridge adjacent experience to the JD's core requirement without exaggerating.

### 🧭 실제 미보유 역량 점검 (`true_gap` — 창작 금지)
- State transparently that wording tweaks cannot invent missing experience; advise whether other items alone can carry the candidate over `80%` (give the math: e.g., "표현 보강 항목만 챙겨도 최대 `+18.4%p` 상승해 `82.9%` 도달 가능") or suggest realistic mitigation.

---

## 5. ATS Missing Keywords Snapshot

- **필수 키워드 미반영 (`must`):** `Term A (별칭: ...)`, `Term B`
- **우대 키워드 미반영 (`preferred`):** `Term C`, ...
- *(Reminder: 실제로 보유/사용한 용어만 프로젝트 맥락 속에 자연스럽게 반영하세요. 단순 키워드 나열은 실무 역량 점수로 인정되지 않습니다.)*

---

## 6. Next-Step Call to Action & Optional Grace Offer

- **If `REVISE` (Normal):**
  - Give a crisp 2–4 item "이번 라운드 핵심 미션" showing the fastest path across `80.0%`.
  - Invite the user: *"위 포인트를 반영해 이력서/포트폴리오를 수정하신 뒤 다시 올려주시면 **Round {N+1}**으로 동일 기준 재평가를 진행하겠습니다. 진행하다가 막히는 항목이 생기면 언제든 말씀해 주세요 — 1~3단계 보조 모드(Grace)로 같이 풀어드릴 수 있습니다."*
- **If `REVISE` + `grace_recommendation.should_offer == true`:**
  - Append the explicit, gentle Grace Offer from [grace-coaching-playbook.md](./grace-coaching-playbook.md#1-activation-triggers), naming the specific stalled item(s).
- **If `PASS`:**
  - Summarize top 3 competitive strengths to lean on in interviews, optionally share 1–2 polish tips, and confirm they are ready to apply!
