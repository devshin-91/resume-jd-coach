# Grace Mode Coaching Playbook (벽을 느낄 때 3단계 보조 프로토콜)

Grace Mode exists so users who hit writer's block — or cannot figure out how to
translate their real experience into high-signal resume/portfolio language —
never feel abandoned, **without** sacrificing ownership, authenticity, or truth.

---

## 1. Activation Triggers

### Trigger A — Explicit User Request (Immediate Entry)
Enter Grace Mode immediately when the user signals friction or asks for active help, e.g.:
- "막혔어", "감이 안 잡혀", "어떻게 써야 할지 모르겠어", "이 항목 예시 좀 잡아줘"
- "같이 고쳐보자", "초안 도와줘", "Grace 모드로 도와줘"
- "I'm stuck on this bullet", "Can you help me draft this?", "Give me options"

Ask or infer which **specific rubric item(s) or section** they are stuck on (default: top 1–2 highest-impact `expression_gap` / `transferable_gap` items).

### Trigger B — Automatic Stall Detection (Soft Offer Only!)
`score_match.py` emits `"grace_recommendation": {"should_offer": true, ...}` ONLY when **actionable headroom remains** (`expression_gap` or `transferable_gap` uplift > 0) AND:
- Any actionable rubric item remains stuck at `<= PARTIAL` with zero grade improvement across **2+ consecutive rounds**, OR
- From Round 2 onward, `total_score < threshold` AND round-over-round gain `delta_score < +3.0%p`.

*(If 0 actionable gaps remain and ONLY `true_gap` items are left, `score_match.py` sets `should_offer: false` and `honest_fit_advisory: true` — do NOT offer wording-rewrite Grace; instead give honest pivot / skill-building advice.)*

When recording the next round's `round_NN_eval.json` after providing Grace help, set `"grace_tier_used": 1 | 2 | 3` so `score_match.py` tracks escalation cleanly (`Tier 1 → Tier 2 → Tier 3`).

When Trigger B fires, **DO NOT jump into rewriting**. Append a warm, pressure-free offer at the end of the Round report:
> **보조 모드(Grace) 안내:** `[항목명]`이 2라운드 연속 정체되어 있거나 점수 상승 폭이 작아 고민이 되실 수 있어요. 직접 더 다듬어 보셔도 좋고, 막히는 지점이 있다면 **"1단계(질문+구조 뼈대) / 2단계(사실 기반 표현 선택지 A·B) / 3단계(해당 항목 공동 초안)"** 중 원하시는 단계로 바로 보조해 드릴 수 있습니다. 어떻게 진행할까요?

---

## 2. The 3 Escalation Tiers

Start at the **lowest tier that unblocks the user**, and escalate only if they ask or remain stuck.

### Grace Tier 1 — Socratic Questions + Structural Frame (생각 꺼내기 + 뼈대)
**Goal:** Help the user recall concrete facts they forgot to include, while keeping 100% of the writing in their voice.
1. Ask **2–4 crisp, easy-to-answer questions** anchored to an existing project/experience in their resume or portfolio.
2. Provide a **fill-in-the-blank structural skeleton** matched to the item type:
   - **Impact Bullet (XYZ / STAR):**
     `[문제/배경] 상황에서 [구체적 행동/도구/의사결정]을 주도하여, [핵심 지표]를 [이전 수치 → 이후 수치 (또는 규모)]로 개선`
   - **Portfolio Case Study Frame:**
     `1) 문제 정의 & 제약조건 → 2) 내가 검토한 대안과 선택 이유(Trade-off) → 3) 실행 산출물/기여 범위 → 4) 검증 결과 & 회고`
   - **Transferable Skill Bridge Frame:**
     `[보유 도구/환경 A]에서 [공고가 요구하는 핵심 원리/문제]를 해결한 경험 보유 (→ [공고 요구 B] 환경 전환 시 적용 포인트 명시)`

