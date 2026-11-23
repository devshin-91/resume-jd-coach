# `resume-jd-coach` (v1.2)

> **Coach-First Resume & Portfolio ↔ Job Description Match Evaluator (`80%` Pass Gate) with Deterministic Python Scoring, Locked Rubrics, Multi-Round Δ Tracking, and 3-Tier Grace Escalation.**

An Antigravity Agent Skill (`SKILL.md`) validated across **6 real Korean job families** (Backend Engineering, Junior PM, Product Design, Brand Marketing, Senior Data Analytics, Entry-Level Non-IT HR), **17/17 automated unit & regression tests**, a **Cold Live LLM E2E Red-Team run**, and an **Independent RHAIF (Human+AI Feedback) Constitutional Audit (`67/100 → 89/100 PASS` + v1.2 hardening)**.

---

## Core Design Philosophy

1. **`80.0%` Pass Gate (`REVISE` / `PASS_WITH_RISK` / `PASS`):**
   - `< 80.0%` → **`REVISE`**: Diagnoses exact gaps, explains *why* the JD cares, ranks fixes by exact `+X.X%p` uplift potential, and invites **self-revision** rather than silently ghostwriting.
   - `>= 80.0%` with Knockout risk (`is_knockout: true` graded `MISSING` or `WEAK`) → **`PASS_WITH_RISK`**: Never hides screening blockers behind a high aggregate score.
   - `>= 80.0%` with zero Knockout risks → **`PASS`**.
2. **Locked Rubric ("No Moving the Goalposts"):**
   - Round 1 decomposes the target JD into 4 weighted dimensions (`must_have`, `portfolio_impact`, `preferred`, `ats_framing`) and locks a canonical SHA-256 `rubric_hash` (`score_match.py --init-rubric`).
   - Every revision round (`Round 2`, `Round 3`, …) is verified against the exact same hash so round-over-round deltas (`Δ`) are strictly apples-to-apples.
3. **Deterministic Math + Negation-Aware ATS + Strict Quote Grounding:**
   - Zero external pip dependencies (Python 3 Standard Library only).
   - `Decimal` `ROUND_HALF_UP` exact conservation (`score + sum(uplifts) == 100.0%`).
   - Negation-aware Korean/English ATS lexical scanner (ignores terms appearing only in `"아직 해 보지 않은 것"`, `"미경험"`, `"no experience"` contexts, and flags `contradictory_mentions` when positive + negative mentions conflict in the same document).
   - `--strict-quotes` enforces verbatim / contiguous bigram quote grounding (`unigram >= 70%` & `bigram >= 45%`), and caps bare skills-list keyword stuffing at **`WEAK (0.25)`**.
4. **3-Tier Graduated Grace Mode (벽을 느낄 때 보조 모드):**
   - Triggers on explicit user request or automatic stall detection (`2R+` consecutive stall on actionable items or `< +3.0%p` gain while `< 80%`, never forcing rewrites and suppressed when only `true_gap`s remain).
   - **Tier 1:** Socratic interview questions + XYZ/STAR/Case-Study skeleton.
   - **Tier 2:** 2–3 fact-grounded phrasing options with explicit `[실제 수치 입력 필요]` placeholders.
   - **Tier 3:** Targeted section pair-draft + mandatory Fact-Check Checklist.
   - **Zero Fabrication Across All Tiers:** Strictly refuses inventing unheld skills, tools, employers, or metrics.

---

## Repository Structure

