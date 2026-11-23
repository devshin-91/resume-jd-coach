# `resume-jd-coach` (v2.2 · Multilingual `ko` / `en` / `zh` / `ja` · Suggestion-Only)

> [!CAUTION]
> **Strictly for Reference Only · Human Ultimate Accountability (순전히 참고용 · 최고책임자인 인간의 직접 결정 원칙)**
>
> - **Reference Only (AI Can Be Wrong):** Every match score, gap diagnosis, and suggestion produced by `resume-jd-coach` is **strictly for reference only**. Because it is based on AI judgment, it **can be inaccurate or wrong**—true job fit must always be judged by the human applicant.
> - **Human as Sole Accountable Owner (Suggestion-Only):** This skill **only offers suggestions** and unconditionally refuses requests to directly edit or rewrite your documents. Ultimately, every expression and sentence that goes into a resume or portfolio **must be decided directly by the human applicant, who holds sole ultimate responsibility**.
>
> - **순전히 참고용 (AI 판단은 틀릴 수 있음):** 본 도구가 제시하는 모든 공고 일치율·진단·제안은 **순전히 참고용**입니다. AI의 판단에 기반하므로 **틀릴 수 있으며**, 실제 공고 적합도는 반드시 사람(지원자)이 직접 판단해야 합니다.
> - **최고책임자인 사람의 직접 결정 (제안 전용 · 직접 수정 거절):** 본 스킬은 **무조건 제안만 제공**하며, 직접 수정·대필 요청(`"됐고 수정해줘"` 등)은 모두 거절합니다. 이력서와 포트폴리오에 최종적으로 들어가는 표현과 문장은 결국 **최고책임자인 사람(지원자 본인)이 직접 결정하고 책임져야 합니다.**

**Coach-First, Suggestion-Only Multilingual Resume & Portfolio ↔ Job Description Match Evaluator (`80%` Pass Gate) with Deterministic Python Scoring, Locked Rubrics, Experience-Gate & Equivalent-Skill Judgment, Multi-Round Δ Tracking, 3-Tier Grace Escalation, and Mandatory AI-Judgment Disclaimers.**

An Antigravity Agent Skill (`SKILL.md`) validated across **4 languages & representative hiring markets** (**Korea `ko` · United States `en` · China `zh` · Japan `ja`**), **18 live real-world job postings (44 evaluation rounds)**, **39/39 automated unit & policy regression tests**, **5 Cold-Start Live LLM E2E Red-Team runs** (including `v2.2` adversarial direct-rewrite refusal), **Independent RLAIF (AI-Feedback Constitutional Audit) cycles** (`v1: 67 → 89/100 PASS`, `v2 multilingual: 74.5 → 91.5/100 PASS`), and **v2.2 Human-in-the-Loop Policy Calibration**.

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
   - **Negation- & Contradiction-Aware ATS Scanner (`v2.2` Human `>= 80%` Partial Rule):** Excludes terms appearing only in unexperienced/negated phrasing across all 4 languages (including Japanese Keigo `ございません`/`いただいた`, Chinese `暂未接触`/`不具备`, English `don't have`/`no production experience`, Korean `미경험`), and awards **`0.0` ATS credit** to self-contradictory keyword mentions (`contradictory_mentions`) even when the linked item is `PARTIAL`. Credit is granted ONLY after asking the human applicant and receiving explicit confirmation that their verified partial experience covers **`>= 80%`** of the JD requirement (`contradiction_human_confirmations`).
   - **Hardened `--strict-quotes`:** Enforces verbatim / contiguous n-gram grounding (including CJK character trigrams) **plus 100% numeric + magnitude-unit lock** (blocking `5千 → 5万`, `5K → 5M`, `2 → 50` fabrication), while capping bare skills-list keyword stuffing at **`WEAK (0.25)`**.
   - **Multilingual Document Extractor (`extract_doc.py`):** Zero-dependency parsing for `.md`, `.txt` (UTF-8/UTF-16 + zero-mojibake auto-detection for `gb18030`, `cp932`, `cp949`/`iso2022_kr`, `cp1252`), `.docx` (nested table/textbox & `mc:Fallback`-safe), `.xlsx` (multi-sheet Japanese `履歴書`/`職務経歴書`, skipping `<rPh>` furigana & hidden tabs), `.pptx` (visual slide order + `mc:Fallback`-safe), `.hwpx` (nested table-safe), `.html`, plus PDF hooks and loud legacy `.hwp`/`.doc`/`.xls` rejection.
