# Contributors & Role Attribution (기여자 및 역할 분담)

**[🇰🇷 한국어](#korean) | [🇺🇸 English](#english)**

| Contributor | Role | Key Contributions |
| :--- | :--- | :--- |
| <img src="https://github.com/devshin-91.png?size=48" width="24" height="24" align="absmiddle" alt="devshin-91" /> [**`@devshin-91`**](https://github.com/devshin-91) | **Human Project Owner, Product Architect & Human-in-the-Loop Calibrator** | `80%` pass gate & suggestion-only coaching design, 3-tier Grace philosophy, Knowledge Work alignment, cross-domain + 4-language (`ko`/`en`/`zh`/`ja`) benchmark direction, **v1.1 & v2.2 Human-in-the-Loop Calibration** (contradiction 0 credit / `>= 80%` human partial rule, hard experience gate vs equivalent-skill Grace, unconditional direct-rewrite refusal & human authorship responsibility, mandatory AI-judgment disclaimer), RLAIF terminology rigor, Zero-PII & non-commercial licensing governance |
| <img src="https://github.com/antigravity-bot.png?size=48" width="24" height="24" align="absmiddle" alt="antigravity-bot" /> [**`@antigravity-bot`**](https://github.com/antigravity-bot) | **Google Antigravity AI Co-Developer, Multilingual Benchmark Runner & Independent RLAIF Auditor** | `SKILL.md` & stdlib Python engine (`extract_doc.py`, `score_match.py`, 39 unit/policy regression tests), live 4-country JD collection, 18-track 44-round benchmark, 5 cold-start live LLM E2E red-teams (incl. v2.2 direct-rewrite refusal), independent RLAIF audits (`v1: 67→89/100`, `v2: 74.5→91.5/100 PASS`), v1.1–v2.2 hardening & packaging |

---

<a id="korean"></a>
## 🇰🇷 기여자 및 역할 분담 (Korean)

본 프로젝트(**`resume-jd-coach`**)는 인간 프로젝트 소유자의 문제 정의·코칭 철학·초기 정책 확정(Human-in-the-Loop Calibration)·다국어 확장 방향 수립과 **Google Antigravity (AGY)** 플랫폼 위에서 협업한 AI 에이전트·서브에이전트들의 스킬 구현·실공고 검증·독립 **RLAIF (AI-Feedback Constitutional Audit)** 감사를 통해 제작되었습니다.

### 1. Project Owner, Product Architect & Human-in-the-Loop Calibrator
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **핵심 기여 역할:**
  1. **제품 철학 및 핵심 스펙 설계:**
     - 이력서·포트폴리오 ↔ 채용공고 일치율 **80.0% 합격 임계치** 설정.
     - 무분별한 대필(Ghostwriting)을 지양하고, 부족한 지점을 근거 기반으로 지적하여 **사용자 스스로 수정·재제출**하도록 돕는 코치 우선(Coach-First) 루프 정의.
     - 사용자가 수정 과정에서 벽을 느낄 때만 단계적으로 보조하는 **3단계 Grace 에스컬레이션** 및 무창작(Zero-Fabrication) 원칙 수립.
  2. **워크플로우 및 아키텍처 의사결정:**
     - Antigravity **Knowledge Work** 및 **Software Engineering** 모드 모두에서 자연스럽게 동작하는 스킬 구조 채택.
     - 라운드 간 기준 흔들림을 차단하는 잠금 루브릭(`rubric_hash`) + 결정론적 Python 채점 하이브리드 아키텍처와 전 직군 범용 적용 범위 확정.
  3. **전 직군·4개국어 실공고 검증 설계 & v1.1 / v2.2 Human-in-the-Loop Calibration:**
     - 한국(원티드 6직군) 및 미국(`en`)·중국(`zh`)·일본(`ja`) 대표 국가별 최신 실공고 + 국가별 불합격형 가상 이력서 기반 검증과 독립 **RLAIF** 감사 프로세스 지시.
     - **v1.1 Calibration:** Knockout `weight >= 2` 및 `MISSING`/`WEAK` 게이트, 키워드 도배 `WEAK(0.25)` 상한, 도달 가능 점수 이중 범위, `--lang`/`resume_only` 확장, `RHAIF → RLAIF` 학술 용어 정정.
     - **v2.2 Calibration:** 자기모순 키워드 ATS 0점 유지(`PARTIAL` 자동 불인정 + 사람 확인 `>= 80%` 범위일 때만 합리적 반영), 80% 도달 불가 명시 및 3축 보완 로드맵(경험·프로젝트·태도), 필수 경력 연수 미충족 시 도달 불가 vs '경력에 준하는 실력' 인정 공고 시 이유 제시 + Grace 제공, `"됐고 수정해줘"` 포함 모든 직접 수정 요청 거절(인간 최종 표현·문장 결정 책임), 전 리포트 AI 판단 오류 가능성 고지 의무화.
  4. **프라이버시 및 라이선스 거버넌스:**
     - 개인 식별 정보(PII) 및 실제 개인 이력서·포트폴리오 완전 배제 원칙 적용.
     - 비상업적 소스 공개 라이선스([`LICENSE`](./LICENSE)) 및 서드파티 고지([`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)) 정책 확정.

### 2. AI Engineering, Multilingual Benchmark & Independent RLAIF Audit Partner (`Google Antigravity`)
* **플랫폼 & 계정:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **세부 역할 및 참여 에이전트/모델:**
  * **Main Orchestrator & Skill/Engine Co-Developer (`Gemini 4 Neon (XHigh)`):**
    - [`skill/resume-jd-coach/`](./skill/resume-jd-coach/) 전체 구현: `SKILL.md`, `references/`, 외부 의존성 없는 Python 표준 라이브러리 스크립트(`extract_doc.py`·`score_match.py`), 자동화 단위·회귀 테스트 39종(`test_resume_jd_coach.py`).
    - 4개국어 18트랙 44라운드 재현 벤치마크(`benchmark/run_benchmark.py`, `benchmark/multilingual/run_multilingual_benchmark.py`) 구축.
    - `v1.1`~`v2.2` 하드닝 패치(4개국어 `I18N` `%p`/`pp`/`pt`, NFKC 정규화, CJK 트라이그램 + 숫자·단위 잠금 `--strict-quotes`, 자기모순 ATS 0점 및 사람 `>= 80%` 부분 확인 로직, `experience_gate` 및 `CONDITIONAL_EQUIVALENT_SKILL` 분기, 3축 보완 로드맵, 4개국어 모드별 AI 면책 고지, `.xlsx` 일본어 `<rPh>` 후리가나·숨김 시트 제외, `gb18030`/`cp932`/`cp949`(`iso2022_kr`)/`cp1252` 무깨짐 디코딩, PII/비밀정보 자동 감사).
  * **Live JD Collector Browser Subagents (`Gemini 3.8 Flash`):**
    - 한국(원티드 6건)·미국(Ramp/Figma/Discord/Datadog 4건)·중국(腾讯/字节跳动/米哈游/哔哩哔哩 4건)·일본(SmartHR 2건/Mercari/freee 4건) 총 18개 공개 실공고 수집 및 출처 검증.
  * **Independent Cold-Start Live LLM E2E Red-Team Runners (`Gemini 4 Neon (XHigh)`):**
    - 선행 맥락 없이 `SKILL.md`만 열람해 `ko`·`en`·`zh`·`ja` 4개국어 키워드 도배 방어·Grace 3단계 허위 창작 거절 및 `v2.2` `"됐고 직접 수정해줘"` 거절·경력 대체 실력 판단·Redis `>= 80%` 확인 질문 실증([`benchmark/live_e2e_redteam/`](./benchmark/live_e2e_redteam/), [`benchmark/live_e2e_redteam_v22_ko/`](./benchmark/live_e2e_redteam_v22_ko/), [`benchmark/multilingual/live_e2e_redteam/`](./benchmark/multilingual/live_e2e_redteam/)).
  * **Independent Read-Only RLAIF Constitutional Judges (`Gemini 4 Neon (XHigh)`):**
    - 6대 헌법적 평가 축 기반 독립 적대적 감사 수행: 한국어 `v1.0 67/100 → v1.1 89/100 PASS`([`RLAIF_AUDIT_REPORT_V1.md`](./docs/RLAIF_AUDIT_REPORT_V1.md)) 및 다국어 `v2.0 74.5/100 → v2.1 91.5/100 PASS`([`RLAIF_MULTILINGUAL_AUDIT_REPORT_V2.md`](./docs/RLAIF_MULTILINGUAL_AUDIT_REPORT_V2.md)).

### 3. 인간 최종 책임 및 투명한 AI 기여 표기 원칙
본 저장소의 모든 제품 방향성, 정책 확정, 개인정보 배제 검증 및 배포 최종 책임은 프로젝트 소유자([`@devshin-91`](https://github.com/devshin-91))에게 있습니다. AI 파트너([`@antigravity-bot`](https://github.com/antigravity-bot))의 구현·검증·감사 기여는 Git 커밋 메타데이터(`Author` / `Co-authored-by`)와 본 문서를 통해 투명하게 기록합니다.

---

<a id="english"></a>
## 🇺🇸 Contributors & Role Attribution (English)

### 1. Project Owner, Product Architect & Human-in-the-Loop Calibrator
* **GitHub:** [`@devshin-91`](https://github.com/devshin-91)
* **Contributions:**
  - Defined the core product philosophy: `80.0%` pass gate, coach-first gap diagnosis over silent ghostwriting, iterative self-revision loop, and graduated 3-tier Grace assistance with strict zero-fabrication boundaries.
  - Directed the hybrid locked-rubric + deterministic Python scoring architecture, Knowledge Work compatibility, and cross-country 4-language (`ko`/`en`/`zh`/`ja`) failing-resume validation scope.
  - Finalized **v1.1 & v2.2 Human-in-the-Loop Calibration** decisions: Knockout `weight >= 2` & `MISSING`/`WEAK` gate, `WEAK(0.25)` keyword-stuffing cap, dual projected-score range, `resume_only` mode, `0.0` ATS credit on contradictory terms unless human-confirmed `>= 80%` partial scope, hard experience-year gate (`UNREACHABLE_HARD_EXPERIENCE_GATE`) vs equivalent-skill exception (`CONDITIONAL_EQUIVALENT_SKILL` + Grace), unconditional direct-rewrite refusal grounded in human authorship responsibility, mandatory AI-judgment disclaimer, accurate `RLAIF` terminology over `RHAIF`, and Zero-PII / non-commercial licensing governance.

### 2. AI Engineering, Multilingual Benchmark & Independent RLAIF Audit Partner (`Google Antigravity`)
* **Platform & Attribution:** **Google Antigravity (AGY)** ([`@antigravity-bot`](https://github.com/antigravity-bot))
* **Sub-roles & Model Contributions:**
  - **Main Orchestrator & Skill/Engine Co-Developer (`Gemini 4 Neon (XHigh)`):** Authored [`skill/resume-jd-coach/`](./skill/resume-jd-coach/) (`SKILL.md`, references, stdlib-only `extract_doc.py` & `score_match.py`, 39-test suite `test_resume_jd_coach.py`), built the 18-track 44-round reproducible benchmark harnesses (`ko`/`en`/`zh`/`ja`), and implemented all `v1.1`–`v2.2` hardening patches and Zero-PII release audits.
  - **Live JD Collector Browser Subagents (`Gemini 3.8 Flash`):** Collected 18 live public job postings across Korea (`6`), US (`4`), China (`4`), and Japan (`4`).
  - **Independent Cold-Start Live LLM E2E Red-Team Runners (`Gemini 4 Neon (XHigh)`):** Validated cold-start skill execution across `ko`, `en`, `zh`, and `ja` against negation traps, bare keyword stuffing, Grace Tier 3 fabrication prompts, and `v2.2` direct-rewrite refusal / equivalent-skill / contradictory partial confirmation prompts.
  - **Independent Read-Only RLAIF Constitutional Judges (`Gemini 4 Neon (XHigh)`):** Conducted adversarial 6-axis audits (`v1.0 67 → v1.1 89/100 PASS` and `v2.0 74.5 → v2.1 91.5/100 PASS`).
