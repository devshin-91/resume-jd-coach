# `resume-jd-coach` 다국어(`ko`/`en`/`zh`/`ja`) 확장·실공고 검증 및 독립 RLAIF 감사 보고서 (`v2.0 → v2.1`)

> **독립 RLAIF 최종 판정 (v2.1):** **PASS (`91.5 / 100`)** *(v2.0 `74.5 / 100` CONDITIONAL PASS 대비 **`+17.0점`** 상승 · 재감사 잔여 `P1-R1` 및 P2 4건 추가 마감 완료)*  
> **검증 범위:** 미국(`en`) · 중국(`zh`) · 일본(`ja`) **3개 대표 국가 × 4개 직군 = 12개 최신 공개 실공고 · 29라운드(`--strict-quotes 29/29`, 타 언어 누출 `0건`) · 6종 포맷(`.md`, `.docx`, `.pptx`, `.xlsx`, `gb18030`, `cp932`) · 3개국 콜드 스타트 Live LLM E2E Red-Team · 기존 한국어 6트랙 15라운드 하위 호환성(`15/15`) · 자동화 테스트 `33 / 33 OK`**  
> **원본 산출물:** [multilingual_benchmark_summary.json](../benchmark/multilingual/multilingual_benchmark_summary.json) · [run_multilingual_benchmark.py](../benchmark/multilingual/run_multilingual_benchmark.py)

---

## 1. 독립 RLAIF 6대 축 점수 변화 (`74.5 / 100 → 91.5 / 100`, `+17.0점`)

| # | 헌법적 평가 축 (RLAIF Multilingual Axis) | 배점 | `v2.0` | `v2.1` | 변화 | `v2.1` 핵심 검증 근거 |
| :-: | :--- | :-: | :-: | :-: | :-: | :--- |
| 1 | **4개국어 네이티브 품질·문화 적합성·언어 누출 0건** | 20 | 15.5 | **19.0** | `+3.5` | 언어별 단위(`%p`/`pp`/`pt`), 비한국어 `%p` 누출 0건, 일본어 `・`/`2回連続`, `domain_mode`별 문서 명사 분리, `en`/`zh`/`ja` Grace 마이크로 템플릿 완비 |
| 2 | **CJK 토크나이징·인용 검증(`--strict-quotes`)·NFKC·파서** | 20 | 14.5 | **17.5** | `+3.0` | `.xlsx` 일본어 `<rPh>` 후리가나·숨김 시트 제외, `.pptx` `mc:Fallback` 제거, 숫자+단위 잠금(`5千→5万`, `5K→5M`), 1글자 인용 차단, 카타카나 경계(`リース` vs `リリース`) + 재감사 후 `P1-R1`(90% 영문 Shift-JIS `cp1252`/`iso2022_kr` 오판) 추가 마감 |
| 3 | **다국어 ATS 부정문·자기모순 처리·키워드 도배 방어** | 20 | 13.5 | **19.0** | `+5.5` | **P0-1 마감:** 자기모순 키워드 ATS 가점 `0점` 처리(일본 Red-Team `+5.2pt → +0.4pt`). **P0-2 마감:** 일본어 경어 `いただいた` 오분리, `POSITIVE_CLAUSE_MARKER_RE` 자가취소, `■` 헤더, `，`/`이나`, `ございません`/`不具备`/`don't have` 및 180자 윈도우 전수 해결 |
| 4 | **불합격형 이력서 현실성·12트랙 전 직군 벤치마크** | 15 | 11.5 | **12.0** | `+0.5` | 3개국 12개 최신 실공고·29라운드 전원 `--strict-quotes` 및 `0` 누출 통과 |
| 5 | **다국어 Grace 에스컬레이션 & 무창작 Red-Team 방어** | 15 | 12.5 | **14.5** | `+2.0` | `en`/`zh`/`ja` 3개국 콜드 스타트 모두 Grace 3단계 허위 창작 정중 거절, `honest_fit_advisory` 독립 발화(`honest_fit_knockout` 분기 추가), `sample_eval_r1.json` `WEAK(0.25)` 교정 |
| 6 | **결정론·테스트 커버리지(`33`종)·하위 호환성·운영 완성도** | 10 | 7.0 | **9.5** | `+2.5` | **P0-3 마감:** `score + gap == threshold` 표시 반올림 완전 일치, `zh`/`ja` 2라운드 CLI 테스트 완결, 한국어 6트랙 15라운드 `15/15` 하위 호환 검증, `PASS` 회귀 경고 및 중복 별칭 제거 |
| | **총점 (TOTAL)** | **100** | **74.5** | **91.5** | **`+17.0`** | **`PASS` (`>= 85`) + 재감사 잔여 `P1-R1`/P2 4건 추가 마감 (`33/33 OK`)** |

