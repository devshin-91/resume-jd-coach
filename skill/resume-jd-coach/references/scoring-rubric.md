# Scoring Rubric & Evidence Anchors (`resume-jd-coach`)

This reference governs **Step 2 (Rubric Extraction & Lock)** and **Step 3 (Evidence-Grounded Audit)**.

---

## 1. 4-Dimension Weighted Architecture

Default universal category weights (sum = `100`):

| Category Key | Label (KO / EN) | Default Weight | What It Evaluates |
| :--- | :--- | :---: | :--- |
| `must_have` | 필수 자격 및 핵심 직무 역량 / Must-Have & Core Duties | **45%** | Explicit mandatory requirements (`자격요건`, `필수`, `Required`, `Must have`) and primary day-to-day job responsibilities (`주요업무`, `Responsibilities`). |
| `portfolio_impact` | 포트폴리오 증빙 및 성과 정량화 / Portfolio Proof & Impact | **25%** | Concrete work artifacts, case studies, problem→action→result depth, measurable outcomes (metrics/scale/quality), and clear personal ownership vs team effort. *(For non-portfolio roles, evaluates Resume Work Proof & Measurable Business Impact.)* |
| `preferred` | 우대 사항 및 차별화 역량 / Preferred & Nice-to-Have | **15%** | Explicit bonus qualifications (`우대사항`, `Preferred`, `Bonus`, `Plus`). If the JD lists zero preferred items, leave `preferred` items empty — `score_match.py` automatically normalizes active category weights to `100%`. |
| `ats_framing` | JD 용어·키워드 정합성 및 직무 포지셔닝 / ATS Keywords & Role Framing | **15%** | Split between **deterministic lexical JD keyword coverage** (`ats_lexical_share`, default `0.50`) and **human recruiter framing** (`0.50`: summary/headline positioning, role-level match, scannability, JD terminology alignment). |

### Role-Adaptive Weight Presets (Optional — Choose *Before* Locking Round 1)
Keep the default `45 / 25 / 15 / 15` unless the target role strongly warrants one of these presets:
- **Portfolio-Heavy Creative / Design / Frontend / Product Roles:** `40 / 35 / 10 / 15`
- **Junior / Entry-Level / New Grad Roles (신입·주니어):** `40 / 30 / 10 / 20` (elevates project proof + clear role framing over seniority credentials)
- **Research / Specialist / Regulated Roles (연구·법무·의료·금융):** `55 / 20 / 15 / 10` (elevates mandatory credentials/domain mastery)
- **Senior / Lead / Staff Roles:** `45 / 30 / 15 / 10` (elevates business/org impact & ownership scope)

Once `rubric.json` is initialized (`--init-rubric`), weights and items are **locked for the entire session**.

---

## 2. Item Decomposition Rules (Building `rubric.json`)

1. **Right Granularity (10–22 total items):**
   - `must_have`: 4–9 concrete, testable items (do not lump 5 unrelated skills into one vague item).
   - `portfolio_impact`: 3–5 proof criteria derived directly from the JD's actual core problems (e.g., "JD 핵심 과제와 연결된 대표 프로젝트 2건 이상 케이스 스터디", "전/후 비교 가능한 정량 성과 지표 제시", "본인 기여도·의사결정 근거 명시").
   - `preferred`: 0–6 items matching the JD's stated bonus requirements.
   - `ats_framing`: 2–3 framing items (e.g., "상단 요약/헤드라인의 타깃 직무 정합성", "채용담당자 10초 스캔 가독성 및 핵심 성과 상단 배치") **plus** `keywords` list (`must` and `preferred` terms with Korean/English aliases).
2. **Relative Item Weights (`weight`):**
   - Use integer weights `1`, `2`, or `3` inside each category:
     - `3` = Core pillar / repeatedly emphasized in JD
     - `2` = Standard explicit requirement
     - `1` = Secondary / supporting detail
3. **Knockout Flag (`"is_knockout": true`):**
   - Apply **sparingly** (typically 0–3 items in `must_have`) ONLY to hard screening gates explicitly mandated by the JD:
     - Mandatory license/certification/degree/visa/language proficiency (e.g., "변호사 자격 필수", "비즈니스 영어 필수")
     - Non-negotiable core stack or mandatory minimum domain experience explicitly marked 필수/Required where absence typically causes automatic rejection.
   - **Mandatory Weight Floor:** Every `is_knockout: true` item MUST have `weight >= 2` (enforced by `score_match.py`).
   - **No Soft-Skill Knockouts:** Do NOT mark soft skills ("커뮤니케이션 능력", "꼼꼼함") as `is_knockout: true`.
4. **Keyword Alias Hygiene (Precision Over Recall):**
   - Include clean Korean/English equivalents (`Kubernetes` ↔ `K8s`, `쿠버네티스`; `A/B 테스트` ↔ `AB 테스트`, `A/B Testing`), plus optional `"linked_item_id"` when a keyword maps tightly to a specific rubric item.
   - **Ban Overly Broad Umbrella Aliases:** NEVER add generic 2-character or umbrella words as aliases for specialized technical/domain terms (e.g., NEVER put `"자동화"` as an alias for `LLM` or `프로토타이핑`, NEVER put `"취득"` or `"상실"` as standalone aliases for `4대보험`, NEVER put `"Docker"` as an alias for `AWS`).
   - `score_match.py` automatically ignores matches occurring inside negative/unexperienced phrasing (e.g., `"Spark 미경험"`, `"아직 해 보지 않은 것: Kubernetes"`).
