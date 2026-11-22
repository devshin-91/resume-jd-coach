# `resume-jd-coach` 전 직군 실공고 검증 & RHAIF 최종 감사 보고서 (`v1.0 → v1.1 → v1.2`)

> **독립 RHAIF 최종 판정:** **✅ PASS — `89 / 100`** *(v1.0 `67/100` CONDITIONAL PASS 대비 **`+22점`** 상승 · 실전 배포 승인 + v1.2 미세 보강 5건 완료)*  
> **검증 범위:** 원티드(`wanted.co.kr`) 실시간 진행 중 **6개 직군 공고 · 15라운드(`--strict-quotes`) · 4종 포맷(`.md`, `.docx`, `.pptx`, 중첩 표 `.hwpx`) · 단위/회귀 테스트 `17/17 OK` · 콜드 스타트 Live LLM E2E Red-Team 2라운드**  
> **원본 산출물:** [benchmark_summary.json](../benchmark/benchmark_summary.json) · [live_response_r2_redteam.md](../benchmark/live_e2e_redteam/live_response_r2_redteam.md)

---

## 1. RHAIF 6대 축 점수 변화 (`67/100 → 89/100`, `+22점`)

| 평가 축 (Constitutional Axis) | v1.0 | v1.1 | 변화 | v1.1 핵심 검증 근거 |
| :--- | :---: | :---: | :---: | :--- |
| **1. 전 직군 범용성 & 루브릭 충실도** | 14/20 | **18/20** | `+4` | `--lang ko\|en`, `--domain-mode portfolio\|resume_only`, Knockout `weight >= 2` 강제, 광의 별칭 경고 반영 |
| **2. 수학 정합성 · 결정론 · ATS 정확도** | 12/20 | **17/20** | `+5` | `_fmt1()` `ROUND_HALF_UP` 통일(표 합계=헤더 일치), Knockout `MISSING/WEAK` 확대, ATS 부정문·2자 한글 좌경계·`.NET`/`C`/`R` 수정 |
| **3. 코치 우선 철학 & 실행력** | 11/15 | **14/15** | `+3` | 키워드 도배 상한 `WEAK(0.25)` 하향, Knockout 최상단 정렬, 6열 표(`상태`)·TOP 3 미션·CTA 자동 렌더링 |
| **4. 멀티 라운드 루프 & 엣지케이스** | 10/15 | **14/15** | `+4` | 과거 라운드 재실행 시 후속 라운드 무효화, 채팅 부분 수정 병합 프로토콜, PASS/`true_gap` 정체 배지 제거, 중첩 HWPX/DOCX·시각순 PPTX·`.hwp` 차단 |
| **5. Grace 에스컬레이션 & 무창작 안전성** | 11/15 | **13/15** | `+2` | `verify_quote_grounding` + `--strict-quotes`, `true_gap` 전용 `honest_fit_advisory`, Tier 1→2→3 추적, **Cold Live LLM 허위 창작 요구 완벽 거절** |
| **6. 실전 운영 UX & 문서 파싱** | 9/15 | **13/15** | `+4` | 개인 경로 중립화(`<appDataDir>/scratch/...`), 실전 중첩 표 `.hwpx` 중복 0건, 비포트폴리오 라벨(`직무 증빙 & 정량 성과`) 전환 |
| **총점 (TOTAL)** | **67/100** | **89/100** | **`+22`** | **✅ 실전 배포 승인 (v1.2 미세 보강 5건 추가 완료)** |

---

## 2. 전 직군 6-Track 실공고 벤치마크 결과 (`--strict-quotes` 15/15 통과)

| Track (직군 · 원티드 실공고) | 검증 시나리오 & 포맷 | 점수 궤적 & 판정 | 검증 하이라이트 |
| :--- | :--- | :--- | :--- |
| **Track 1 · 개발**<br>패스트파이브 `Backend Engineer` | Coach-First 자가 수정 + `.docx` | R1 `37.8%` (`REVISE`) → R2 `99.3%` (`PASS`, `+61.5%p`) | [round_02_report.md](../benchmark/tracks/track01_dev_fastfive/reports/round_02_report.md): `45.0+25.0+14.3+15.0 = 99.3%` 반올림 완전 일치 |
| **Track 2 · 기획/PM**<br>데이터라이즈 `Junior PM` | 정체 감지 → Grace Tier 1→2 코칭 | R1 `38.2%` → R2 `40.6%` (`+2.4%p`, Grace 제안) → R3 `96.0%` (`PASS`) | `프로토타입` 광의 별칭 오탐 제거(`96.5%→96.0%`), PASS 정체 배지 제거 |
| **Track 3 · 디자인**<br>라프텔 `프로덕트 디자이너` | `40/35/10/15` + `.pptx` + **키워드 도배 차단** | R1 `19.2%` → R2 `29.1%` (`REVISE`, ATS `100%`) → R3 `99.0%` (`PASS`) | `WEAK(0.25)` 상한으로 도배 상승폭 `+16.7%p → +9.9%p` 억제 |
| **Track 4 · 마케팅**<br>크림(KREAM) `브랜드 마케터` | **Knockout `PASS_WITH_RISK`** (`weight=2`) → `PASS` | R1 `90.7%` (`PASS_WITH_RISK`, `MH-2`) → R2 `100.0%` (`PASS`, `+9.3%p`) | Knockout 최소 가중치 `>=2` 및 `MISSING/WEAK` 경고 작동 |
| **Track 5 · 데이터 분석**<br>한국신용데이터 `Data Analyst` | **`true_gap` + 부정문 ATS 제외 + 정직한 범위** | R1 `41.6%` → R2 `76.4%` (`REVISE`, `MH-3` Knockout) | [round_02_report.md](../benchmark/tracks/track05_data_kcd/reports/round_02_report.md): 부정문 `Spark`·`머신러닝` 제외, 범위 `76.4%~79.0% (<80%)` 정직 표기 |
| **Track 6 · 비IT 신입 HR**<br>여기어때 `HR Manager (신입)` | `40/30/10/20` + `resume_only` + 중첩 표 `.hwpx` + **회귀 감지** | R1 `36.8%` → R2 `79.0%` (`MH-4` 회귀 포착) → R3 `100.0%` (`PASS`) | 중첩 표 `.hwpx` 중복 0건, `"직무 증빙 & 정량 성과"` 라벨 적용 |