4. **Honest Unreachable Verdict (`< 80%`) & Experience-Year Gate vs Equivalent-Skill (`v2.2`):**
   - When `80.0%` is unreachable (`UNREACHABLE` / `UNREACHABLE_HARD_EXPERIENCE_GATE`), states clearly that `80%` is **unreachable**, suppresses Grace for chasing an impossible `80%`, and outputs a structured **3-pillar growth roadmap (Experience · Projects · Attitude & Positioning)**.
   - **Mandatory Experience-Year Gate (`experience_gate`):** If a JD requires `X years of experience` without an equivalent-skill clause (`allows_equivalent_skill: false`) and the candidate lacks those years → strictly judged **`UNREACHABLE_HARD_EXPERIENCE_GATE`**.
   - **Equivalent-Skill Exception (`경력에 준하는 실력`):** If the JD accepts equivalent practical skill (`allows_equivalent_skill: true`) and verified artifacts meet the target bar (`meets_bar: true`) → judged **`CONDITIONAL_EQUIVALENT_SKILL`**, explains the concrete reason why limited possibility remains, and activates **suggestion-only Grace**.
5. **Strictly Suggestion-Only Coaching, Direct-Rewrite Refusal & Mandatory AI Disclaimer (`v2.2`):**
   - **Direct-Rewrite Refusal (`"됐고 수정해줘"`):** Even if the user explicitly demands direct editing or final copy rewriting (`ko`/`en`/`zh`/`ja`), the coach **ALWAYS refuses** and preserves original files untouched—emphasizing that **every final sentence and expression in a resume/portfolio must be decided and owned solely by the human applicant**.
   - **3-Tier Suggestion-Only Grace Mode:** Offers Tier 1 (Socratic questions + skeleton), Tier 2 (fact-grounded options A·B with metric placeholders), or Tier 3 (targeted section structural blueprint + mandatory Fact-Check & Human Authorship Checklist)—never ghostwriting or fabricating unheld facts.
   - **Mandatory AI-Judgment Fallibility Disclaimer:** Every rendered Markdown report (`ko`/`en`/`zh`/`ja`) and user response explicitly states that the match percentage is an AI estimate that can be wrong, and true role fit must be judged by the human applicant.

---

## Repository Structure