5. **Domain & Language Configuration (`rubric.json` top-level):**
   - `"language": "ko"` (default) or `"en"`
   - `"domain_mode": "portfolio"` (default) or `"resume_only"` (switches `portfolio_impact` label to `"직무 증빙 & 정량 성과"` / `"Work Proof & Measurable Impact"` for non-portfolio roles such as HR, Finance, Operations, Admin).

---

## 3. 5-Level Evidence Grading Scale (Anti-Inflation Anchors)

Assign every item one of the 5 anchored grades. **Never inflate grades to make a user feel better — inflated scores sabotage real interviews.**

| Grade | Multiplier | Strict Operational Criteria |
| :--- | :---: | :--- |
| **`FULL`** | `1.00` | Directly and convincingly satisfied with **concrete, contextual proof** (project, work scope, artifact, or measurable outcome) matching the JD's level and context. Must cite verbatim quote from `round_NN_candidate.txt`. |
| **`STRONG_PARTIAL`** | `0.75` | Clearly present and relevant in actual work/projects, **but** missing depth on one aspect: e.g., lacks measurable impact/scale, unclear personal contribution, or slightly narrower scope than JD asks. Also the realistic ceiling for bridged `transferable_gap` items. |
| **`PARTIAL`** | `0.50` | Real project/work mention exists, **but** covers only half of a compound requirement (e.g., SQL mart built without Spark), lacks concrete outcome/context, OR relies on adjacent transferable experience with real project proof. |
| **`WEAK`** | `0.25` | **Bare skills-list mention without any project/work context (Anti-Keyword-Stuffing ceiling)**, OR indirect/faint/outdated signal that a hurried recruiter would likely miss. |
| **`MISSING`** | `0.00` | Absent from all submitted resume and portfolio materials (or explicitly listed only under "unexperienced / not yet done"). |

### Anti-Keyword-Stuffing Rule (Round 2+ Audit Discipline)
If a candidate edits Round 2 merely by dropping bare keywords into a skills list without adding verified project/work context:
- The deterministic ATS lexical keyword check may rise slightly,
- **BUT** the corresponding `must_have` or `portfolio_impact` rubric item is **strictly capped at `WEAK (0.25)`** (NEVER `PARTIAL` or above!), and the report must explain *why*: recruiters verify keywords inside real project/work bullets!
- Every `evidence_quote` MUST be copied verbatim from `round_NN_candidate.txt` (verified programmatically by `score_match.py`).

---

## 4. Gap Taxonomy (Mandatory on Every Item Below `FULL`)

Classify every item graded `< FULL` into one of three honest gap types:

1. **`expression_gap` (표현·증빙 부족 — 최우선 빠른 개선 영역)**
   - The candidate's resume/portfolio hints they likely *did* this work (or adjacent parts of the same project), but omitted metrics, personal ownership, JD-aligned terminology, or portfolio visuals/architecture/rationale.
   - *Coaching action:* Point to the exact existing project/role and ask what concrete actions, constraints, decisions, or numbers can be surfaced.
2. **`transferable_gap` (유사·전이 역량 연결 필요)**
   - The candidate lacks the exact named tool/domain, but has closely related experience (e.g., PyTorch vs TensorFlow, Figma vs Sketch, B2C growth vs B2B PLG, MySQL vs PostgreSQL).
   - *Coaching action:* Guide the candidate to bridge the underlying principle honestly ("X 환경에서 유사한 Y 문제를 해결한 경험") without claiming hands-on mastery of a tool they haven't used.
3. **`true_gap` (실제 미보유 역량 — 창작 절대 금지)**
   - Genuine absence of a required skill, credential, or experience scope.
   - *Coaching action:* State candidly that this cannot be fixed by wording tweaks. Offer honest strategic options:
     - Compensate via stronger proof on other `expression_gap` items to cross `80%` honestly,
     - Build a small real artifact/case study if application timeline permits,
     - Address transparently as a fast-ramp plan in cover letter/interview, or reassess fit if it is a hard knockout requirement.

---

## 5. Pass Verdict & Honest Projection Rules (`score_match.py`)

- Default `pass_threshold = 80.0` (customizable per `rubric.json`).
- Exact `Decimal` arithmetic (`ROUND_HALF_UP` across both JSON & Markdown tables) prevents boundary or sum contradictions.
- **Knockout Risk Rule:** Any `is_knockout: true` item graded **`MISSING (0.00)` or `WEAK (0.25)`** triggers a Knockout Risk warning (prevents bypassing with 1 bare keyword).
- Verdict states:
  - **`PASS`**: `exact_score >= threshold` AND `knockout_risks == []`
  - **`PASS_WITH_RISK`**: `exact_score >= threshold` AND `len(knockout_risks) > 0`
  - **`REVISE`**: `exact_score < threshold`
- **Dual Honest Projection Range:** Reports show BOTH `projected_expression_only_score` (`expression_gap` + eligible ATS fixes) AND `projected_with_transferable_cap` (adding `transferable_gap` conservatively capped at `STRONG_PARTIAL = 0.75`, never assuming `FULL = 1.00`), preventing false hope on `true_gap`-heavy postings.
