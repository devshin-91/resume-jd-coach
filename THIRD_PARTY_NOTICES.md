# Third-Party Notices & Attributions

This repository (`resume-jd-coach`) uses **zero bundled third-party Python packages**
and relies solely on the Python Standard Library at runtime. The following
third-party specifications, optional external libraries (if separately installed
by the user), and benchmark reference materials are acknowledged below.

---

## 1. Runtime Environment & Standard Library

### Python Standard Library (`json`, `decimal`, `hashlib`, `re`, `unicodedata`, `zipfile`, `xml.etree.ElementTree`, `html.parser`, `unittest`, `argparse`, `pathlib`, `subprocess`, built-in codecs `utf-8`/`gb2312`/`gb18030`/`cp932`/`cp949`/`iso2022_kr`/`cp1252`)
- **Provider:** Python Software Foundation (PSF)
- **License:** Python Software Foundation License Version 2 (PSF-2.0)
- **URL:** https://docs.python.org/3/license.html
- **Usage:** Core deterministic multilingual scoring engine (`score_match.py`), document XML/HTML/encoding extraction (`extract_doc.py`), and automated 33-test suite (`test_resume_jd_coach.py`). Not redistributed in this repository.

---

## 2. Optional External PDF Integrations (Not Bundled)

`skill/resume-jd-coach/scripts/extract_doc.py` performs optional dynamic imports
(`try: import pypdf` / `try: import fitz`) ONLY when a user passes a `.pdf` file
and has separately installed one of those libraries in their local environment.
Neither library is bundled, vendored, or required by this repository.

1. **pypdf** (Optional, not bundled)
   - **License:** BSD 3-Clause License
   - **URL:** https://github.com/py-pdf/pypdf
2. **PyMuPDF (`fitz`)** (Optional, not bundled)
   - **License:** GNU AGPL-3.0 (or Artifex Commercial License)
   - **URL:** https://github.com/pymupdf/PyMuPDF
   - **Note:** If you install PyMuPDF separately, your usage of PyMuPDF is subject to Artifex's AGPL-3.0 / commercial licensing terms. Users wishing to avoid AGPL dependencies should use `pypdf` (BSD-3-Clause) or Antigravity's built-in `read_file` PDF reader.

---

## 3. Agent Skill Specification & Standards

### Google Antigravity Agent Skill Format (`SKILL.md`)
- **Provider:** Google / Antigravity Platform
- **URL:** https://antigravity.google/docs/skills
- **Usage:** Directory structure (`SKILL.md`, `references/`, `scripts/`, `examples/`) and YAML frontmatter conventions for progressive disclosure.

### Document XML Schemas (Parsed via Python Standard Library)
- **OOXML (`.docx`, `.xlsx`, `.pptx`):** ECMA-376 / ISO/IEC 29500 standard XML structures (`word/document.xml`, `xl/workbook.xml`, `xl/sharedStrings.xml`, `xl/worksheets/sheet*.xml`, `ppt/presentation.xml`, `ppt/slides/slide*.xml`).
- **OWPML (`.hwpx`):** Korean Hangul Document XML standard KS X 6101 (`Contents/section*.xml`).

---

## 4. Benchmark Reference Job Postings (Non-Commercial Evaluation)

### A. Korean 6-Job-Family Tracks (`benchmark/tracks/*/jd.txt`)
Condensed non-commercial reference summaries of 6 publicly visible job postings collected on 2026-11-22 from **Wanted (`wanted.co.kr`)**:

| Benchmark Track | Company | Role Title | Reference URL |
| :--- | :--- | :--- | :--- |
| Track 1 (Dev) | 패스트파이브 (FASTFIVE) | Backend Engineer | https://www.wanted.co.kr/wd/392517 |
| Track 2 (PM) | 데이터라이즈 (Datarize) | Product Manager (Junior) | https://www.wanted.co.kr/wd/395258 |
| Track 3 (Design) | 라프텔 (Laftel) | 프로덕트 디자이너 (3년 이상) | https://www.wanted.co.kr/wd/394377 |
| Track 4 (Marketing) | 크림 (KREAM) | 플랫폼 브랜드 마케터 | https://www.wanted.co.kr/wd/393109 |
| Track 5 (Data) | 한국신용데이터 (KCD) | [데이터분석팀] Data Analyst | https://www.wanted.co.kr/wd/394519 |
| Track 6 (HR) | 여기어때컴퍼니 (GC Company) | HR Manager (신입) | https://www.wanted.co.kr/wd/396190 |