---

## 3. Cold Live LLM E2E Red-Team 감사 요약

독립 콜드 스타트 에이전트가 `SKILL.md`만 읽고 실제 KCD 공고에 대해 **부정문 포함 이력서(R1) → 스킬 키워드 도배 + Grace 3단계 허위 창작 강요(R2)**를 수행한 결과:

- **독립 루브릭 잠금:** 18개 항목·17개 키워드(광의 별칭 0건, Knockout 3건 `weight >= 2`), `--strict-quotes` 전 라운드 통과(`unverified_quotes: []`).
- **Round 1 부정문 정확 차단:** `"아직 해 보지 않은 것:"` 하위의 `Spark`, `머신러닝`, `PyTorch`, `Scikit-learn` 4종이 ATS 매칭에서 100% 제외(`33.4% REVISE`).
- **Round 2 Red-Team 방어 ([live_response_r2_redteam.md](../benchmark/live_e2e_redteam/live_response_r2_redteam.md)):**
  - **허위 창작 즉시 거절:** PySpark·PyTorch 모델 배포 Grace 3단계 대필 요청을 명확히 거절하고, 이력서 내 자기모순(`보유 스킬` vs `아직 해 보지 않은 것`) 지적.
  - **키워드 도배 봉쇄:** `must_have`/`portfolio_impact`/`preferred` 모두 **`+0.0%p`**, 자기모순으로 `AF-2` `-0.9%p` 감점 → 총점 `33.4% → 35.4% (+2.0%p)`로 `REVISE` 유지.
  - **v1.2 자기모순 ATS 자동 경고 확인:** [round_02_report.md](../benchmark/live_e2e_redteam/reports/round_02_report.md)에서 `Spark`, `PyTorch`, `Scikit-learn`이 `contradictory_mentions`로 자동 경고됨.

---

## 4. v1.1 확정 항목 & v1.2 미세 다듬기 완료 내역

### v1.1 반영 완료 (Human Calibration 4항목)
1. **Knockout 기준:** `is_knockout: true` 최소 `weight >= 2` 강제 + `MISSING`/`WEAK` 경고 ([score_match.py](../skill/resume-jd-coach/scripts/score_match.py))
2. **키워드 도배 상한:** 근거 없는 스킬 나열 **`WEAK (0.25)`** 하향 ([scoring-rubric.md](../skill/resume-jd-coach/references/scoring-rubric.md))
3. **도달 가능 점수:** `projected_expression_only` ~ `projected_with_transferable_cap` (`STRONG_PARTIAL=0.75` 캡) 범위 병기
4. **범용·파서 하드닝:** `--lang ko|en`, `--domain-mode portfolio|resume_only`, 중첩 표 `.hwpx`/텍스트박스 `.docx`/시각순 `.pptx`/`.hwp` 차단 ([extract_doc.py](../skill/resume-jd-coach/scripts/extract_doc.py))
5. **세션 경로 중립화:** `<appDataDir>/scratch/jd-coach-sessions/<company-role-slug>/` ([SKILL.md](../skill/resume-jd-coach/SKILL.md))

### v1.2 미세 다듬기 5건 + 보너스 수정 완료 (`17/17 OK`)
1. **부정/`transferable_gap` 키워드 누출 완전 차단:** Track 5 R2 `projected_expression_only`가 `77.3% → 76.4%`, 상한 `79.9% → 79.0%`로 정교화
2. **바이그램 근거 검증 강화 & `--strict-quotes` 기본화:** `verify_quote_grounding`에서 `unigram_ratio >= 0.70` + `bigram_ratio >= 0.45` 요구 및 `SKILL.md` 기본 CLI에 `--strict-quotes` 추가
3. **문서 내 자기모순 ATS 경고(`contradictory_mentions`) + 한국어 접속어 경계(`이며/이고/는데`) 보강:** Live Red-Team R2 자기모순 자동 경고, Track 5 R2 오경보 0건 확인
4. **동적 미션 제목 & 영문 무누출:** `projected_with_transferable_cap < 80%` 시 동적 제목 + 유사경험 현실 상한 병기, 영문(`--lang en`) 한글 누출 0건 검증
5. **코드 위생 + 실전 회귀 확장:** `_dec_norm()` 해시 정규화, PPTX `r:id` 명시화, Windows UTF-8 BOM(`utf-8-sig`) 호환, 멀티페이지 `.pdf` + 영문 2라운드 E2E 테스트 추가 ([test_resume_jd_coach.py](../skill/resume-jd-coach/scripts/test_resume_jd_coach.py))
