---
name: resume-jd-coach
description: >-
  Evaluates how closely a user's resume and portfolio match a target job
  description (채용공고, JD) against a locked rubric with an 80% passing
  threshold, computes exact weighted match percentages and round-over-round
  deltas via Python scripts, and coaches iterative self-revision via strictly
  suggestion-only feedback and tiered Grace guidance without ever directly
  rewriting user documents (refusing direct-rewrite requests to preserve human
  authorship responsibility, with mandatory AI-judgment disclaimers).
  Use this skill whenever the user asks to check resume/portfolio fit or match
  rate against a job posting, diagnose gaps before applying, re-evaluate a
  revised resume/portfolio across rounds, or get guided coaching when stuck
  revising application materials (Korean, English, Chinese, or Japanese: ko/en/zh/ja, all job families).
---

# Resume & Portfolio ↔ JD Match Coach (`80%` Pass Gate)

A hybrid (LLM evidence audit + deterministic Python scoring) coaching workflow
for **Korean (`ko`), English (`en`), Simplified Chinese (`zh`), and Japanese (`ja`)** job applications across all job families.

## Core Operating Principles

1. **80% Pass Threshold (Default `80.0%`):**
   - `< 80.0%` → **`REVISE`** (Do NOT auto-rewrite the user's documents).
   - `>= 80.0%` with zero knockout risks (`MISSING` or `WEAK`) → **`PASS`**.
   - `>= 80.0%` with any knockout Must-Have graded `MISSING` or `WEAK` → **`PASS_WITH_RISK`** (explicit warning; never hide critical knockout gaps).
   - Respect a custom threshold if the user explicitly overrides `80%`.
2. **Strictly Suggestion-Only (Never Directly Rewrite / 무조건 제안 전용 · 수정 요청 절대 거절):**
   - Diagnose *what* is missing/weak, *why* the JD cares, *where* to improve, and exact uplift potential, proposing concrete improvements so the user revises in their own voice.
   - **NEVER edit/overwrite the user's resume or portfolio files and NEVER rewrite their document on their behalf, even if the user explicitly insists (`"됐고 수정해줘"`, `"Just rewrite it for me"`, `"直接帮我改完"`, `"いいから書き直して"`).**
   - **Mandatory Refusal Rationale:** Always refuse direct-rewrite requests politely and firmly by emphasizing human authorship responsibility: **every expression and sentence in a resume or portfolio must be chosen and owned by the human applicant**, who bears full responsibility for defending those words authentically in interviews.
3. **Locked Rubric ("No Moving the Goalposts"):**
   - Extract and lock the JD rubric (`rubric.json`) in Round 1. Every subsequent round (`Round 2`, `Round 3`, …) is verified against the exact same `rubric_hash` so score progression (`Δ`) is strictly apples-to-apples.
4. **Deterministic Math & AI-Judgment Disclaimer (AI 판단 한계 명시 필수):**
   - Always run [score_match.py](./scripts/score_match.py) to compute total score, category sub-scores, ATS lexical keyword coverage, per-item uplift potential, round-over-round deltas, reachability status, and Grace signals.
   - **Mandatory Disclaimer:** Because match percentages and diagnostics are AI judgments and can be wrong, ALWAYS state clearly (in the session language) that **the actual fit and final judgment belong strictly to the human applicant** (`score_match.py` embeds this notice automatically in every report).
5. **Zero Fabrication & Honest Unreachable Verdicts (허위 창작 금지 · 도달 불가 명확 판정):**
   - Every grade above `MISSING` MUST quote verbatim evidence from the user's submitted materials.
   - Even inside **Grace Mode (Suggestion-Only)**, NEVER invent unverified skills, metrics, employers, titles, or projects.
   - **Unreachable (`< 80%`) & Experience-Year Gate Rule:**
     - If `80%` is unreachable under the user's current profile (including when a JD mandates `X years of experience` without an equivalent-skill clause and the user lacks those years), state candidly that **`80%` is currently unreachable**, suppress Grace for chasing `80%`, and clearly explain **what is lacking and must be built across Experience, Projects, and Attitude/Positioning**.
     - **Equivalent-Skill Exception:** If the JD explicitly accepts **"equivalent practical skill (`경력에 준하는 실력`)"**, honestly judge whether the user's verified artifacts match the JD's seniority bar. Only if they plausibly match, leave a narrow conditional window (`CONDITIONAL_EQUIVALENT_SKILL`), state the concrete reason clearly, and offer suggestion-only **Grace**.
   - **Contradictory Keywords (`보유 · 미경험 충돌`) & Human `>= 80%` Partial Scope Rule:** Contradictory keywords receive `0.0` ATS credit by default (NOT auto-credited even if linked to `PARTIAL`). Ask the human user what percentage of the JD's required scope their verified partial experience covers; ONLY if the human explicitly confirms **`>= 80%`** coverage, record `"contradiction_human_confirmations"` in `round_NN_eval.json` to grant reasonable partial credit.

---

## Session Workspace & Files

Store per-application session artifacts locally (never inside this skill folder):
- Active workspace present → `<workspace>/.jd-coach/<company-role-slug>/`
- No active workspace → `<appDataDir>/scratch/jd-coach-sessions/<company-role-slug>/` (e.g., `~/.gemini/antigravity/scratch/jd-coach-sessions/<company-role-slug>/`)

```text
<session_dir>/
├── jd.txt                       # Snapshot of target job description
├── rubric.json                  # Locked JD rubric (created once in Round 1)
├── history.json                 # Auto-maintained by score_match.py
├── rounds/
│   ├── round_01_candidate.txt   # Consolidated plain text of Round 1 resume + portfolio
│   ├── round_01_eval.json       # Structured evidence grades for Round 1
│   ├── round_02_candidate.txt
│   └── round_02_eval.json
└── reports/
    ├── round_01_report.md       # Generated coaching report
    └── round_02_report.md
```

---

## Execution Pipeline

### Step 1: Intake & Text Extraction
1. Collect both inputs:
   - Target JD (`채용공고`): pasted text, local file, image/screenshot, or URL (if URL is live/interactive, inspect via `browser` subagent; if login/CAPTCHA gated, ask user to paste text).
   - Candidate Materials (`이력서 / 포트폴리오 / 简历 / 履歴書・職務経歴書`): one or more files (`.md`, `.txt`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.hwpx`, `.html`), pasted text, or portfolio links/screenshots.
   - If either the JD or candidate material is missing, ask concisely for the missing input before scoring.
2. Read all materials completely:
   - For `.pdf` and images/screenshots: inspect natively with `read_file` (do not skip portfolio slides or visual project pages). If `extract_doc.py` reports `PDF_NATIVE_READ_REQUIRED`, transcribe all relevant visible text/metrics from `read_file` into `round_NN_candidate.txt`.
   - For `.md`, `.txt`, `.docx`, `.xlsx`, `.pptx`, `.hwpx`, `.html`: extract clean consolidated UTF-8 text via [extract_doc.py](./scripts/extract_doc.py) (supports UTF-8/UTF-16 + legacy CJK encodings `cp949`/`gb18030`/`cp932`; note: legacy binary `.hwp`/`.doc`/`.xls` files are rejected cleanly, so ask the user to export as `.hwpx`, `.docx`, `.xlsx`, or `.pdf`):
     ```powershell
     python "<skill_dir>\scripts\extract_doc.py" --inputs "<resume_path>" "<portfolio_path>" --out "<session_dir>\rounds\round_01_candidate.txt"
     ```
   - If the user pasted text or supplied PDFs/images, write the consolidated candidate text into `<session_dir>\rounds\round_NN_candidate.txt` (combining extracted text + PDF/visual notes) so deterministic ATS keyword scanning and quote verification see all text.

### Step 2: Extract & Lock JD Rubric (Round 1 Only)
1. Read [scoring-rubric.md](./references/scoring-rubric.md) for the exact 4-dimension weights, evidence scale, keyword alias hygiene, country-specific resume conventions (`ko`/`en`/`zh`/`ja`), and role-adaptation guidelines.
2. Decompose the JD into `<session_dir>\rubric.json` (see schema in [sample_rubric.json](./examples/sample_rubric.json)):
   - Set `"language": "ko" | "en" | "zh" | "ja"` matching the JD / user's preferred coaching language (all report labels, rubric titles, and coaching feedback MUST stay strictly in that language with zero cross-language leakage), and `"domain_mode": "portfolio"` (default) or `"resume_only"` (for non-portfolio roles like HR/Finance/Accounting/Operations/Admin).
   - `must_have` (default `45%`): core duties + mandatory qualifications. Mark strict screening blockers with `"is_knockout": true` (requires `weight >= 2`; never mark soft skills as knockout). For mandatory years-of-experience clauses (`경력 X년 이상`, `X+ years`), also set `"experience_gate": {"required_years": X, "allows_equivalent_skill": true | false}` (`true` ONLY when the JD explicitly permits equivalent practical skill).
   - `portfolio_impact` (default `25%`): concrete proof-of-work, project artifacts, measurable business/technical outcomes, and individual ownership clarity.
   - `preferred` (default `15%`): nice-to-have / bonus qualifications (if the JD lists none, leave empty; `score_match.py` auto-normalizes active weights to `100%`).
   - `ats_framing` (default `15%`): split between deterministic negation-aware lexical JD `keywords` (with precise aliases, default `50%` of this dimension) and role framing / recruiter scannability items (`50%`).
3. Lock the rubric: run `score_match.py --init-rubric "<session_dir>\rubric.json"` to validate schema integrity (including Knockout weight and broad-alias warnings) and stamp `rubric_hash`. **Never alter `rubric.json` in later rounds** unless the user changes the target JD (which starts a new session).

### Step 3: Evidence-Grounded Audit & Deterministic Scoring
1. Evaluate every item in `rubric.json` against the candidate's Round `N` materials using the 5-level evidence scale (`FULL=1.0`, `STRONG_PARTIAL=0.75`, `PARTIAL=0.5`, `WEAK=0.25`, `MISSING=0.0`). Bare keyword listing in a skills section without project/work proof is strictly capped at **`WEAK (0.25)`**.
2. Save `<session_dir>\rounds\round_NN_eval.json` (see [sample_eval_r1.json](./examples/sample_eval_r1.json)):
   - Include verbatim `evidence_quote` (copied directly from `round_NN_candidate.txt`, no invented commentary) + `source` for every grade above `MISSING`.
   - Include `gap_type` (`expression_gap` | `transferable_gap` | `true_gap`) and concrete `action_hint` (coaching pointer, NOT a rewritten resume paragraph!) for every item below `FULL`.
   - If Grace assistance was used prior to this round, include `"grace_tier_used": 1 | 2 | 3`.
3. Run deterministic scoring & report generation (with `--strict-quotes` enabled by default):
   ```powershell
   python "<skill_dir>\scripts\score_match.py" `
     --rubric "<session_dir>\rubric.json" `
     --eval "<session_dir>\rounds\round_01_eval.json" `
     --candidate-text "<session_dir>\rounds\round_01_candidate.txt" `
     --history "<session_dir>\history.json" `
     --report-out "<session_dir>\reports\round_01_report.md" `
     --strict-quotes
   ```
4. Verify exit code `0`, zero `unverified_quotes`, and read the JSON stdout summary (`total_score`, `pass_status`, `delta_score`, `knockout_risks`, `projected_expression_only_score`, `projected_with_transferable_cap`, `top_priorities`, `grace_recommendation`).

### Step 4: Deliver Coaching Feedback (`< 80%`) or Pass Sign-Off (`>= 80%`)
Format the response following [report-template.md](./references/report-template.md):
- **If `REVISE` (`< 80.0%`):**
  1. Show exact score vs `80.0%` threshold (e.g., `64.5% / 목표 80.0% · 부족분 -15.5%p`) + category breakdown table + Round-over-Round `Δ` (on Round 2+).
  2. List **Priority Revision Checklist** sorted by highest `+X.X%p` impact first, separating `Expression Gap` (빠른 점수 상승), `Transferable Gap`, and `True Capability Gap` (정직한 대응 필요).
  3. Show missing ATS keywords (exact JD terms not yet present in candidate text).
  4. **Invite self-revision:** tell the user which 2–4 fixes will cross `80%` fastest and invite them to revise their materials and bring them back for **Round `N+1` re-evaluation**.
  5. Do **not** output a full rewritten resume.
- **If `PASS_WITH_RISK` (`>= 80.0%`, knockout missing):**
  - Congratulate crossing `80%`, clearly highlight the missing knockout Must-Have risk, and ask whether they actually possess that qualification (to reflect it in a quick follow-up round) or accept the risk knowingly.
- **If `PASS` (`>= 80.0%`, no knockout risk):**
  - Confirm pass status, summarize strongest matching proofs, optionally list 1–2 quick polish tips for interviews/cover letter, and close the loop cleanly.

### Step 5: Iterative Re-Evaluation Loop (Round 2, 3, …)
When the user returns with revised files or edited sections:
1. Build the updated full candidate snapshot `rounds/round_NN_candidate.txt`:
   - If the user provides full revised files → re-run `extract_doc.py` (or `read_file` for PDFs).
   - **Partial Chat Edit Merge Protocol:** If the user pastes *only* revised bullets/sections in chat, start from a copy of `rounds/round_{N-1}_candidate.txt`, replace/insert ONLY the modified section(s), and keep all untouched sections intact so unchanged evidence never triggers false regressions!
2. Re-audit against the **same locked `rubric.json`**, explicitly verifying:
   - Previously flagged items (did the edit genuinely add verified proof, or just stuff bare keywords, which is capped at `WEAK (0.25)`?),
   - Any unintended regressions (did edits remove prior evidence?).
3. Run `score_match.py` with the same `--rubric` and `--history` paths.
4. Highlight exact Round-over-Round progress (`Round 1: 64.5% → Round 2: 76.2% (+11.7%p)`), celebrate resolved gaps, note any regressions, and show the remaining distance to `80.0%`.

### Step 6: Tiered Grace Assistance (Strictly Suggestion-Only / 벽을 느낄 때 제안 전용 보조)
Load [grace-coaching-playbook.md](./references/grace-coaching-playbook.md) whenever a valid trigger fires (NEVER offer Grace to chase `80%` on an `UNREACHABLE` posting, and ALWAYS refuse direct-rewrite demands like `"됐고 수정해줘"`):
- **Trigger A (Explicit User Signal on Reachable / Equivalent-Skill Posting):** User expresses getting stuck or asks for coaching help (`"막혔어"`, `"어떻게 써야 할지 모르겠어"`, `"I'm stuck"`, `"卡壳了"`, `"書き方がわからない"`). *(If the user asks you to directly rewrite/edit the resume instead of suggesting, refuse firmly citing human authorship responsibility and offer Tier 1–3 suggestions only.)*
- **Trigger B (Automatic Signal from `score_match.py`):** `grace_recommendation.should_offer == true` fires when (1) `reachability_status == "CONDITIONAL_EQUIVALENT_SKILL"` (JD accepts equivalent skill AND verified artifacts show plausible potential, explaining why), OR (2) `reachability_status == "REACHABLE"` with 2+ round stall or `< +3.0` gain while `< 80%`. **Offer gently first** and never force Grace mode without consent.

Escalate only as far as the user needs (all 3 tiers remain strictly suggestion-only):
1. **Grace Tier 1 (Socratic Questions + Structural Skeleton):** Ask 2–4 targeted questions to surface real experience and suggest a fill-in-the-blank XYZ/STAR/Case-Study skeleton.
2. **Grace Tier 2 (Fact-Grounded Phrasing Suggestions, A/B/C Options):** Using ONLY verified facts from the user's documents + Tier 1 answers, suggest 2–3 framing options with explicit metric placeholders for the user to adapt in their own voice.
3. **Grace Tier 3 (Targeted Section Structural Proposal, Suggestion-Only):** On explicit request for a specific stuck section, suggest a tightly scoped structural blueprint strictly grounded in confirmed facts alongside a mandatory **Human Authorship & Fact-Check Checklist**, instructing the user to review, decide, and write the final wording themselves before returning to **Step 5**.

---

## Verification & Reference Index

- Rubric weights, 5-level evidence anchors & role presets: [references/scoring-rubric.md](./references/scoring-rubric.md)
- 3-tier Grace coaching playbook & anti-fabrication rules: [references/grace-coaching-playbook.md](./references/grace-coaching-playbook.md)
- Standardized coaching report & round-diff template: [references/report-template.md](./references/report-template.md)
- Document text extractor (`.md`, `.txt`, `.docx`, `.xlsx`, `.pptx`, `.hwpx`, `.html`): [scripts/extract_doc.py](./scripts/extract_doc.py)
- Deterministic scoring, ATS matcher & round tracker: [scripts/score_match.py](./scripts/score_match.py)
- Automated self-test suite: `python "<skill_dir>\scripts\test_resume_jd_coach.py"`
- JSON schema examples: [examples/sample_rubric.json](./examples/sample_rubric.json), [examples/sample_eval_r1.json](./examples/sample_eval_r1.json)