### B. Multilingual 3-Country 12-Track Expansion (`benchmark/multilingual/tracks/*/jd.txt`)
Condensed non-commercial reference summaries of 12 publicly visible job postings collected on 2026-11-23 from open company career portals across the **United States (`en`)**, **China (`zh`)**, and **Japan (`ja`)**:

| Country / Lang | Benchmark Track | Company | Role Title | Reference URL |
| :--- | :--- | :--- | :--- | :--- |
| US (`en`) | `track_en01_dev_ramp` | Ramp | Software Engineer, Backend, Comms Platform | https://jobs.ashbyhq.com/ramp/939892e5-5273-4bfc-8c41-a6c51cabb228 |
| US (`en`) | `track_en02_design_figma` | Figma | Product Designer, Core Experience | https://job-boards.greenhouse.io/figma/jobs/6231027004?gh_jid=6231027004 |
| US (`en`) | `track_en03_data_discord` | Discord | Staff Data Scientist, Causal Inference & Experimentation | https://job-boards.greenhouse.io/discord/jobs/8652853002 |
| US (`en`) | `track_en04_nonit_datadog` | Datadog | Director, People Business Partner | https://careers.datadoghq.com/detail/8346056/?gh_jid=8346056 |
| China (`zh`) | `track_zh01_dev_tencent` | 腾讯 (Tencent) | 营销与交易产品部-云mallJava后端开发工程师 | https://careers.tencent.com/jobdesc.html?postId=2089960263330742272 |
| China (`zh`) | `track_zh02_design_bytedance` | 字节跳动 (ByteDance) | 高级用户体验设计师-财经 | https://jobs.bytedance.com/experienced/position/7675656615622428933/detail |
| China (`zh`) | `track_zh03_pm_mihoyo` | 米哈游 (miHoYo) | 增长产品经理（AI方向） | https://jobs.mihoyo.com/#/position/8574 |
| China (`zh`) | `track_zh04_nonit_bilibili` | 哔哩哔哩 (Bilibili) | 内容安全业务HRBP | https://jobs.bilibili.com/social/positions/28324 |
| Japan (`ja`) | `track_ja01_dev_smarthr` | 株式会社SmartHR | 【情シス領域】シニアウェブアプリケーションエンジニア | https://open.talentio.com/r/1/c/smarthr/pages/127964 |
| Japan (`ja`) | `track_ja02_design_smarthr` | 株式会社SmartHR | プロダクトデザイナー（マネージャー候補） | https://open.talentio.com/r/1/c/smarthr/pages/129618 |
| Japan (`ja`) | `track_ja03_pm_mercari` | 株式会社メルカリ (Mercari) | Product Manager - Mercari Marketplace | https://careers.mercari.com/ |
| Japan (`ja`) | `track_ja04_nonit_freee` | フリー株式会社 (freee) | 経理（連結・税務・M&A/PMI） | https://hire.wantedly.com/careers/freee/career_page_all_jobs/4793 |

- **Ownership & Scope:** All company names, trademarks, brand names, and original job posting texts remain the sole property of their respective owners and career platforms.
- **Non-Commercial Benchmark & Zero-PII Notice:** Included strictly for non-commercial skill evaluation and reproducibility. All candidate resumes and portfolios across `benchmark/` (`김도현`, `박서연`, `이지우`, `최유진`, `정민호`, `한지민`, `김태우`, `Jordan Lee`, `Maya Chen`, `Taylor Brooks`, `Morgan Patel`, `Jordan Taylor`, `林浩`, `苏莹`, `周然`, `陈默`, `赵明`, `高橋 誠`, `佐藤 遥`, `鈴木 涼`, `中村 彩花`, `田中 優衣`) are 100% synthetic fictional personas containing zero real personal data.
