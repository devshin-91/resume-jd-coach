# Third-Party Notices & Attributions

This repository (`resume-jd-coach`) uses **zero bundled third-party Python packages**
and relies solely on the Python Standard Library at runtime. The following
third-party specifications, optional external libraries (if separately installed
by the user), and benchmark reference materials are acknowledged below.

---

## 1. Runtime Environment & Standard Library

### Python Standard Library (`json`, `decimal`, `hashlib`, `re`, `zipfile`, `xml.etree.ElementTree`, `html.parser`, `unittest`, `argparse`, `pathlib`, `subprocess`)
- **Provider:** Python Software Foundation (PSF)
- **License:** Python Software Foundation License Version 2 (PSF-2.0)
- **URL:** https://docs.python.org/3/license.html
- **Usage:** Core deterministic scoring engine (`score_match.py`), document XML/HTML extraction (`extract_doc.py`), and automated test suite (`test_resume_jd_coach.py`). Not redistributed in this repository.

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
- **OOXML (`.docx`, `.pptx`):** ECMA-376 / ISO/IEC 29500 standard XML structures (`word/document.xml`, `ppt/presentation.xml`, `ppt/slides/slide*.xml`).
- **OWPML (`.hwpx`):** Korean Hangul Document XML standard KS X 6101 (`Contents/section*.xml`).

---

## 4. Benchmark Reference Job Postings (`benchmark/tracks/*/jd.txt`)

To validate cross-domain skill fidelity across 6 job families, `benchmark/tracks/`
contains condensed non-commercial reference summaries of 6 publicly visible job
postings collected on 2026-11-22 from **Wanted (`wanted.co.kr`)**:

| Benchmark Track | Company | Role Title | Reference URL |
| :--- | :--- | :--- | :--- |
| Track 1 (Dev) | 패스트파이브 (FASTFIVE) | Backend Engineer | https://www.wanted.co.kr/wd/392517 |
| Track 2 (PM) | 데이터라이즈 (Datarize) | Product Manager (Junior) | https://www.wanted.co.kr/wd/395258 |
| Track 3 (Design) | 라프텔 (Laftel) | 프로덕트 디자이너 (3년 이상) | https://www.wanted.co.kr/wd/394377 |
| Track 4 (Marketing) | 크림 (KREAM) | 플랫폼 브랜드 마케터 | https://www.wanted.co.kr/wd/393109 |
| Track 5 (Data) | 한국신용데이터 (KCD) | [데이터분석팀] Data Analyst | https://www.wanted.co.kr/wd/394519 |
| Track 6 (HR) | 여기어때컴퍼니 (GC Company) | HR Manager (신입) | https://www.wanted.co.kr/wd/396190 |

- **Ownership & Scope:** All company names, trademarks, brand names, and original
  job posting texts remain the sole property of their respective owners and Wantedlab.
- **Non-Commercial Benchmark Notice:** Included strictly for private, non-commercial
  skill evaluation and reproducibility. All candidate resumes and portfolios in
  `benchmark/` (`김도현`, `박서연`, `이지우`, `최유진`, `정민호`, `한지민`, `김태우`)
  are 100% synthetic fictional personas containing zero real personal data.
