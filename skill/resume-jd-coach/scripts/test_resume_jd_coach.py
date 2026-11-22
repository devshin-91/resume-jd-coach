#!/usr/bin/env python3
"""Automated self-test suite for resume-jd-coach v1.1 scripts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from decimal import Decimal
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import extract_doc  # noqa: E402
import score_match  # noqa: E402


def _make_minimal_rubric(
    *,
    include_preferred: bool = True,
    knockout_mh2: bool = False,
    pass_threshold: float = 80.0,
    language: str = "ko",
    domain_mode: str = "portfolio",
) -> dict:
    rubric = {
        "company": "TestCo",
        "role_title": "Test Role",
        "language": language,
        "domain_mode": domain_mode,
        "pass_threshold": pass_threshold,
        "ats_lexical_share": 0.5,
        "category_weights": {
            "must_have": 45,
            "portfolio_impact": 25,
            "preferred": 15,
            "ats_framing": 15,
        },
        "categories": {
            "must_have": [
                {"id": "MH-1", "title": "Core Skill 1", "weight": 2, "is_knockout": True},
                {"id": "MH-2", "title": "Core Skill 2", "weight": 2, "is_knockout": knockout_mh2},
            ],
            "portfolio_impact": [
                {"id": "PI-1", "title": "Case Study", "weight": 1, "is_knockout": False},
            ],
            "preferred": (
                [{"id": "PR-1", "title": "Bonus Skill", "weight": 1, "is_knockout": False}]
                if include_preferred
                else []
            ),
            "ats_framing": [
                {"id": "AF-1", "title": "Summary Positioning", "weight": 1, "is_knockout": False},
            ],
        },
        "keywords": [
            {"term": "Go", "aliases": ["Golang"], "tier": "must"},
            {"term": "데이터 분석", "aliases": ["Data Analysis"], "tier": "preferred"},
        ],
    }
    rubric["rubric_hash"] = score_match.compute_rubric_hash(rubric)
    return rubric


class TestATSKeywordBoundaryAndNegation(unittest.TestCase):
    def test_ascii_korean_boundaries_and_special_symbols(self) -> None:
        keywords = [
            {"term": "Go", "aliases": ["Golang"], "tier": "must"},
            {"term": "Java", "aliases": [], "tier": "must"},
            {"term": "C", "aliases": [], "tier": "must"},
            {"term": "R", "aliases": [], "tier": "must"},
            {"term": "C++", "aliases": [], "tier": "must"},
            {"term": ".NET", "aliases": [], "tier": "must"},
            {"term": "Kubernetes", "aliases": ["K8s", "쿠버네티스"], "tier": "must"},
            {"term": "인사", "aliases": [], "tier": "preferred"},
            {"term": "데이터 분석", "aliases": [], "tier": "preferred"},
        ]

        tricky_text = (
            "Google Cloud, Django, Logo, MongoDB, JavaScript, C-level 임원 보고, R&D 조직, "
            "C++17, C#, CSS, ASP.NET 백엔드, 개인사정으로 휴학, 확인사항 점검, 데이터분석 수행"
        )
        audit = score_match.audit_ats_keywords(keywords, tricky_text)
        by_term = {d["term"]: d for d in audit["details"]}

        self.assertFalse(by_term["Go"]["matched"])
        self.assertFalse(by_term["Java"]["matched"])
        self.assertFalse(by_term["C"]["matched"])
        self.assertFalse(by_term["R"]["matched"])
        self.assertTrue(by_term["C++"]["matched"])
        self.assertTrue(by_term[".NET"]["matched"])
        self.assertFalse(by_term["Kubernetes"]["matched"])
        self.assertFalse(by_term["인사"]["matched"])  # Must NOT match 개인사정 or 확인사항!
        self.assertTrue(by_term["데이터 분석"]["matched"])

        korean_text = "Go로 API 개발, Java기반 결제, C 언어로 임베디드, R 통계, 쿠버네티스를 운영, 인사운영 인턴"
        audit2 = score_match.audit_ats_keywords(keywords, korean_text)
        by_term2 = {d["term"]: d for d in audit2["details"]}

        self.assertTrue(by_term2["Go"]["matched"])
        self.assertTrue(by_term2["Java"]["matched"])
        self.assertTrue(by_term2["C"]["matched"])
        self.assertTrue(by_term2["R"]["matched"])
        self.assertTrue(by_term2["Kubernetes"]["matched"])
        self.assertTrue(by_term2["인사"]["matched"])

    def test_negation_section_and_clause_filtering(self) -> None:
        keywords = [
            {"term": "Kubernetes", "aliases": ["K8s"], "tier": "must"},
            {"term": "MCP", "aliases": [], "tier": "must"},
            {"term": "Spark", "aliases": ["PySpark"], "tier": "must"},
            {"term": "PyTorch", "aliases": [], "tier": "must"},
            {"term": "SQL", "aliases": ["BigQuery"], "tier": "must"},
            {"term": "Python", "aliases": [], "tier": "must"},
        ]
        text = (
            "경력 요약\n"
            "- Spark는 미경험이지만 BigQuery SQL로 데이터 마트 구축.\n"
            "- PyTorch는 아직 미경험이며, Python 통계 실험 중심으로 기여 가능.\n"
            "- No experience with PyTorch but used Python extensively in production.\n\n"
            "아직 해 보지 않은 것\n"
            "MCP 서버 운영, Kubernetes 다중 노드 운영\n"
        )
        audit = score_match.audit_ats_keywords(keywords, text)
        by_term = {d["term"]: d for d in audit["details"]}

        self.assertFalse(by_term["Kubernetes"]["matched"])
        self.assertTrue(by_term["Kubernetes"]["negated_mention"])
        self.assertFalse(by_term["MCP"]["matched"])
        self.assertTrue(by_term["MCP"]["negated_mention"])
        self.assertFalse(by_term["Spark"]["matched"])
        self.assertTrue(by_term["Spark"]["negated_mention"])
        self.assertFalse(by_term["PyTorch"]["matched"])
        self.assertTrue(by_term["PyTorch"]["negated_mention"])
        self.assertTrue(by_term["SQL"]["matched"])
        self.assertFalse(by_term["SQL"]["contradictory_mention"])
        self.assertTrue(by_term["Python"]["matched"])
        self.assertFalse(by_term["Python"]["contradictory_mention"])

    def test_contradictory_mention_detected_and_reported(self) -> None:
        keywords = [{"term": "Spark", "aliases": ["PySpark"], "tier": "must"}]
        text = (
            "보유 스킬: SQL, Spark, Python\n"
            "아직 해 보지 않은 것\n"
            "Spark 분산 처리\n"
        )
        audit = score_match.audit_ats_keywords(keywords, text)
        detail = audit["details"][0]
        self.assertTrue(detail["matched"])
        self.assertTrue(detail["contradictory_mention"])


class TestScoringMathAndGuardrailsV11(unittest.TestCase):
    def test_exact_weighted_score_conservation_and_rounding_half_up(self) -> None:
        rubric = _make_minimal_rubric()
        cand = "Go로 마이크로서비스 개발. Built X. Mentioned Y. Portfolio slide 2. Clear headline."
        eval_data = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "PARTIAL", "evidence_quote": "Mentioned Y", "gap_type": "expression_gap"},
                {"id": "PI-1", "grade": "STRONG_PARTIAL", "evidence_quote": "Portfolio slide 2", "gap_type": "expression_gap"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Clear headline"},
            ],
        }
        res = score_match.evaluate_round(rubric, eval_data, candidate_text=cand, strict_quotes=True)
        self.assertEqual(res["total_score"], 65.0)
        self.assertEqual(res["pass_status"], "REVISE")
        self.assertEqual(res["unverified_quotes"], [])

        # Verify ROUND_HALF_UP helper: 14.25 -> "14.3" (never "14.2" Banker's Rounding!)
        self.assertEqual(score_match._fmt1(Decimal("14.25")), "14.3")
        self.assertEqual(score_match._fmt1(Decimal("11.25")), "11.3")

    def test_dual_projection_range_and_zero_true_gap_reaches_100(self) -> None:
        rubric = _make_minimal_rubric()
        cand = "Go 개발. Built X."
        # Zero true gaps -> projected_expression_only includes ATS uplift and reaches 100.0
        eval_no_true = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "gap_type": "expression_gap"},
                {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "expression_gap"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "expression_gap"},
                {"id": "AF-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "expression_gap"},
            ],
        }
        res_100 = score_match.evaluate_round(rubric, eval_no_true, candidate_text=cand)
        self.assertEqual(res_100["projected_expression_only_score"], 100.0)
        self.assertEqual(res_100["projected_with_transferable_cap"], 100.0)

        # With true_gap + transferable_gap (at PARTIAL=0.50): transferable capped at 0.75 (not 1.00!)
        eval_mixed = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "PARTIAL", "evidence_quote": "Go 개발", "gap_type": "transferable_gap"},
                {"id": "PI-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Go 개발"},
            ],
        }
        res_mix = score_match.evaluate_round(rubric, eval_mixed, candidate_text="Go 개발 데이터 분석 Built X")
        # total = 45*0.75 (33.75) + 25 + 0 + 15 = 73.75 -> 73.8
        # expression_only = 73.8 (0 expression_gap)
        # transferable MH-2 max=22.5, earned=11.25, capped at 0.75 -> +5.625 -> 79.375 -> 79.4 (< 80.0! honest!)
        self.assertEqual(res_mix["projected_expression_only_score"], 73.8)
        self.assertEqual(res_mix["projected_with_transferable_cap"], 79.4)
        self.assertLess(res_mix["projected_with_transferable_cap"], 80.0)

    def test_knockout_weight_floor_and_weak_triggers_pass_with_risk(self) -> None:
        bad_rubric = _make_minimal_rubric(knockout_mh2=True)
        bad_rubric["categories"]["must_have"][1]["weight"] = 1
        with self.assertRaisesRegex(ValueError, "KNOCKOUT_WEIGHT_ERROR"):
            score_match.validate_rubric(bad_rubric)

        # Knockout with weight >= 2 graded WEAK while overall >= 80% -> PASS_WITH_RISK!
        rubric = _make_minimal_rubric(knockout_mh2=True)
        rubric["categories"]["must_have"] = [
            {"id": "MH-1", "title": "Big Pillar", "weight": 8, "is_knockout": False},
            {"id": "MH-2", "title": "Mandatory License", "weight": 2, "is_knockout": True},
        ]
        rubric["rubric_hash"] = score_match.compute_rubric_hash(rubric)
        cand = "Go 데이터 분석 Deep proof Strong portfolio Bonus Sharp framing License tag"
        eval_data = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Deep proof"},
                {"id": "MH-2", "grade": "WEAK", "evidence_quote": "License tag", "gap_type": "expression_gap"},
                {"id": "PI-1", "grade": "FULL", "evidence_quote": "Strong portfolio"},
                {"id": "PR-1", "grade": "FULL", "evidence_quote": "Bonus"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Sharp framing"},
            ],
        }
        res = score_match.evaluate_round(rubric, eval_data, candidate_text=cand)
        self.assertGreaterEqual(res["total_score"], 80.0)
        self.assertEqual(res["pass_status"], "PASS_WITH_RISK")
        self.assertEqual(res["knockout_risks"][0]["id"], "MH-2")
        self.assertEqual(res["knockout_risks"][0]["grade"], "WEAK")
        # Knockout risk must sort #1 in top_priorities!
        self.assertEqual(res["top_priorities"][0]["id"], "MH-2")

    def test_unlocked_rubric_missing_candidate_text_and_unverified_quote_guards(self) -> None:
        unlocked = _make_minimal_rubric()
        del unlocked["rubric_hash"]
        ev = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "FULL", "evidence_quote": "Built Y"},
                {"id": "PI-1", "grade": "FULL", "evidence_quote": "Slide 1"},
                {"id": "PR-1", "grade": "FULL", "evidence_quote": "Bonus"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Summary"},
            ],
        }
        with self.assertRaisesRegex(ValueError, "RUBRIC_UNLOCKED_ERROR"):
            score_match.evaluate_round(unlocked, ev, candidate_text="Go")

        locked = _make_minimal_rubric()
        with self.assertRaisesRegex(ValueError, "CANDIDATE_TEXT_REQUIRED_ERROR"):
            score_match.evaluate_round(locked, ev, candidate_text=None)

        # Unverified fabricated quote caught!
        with self.assertRaisesRegex(ValueError, "QUOTE_VERIFICATION_ERROR"):
            score_match.evaluate_round(locked, ev, candidate_text="Completely unrelated resume text", strict_quotes=True)

    def test_true_gap_only_suppresses_grace_and_emits_honest_fit_advisory(self) -> None:
        rubric = _make_minimal_rubric()
        cand = "Go 데이터 분석 Built X Summary"
        ev_r1 = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "PI-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Summary"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            hp = Path(tmp) / "history.json"
            r1 = score_match.evaluate_round(rubric, ev_r1, candidate_text=cand)
            score_match.update_history(hp, r1)
            hist1 = json.loads(hp.read_text(encoding="utf-8"))
            ev_r2 = json.loads(json.dumps(ev_r1))
            ev_r2["round"] = 2
            r2 = score_match.evaluate_round(rubric, ev_r2, candidate_text=cand, history=hist1)
            self.assertEqual(r2["pass_status"], "REVISE")
            self.assertFalse(r2["grace_recommendation"]["should_offer"])
            self.assertTrue(r2["grace_recommendation"]["honest_fit_advisory"])

    def test_grace_tier3_escalation_history_invalidation_and_english_resume_only_mode(self) -> None:
        rubric = _make_minimal_rubric(language="en", domain_mode="resume_only")
        cand = "Go Built X Brief mention Slide 2 Summary"
        ev = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built X"},
                {"id": "MH-2", "grade": "PARTIAL", "evidence_quote": "Brief mention", "gap_type": "expression_gap"},
                {"id": "PI-1", "grade": "STRONG_PARTIAL", "evidence_quote": "Slide 2", "gap_type": "expression_gap"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Summary"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            hp = Path(tmp) / "history.json"
            r1 = score_match.evaluate_round(rubric, ev, candidate_text=cand)
            score_match.update_history(hp, r1)
            md_en = score_match.render_markdown_report(r1)
            self.assertIn("JD Match Diagnostic — Round 1", md_en)
            self.assertIn("Work Proof & Measurable Impact", md_en)

            # Round 2 with grace_tier_used=2 -> next stall escalates to Tier 3!
            e2 = json.loads(json.dumps(ev))
            e2["round"] = 2
            e2["grace_tier_used"] = 2
            r2 = score_match.evaluate_round(rubric, e2, candidate_text=cand, history=json.loads(hp.read_text(encoding="utf-8")))
            score_match.update_history(hp, r2)
            self.assertEqual(r2["grace_recommendation"]["suggested_tier"], 3)

            # Add Round 3, then re-run Round 2 -> Round 3 invalidated cleanly!
            e3 = json.loads(json.dumps(ev))
            e3["round"] = 3
            r3 = score_match.evaluate_round(rubric, e3, candidate_text=cand, history=json.loads(hp.read_text(encoding="utf-8")))
            score_match.update_history(hp, r3)

            r2_rerun = score_match.evaluate_round(rubric, e2, candidate_text=cand, history=json.loads(hp.read_text(encoding="utf-8")))
            self.assertEqual(r2_rerun["invalidated_subsequent_rounds"], [3])
            hist_after = score_match.update_history(hp, r2_rerun)
            self.assertEqual([r["round"] for r in hist_after["rounds"]], [1, 2])

    def test_v12_negated_transferable_no_leak_bigram_quote_and_hash_norm(self) -> None:
        # 1. Decimal normalization hash stability: 80.0 == 80 == "80.00"
        r_a = _make_minimal_rubric(pass_threshold=80.0)
        r_b = _make_minimal_rubric(pass_threshold=80)
        r_b["ats_lexical_share"] = "0.50"
        self.assertEqual(score_match.compute_rubric_hash(r_a), score_match.compute_rubric_hash(r_b))

        # 2. Scattered bag-of-words quote bypass MUST be rejected by bigram check!
        cand = "BigQuery SQL로 데이터 마트 12개를 구축 했습니다. Git PR 운영 및 배포 완료."
        self.assertTrue(score_match.verify_quote_grounding("BigQuery SQL로 데이터 마트 12개를 구축", cand))
        self.assertFalse(score_match.verify_quote_grounding("Spark로 데이터 구축 마트 배포 운영", cand))

        # 3. Negated transferable_gap linked keyword MUST NOT leak into projected_expression_only_score
        rubric = _make_minimal_rubric()
        rubric["keywords"] = [
            {"term": "Go", "aliases": [], "tier": "must"},
            {"term": "Spark", "aliases": [], "tier": "must", "linked_item_id": "MH-2"},
        ]
        rubric["rubric_hash"] = score_match.compute_rubric_hash(rubric)
        cand2 = "Go로 Built X 완료. Summary 작성. Spark는 아직 미경험입니다."
        ev = {
            "round": 1,
            "items": [
                {"id": "MH-1", "grade": "FULL", "evidence_quote": "Go로 Built X 완료"},
                {"id": "MH-2", "grade": "PARTIAL", "evidence_quote": "Go로 Built X 완료", "gap_type": "transferable_gap"},
                {"id": "PI-1", "grade": "FULL", "evidence_quote": "Go로 Built X 완료"},
                {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap"},
                {"id": "AF-1", "grade": "FULL", "evidence_quote": "Summary 작성"},
            ],
        }
        res = score_match.evaluate_round(rubric, ev, candidate_text=cand2, strict_quotes=True)
        # Zero expression_gap items + negated Spark -> projected_expression_only == total_score (zero leak!)
        self.assertEqual(res["projected_expression_only_score"], res["total_score"])
        self.assertLess(res["projected_with_transferable_cap"], 80.0)
        md = score_match.render_markdown_report(res)
        self.assertIn("단독 도달 어려움", md)
        self.assertIn("유사경험 현실 상한", md)


class TestComplexDocumentExtractorsV11(unittest.TestCase):
    def test_hwpx_nested_table_zero_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            hwpx_file = Path(tmp) / "table_resume.hwpx"
            with zipfile.ZipFile(hwpx_file, "w") as zf:
                zf.writestr(
                    "Contents/section0.xml",
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" '
                    'xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">'
                    "<hp:p><hp:run><hp:t>한지민 이력서</hp:t></hp:run>"
                    "<hp:run><hp:tbl>"
                    "<hp:tr>"
                    "<hp:tc><hp:subList><hp:p><hp:run><hp:t>회사명</hp:t></hp:run></hp:p></hp:subList></hp:tc>"
                    "<hp:tc><hp:subList><hp:p><hp:run><hp:t>담당업무</hp:t></hp:run></hp:p></hp:subList></hp:tc>"
                    "</hp:tr>"
                    "<hp:tr>"
                    "<hp:tc><hp:subList><hp:p><hp:run><hp:t>여기어때</hp:t></hp:run></hp:p></hp:subList></hp:tc>"
                    "<hp:tc><hp:subList><hp:p><hp:run><hp:t>급여 정산</hp:t></hp:run></hp:p></hp:subList></hp:tc>"
                    "</hp:tr>"
                    "</hp:tbl></hp:run></hp:p>"
                    "</hs:sec>",
                )
            extracted = extract_doc.extract_hwpx(hwpx_file)
            self.assertIn("한지민 이력서", extracted)
            self.assertIn("회사명 | 담당업무", extracted)
            self.assertIn("여기어때 | 급여 정산", extracted)
            # Zero duplication check!
            self.assertEqual(extracted.count("급여 정산"), 1)
            self.assertEqual(extracted.count("회사명"), 1)

    def test_docx_textbox_skips_mc_fallback_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx_file = Path(tmp) / "textbox.docx"
            with zipfile.ZipFile(docx_file, "w") as zf:
                zf.writestr(
                    "word/document.xml",
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
                    "<w:body><w:p><w:r><w:t>본문 요약</w:t></w:r>"
                    "<mc:AlternateContent>"
                    "<mc:Choice><w:txbxContent><w:p><w:r><w:t>텍스트박스 성과 42%</w:t></w:r></w:p></w:txbxContent></mc:Choice>"
                    "<mc:Fallback><w:txbxContent><w:p><w:r><w:t>텍스트박스 성과 42%</w:t></w:r></w:p></w:txbxContent></mc:Fallback>"
                    "</mc:AlternateContent></w:p></w:body></w:document>",
                )
            extracted = extract_doc.extract_docx(docx_file)
            self.assertIn("본문 요약", extracted)
            self.assertEqual(extracted.count("텍스트박스 성과 42%"), 1)

    def test_pptx_presentation_xml_visual_slide_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pptx_file = Path(tmp) / "reordered.pptx"
            with zipfile.ZipFile(pptx_file, "w") as zf:
                # Visually slide2 comes BEFORE slide1 in presentation.xml!
                zf.writestr(
                    "ppt/presentation.xml",
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                    '<p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId1"/></p:sldIdLst>'
                    "</p:presentation>",
                )
                zf.writestr(
                    "ppt/_rels/presentation.xml.rels",
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>'
                    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>'
                    "</Relationships>",
                )
                for num, txt in [(1, "두번째 시각 슬라이드"), (2, "첫번째 시각 표지")]:
                    zf.writestr(
                        f"ppt/slides/slide{num}.xml",
                        '<?xml version="1.0" encoding="UTF-8"?>'
                        '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                        f"<p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>{txt}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>",
                    )
            extracted = extract_doc.extract_pptx(pptx_file)
            self.assertLess(extracted.index("첫번째 시각 표지"), extracted.index("두번째 시각 슬라이드"))

    def test_legacy_hwp_rejected_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            hwp_file = Path(tmp) / "legacy.hwp"
            hwp_file.write_bytes(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00binary hwp")
            with self.assertRaisesRegex(extract_doc.UnsupportedBinaryFormatError, "UNSUPPORTED_BINARY_FORMAT"):
                extract_doc.extract_file(hwp_file)

    def test_real_multipage_pdf_graceful_handling(self) -> None:
        # Minimal valid 2-page PDF 1.4 binary
        pdf_bytes = (
            b"%PDF-1.4\n"
            b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
            b"2 0 obj << /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >> endobj\n"
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 7 0 R >> >> >> endobj\n"
            b"4 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> >> endobj\n"
            b"5 0 obj << /Length 50 >> stream\nBT /F1 12 Tf 72 720 Td (Page 1 Python FastAPI) Tj ET\nendstream endobj\n"
            b"6 0 obj << /Length 50 >> stream\nBT /F1 12 Tf 72 720 Td (Page 2 Portfolio Impact) Tj ET\nendstream endobj\n"
            b"7 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
            b"xref\n0 8\n0000000000 65535 f \n"
            b"trailer << /Size 8 /Root 1 0 R >>\nstartxref\n0\n%%EOF\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            pdf_file = Path(tmp) / "portfolio.pdf"
            pdf_file.write_bytes(pdf_bytes)
            txt, warn = extract_doc.extract_file(pdf_file)
            # Either extracted cleanly via pypdf/fitz OR emitted clear PDF_NATIVE_READ_REQUIRED warning
            if warn:
                self.assertIn("PDF_NATIVE_READ_REQUIRED", warn)
            else:
                self.assertIn("Python FastAPI", txt)


class TestSampleCLISmoke(unittest.TestCase):
    def test_sample_examples_cli_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            rubric_copy = tmp_dir / "rubric.json"
            shutil.copy2(SKILL_DIR / "examples" / "sample_rubric.json", rubric_copy)
            cand_txt = tmp_dir / "candidate.txt"
            cand_txt.write_text(
                "사용자 중심의 서비스를 만드는 기획자입니다.\n"
                "2022.03~현재 A사 B2C 커머스 앱 프로덕트 매니저(3년 6개월), 신규 온보딩 및 장바구니 개편 E2E 출시 주도.\n"
                "보유 역량: SQL, Amplitude, Figma. 개발자 4명, 디자이너 2명과 2주 스프린트 협업.\n"
                "온보딩 화면을 여러 시안으로 테스트함. 신규 온보딩 개편 화면 스크린샷 및 기능 목록.\n"
                "개편 이후 사용자 반응이 긍정적으로 향상됨. 팀 프로젝트로 결제 UX 개선 수행. 단건 결제 UX 개선 수행.\n"
                "경력 역순 정리 및 프로젝트별 구분 명확.",
                encoding="utf-8",
            )
            hist_path = tmp_dir / "history.json"
            report_path = tmp_dir / "round_01_report.md"

            p1 = subprocess.run(
                [sys.executable, "-B", str(SCRIPT_DIR / "score_match.py"), "--init-rubric", str(rubric_copy)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            init_out = json.loads(p1.stdout)
            self.assertEqual(init_out["status"], "RUBRIC_LOCKED")

            p2 = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT_DIR / "score_match.py"),
                    "--rubric",
                    str(rubric_copy),
                    "--eval",
                    str(SKILL_DIR / "examples" / "sample_eval_r1.json"),
                    "--candidate-text",
                    str(cand_txt),
                    "--history",
                    str(hist_path),
                    "--report-out",
                    str(report_path),
                    "--strict-quotes",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            score_out = json.loads(p2.stdout)
            self.assertEqual(score_out["pass_status"], "REVISE")
            self.assertEqual(score_out["unverified_quotes"], [])
            report_text = report_path.read_text(encoding="utf-8")
            self.assertIn("이번 라운드 핵심 미션", report_text)

    def test_english_two_round_cli_zero_korean_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            rubric_path = tmp_dir / "rubric_en.json"
            rubric = {
                "company": "Acme FinTech",
                "role_title": "Operations Analyst",
                "language": "en",
                "domain_mode": "resume_only",
                "pass_threshold": 80.0,
                "ats_lexical_share": 0.5,
                "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
                "categories": {
                    "must_have": [
                        {"id": "MH-1", "title": "SQL reporting & reconciliation", "weight": 3, "is_knockout": True},
                        {"id": "MH-2", "title": "Cross-functional stakeholder operations", "weight": 2, "is_knockout": False},
                    ],
                    "portfolio_impact": [
                        {"id": "PI-1", "title": "Quantified operational efficiency gains", "weight": 2, "is_knockout": False},
                    ],
                    "preferred": [
                        {"id": "PR-1", "title": "Python workflow automation", "weight": 2, "is_knockout": False},
                    ],
                    "ats_framing": [
                        {"id": "AF-1", "title": "Clear role positioning headline", "weight": 2, "is_knockout": False},
                    ],
                },
                "keywords": [
                    {"term": "SQL", "aliases": ["PostgreSQL"], "tier": "must"},
                    {"term": "Reconciliation", "aliases": [], "tier": "must"},
                    {"term": "Python", "aliases": [], "tier": "preferred"},
                ],
            }
            rubric_path.write_text(json.dumps(rubric, indent=2), encoding="utf-8")
            subprocess.run(
                [sys.executable, "-B", str(SCRIPT_DIR / "score_match.py"), "--init-rubric", str(rubric_path)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )

            c1 = tmp_dir / "r1.txt"
            c1.write_text("Alex Kim - General Analyst. Used SQL for weekly reports with Finance team.", encoding="utf-8")
            e1 = tmp_dir / "e1.json"
            e1.write_text(
                json.dumps(
                    {
                        "round": 1,
                        "items": [
                            {"id": "MH-1", "grade": "PARTIAL", "evidence_quote": "Used SQL for weekly reports", "gap_type": "expression_gap", "action_hint": "Add reconciliation process details."},
                            {"id": "MH-2", "grade": "PARTIAL", "evidence_quote": "with Finance team", "gap_type": "expression_gap", "action_hint": "Detail stakeholder cadence."},
                            {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "expression_gap", "action_hint": "Add quantified metrics."},
                            {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap", "action_hint": "Do not fabricate Python."},
                            {"id": "AF-1", "grade": "PARTIAL", "evidence_quote": "Alex Kim - General Analyst", "gap_type": "expression_gap", "action_hint": "Target Operations Analyst explicitly."},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            hist = tmp_dir / "history.json"
            rep1 = tmp_dir / "r1_report.md"
            subprocess.run(
                [
                    sys.executable, "-B", str(SCRIPT_DIR / "score_match.py"),
                    "--rubric", str(rubric_path), "--eval", str(e1),
                    "--candidate-text", str(c1), "--history", str(hist),
                    "--report-out", str(rep1), "--strict-quotes",
                ],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            r1_md = rep1.read_text(encoding="utf-8")
            self.assertIn("Next Round Fastest Path Mission", r1_md)
            self.assertIn("Work Proof & Measurable Impact", r1_md)
            # Zero Hangul leakage check in English mode!
            self.assertIsNone(score_match.HANGUL_OR_CJK_RE.search(r1_md))

            # Round 2 -> PASS
            c2 = tmp_dir / "r2.txt"
            c2.write_text(
                "Alex Kim - Operations Analyst. Built PostgreSQL SQL payment reconciliation pipeline across 40k daily payouts with Finance and Risk teams, cutting close time by 52% and errors to 0.01%.",
                encoding="utf-8",
            )
            e2 = tmp_dir / "e2.json"
            e2.write_text(
                json.dumps(
                    {
                        "round": 2,
                        "items": [
                            {"id": "MH-1", "grade": "FULL", "evidence_quote": "Built PostgreSQL SQL payment reconciliation pipeline across 40k daily payouts"},
                            {"id": "MH-2", "grade": "FULL", "evidence_quote": "with Finance and Risk teams"},
                            {"id": "PI-1", "grade": "FULL", "evidence_quote": "cutting close time by 52% and errors to 0.01%"},
                            {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "gap_type": "true_gap", "action_hint": "Unheld bonus skill."},
                            {"id": "AF-1", "grade": "FULL", "evidence_quote": "Alex Kim - Operations Analyst"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            rep2 = tmp_dir / "r2_report.md"
            p2 = subprocess.run(
                [
                    sys.executable, "-B", str(SCRIPT_DIR / "score_match.py"),
                    "--rubric", str(rubric_path), "--eval", str(e2),
                    "--candidate-text", str(c2), "--history", str(hist),
                    "--report-out", str(rep2), "--strict-quotes",
                ],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
            out2 = json.loads(p2.stdout)
            self.assertEqual(out2["pass_status"], "PASS")
            r2_md = rep2.read_text(encoding="utf-8")
            self.assertIsNone(score_match.HANGUL_OR_CJK_RE.search(r2_md))


if __name__ == "__main__":
    unittest.main(verbosity=2)
