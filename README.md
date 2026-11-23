# `resume-jd-coach` (v2.1 · Multilingual `ko` / `en` / `zh` / `ja`)

> **Coach-First Multilingual Resume & Portfolio ↔ Job Description Match Evaluator (`80%` Pass Gate) with Deterministic Python Scoring, Locked Rubrics, Multi-Round Δ Tracking, and 3-Tier Grace Escalation.**

An Antigravity Agent Skill (`SKILL.md`) validated across **4 languages & representative hiring markets** (**Korea `ko` · United States `en` · China `zh` · Japan `ja`**), **18 live real-world job postings (44 evaluation rounds)**, **33/33 automated unit & regression tests**, **4-language Cold Live LLM E2E Red-Team runs**, and **Independent RLAIF (AI-Feedback Constitutional Audit) cycles** (`v1: 67 → 89/100 PASS`, `v2 multilingual: 74.5 → 91.5/100 PASS`).

---

## Core Design Philosophy

1. **`80.0%` Pass Gate (`REVISE` / `PASS_WITH_RISK` / `PASS`):**
   - `< 80.0%` → **`REVISE`**: Diagnoses exact gaps, explains *why* the JD cares, ranks fixes by exact uplift potential (`%p` / `pp` / `pt`), and invites **self-revision** rather than silently ghostwriting.
   - `>= 80.0%` with Knockout risk (`is_knockout: true` graded `MISSING` or `WEAK`) → **`PASS_WITH_RISK`**: Never hides screening blockers behind a high aggregate score.
   - `>= 80.0%` with zero Knockout risks → **`PASS`** (with automatic caveat if any item regressed during revision).
2. **Locked Rubric ("No Moving the Goalposts"):**
   - Round 1 decomposes the target JD into 4 weighted dimensions (`must_have`, `portfolio_impact`, `preferred`, `ats_framing`) and locks a canonical SHA-256 `rubric_hash` (`score_match.py --init-rubric`).
   - Every revision round (`Round 2`, `Round 3`, …) is verified against the exact same hash so round-over-round deltas (`Δ`) are strictly apples-to-apples.
3. **Deterministic 4-Language Math + Negation/Contradiction ATS + Strict Quote Grounding:**
   - Zero external pip dependencies (Python 3 Standard Library only).
   - `Decimal` `ROUND_HALF_UP` exact conservation (`score + sum(uplifts) == 100.0%`) and display-consistent scoreboard sums (`score + gap == threshold`).
   - **Native `ko` / `en` / `zh` / `ja` support:** NFKC full-width normalization (`ＡＷＳ`→`AWS`, `ＳＱＬ`→`SQL`), locale-native units (`%p` / `pp` / `pt`), mode-aware labels (`portfolio` vs `resume_only`), and zero cross-language leakage.
   - **Negation- & Contradiction-Aware ATS Scanner:** Excludes terms appearing only in unexperienced/negated phrasing across all 4 languages (including Japanese Keigo `ございません`/`いただいた`, Chinese `暂未接触`/`不具备`, English `don't have`/`no production experience`, Korean `미경험`), and awards **`0.0` ATS credit** to self-contradictory keyword stuffing (`contradictory_mentions`).
   - **Hardened `--strict-quotes`:** Enforces verbatim / contiguous n-gram grounding (including CJK character trigrams) **plus 100% numeric + magnitude-unit lock** (blocking `5千 → 5万`, `5K → 5M`, `2 → 50` fabrication), while capping bare skills-list keyword stuffing at **`WEAK (0.25)`**.
   - **Multilingual Document Extractor (`extract_doc.py`):** Zero-dependency parsing for `.md`, `.txt` (UTF-8/UTF-16 + zero-mojibake auto-detection for `gb18030`, `cp932`, `cp949`/`iso2022_kr`, `cp1252`), `.docx` (nested table/textbox & `mc:Fallback`-safe), `.xlsx` (multi-sheet Japanese `履歴書`/`職務経歴書`, skipping `<rPh>` furigana & hidden tabs), `.pptx` (visual slide order + `mc:Fallback`-safe), `.hwpx` (nested table-safe), `.html`, plus PDF hooks and loud legacy `.hwp`/`.doc`/`.xls` rejection.