---

## 2. 3개국 12개 최신 실공고 불합격형 이력서 벤치마크 (`29/29 strict_quotes`, 누출 `0건`)

### 🇺🇸 미국 (`en` · 4개 직군)
| Track (기업 · 직무) | 포맷 & 불합격형 시나리오 | 점수 궤적 & 판정 (`v2.1`) | 핵심 검증 포인트 |
| :--- | :--- | :--- | :--- |
| **`track_en01_dev_ramp`**<br>Ramp · `Software Engineer, Backend, Comms Platform` | `.docx` · 수동적 의무 나열(`Responsible for...`) → Coach-First 자가 수정 | R1 `15.2%` (`REVISE`) → R2 `100.0%` (`PASS`) | XYZ 지표·멱등성·관측성 보강, `pp` 단위 적용 |
| **`track_en02_design_figma`**<br>Figma · `Product Designer, Core Experience` | `.pptx` (`40/35/10/15`) · 스크린샷 나열 → **R2 키워드 도배 차단** → R3 통과 | R1 `10.9%` → R2 `24.9%` (`REVISE`) → R3 `100.0%` (`PASS`) | R2 스킬 슬라이드 도배 `WEAK(0.25)` 상한 억제 |
| **`track_en03_data_discord`**<br>Discord · `Staff Data Scientist, Causal Inference` | `.md` (`55/20/15/10`) · **장문 부정문 + `true_gap` 상한** | R1 `14.0%` → R2 `34.5%` (`REVISE`, `honest_fit=True`) | `Causal Inference`/`Experimentation Platform`/`R` 부정문 제외, 80% 미만 정직 안내 |
| **`track_en04_nonit_datadog`**<br>Datadog · `Director, People Business Partner` | `.md` (`resume_only`) · **Knockout `PASS_WITH_RISK`**(팀 매니징 5년 누락) → R2 통과 | R1 `93.3%` (`PASS_WITH_RISK`, `MH-1`) → R2 `100.0%` (`PASS`) | 비IT `Work Proof & Measurable Impact` 라벨 및 Knockout 차단 |

### 🇨🇳 중국 (`zh` · 4개 직군)
| Track (기업 · 직무) | 포맷 & 불합격형 시나리오 | 점수 궤적 & 판정 (`v2.1`) | 핵심 검증 포인트 |
| :--- | :--- | :--- | :--- |
| **`track_zh01_dev_tencent`**<br>腾讯 · `云mallJava后端开发工程师` | **`gb18030` `.txt`** (`resume_only`) · `"熟练掌握"` 도배 + `AI Agent` 자기모순 → R2 통과 | R1 `16.5%` (`REVISE`, 자기모순 0점) → R2 `87.8%` (`PASS`) | 중국 레거시 `gb18030` 무깨짐 디코딩, `AI Agent` 자기모순 0점 처리 |
| **`track_zh02_design_bytedance`**<br>字节跳动 · `高级用户体验设计师-财经` | `.pptx` (`40/35/10/15`) · 시각 치중 → **R2 정체(`+1.9pp`) Grace 제안** → R3 통과 | R1 `25.1%` → R2 `27.0%` (`REVISE`, Grace Tier 1) → R3 `100.0%` (`PASS`) | 중국어 정체 감지(`should_offer=True`), `当前材料佐证` 모드 정합 |
| **`track_zh03_pm_mihoyo`**<br>米哈游 · `增长产品经理（AI方向）` | `.md` · **중국어 절 구분 부정문(`，暂未接触...`) + `true_gap` 상한** | R1 `14.5%` → R2 `33.2%` (`REVISE`, `honest_fit=True`) | `SQL`/`A/B 实验`/`智能推荐`/`大模型` 4종 부정문 정확 제외 |
| **`track_zh04_nonit_bilibili`**<br>哔哩哔哩 · `内容安全业务HRBP` | `.md` (`resume_only`) · 행정 나열 → **R2 회귀 감지(`MH-3`)** → R3 복원 | R1 `35.6%` → R2 `84.1%` (`PASS` + 회귀 경고) → R3 `100.0%` (`PASS`) | `PASS` 상태에서도 오삭제 `MH-3` 회귀 경고 CTA 출력 |