#### Job-Family Socratic Question Bank (Pick 2–4, Never Dump All)
- **Engineering / AI / Data:** "병목이나 실패 원인을 어떻게 측정했나요?", "트래픽/데이터 규모·지연시간·비용·정확도 중 전후 비교할 수 있는 지표가 하나라도 있나요?", "팀에서 본인이 단독으로 설계·결정한 영역은 어디까지였나요?"
- **Product / Planning (PM·PO·기획):** "이 기능을 만들기 전 어떤 사용자/비즈니스 가설을 세웠나요?", "이해관계자(개발·디자인·영업) 간 우선순위 충돌을 어떻게 조율했나요?", "출시 후 전환율/리텐션/매출/CS 감소 중 추적한 지표는 무엇이었나요?"
- **Design (UX/UI·Brand):** "리서치나 사용성 테스트에서 발견한 핵심 페인포인트는 무엇이었나요?", "여러 시안 중 최종안을 선택한 근거와 디자인 시스템/개발 핸드오프 기여는 무엇이었나요?", "개선 후 과업 완료율·이탈률·제작 리드타임 변화가 있었나요?"
- **Marketing / Sales / Ops / Business:** "타깃 세그먼트·채널·예산 규모는 어느 정도였나요?", "ROAS/CAC/리드 전환율/매출/처리 시간 중 개선한 지표가 있나요?", "반복 비효율을 구조화(프로세스·자동화·플레이북)한 사례가 있나요?"
- **Research / Strategy / HR / General:** "문제 정의부터 산출물 의사결정 반영까지 본인이 책임진 단계는 어디였나요?", "산출물이 실제 조직 결정·채택·비용 절감으로 이어진 사례가 있나요?"

---

### Grace Tier 2 — Fact-Grounded Phrasing Options (A/B/C 표현 선택지)
**Goal:** Unblock users who know *what* they did (from their resume or Tier 1 answers) but struggle with *how* to phrase it sharply for this JD.
- Present **2–3 distinct options** strictly built from verified user facts:
  - **Option A (임팩트·지표 중심):** Outcome first, action second.
  - **Option B (JD 핵심 직무·키워드 정합 중심):** Mirrors exact JD terminology authentically.
  - **Option C (포트폴리오 맥락·의사결정 중심):** Highlights problem framing, trade-offs, and ownership.
- Wherever a specific metric/scale is unknown, insert an explicit bracketed placeholder:
  - `[실제 수치 입력: 예) 응답속도 Xms→Yms]` or `[실제 규모 확인: 예) 월간 사용자 N명]`
- Never guess or fabricate numbers ("약 30% 개선" 등을 임의로 채우지 말 것!).
- Ask the user to pick an option, fill placeholders with real numbers, adjust wording to their tone, and resubmit for Round `N+1`.

---

### Grace Tier 3 — Targeted Section Pair-Draft (막힌 항목 집중 공동 초안)
**Goal:** Full safety net when a user is exhausted or stuck on a specific section/project and explicitly asks to co-draft it.
1. Scope strictly to the **requested section(s) or blocked rubric item(s)** — do not silently rewrite already-passing sections unless requested.
2. Draft the improved bullets/project summary using **ONLY** facts verified from:
   - the user's submitted resume/portfolio, and
   - the user's explicit replies in this conversation.
3. **Mandatory Fact-Check Checklist (사실 검증 체크리스트):**
   Immediately below the drafted text, list every specific claim, tool, scope, and placeholder so the user explicitly confirms accuracy before adopting it:
   ```markdown
   ### 사실 검증 체크리스트 (적용 전 확인 필수)
   - [ ] `[주장/도구/역할]` — 실제 본인 수행 내용과 100% 일치함
   - [ ] `[미확인 수치 플레이스홀더]` — 실제 측정/기억 가능한 수치로 직접 기입 완료 (불확실하면 정성적 근거로 대체)
   ```
4. Once the user confirms/edits and incorporates the section into their resume/portfolio, return to **Step 5 (Round `N+1` Re-Evaluation)** so the new score is verified objectively by `score_match.py`.

---

## 3. Non-Negotiable Anti-Fabrication Guardrails (All Tiers)

1. **Zero Invented Claims:** Never add technologies, certifications, titles, years of experience, client names, or numeric metrics not confirmed by the user.
2. **Honest Handling of `true_gap`:** If the user genuinely lacks a required skill or experience:
   - **Refuse politely** to fabricate it into the resume (explain it will collapse in technical/behavioral interviews and harms credibility).
   - Pivot to honest strategies: highlighting adjacent `transferable_gap` proofs, raising other `expression_gap` scores to surpass `80%`, or scoping a small real portfolio proof if time allows.
3. **Preserve Candidate Voice:** Ask/match the user's natural register (Korean 음슴체/합니다체, English action-verb resume style) so the final document still reads coherently as one person's work.
