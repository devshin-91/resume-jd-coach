# Contributors & Role Attribution (기여자 및 역할 분담)

**[🇰🇷 한국어](#korean) | [🇺🇸 English](#english)**

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Product Architect & RHAIF Human Calibrator** | 80% pass gate & coach-first design, 3-tier Grace philosophy, Knowledge Work alignment, 6-job-family + RHAIF validation design, v1.1/v1.2 Human Calibration sign-off, Zero-PII & non-commercial licensing governance |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Benchmark Runner & Independent RHAIF Auditor** | `SKILL.md` & stdlib Python engine (`extract_doc.py`, `score_match.py`, 17 unit/regression tests), live Wanted JD collection, 6-track 15-round benchmark, cold live LLM E2E red-team, independent RHAIF audit (`67 → 89/100 PASS`), v1.1/v1.2 hardening & packaging |

---

<a id="korean"></a>
## 🇰🇷 기여자 및 역할 분담 (Korean)

본 프로젝트(**`resume-jd-coach`**)는 인간 프로젝트 소유자의 문제 정의·코칭 철학·평가 기준 확정(Human Calibration)과 **Google Antigravity (AGY)** 플랫폼 위에서 협업한 AI 에이전트·서브에이전트들의 스킬 구현·실공고 검증·독립 RHAIF 감사를 통해 제작되었습니다.

### 1. Project Owner, Product Architect & RHAIF Human Calibrator
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **핵심 기여 역할:**
  1. **제품 철학 및 핵심 스펙 설계:**
     - 이력서·포트폴리오 ↔ 채용공고 일치율 **80.0% 합격 임계치** 설정.
     - 무분별한 대필(Ghostwriting)을 지양하고, 부족한 지점을 근거 기반으로 지적하여 **사용자 스스로 수정·재제출**하도록 돕는 코치 우선(Coach-First) 루프 정의.
     - 사용자가 수정 과정에서 벽을 느낄 때만 단계적으로 보조하는 **3단계 Grace 에스컬레이션** 및 무창작(Zero-Fabrication) 원칙 수립.
  2. **워크플로우 및 아키텍처 의사결정:**
     - Antigravity **Knowledge Work** 및 **Software Engineering** 모드 모두에서 자연스럽게 동작하는 스킬 구조 채택.
     - 라운드 간 기준 흔들림을 차단하는 잠금 루브릭(`rubric_hash`) + 결정론적 Python 채점 하이브리드 아키텍처와 전 직군 범용 적용 범위 확정.
  3. **전 직군 실공고 검증 및 RHAIF Human Calibration 확정:**
     - 실제 채용 사이트 전 직군 공고 기반 가상 이력서/포트폴리오 교차 검증 및 독립 **RHAIF (Human+AI Feedback)** 평가 프로세스 지시.
     - RHAIF 감사 결과를 검토하고 핵심 정책 4항목(Knockout `weight >= 2` 및 `MISSING`/`WEAK` 게이트, 근거 없는 키워드 도배 `WEAK(0.25)` 상한, 도달 가능 점수 이중 범위 표기, `--lang ko|en` 및 `resume_only` 지원)과 **v1.2 미세 보강 5건**을 최종 승인.
  4. **프라이버시 및 라이선스 거버넌스:**
     - 개인 식별 정보(PII) 및 실제 개인 이력서·포트폴리오 완전 배제 원칙 적용.
     - 비상업적 소스 공개 라이선스([`LICENSE`](./LICENSE)) 및 서드파티 고지([`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)) 정책 확정.

### 2. AI Engineering, Benchmark & Independent RHAIF Audit Partner (`Google Antigravity`)
* **플랫폼 & 계정:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **세부 역할 및 참여 에이전트/모델:**
  * **Main Orchestrator & Skill/Engine Co-Developer (`Gemini 4 Neon (XHigh)`):**
    - [`skill/resume-jd-coach/`](./skill/resume-jd-coach/) 전체 구현: `SKILL.md`, `references/`(루브릭·Grace 플레이북·리포트 템플릿), 외부 의존성 없는 Python 표준 라이브러리 스크립트(`extract_doc.py`, `score_match.py`), 자동화 단위·회귀 테스트 17종(`test_resume_jd_coach.py`).
    - 6개 직군 15라운드 재현 벤치마크(`benchmark/run_benchmark.py` 및 `benchmark/tracks/`) 구축과 가상 지원자/라운드 산출물 생성.
    - RHAIF 감사 및 Human Calibration 반영 패치(`v1.1` → `v1.2`): 부정문·자기모순(`contradictory_mentions`) ATS 탐지, 바이그램 기반 엄격 인용 검증(`--strict-quotes`), 중첩 표 `.hwpx`/텍스트박스 `.docx`/시각순 `.pptx`/레거시 `.hwp` 차단, Windows UTF-8 BOM(`utf-8-sig`) 호환, PII·비밀정보 자동 스캔 및 라이선스 패키징.
  * **Live JD Collector Browser Subagents (`Gemini 3.8 Flash`):**
    - 원티드(`wanted.co.kr`) 공개 채용 공고에서 개발·기획/PM·디자인·마케팅·데이터·비IT 신입 HR 6개 직군 실시간 요구사항 수집 및 출처 검증.
  * **Independent Cold-Start Live LLM E2E Red-Team Runner (`Gemini 4 Neon (XHigh)`):**
    - 선행 맥락 없이 `SKILL.md`만 읽고 실제 공고(Track 5)에 대해 부정문 이력서 평가(R1), 키워드 도배 공격 방어 및 Grace 3단계 허위 창작 요구 거절(R2)을 수행([`benchmark/live_e2e_redteam/`](./benchmark/live_e2e_redteam/)).
  * **Independent Read-Only RHAIF Constitutional Judge (`Gemini 4 Neon (XHigh)`):**
    - 6대 헌법적 평가 축 기반 독립 적대적 감사 수행(`v1.0 67/100` CONDITIONAL PASS → `v1.1 89/100` PASS, `+22점`), P0/P1 결함 7건 및 v1.2 미세 보강 항목 5건 도출([`docs/RHAIF_AUDIT_REPORT.md`](./docs/RHAIF_AUDIT_REPORT.md)).

### 3. 인간 최종 책임 및 투명한 AI 기여 표기 원칙
본 저장소의 모든 제품 방향성, 평가 기준 확정, 개인정보 배제 검증 및 배포 최종 책임은 프로젝트 소유자([`@devshin-91`](https://github.com/devshin-91))에게 있습니다. AI 파트너([`@antigravity-bot`](https://github.com/antigravity-bot))의 구현·검증·감사 기여는 Git 커밋 메타데이터(`Author` / `Co-authored-by`)와 본 문서를 통해 투명하게 기록합니다.

---

<a id="english"></a>
## 🇺🇸 Contributors & Role Attribution (English)

### 1. Project Owner, Product Architect & RHAIF Human Calibrator
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **Contributions:**
  - Defined the core product philosophy: `80.0%` pass gate, coach-first gap diagnosis over silent ghostwriting, iterative self-revision loop, and graduated 3-tier Grace assistance with strict zero-fabrication boundaries.
  - Directed the hybrid locked-rubric + deterministic Python scoring architecture, universal cross-domain support, and Antigravity **Knowledge Work** workflow compatibility.
  - Designed the 6-job-family live-JD validation and independent RHAIF audit workflow, finalized Human Calibration decisions (Knockout `weight >= 2` & `MISSING`/`WEAK` gate, `WEAK(0.25)` keyword-stuffing cap, dual projected-score range, `ko|en` & `resume_only` modes, v1.2 micro-hardening), and established Zero-PII and non-commercial licensing governance.

### 2. AI Engineering, Benchmark & Independent RHAIF Audit Partner (`Google Antigravity`)
* **Platform & Attribution:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **Sub-roles & Model Contributions:**
  - **Main Orchestrator & Skill/Engine Co-Developer (`Gemini 4 Neon (XHigh)`):** Authored [`skill/resume-jd-coach/`](./skill/resume-jd-coach/) (`SKILL.md`, references, stdlib-only `extract_doc.py` & `score_match.py`, 17-test suite `test_resume_jd_coach.py`), built the 6-track 15-round reproducible benchmark harness (`benchmark/`), implemented all `v1.1` & `v1.2` hardening fixes, and executed PII/secret auditing and release packaging.
  - **Live JD Collector Browser Subagents (`Gemini 3.8 Flash`):** Collected 6 live public Wanted job postings across Backend Engineering, PM, Product Design, Brand Marketing, Data Analytics, and Entry-Level Non-IT HR.
  - **Independent Cold-Start Live LLM E2E Red-Team Runner (`Gemini 4 Neon (XHigh)`):** Validated cold-start skill execution against negation handling, bare keyword stuffing, and Grace Tier 3 fabrication prompts ([`benchmark/live_e2e_redteam/`](./benchmark/live_e2e_redteam/)).
  - **Independent Read-Only RHAIF Constitutional Judge (`Gemini 4 Neon (XHigh)`):** Conducted the 6-axis adversarial audit (`v1.0 67/100` → `v1.1 89/100 PASS`, `+22 pts`), identifying 7 P0/P1 issues and 5 v1.2 residual micro-fixes ([`docs/RHAIF_AUDIT_REPORT.md`](./docs/RHAIF_AUDIT_REPORT.md)).