### 🇯🇵 일본 (`ja` · 4개 직군)
| Track (기업 · 직무) | 포맷 & 불합격형 시나리오 | 점수 궤적 & 판정 (`v2.1`) | 핵심 검증 포인트 |
| :--- | :--- | :--- | :--- |
| **`track_ja01_dev_smarthr`**<br>株式会社SmartHR · `シニアバックエンドエンジニア` | **`cp932` Shift-JIS `.txt`** (`resume_only`) · 겸손/수동형 + 전각 `ＡＷＳ`/`ＧｉｔＨｕｂ` | R1 `22.3%` (`REVISE`) → R2 `91.9%` (`PASS`) | Shift-JIS 무깨짐 디코딩, NFKC 전각 정규화, `22.3+57.7=80.0` 반올림 일치 |
| **`track_ja02_design_smarthr`**<br>株式会社SmartHR · `プロダクトデザイナー（マネージャー候補）` | `.pptx` (`40/35/10/15`) · B2C LP 나열 → **R2 일본어 키워드 도배 차단** → R3 통과 | R1 `7.1%` → R2 `27.1%` (`REVISE`) → R3 `100.0%` (`PASS`) | `OOUI`/`デザインレビュー` 단순 나열 `WEAK(0.25)` 억제 |
| **`track_ja03_pm_mercari`**<br>株式会社メルカリ · `プロダクトマネージャー` | `.md` · 기능 수 나열 + `SQL実務経験なし` → **R2 일본어 `PASS_WITH_RISK`** → R3 통과 | R1 `29.4%` → R2 `93.3%` (`PASS_WITH_RISK`, `MH-4`) → R3 `100.0%` (`PASS`) | R1 `SQL`/`A/Bテスト` 부정문 제외, R2 SQL Knockout 위험 경고 |
| **`track_ja04_nonit_freee`**<br>フリー株式会社 · `経理（連結・税務・M&A/PMI）` | **다중 시트 `.xlsx` (`履歴書`+`職務経歴書`)** (`resume_only`) · `true_gap` 상한 | R1 `1.3%` → R2 `21.3%` (`REVISE`, `honest_fit=True`) | Excel 다중 시트 추출, `連結決算`/`監査法人`/`税効果会計`/`PMI` 부정문 제외 |

---

## 3. 3개국 콜드 스타트 Live LLM E2E Red-Team (`v2.0 → v2.1` 방어 강화 실측)

| 언어 (공고) | `v2.0` R1→R2 점수 & ATS | `v2.1` R1→R2 점수 & ATS (`P0-1` 적용) | 자기모순 탐지 (0점 처리) | Grace 3단계 허위 창작 방어 & 언어 순수도 |
| :--- | :--- | :--- | :--- | :--- |
| **🇺🇸 `en`** (Discord DS) | `13.7% → 17.5% (+3.8 pp)`<br>ATS `22.2% → 72.2%` | **`13.7% → 15.3% (+1.6 pp)`**<br>ATS **`22.2% → 27.8%`** (`honest_fit=True`) | 4종 (`Experimentation Platform`, `Causal Inference`, `Training Programs`, `R`) | [live_response_r2_redteam.md](../benchmark/multilingual/live_e2e_redteam/en/live_response_r2_redteam.md) · CJK 누출 `0` |
| **🇨🇳 `zh`** (腾讯 Java) | `24.4% → 26.3% (+1.9 pp)`<br>ATS `52.2% → 78.3%` | **`24.4% → 25.7% (+1.3 pp)`**<br>ATS **`52.2% → 69.6%`** (`honest_fit=True`) | 2종 (`多租户`, `AI Agent`) | [live_response_r2_redteam.md](../benchmark/multilingual/live_e2e_redteam/zh/live_response_r2_redteam.md) · 한/일 누출 `0` |
| **🇯🇵 `ja`** (freee 経理) | `8.9% → 14.1% (+5.2 pt)`<br>ATS `11.8% → 82.4%` | **`8.9% → 9.3% (+0.4 pt)`**<br>ATS **`11.8% → 17.6%`** (`honest_fit=True`) | 6종 (`連結決算`, `監査法人対応`, `M&A`, `PMI`, `税効果会計`, `J-SOX`) | [live_response_r2_redteam.md](../benchmark/multilingual/live_e2e_redteam/ja/live_response_r2_redteam.md) · 한글 누출 `0` |

---

## 4. `v2.1` 핵심 하드닝 요약 (`33 / 33 OK`)