```text
resume-jd-coach/
├── README.md
├── CONTRIBUTORS.md                      # Role attribution between human owner (@devshin-91) and AI partner (@antigravity-bot)
├── LICENSE                              # Non-Commercial Source-Available License
├── THIRD_PARTY_NOTICES.md               # Python stdlib, optional PDF libs, skill spec, benchmark JD attributions
├── skill/
│   └── resume-jd-coach/                 # Ready-to-install Antigravity Skill (v1.2)
│       ├── SKILL.md
│       ├── references/
│       │   ├── scoring-rubric.md
│       │   ├── grace-coaching-playbook.md
│       │   └── report-template.md
│       ├── scripts/
│       │   ├── extract_doc.py           # .md/.txt/.docx/.pptx/.hwpx/.html + PDF hook + legacy .hwp guard
│       │   ├── score_match.py           # Deterministic rubric lock, scoring, ATS, round diff, ko/en reports
│       │   └── test_resume_jd_coach.py  # 17 unit & regression tests
│       └── examples/
│           ├── sample_rubric.json
│           └── sample_eval_r1.json
├── benchmark/
│   ├── run_benchmark.py                 # Reproducible 6-job-family 15-round benchmark runner
│   ├── benchmark_summary.json
│   ├── tracks/                          # 6 synthetic cross-domain tracks grounded in real Wanted JDs
│   └── live_e2e_redteam/                # Cold Live LLM E2E Red-Team run (keyword stuffing + fabrication refusal)
└── docs/
    └── RHAIF_AUDIT_REPORT.md            # Full v1.0 (67/100) -> v1.1 (89/100 PASS) -> v1.2 audit summary
```

---

## Installation (Antigravity Skill)

Copy `skill/resume-jd-coach/` into your Antigravity skills discovery directory:

- **Global (all workspaces):** `~/.gemini/config/skills/resume-jd-coach/`
- **Project-local:** `<workspace>/.agents/skills/resume-jd-coach/`

Compatible with both **Software Engineering** and **Knowledge Work** layouts in Antigravity.

---

## Running Verification Tests

```bash
# 1. Run all 17 unit & regression tests (zero external dependencies)
python -B skill/resume-jd-coach/scripts/test_resume_jd_coach.py

# 2. Re-run the full 6-job-family 15-round cross-domain benchmark
python -B benchmark/run_benchmark.py
```

---

## Validation & RHAIF Audit Highlights

See full audit details in [docs/RHAIF_AUDIT_REPORT.md](./docs/RHAIF_AUDIT_REPORT.md):

| Verification Milestone | Result |
| :--- | :--- |
| Automated Unit & Regression Suite (`test_resume_jd_coach.py`) | **17 / 17 OK** (ko/en boundaries, negation, contradiction, bigram quotes, nested HWPX/DOCX/PPTX, `.hwp` block, multipage `.pdf`, English zero-Hangul-leakage E2E) |
| 6-Job-Family Real-JD Benchmark (`benchmark/run_benchmark.py`) | **6 / 6 Tracks · 15 / 15 Rounds** passed `--strict-quotes` (`Dev`, `PM`, `Design`, `Marketing`, `Data`, `Non-IT HR`) |
| Cold Live LLM E2E Red-Team (`benchmark/live_e2e_redteam/`) | Bare keyword stuffing yielded `+0.0%p` on core categories, `-0.9%p` self-contradiction penalty, and clean refusal of Grace Tier 3 fabrication request |
| Independent RHAIF Constitutional Judge Audit | **v1.0 `67 / 100` (Conditional Pass) → v1.1 `89 / 100` (✅ PASS, `+22 pts`)** + all 5 v1.2 residual micro-defects closed |

---

## Contributors

This project is co-authored by a human product architect and **Google Antigravity** AI agents. See full bilingual role breakdown in [CONTRIBUTORS.md](./CONTRIBUTORS.md).

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Architect & RHAIF Human Calibrator** | `80%` pass gate & coach-first design, 3-tier Grace philosophy, Knowledge Work alignment, 6-job-family + RHAIF validation design, v1.1/v1.2 Human Calibration decisions, Zero-PII & non-commercial licensing governance |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Benchmark Runner & RHAIF Auditor** | `SKILL.md` & stdlib Python engine (`Gemini 4 Neon (XHigh)`), live Wanted JD collection (`Gemini 3.8 Flash` browser subagents), 6-track 15-round benchmark, cold live LLM E2E red-team, independent RHAIF audit (`67 → 89/100 PASS`), v1.1/v1.2 hardening & 17-test verification |

---

## License

Licensed for **Non-Commercial Use Only**. See [LICENSE](./LICENSE) and [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).  
Copyright (c) 2026 [`devshin-91`](https://github.com/devshin-91) (Co-authored with Google Antigravity [`@antigravity-bot`](https://github.com/antigravity-bot)).