```text
resume-jd-coach/
├── README.md
├── CONTRIBUTORS.md                                # Role attribution (@devshin-91 & @antigravity-bot)
├── LICENSE                                        # Non-Commercial Source-Available License
├── THIRD_PARTY_NOTICES.md                         # Python stdlib, optional PDF libs, skill spec, 18 benchmark JD attributions
├── skill/
│   └── resume-jd-coach/                           # Ready-to-install Antigravity Skill (v2.2 · ko/en/zh/ja · Suggestion-Only)
│       ├── SKILL.md
│       ├── references/
│       │   ├── scoring-rubric.md
│       │   ├── grace-coaching-playbook.md         # Suggestion-only 3-tier Grace + 4-lang direct-rewrite refusal scripts
│       │   └── report-template.md
│       ├── scripts/
│       │   ├── extract_doc.py                     # .md/.txt/.docx/.xlsx/.pptx/.hwpx/.html + CJK/cp1252 auto-decode + PDF hook
│       │   ├── score_match.py                     # 4-lang deterministic scoring, experience_gate, >=80% partial, AI disclaimer
│       │   └── test_resume_jd_coach.py            # 39 unit, RLAIF & v2.2 Human-Calibration policy tests
│       └── examples/
│           ├── sample_rubric.json
│           └── sample_eval_r1.json
├── benchmark/
│   ├── run_benchmark.py                           # Korean 6-job-family 15-round benchmark runner
│   ├── benchmark_summary.json
│   ├── tracks/                                    # 6 Korean Wanted real-JD tracks
│   ├── live_e2e_redteam/                          # Korean Cold Live LLM E2E Red-Team run (v1.x)
│   ├── live_e2e_redteam_v22_ko/                   # Korean v2.2 Cold Live E2E Policy Check (rewrite refusal + equiv-skill + Redis 80%)
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
# 1. Run all 39 unit, RLAIF & v2.2 policy tests (zero external dependencies)
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
| Automated Unit & Policy Regression Suite (`test_resume_jd_coach.py`) | **39 / 39 OK** (4-lang ATS negation/contradiction/NFKC, `>= 80%` human-confirmed partial scope, hard `experience_gate` vs `CONDITIONAL_EQUIVALENT_SKILL`, 3-pillar unreachable roadmap, mode-aware 4-lang AI disclaimer, CJK trigrams + numeric-unit quote lock, `.xlsx`/`.hwpx`/`.docx`/`.pptx`/`.pdf`, 2-round `en`/`zh`/`ja` zero-leakage CLI E2E) |
| Korean 6-Job-Family Real-JD Benchmark (`benchmark/run_benchmark.py`) | **6 / 6 Tracks · 15 / 15 Rounds** passed `--strict-quotes` (Wanted live JDs: Dev, PM, Design, Marketing, Data, Non-IT HR) |
| 3-Country Multilingual Real-JD Benchmark (`benchmark/multilingual/`) | **12 / 12 Tracks · 29 / 29 Rounds** passed `--strict-quotes` with **0 cross-language / `%p` leaks** (US `en` × 4 · China `zh` × 4 · Japan `ja` × 4, failing native resumes across `.docx`/`.pptx`/`.xlsx`/`gb18030`/`cp932`/`.md`) |
| 5 Cold-Start Live LLM E2E Red-Teams (`ko` · `en` · `zh` · `ja` + `v2.2 ko`) | Contradictory keyword stuffing earned **`0.0` ATS credit**, `honest_fit_advisory` triggered, all 4 languages cleanly refused fabrication, and **`v2.2` Cold Live E2E cleanly refused `"됐고 직접 수정해줘"` (SHA-256 unchanged), asked for `>= 80%` Redis scope confirmation, explained `CONDITIONAL_EQUIVALENT_SKILL` + Grace, and included the AI disclaimer** |
| Independent RLAIF Constitutional Judge Audits | **v1 (`ko`):** `67 → 89 / 100` (**✅ PASS**, `+22 pts` + Human-in-the-Loop Calibration) · **v2 (`ko`/`en`/`zh`/`ja`):** `74.5 → 91.5 / 100` (**✅ PASS**, `+17.0 pts`) · **v2.2:** Human-in-the-Loop Policy Calibration (`39/39 OK`) |

---

## Contributors

This project is co-authored by a human product architect and **Google Antigravity** AI agents. See full bilingual role breakdown in [CONTRIBUTORS.md](./CONTRIBUTORS.md).

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Architect & Human-in-the-Loop Calibrator** | `80%` pass gate & suggestion-only coaching philosophy, 3-tier Grace design, 4-language validation direction, **v1.1 & v2.2 Human-in-the-Loop Calibration** (contradiction 0 credit / `>= 80%` human partial rule, hard experience gate vs equivalent-skill Grace, unconditional direct-rewrite refusal & human authorship responsibility, mandatory AI-judgment disclaimer), `RLAIF` terminology rigor, Zero-PII & non-commercial licensing governance |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Benchmark Runner & Independent RLAIF Auditor** | `SKILL.md` & stdlib Python engine (`Gemini 4 Neon (XHigh)`), 4-country live JD collection (`Gemini 3.8 Flash` browser subagents), 18-track 44-round benchmarks, 5 cold-start live LLM E2E red-teams, independent RLAIF audits (`v1: 89/100`, `v2: 91.5/100 PASS`), v1.1–v2.2 hardening & 39-test verification |

---

## License

Licensed for **Non-Commercial Use Only**. See [LICENSE](./LICENSE) and [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).  
Copyright (c) 2026 [`devshin-91`](https://github.com/devshin-91) (Co-authored with Google Antigravity [`@antigravity-bot`](https://github.com/antigravity-bot)).
