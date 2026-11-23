#!/usr/bin/env python3
"""Reproducible 3-country (US en, China zh, Japan ja) 12-track multilingual benchmark runner for resume-jd-coach v2.0.

Generates native candidate files (.docx, .pptx, .xlsx, .md, gb18030 .txt, cp932 .txt),
extracts text via extract_doc.py, locks rubrics via score_match.py --init-rubric,
runs every round with --strict-quotes, verifies zero cross-language leakage, and writes multilingual_benchmark_summary.json.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.sax.saxutils as sax
import zipfile
from pathlib import Path
from typing import Any

BENCH_DIR = Path(__file__).resolve().parent
SKILL_DIR = BENCH_DIR.parent.parent / "skill" / "resume-jd-coach"
EXTRACT_PY = SKILL_DIR / "scripts" / "extract_doc.py"
SCORE_PY = SKILL_DIR / "scripts" / "score_match.py"

sys.path.insert(0, str(BENCH_DIR))
from tracks_en import EN_TRACKS  # noqa: E402
from tracks_ja import JA_TRACKS  # noqa: E402
from tracks_zh import ZH_TRACKS  # noqa: E402


HANGUL_RE = re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]")
KANA_RE = re.compile(r"[\u3040-\u30ff]")
CJK_ANY_RE = re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff]")


def _make_docx(path: Path, paragraphs: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        f"<w:p><w:r><w:t>{sax.escape(p)}</w:t></w:r></w:p>" for p in paragraphs
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", xml)


def _make_pptx(path: Path, slides: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sld_ids = []
    rels = []
    with zipfile.ZipFile(path, "w") as zf:
        for idx, text in enumerate(slides, start=1):
            rid = f"rId{idx}"
            sld_ids.append(f'<p:sldId id="{255 + idx}" r:id="{rid}"/>')
            rels.append(
                f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{idx}.xml"/>'
            )
            sxml = (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                f"<p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>{sax.escape(text)}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>"
            )
            zf.writestr(f"ppt/slides/slide{idx}.xml", sxml)
        zf.writestr(
            "ppt/presentation.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<p:sldIdLst>{''.join(sld_ids)}</p:sldIdLst></p:presentation>",
        )
        zf.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f"{''.join(rels)}</Relationships>",
        )


def _make_xlsx(path: Path, sheets: list[tuple[str, list[list[str]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    shared: list[str] = []
    shared_idx: dict[str, int] = {}

    def get_si(val: str) -> int:
        if val not in shared_idx:
            shared_idx[val] = len(shared)
            shared.append(val)
        return shared_idx[val]

    sheet_entries = []
    rel_entries = []
    with zipfile.ZipFile(path, "w") as zf:
        for idx, (sname, rows) in enumerate(sheets, start=1):
            rid = f"rId{idx}"
            sheet_entries.append(f'<sheet name="{sax.escape(sname)}" sheetId="{idx}" r:id="{rid}"/>')
            rel_entries.append(
                f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
            )
            row_xml = []
            for r_i, row in enumerate(rows, start=1):
                cells = []
                for c_i, val in enumerate(row):
                    col = chr(ord("A") + c_i)
                    si = get_si(val)
                    cells.append(f'<c r="{col}{r_i}" t="s"><v>{si}</v></c>')
                row_xml.append(f'<row r="{r_i}">{"".join(cells)}</row>')
            zf.writestr(
                f"xl/worksheets/sheet{idx}.xml",
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                f"<sheetData>{''.join(row_xml)}</sheetData></worksheet>",
            )
        si_xml = "".join(f"<si><t>{sax.escape(s)}</t></si>" for s in shared)
        zf.writestr(
            "xl/sharedStrings.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f"{si_xml}</sst>",
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<sheets>{''.join(sheet_entries)}</sheets></workbook>",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f"{''.join(rel_entries)}</Relationships>",
        )


def _materialize_candidate_doc(raw_dir: Path, doc_spec: dict[str, Any]) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    fpath = raw_dir / doc_spec["filename"]
    dtype = doc_spec["type"]
    if dtype == "docx":
        _make_docx(fpath, doc_spec["paragraphs"])
    elif dtype == "pptx":
        _make_pptx(fpath, doc_spec["slides"])
    elif dtype == "xlsx":
        _make_xlsx(fpath, doc_spec["sheets"])
    elif dtype == "txt_gb18030":
        fpath.write_bytes(doc_spec["content"].encode("gb18030"))
    elif dtype == "txt_cp932":
        fpath.write_bytes(doc_spec["content"].encode("cp932"))
    elif dtype == "md":
        fpath.write_text(doc_spec["content"], encoding="utf-8")
    else:
        raise ValueError(f"Unsupported doc type: {dtype}")
    return fpath


def _check_language_leakage(lang: str, report_md: str) -> list[str]:
    issues: list[str] = []
    if lang == "en":
        if CJK_ANY_RE.search(report_md):
            issues.append("CJK/Hangul leaked into English report")
    elif lang == "zh":
        if HANGUL_RE.search(report_md):
            issues.append("Hangul leaked into Chinese report")
        if KANA_RE.search(report_md):
            issues.append("Japanese Kana leaked into Chinese report")
    elif lang == "ja":
        if HANGUL_RE.search(report_md):
            issues.append("Hangul leaked into Japanese report")
    return issues


def run_all() -> dict[str, Any]:
    all_tracks = EN_TRACKS + ZH_TRACKS + JA_TRACKS
    tracks_root = BENCH_DIR / "tracks"
    summary_tracks: list[dict[str, Any]] = []

    for track in all_tracks:
        tdir = tracks_root / track["slug"]
        tdir.mkdir(parents=True, exist_ok=True)
        (tdir / "jd.txt").write_text(track["jd_text"].strip() + "\n", encoding="utf-8")

        rubric_path = tdir / "rubric.json"
        rubric_copy = json.loads(json.dumps(track["rubric"]))
        rubric_path.write_text(json.dumps(rubric_copy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        init_proc = subprocess.run(
            [sys.executable, "-B", str(SCORE_PY), "--init-rubric", str(rubric_path)],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        init_res = json.loads(init_proc.stdout)

        history_path = tdir / "history.json"
        if history_path.exists():
            history_path.unlink()

        round_summaries: list[dict[str, Any]] = []
        for rspec in track["rounds"]:
            rnum = rspec["round"]
            raw_path = _materialize_candidate_doc(tdir / "raw_inputs", rspec["candidate_doc"])
            cand_txt = tdir / "rounds" / f"round_{rnum:02d}_candidate.txt"
            eval_json = tdir / "rounds" / f"round_{rnum:02d}_eval.json"
            report_md = tdir / "reports" / f"round_{rnum:02d}_report.md"

            subprocess.run(
                [sys.executable, "-B", str(EXTRACT_PY), "--inputs", str(raw_path), "--out", str(cand_txt)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )

            eval_json.parent.mkdir(parents=True, exist_ok=True)
            eval_json.write_text(json.dumps(rspec["eval"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            score_proc = subprocess.run(
                [
                    sys.executable, "-B", str(SCORE_PY),
                    "--rubric", str(rubric_path),
                    "--eval", str(eval_json),
                    "--candidate-text", str(cand_txt),
                    "--history", str(history_path),
                    "--report-out", str(report_md),
                    "--strict-quotes",
                ],
                capture_output=True, text=True, encoding="utf-8",
            )
            if score_proc.returncode != 0:
                raise RuntimeError(
                    f"Track {track['slug']} Round {rnum} FAILED:\nSTDOUT: {score_proc.stdout}\nSTDERR: {score_proc.stderr}"
                )
            res = json.loads(score_proc.stdout)
            md_text = report_md.read_text(encoding="utf-8")
            leakage = _check_language_leakage(track["language"], md_text)
            if leakage:
                raise RuntimeError(f"Language leakage in {track['slug']} R{rnum}: {leakage}")

            round_summaries.append(
                {
                    "round": rnum,
                    "input_file": raw_path.name,
                    "total_score": res["total_score"],
                    "pass_status": res["pass_status"],
                    "delta_score_pp": res["round_diff"]["delta_score_pp"],
                    "must_have_pct": res["must_have_attainment_pct"],
                    "ats_coverage_pct": res["ats_keywords"]["coverage_pct"],
                    "negated_mentions": [k["term"] for k in res["ats_keywords"]["negated_mentions"]],
                    "contradictory_mentions": [k["term"] for k in res["ats_keywords"]["contradictory_mentions"]],
                    "knockout_risks": [k["id"] for k in res["knockout_risks"]],
                    "regressed_items": [k["id"] for k in res["round_diff"]["regressed_items"]],
                    "projected_expression_only": res["projected_expression_only_score"],
                    "projected_with_transferable_cap": res["projected_with_transferable_cap"],
                    "grace_should_offer": res["grace_recommendation"]["should_offer"],
                    "grace_suggested_tier": res["grace_recommendation"]["suggested_tier"],
                    "honest_fit_advisory": res["grace_recommendation"]["honest_fit_advisory"],
                    "unverified_quotes": len(res["unverified_quotes"]),
                    "language_leakage": leakage,
                }
            )

        summary_tracks.append(
            {
                "slug": track["slug"],
                "country": track["country"],
                "language": track["language"],
                "family": track["family"],
                "company": track["company"],
                "role": track["role"],
                "jd_url": track["jd_url"],
                "location": track["location"],
                "format": track["format"],
                "scenario": track["scenario"],
                "rubric_hash": init_res["rubric_hash"],
                "rubric_warnings": init_res["warnings"],
                "rounds": round_summaries,
            }
        )

    total_rounds = sum(len(t["rounds"]) for t in summary_tracks)
    summary = {
        "benchmark_version": "v2.1-multilingual",
        "languages": ["en", "zh", "ja"],
        "total_tracks": len(summary_tracks),
        "total_rounds": total_rounds,
        "strict_quotes_passed": sum(
            1 for t in summary_tracks for r in t["rounds"] if r["unverified_quotes"] == 0
        ),
        "zero_language_leakage_passed": sum(
            1 for t in summary_tracks for r in t["rounds"] if not r["language_leakage"]
        ),
        "tracks": summary_tracks,
    }
    out_path = BENCH_DIR / "multilingual_benchmark_summary.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    summary = run_all()
    print(
        f"MULTILINGUAL BENCHMARK COMPLETE: {summary['total_tracks']} tracks | "
        f"{summary['total_rounds']} rounds | strict_quotes={summary['strict_quotes_passed']}/{summary['total_rounds']} | "
        f"zero_leakage={summary['zero_language_leakage_passed']}/{summary['total_rounds']}"
    )
    for t in summary["tracks"]:
        traj = " -> ".join(f"R{r['round']}:{r['total_score']}%({r['pass_status']})" for r in t["rounds"])
        print(f"  [{t['country']}/{t['language']}] {t['slug']} ({t['format']}): {traj}")