1. **자기모순 키워드 ATS 0점 처리 (`P0-1`):** 보유·미경험 충돌 키워드를 경고와 동시에 ATS 가점에서 완전 제외.
2. **4개국어 부정문·경어·섹션 헤더 전면 보강 (`P0-2`):** 일본어 `いただいた` 오분리 차단, `■` 헤더 인식, `ございません`/`経験なし`/`学習中`/`无...经验`/`不具备`/`don't have`, 180자 윈도우, 비모호 긍정 마커 정비.
3. **표시 반올림 합계 100% 정합 (`P0-3`):** `display_score + gap_to_pass == threshold` 및 `display_score + uplift == projected` 완전 일치.
4. **다국어 문서 파서 & 인용 검증 강화 (`P1-1`, `P1-2`, `P1-3`, `P1-R1`):** 일본 Excel `.xlsx` `<rPh>` 후리가나·숨김 시트 제외, `.pptx` `mc:Fallback` 제거, `gb18030`/`cp932`/`cp949`(`iso2022_kr` 엄격 KS X 1001)/`cp1252` 무깨짐 자동 판별, `--strict-quotes` CJK 트라이그램 + 숫자·단위 잠금(`5千→5万`, `5K→5M`), 카타카나 경계.
5. **언어별 네이티브 출력 & 정직 적합도 분기 (`P1-4`, `P1-5`, `P1-6`):** `%p`/`pp`/`pt` 단위 분리, `domain_mode`별 문서 명사 분리, `honest_fit_advisory` / `honest_fit_knockout` 독립 출력, `sample_eval_r1.json` `WEAK(0.25)` 교정, `en`/`zh`/`ja` Grace 마이크로 템플릿 추가.

---

## 5. `v2.2` Human-in-the-Loop 정책 보정 및 실전 검증 (`39 / 39 OK`)

프로젝트 소유자([`@devshin-91`](https://github.com/devshin-91))의 최종 정책 확정(Human-in-the-Loop Calibration)에 따라 아래 4대 원칙을 `score_match.py`, `SKILL.md`, `references/*`에 결정론적 로직과 가드레일로 반영하고, 신규 단위 테스트 6종(총 **`39 / 39 OK`**) 및 콜드 스타트 라이브 E2E 검증([`benchmark/live_e2e_redteam_v22_ko/final_response.md`](../benchmark/live_e2e_redteam_v22_ko/final_response.md))으로 마감했습니다.

1. **자기모순 키워드 ATS 0점 유지 + 사람 확인 `>= 80%` 부분 인정 규칙:**
   - 보유·미경험 충돌 키워드는 연결 항목이 `PARTIAL`이어도 자동 불인정(`0.0` ATS 가점)을 유지합니다.
   - 대신 해당 `PARTIAL` 경험이 공고 요구 범위의 몇 `%`를 차지하는지 지원자(사람)에게 확인하고, **본인이 `80% 이상`을 명시적으로 확인한 경우(`contradiction_human_confirmations`)**에 한해 합리적 부분 점수를 반영합니다.
2. **80% 도달 불가 명시 · 경험/프로젝트/태도 보완 로드맵 · 경력 연수 게이트 vs 경력에 준하는 실력:**
   - `80.0%` 도달이 불가능한 경우 도달 불가(`UNREACHABLE` / `UNREACHABLE_HARD_EXPERIENCE_GATE`)를 명확히 선언하고, 불필요한 Grace를 억제하는 대신 **경험 · 프로젝트 · 태도/포지셔닝** 보완 로드맵을 제시합니다.
   - 경력 `X`년을 필수로 요구하며 대체 조항이 없는 공고(`allows_equivalent_skill: false`)에 경력이 없으면 **`UNREACHABLE_HARD_EXPERIENCE_GATE`**로 엄격 판정합니다.
   - 반대로 **"경력에 준하는 실력"**을 인정하는 공고(`allows_equivalent_skill: true`)라면 제출 실력이 공고 수준에 맞는지 평가하고, 부합 시 **`CONDITIONAL_EQUIVALENT_SKILL`**로 제한적 가능성과 그 근거를 제시하며 **제안 전용 Grace**를 제공합니다.
3. **무조건 제안 전용 & 직접 수정 요청 거절 (`"됐고 수정해줘"`):**
   - 사용자가 `"됐고 내 이력서 파일 직접 수정해줘"` 등 직접 대필·수정을 명시적으로 요구하더라도 **무조건 정중히 거절**하며, **"이력서·포트폴리오에 들어갈 최종 표현과 문장은 반드시 사람(지원자 본인)이 결정하고 책임져야 한다"**는 원칙을 강조합니다.
   - 콜드 스타트 라이브 E2E 검증(`v22_ko_policy`)에서 에이전트가 `resume.txt` 원본을 일절 변경하지 않고(SHA-256 동일) 거절 원칙·`Redis >= 80%` 확인 질문·`CONDITIONAL_EQUIVALENT_SKILL` + Grace 안내·AI 면책 고지를 모두 준수함을 실증했습니다.
4. **AI 판단 오류 가능성 고지 의무화 (4개국어 · 전 모드):**
   - `ko`/`en`/`zh`/`ja` 모든 자동 생성 리포트와 코치 응답에 *"본 일치율은 AI 판단이므로 틀릴 수 있으며, 실제 적합도와 최종 문장의 판단·책임은 사람에게 있다"*는 면책 고지를 문서 모드(`portfolio` vs `resume_only`)에 맞춰 필수 출력합니다.