4. **3-Tier Graduated Grace Mode (벽을 느낄 때 보조 모드):**
   - Triggers on explicit user request (`ko`/`en`/`zh`/`ja`) or automatic stall detection (`2R+` consecutive stall on actionable items or `< +3.0` gain while `< 80%`), alongside independent `honest_fit_advisory` / `honest_fit_knockout` warnings whenever `true_gap`s block honest `80%` reachability.
   - **Tier 1:** Socratic interview questions + localized XYZ/STAR/Case-Study skeleton.
   - **Tier 2:** 2–3 fact-grounded phrasing options with explicit localized metric placeholders.
   - **Tier 3:** Targeted section pair-draft + mandatory localized Fact-Check Checklist.
   - **Zero Fabrication Across All Tiers:** Strictly refuses inventing unheld skills, tools, employers, or metrics.

---

## Repository Structure

```text
resume-jd-coach/
├── README.md
├── CONTRIBUTORS.md                                # Role attribution (@devshin-91 & @antigravity-bot)
├── LICENSE                                        # Non-Commercial Source-Available License
├── THIRD_PARTY_NOTICES.md                         # Python stdlib, optional PDF libs, skill spec, 18 benchmark JD attributions
├── skill/
│   └── resume-jd-coach/                           # Ready-to-install Antigravity Skill (v2.1 · ko/en/zh/ja)
│       ├── SKILL.md
│       ├── references/
│       │   ├── scoring-rubric.md
│       │   ├── grace-coaching-playbook.md         # 3-tier Grace protocol + en/zh/ja micro-templates
│       │   └── report-template.md
│       ├── scripts/
│       │   ├── extract_doc.py                     # .md/.txt/.docx/.xlsx/.pptx/.hwpx/.html + CJK/cp1252 auto-decode + PDF hook
│       │   ├── score_match.py                     # 4-lang deterministic rubric lock, scoring, ATS, round diff & native reports
│       │   └── test_resume_jd_coach.py            # 33 unit & RLAIF regression tests
│       └── examples/
│           ├── sample_rubric.json
│           └── sample_eval_r1.json
├── benchmark/
│   ├── run_benchmark.py                           # Korean 6-job-family 15-round benchmark runner
│   ├── benchmark_summary.json
│   ├── tracks/                                    # 6 Korean Wanted real-JD tracks
│   ├── live_e2e_redteam/                          # Korean Cold Live LLM E2E Red-Team run
│   └── multilingual/                              # 3-country (US en, China zh, Japan ja) 12-track 29-round benchmark
│       ├── run_multilingual_benchmark.py          # Reproducible 12-track multilingual runner (.docx/.pptx/.xlsx/gb18030/cp932)
│       ├── tracks_en.py / tracks_zh.py / tracks_ja.py
│       ├── multilingual_benchmark_summary.json
│       ├── tracks/                                # 12 US/China/Japan failing-resume & revision tracks
│       └── live_e2e_redteam/                      # en / zh / ja Cold Live LLM E2E Red-Team runs
└── docs/
    ├── RLAIF_AUDIT_REPORT_V1.md                   # v1.0 (67/100) -> v1.1 (89/100 PASS + Human Calibration) -> v1.2 report
    └── RLAIF_MULTILINGUAL_AUDIT_REPORT_V2.md      # v2.0 (74.5/100) -> v2.1 (91.5/100 PASS) multilingual RLAIF report
```

---

## Installation (Antigravity Skill)

Copy `skill/resume-jd-coach/` into your Antigravity skills discovery directory:

- **Global (all workspaces):** `~/.gemini/config/skills/resume-jd-coach/`
- **Project-local:** `<workspace>/.agents/skills/resume-jd-coach/`

Compatible with both **Software Engineering** and **Knowledge Work** layouts in Antigravity across `ko`, `en`, `zh`, and `ja`.

---

## Running Verification Tests

```bash
# 1. Run all 33 unit & RLAIF regression tests (zero external dependencies)
python -B skill/resume-jd-coach/scripts/test_resume_jd_coach.py

# 2. Re-run the Korean 6-job-family 15-round benchmark
python -B benchmark/run_benchmark.py

# 3. Re-run the US/China/Japan 12-track 29-round multilingual benchmark
python -B benchmark/multilingual/run_multilingual_benchmark.py
```

---

## Validation & Independent RLAIF Audit Highlights

See full reports in [docs/RLAIF_AUDIT_REPORT_V1.md](./docs/RLAIF_AUDIT_REPORT_V1.md) and [docs/RLAIF_MULTILINGUAL_AUDIT_REPORT_V2.md](./docs/RLAIF_MULTILINGUAL_AUDIT_REPORT_V2.md):

| Verification Milestone | Result |
| :--- | :--- |
| Automated Unit & Regression Suite (`test_resume_jd_coach.py`) | **33 / 33 OK** (4-lang ATS negation/contradiction/NFKC, CJK trigrams + numeric-unit quote lock, `.xlsx` `<rPh>` furigana & hidden sheets, `gb18030`/`cp932`/`iso2022_kr`/`cp1252`, `.hwpx`/`.docx`/`.pptx`/`.pdf`, 2-round `en`/`zh`/`ja` zero-leakage CLI E2E) |
| Korean 6-Job-Family Real-JD Benchmark (`benchmark/run_benchmark.py`) | **6 / 6 Tracks · 15 / 15 Rounds** passed `--strict-quotes` (Wanted live JDs: Dev, PM, Design, Marketing, Data, Non-IT HR) |
| 3-Country Multilingual Real-JD Benchmark (`benchmark/multilingual/`) | **12 / 12 Tracks · 29 / 29 Rounds** passed `--strict-quotes` with **0 cross-language / `%p` leaks** (US `en` × 4 · China `zh` × 4 · Japan `ja` × 4, failing native resumes across `.docx`/`.pptx`/`.xlsx`/`gb18030`/`cp932`/`.md`) |
| 4-Language Cold Live LLM E2E Red-Team (`ko` · `en` · `zh` · `ja`) | Contradictory keyword stuffing earned **`0.0` ATS credit** (`ja` red-team gain suppressed `+5.2pt → +0.4pt`), `honest_fit_advisory` triggered, and **all 4 languages cleanly refused Grace Tier 3 fabrication** |
| Independent RLAIF Constitutional Judge Audits | **v1 (`ko`):** `67 → 89 / 100` (**✅ PASS**, `+22 pts` + Human-in-the-Loop Calibration) · **v2 (`ko`/`en`/`zh`/`ja`):** `74.5 → 91.5 / 100` (**✅ PASS**, `+17.0 pts` + residual `P1-R1` closed) |

---

## Contributors

This project is co-authored by a human product architect and **Google Antigravity** AI agents. See full bilingual role breakdown in [CONTRIBUTORS.md](./CONTRIBUTORS.md).

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Architect & Human-in-the-Loop Calibrator** | `80%` pass gate & coach-first design, 3-tier Grace philosophy, Knowledge Work alignment, 4-language cross-domain validation direction, v1.1 Human-in-the-Loop Calibration decisions, `RLAIF` terminology rigor, Zero-PII & non-commercial licensing governance |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Benchmark Runner & Independent RLAIF Auditor** | `SKILL.md` & stdlib Python engine (`Gemini 4 Neon (XHigh)`), 4-country live JD collection (`Gemini 3.8 Flash` browser subagents), 18-track 44-round benchmarks, 4-language cold live LLM E2E red-teams, independent RLAIF audits (`v1: 89/100`, `v2: 91.5/100 PASS`), v1.1–v2.1 hardening & 33-test verification |

---

## License

Licensed for **Non-Commercial Use Only**. See [LICENSE](./LICENSE) and [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).  
Copyright (c) 2026 [`devshin-91`](https://github.com/devshin-91) (Co-authored with Google Antigravity [`@antigravity-bot`](https://github.com/antigravity-bot)).
