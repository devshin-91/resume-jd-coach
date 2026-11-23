#!/usr/bin/env python3
"""Zero-dependency multilingual document text extractor for resume-jd-coach (v2.1).

Supports:
  - Plain text / Markdown / structured text: .md, .markdown, .txt, .csv, .json, .yaml, .yml, .rst
    (UTF-8/UTF-16 + CJK-safe heuristic decoding for Korean cp949, Chinese gb18030, Japanese cp932/euc-jp)
  - Microsoft Word: .docx (nested textbox/table safe, skips mc:Fallback duplicates)
  - Microsoft Excel: .xlsx (sharedStrings + inlineStr + workbook sheet order; widely used for Japanese 履歴書/職務経歴書)
  - PowerPoint portfolio decks: .pptx (exact ppt/presentation.xml slide order + _rels speaker notes)
  - Korean Hancom Hangul XML: .hwpx (nested table/paragraph safe — zero duplication/mashing)
  - HTML pages: .html, .htm
  - PDF: uses pypdf or PyMuPDF (fitz) if installed; otherwise emits PDF_NATIVE_READ_REQUIRED
    warning guiding Antigravity native read_file inspection.
  - Rejects legacy binary formats (.hwp, .doc, .xls, .ppt, .rtf, or null-byte binaries) loudly instead
    of dumping corrupted latin-1 text.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".csv", ".json", ".yaml", ".yml", ".rst"}
HTML_EXTENSIONS = {".html", ".htm"}
UNSUPPORTED_BINARY_EXTENSIONS = {".hwp", ".doc", ".xls", ".ppt", ".rtf"}


class UnsupportedBinaryFormatError(ValueError):
    """Raised when a legacy binary document cannot be cleanly decoded as plain text."""


class _HTMLTextExtractor(html.parser.HTMLParser):
    BLOCK_TAGS = {
        "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
        "section", "article", "header", "footer", "blockquote", "pre", "dt", "dd",
    }
    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        if t in self.SKIP_TAGS:
            self._skip_depth += 1
        elif self._skip_depth == 0 and t in self.BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        elif self._skip_depth == 0 and t in self.BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and data:
            self._chunks.append(data)

    def get_text(self) -> str:
        raw = "".join(self._chunks)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
        collapsed: list[str] = []
        prev_blank = False
        for line in lines:
            if not line:
                if not prev_blank and collapsed:
                    collapsed.append("")
                prev_blank = True
            else:
                collapsed.append(line)
                prev_blank = False
        return "\n".join(collapsed).strip()


def _natural_key(name: str) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", name)]


def _local_tag(elem: ET.Element) -> str:
    return elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag


def _score_decoded_cjk_text(text: str, enc: str) -> float:
    """Heuristic scorer to disambiguate non-UTF-8 legacy CJK encodings (cp949 vs gb18030 vs cp932/euc-jp).

    Uses built-in stdlib codecs (gb2312 for common Simplified Chinese, euc-kr for common KS X 1001 Korean,
    and Hiragana/Katakana + Japanese punctuation for cp932/euc-jp) to separate authentic prose from
    cross-codepage mojibake (which overwhelmingly lands in rare GBK/UHC extension blocks).
    """
    if not text:
        return -1e9
    total = len(text)
    hangul_common = 0
    hangul_rare = 0
    hiragana = 0
    katakana = 0
    hanzi_gb2312 = 0
    hanzi_non_gb2312 = 0
    cjk_punct = 0
    fullwidth_alnum = 0
    ascii_ok = 0
    suspicious = 0

    for ch in text:
        cp = ord(ch)
        if 0xAC00 <= cp <= 0xD7AF:
            try:
                ch.encode("iso2022_kr")
                hangul_common += 1
            except UnicodeEncodeError:
                hangul_rare += 1
        elif 0x3041 <= cp <= 0x3096:
            hiragana += 1
        elif (0x30A1 <= cp <= 0x30FA) or cp == 0x30FC:
            katakana += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            try:
                ch.encode("gb2312")
                hanzi_gb2312 += 1
            except UnicodeEncodeError:
                hanzi_non_gb2312 += 1
        elif ch in "。、，；：！？（）「」『』【】・ー〜―■●":
            cjk_punct += 1
        elif (0xFF10 <= cp <= 0xFF19) or (0xFF21 <= cp <= 0xFF3A) or (0xFF41 <= cp <= 0xFF5A):
            fullwidth_alnum += 1
        elif ch in "\r\n\t" or (0x20 <= cp <= 0x7E):
            ascii_ok += 1
        elif (0xE000 <= cp <= 0xF8FF) or cp == 0xFFFD or (0x00 <= cp < 0x20) or (0xFF61 <= cp <= 0xFF9F):
            suspicious += 1
        elif (0x2500 <= cp <= 0x25FF) or (0x0400 <= cp <= 0x04FF) or (0x0370 <= cp <= 0x03FF):
            suspicious += 1
        else:
            suspicious += 0.5

    kana = hiragana + katakana
    hanzi = hanzi_gb2312 + hanzi_non_gb2312
    hangul = hangul_common + hangul_rare
    non_ascii = max(1, total - ascii_ok)
    score = (ascii_ok * 0.5) + (cjk_punct * 3.0) + (fullwidth_alnum * 2.5) - (suspicious * 12.0)

    if enc in ("cp932", "euc-jp"):
        # Authentic Japanese prose nearly always contains Hiragana/Katakana + Kanji (never Hangul)
        score += (hiragana * 5.5) + (katakana * 4.5) + (hanzi * 2.5) - (hangul * 15.0)
        if hiragana >= 3 and hanzi >= 2:
            score += non_ascii * 2.5
    elif enc == "gb18030":
        # Authentic Simplified Chinese uses overwhelmingly GB2312 common Hanzi; Shift-JIS mojibake lands in rare GBK Hanzi!
        score += (hanzi_gb2312 * 3.8) - (hanzi_non_gb2312 * 8.0) - (hangul * 15.0) - (kana * 8.0)
        if hanzi > 0 and (hanzi_gb2312 / hanzi) >= 0.85 and kana == 0 and hangul == 0:
            score += non_ascii * 2.0
    elif enc in ("cp949", "euc-kr"):
        # Authentic Korean uses common KS X 1001 Hangul syllables; mojibake produces rare UHC syllables
        score += (hangul_common * 4.0) - (hangul_rare * 8.0) + (hanzi_gb2312 * 0.5) - (hanzi_non_gb2312 * 4.0) - (kana * 8.0)
        if hangul_common / non_ascii >= 0.55 and hangul_rare <= max(2, hangul_common * 0.08):
            score += non_ascii * 2.0
    elif enc == "cp1252":
        # Authentic Western/US Windows ANSI text: keep exact same ascii_ok * 0.5 weight as CJK codecs
        # and require 100% of non-ASCII chars to be clean Latin-1 / smart punctuation (zero byte mojibake).
        latin_ext = sum(1 for ch in text if (0x00C0 <= ord(ch) <= 0x00FF) or ch in "–—‘’“”•…€™®©")
        invalid_c1 = sum(1 for ch in text if 0x0080 <= ord(ch) <= 0x009F)
        other_non_ascii = max(0, (total - ascii_ok) - latin_ext - invalid_c1)
        if invalid_c1 == 0 and other_non_ascii == 0 and latin_ext > 0:
            score = (ascii_ok * 0.5) + (latin_ext * 5.0)
        else:
            score = (ascii_ok * 0.5) + (latin_ext * 1.0) - (invalid_c1 * 30.0) - (other_non_ascii * 12.0) - (suspicious * 15.0)
    return score


def _read_text_with_fallback(path: Path, encoding_hint: str | None = None) -> str:
    data = path.read_bytes()
    has_utf16_bom = data.startswith((b"\xff\xfe", b"\xfe\xff"))
    if not has_utf16_bom and b"\x00" in data[:4096]:
        raise UnsupportedBinaryFormatError(
            f"UNSUPPORTED_BINARY_FORMAT: '{path.name}' appears to be a binary file and cannot be extracted as plain text. "
            "Please convert it to .docx, .xlsx, .hwpx, .pdf, or .md and resubmit."
        )

    if encoding_hint and encoding_hint.lower() != "auto":
        return data.decode(encoding_hint)

    if has_utf16_bom:
        return data.decode("utf-16")

    for enc in ("utf-8-sig", "utf-8"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue

    # Disambiguate legacy CJK and Windows ANSI (cp1252) codepages cleanly
    candidates: list[tuple[float, str]] = []
    for enc in ("cp932", "euc-jp", "gb18030", "cp949", "euc-kr", "cp1252"):
        try:
            decoded = data.decode(enc)
            candidates.append((_score_decoded_cjk_text(decoded, enc), decoded))
        except UnicodeDecodeError:
            continue

    if candidates:
        candidates.sort(key=lambda pair: pair[0], reverse=True)
        return candidates[0][1]

    return data.decode("utf-8", errors="replace")


def _extract_docx_own_text(elem: ET.Element, parts: list[str]) -> None:
    """Collect text belonging directly to a <w:p> without crossing into nested <w:p>, <w:tbl>, <w:txbxContent>, or <mc:Fallback>."""
    for child in elem:
        tag = _local_tag(child)
        if tag in ("p", "tbl", "txbxContent", "Fallback"):
            continue
        if tag == "t" and child.text:
            parts.append(child.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag in ("br", "cr"):
            parts.append("\n")
        else:
            _extract_docx_own_text(child, parts)


def _walk_docx_paragraphs(node: ET.Element, lines: list[str]) -> None:
    """Walk DOCX XML tree in document order, skipping mc:Fallback duplicates and preserving table rows cleanly."""
    tag = _local_tag(node)
    if tag == "Fallback":
        return
    if tag == "tr":
        row_cells: list[str] = []
        for child in node:
            if _local_tag(child) == "tc":
                cell_lines: list[str] = []
                _walk_docx_paragraphs(child, cell_lines)
                if cell_lines:
                    row_cells.append(" ".join(cell_lines))
        if row_cells:
            lines.append(" | ".join(row_cells))
        return
    if tag == "p":
        parts: list[str] = []
        _extract_docx_own_text(node, parts)
        text = "".join(parts).strip()
        if text:
            lines.append(text)
        for child in node:
            _walk_docx_nested_containers(child, lines)
        return
    for child in node:
        _walk_docx_paragraphs(child, lines)


def _walk_docx_nested_containers(node: ET.Element, lines: list[str]) -> None:
    tag = _local_tag(node)
    if tag == "Fallback":
        return
    if tag in ("txbxContent", "tbl"):
        _walk_docx_paragraphs(node, lines)
        return
    for child in node:
        _walk_docx_nested_containers(child, lines)


def _extract_docx_xml_paragraphs(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    _walk_docx_paragraphs(root, lines)
    return lines


def extract_docx(path: Path) -> str:
    sections: list[str] = []
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        targets = (
            sorted([n for n in names if re.fullmatch(r"word/header\d+\.xml", n)], key=_natural_key)
            + (["word/document.xml"] if "word/document.xml" in names else [])
            + sorted([n for n in names if re.fullmatch(r"word/footnotes\.xml|word/endnotes\.xml", n)], key=_natural_key)
            + sorted([n for n in names if re.fullmatch(r"word/footer\d+\.xml", n)], key=_natural_key)
        )
        for target in targets:
            lines = _extract_docx_xml_paragraphs(zf.read(target))
            if lines:
                sections.append("\n".join(lines))
    return "\n\n".join(sections).strip()


def _collect_xlsx_text_without_furigana(node: ET.Element, parts: list[str]) -> None:
    """Collect visible <t> text inside Excel <si> or <is> while skipping Japanese <rPh>/<phoneticPr> furigana runs."""
    for child in node:
        tag = _local_tag(child)
        if tag in ("rPh", "phoneticPr"):
            continue
        if tag == "t" and child.text:
            parts.append(child.text)
        else:
            _collect_xlsx_text_without_furigana(child, parts)


def _parse_xlsx_shared_strings(zf: zipfile.ZipFile, names_set: set[str]) -> list[str]:
    if "xl/sharedStrings.xml" not in names_set:
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    shared: list[str] = []
    for elem in root:
        if _local_tag(elem) == "si":
            parts: list[str] = []
            _collect_xlsx_text_without_furigana(elem, parts)
            shared.append("".join(parts))
    return shared


def _resolve_xlsx_sheets(zf: zipfile.ZipFile, names: list[str], names_set: set[str]) -> list[tuple[str, str]]:
    """Resolve visible (sheet_display_name, zip_member_path) in workbook visual order, skipping hidden/veryHidden tabs."""
    wb_path = "xl/workbook.xml"
    rels_path = "xl/_rels/workbook.xml.rels"
    if wb_path in names_set and rels_path in names_set:
        try:
            rels_root = ET.fromstring(zf.read(rels_path))
            rid_to_target: dict[str, str] = {}
            for rel in rels_root.iter():
                if _local_tag(rel) == "Relationship":
                    rid = rel.attrib.get("Id", "")
                    target = rel.attrib.get("Target", "").replace("\\", "/").lstrip("/")
                    while target.startswith("../"):
                        target = target[3:]
                    if rid and target:
                        if not target.startswith("xl/"):
                            target = f"xl/{target}"
                        rid_to_target[rid] = target

            wb_root = ET.fromstring(zf.read(wb_path))
            ordered: list[tuple[str, str]] = []
            for elem in wb_root.iter():
                if _local_tag(elem) == "sheet":
                    state = elem.attrib.get("state", "visible").lower()
                    if state in ("hidden", "veryhidden"):
                        continue
                    sname = elem.attrib.get("name", "") or f"Sheet{len(ordered) + 1}"
                    rid = next(
                        (
                            v
                            for k, v in elem.attrib.items()
                            if k == "r:id" or ("relationships" in k and k.endswith("}id"))
                        ),
                        "",
                    )
                    target = rid_to_target.get(rid, "")
                    if target in names_set:
                        ordered.append((sname, target))
            if ordered:
                return ordered
        except ET.ParseError:
            pass

    fallback_sheets = sorted(
        [n for n in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)],
        key=_natural_key,
    )
    return [(Path(s).stem, s) for s in fallback_sheets]


def extract_xlsx(path: Path) -> str:
    """Zero-dependency Excel (.xlsx) extractor supporting sharedStrings, inlineStr, furigana filtering & visible sheet order."""
    blocks: list[str] = []
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        names_set = set(names)
        shared = _parse_xlsx_shared_strings(zf, names_set)
        sheets = _resolve_xlsx_sheets(zf, names, names_set)

        for sheet_name, sheet_path in sheets:
            root = ET.fromstring(zf.read(sheet_path))
            sheet_lines: list[str] = []
            for elem in root.iter():
                if _local_tag(elem) != "row":
                    continue
                row_vals: list[str] = []
                for cell in elem:
                    if _local_tag(cell) != "c":
                        continue
                    ctype = cell.attrib.get("t", "")
                    val = ""
                    if ctype == "s":
                        v_elem = next((c for c in cell if _local_tag(c) == "v"), None)
                        if v_elem is not None and v_elem.text and v_elem.text.strip().isdigit():
                            idx = int(v_elem.text.strip())
                            if 0 <= idx < len(shared):
                                val = shared[idx]
                    elif ctype == "inlineStr":
                        parts: list[str] = []
                        _collect_xlsx_text_without_furigana(cell, parts)
                        val = "".join(parts)
                    else:
                        v_elem = next((c for c in cell if _local_tag(c) == "v"), None)
                        if v_elem is not None and v_elem.text:
                            val = v_elem.text
                    cleaned = re.sub(r"\s+", " ", val).strip()
                    if cleaned:
                        row_vals.append(cleaned)
                if row_vals:
                    sheet_lines.append(" | ".join(row_vals))
            if sheet_lines:
                blocks.append(f"--- Sheet: {sheet_name} ---\n" + "\n".join(sheet_lines))
    return "\n\n".join(blocks).strip()


def _walk_pptx_paragraphs(node: ET.Element, paragraphs: list[str]) -> None:
    """Walk PPTX XML in document order while skipping <mc:Fallback> duplicate branches."""
    tag = _local_tag(node)
    if tag == "Fallback":
        return
    if tag == "p":
        parts: list[str] = []
        for sub in node.iter():
            sub_local = _local_tag(sub)
            if sub_local == "t" and sub.text:
                parts.append(sub.text)
            elif sub_local == "br":
                parts.append("\n")
        line = "".join(parts).strip()
        if line:
            paragraphs.append(line)
        return
    for child in node:
        _walk_pptx_paragraphs(child, paragraphs)


def _extract_pptx_xml_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    _walk_pptx_paragraphs(root, paragraphs)
    return "\n".join(paragraphs).strip()


def _resolve_pptx_slide_order(zf: zipfile.ZipFile, names: list[str], names_set: set[str]) -> list[str]:
    """Use ppt/presentation.xml p:sldIdLst visual slide order when available; fallback to natural sort."""
    pres_path = "ppt/presentation.xml"
    rels_path = "ppt/_rels/presentation.xml.rels"
    if pres_path in names_set and rels_path in names_set:
        try:
            rels_root = ET.fromstring(zf.read(rels_path))
            rid_to_target: dict[str, str] = {}
            for rel in rels_root.iter():
                if _local_tag(rel) == "Relationship":
                    rid = rel.attrib.get("Id", "")
                    target = rel.attrib.get("Target", "").replace("\\", "/")
                    if rid and target:
                        norm = target.lstrip("/")
                        while norm.startswith("../"):
                            norm = norm[3:]
                        if not norm.startswith("ppt/"):
                            norm = f"ppt/{norm}"
                        rid_to_target[rid] = norm

            pres_root = ET.fromstring(zf.read(pres_path))
            ordered: list[str] = []
            for elem in pres_root.iter():
                if _local_tag(elem) == "sldId":
                    rid = next(
                        (
                            v
                            for k, v in elem.attrib.items()
                            if k == "r:id"
                            or ("relationships" in k and k.endswith("}id"))
                            or (k == "id" and v.startswith("rId"))
                        ),
                        "",
                    )
                    target = rid_to_target.get(rid, "")
                    if target in names_set and target not in ordered:
                        ordered.append(target)
            if ordered:
                return ordered
        except ET.ParseError:
            pass

    return sorted(
        [n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)],
        key=_natural_key,
    )


def _find_pptx_note_target(zf: zipfile.ZipFile, slide_name: str, names_set: set[str]) -> str | None:
    slide_base = slide_name.rsplit("/", 1)[-1]
    rels_name = f"ppt/slides/_rels/{slide_base}.rels"
    if rels_name in names_set:
        try:
            rels_root = ET.fromstring(zf.read(rels_name))
            for rel in rels_root.iter():
                if _local_tag(rel) == "Relationship":
                    rtype = rel.attrib.get("Type", "")
                    target = rel.attrib.get("Target", "")
                    if "notesSlide" in rtype and target:
                        norm = target.replace("\\", "/")
                        while norm.startswith("../"):
                            norm = norm[3:]
                        if not norm.startswith("ppt/"):
                            norm = f"ppt/{norm.lstrip('/')}"
                        if norm in names_set:
                            return norm
        except ET.ParseError:
            pass
    m = re.search(r"slide(\d+)\.xml$", slide_base, flags=re.IGNORECASE)
    if m:
        fallback = f"ppt/notesSlides/notesSlide{m.group(1)}.xml"
        if fallback in names_set:
            return fallback
    return None


def extract_pptx(path: Path) -> str:
    blocks: list[str] = []
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        names_set = set(names)
        slides = _resolve_pptx_slide_order(zf, names, names_set)
        for idx, slide_name in enumerate(slides, start=1):
            slide_text = _extract_pptx_xml_text(zf.read(slide_name))
            note_name = _find_pptx_note_target(zf, slide_name, names_set)
            note_text = _extract_pptx_xml_text(zf.read(note_name)) if note_name else ""
            chunk_parts = [f"--- Slide {idx} ---"]
            if slide_text:
                chunk_parts.append(slide_text)
            if note_text:
                chunk_parts.append(f"[Speaker Notes]\n{note_text}")
            if len(chunk_parts) > 1:
                blocks.append("\n".join(chunk_parts))
    return "\n\n".join(blocks).strip()


def _extract_hwpx_own_text(elem: ET.Element, parts: list[str]) -> None:
    """Collect text directly inside an HWPX <hp:p> without descending into nested <tbl>, <p>, or <subList>."""
    for child in elem:
        tag = _local_tag(child)
        if tag in ("tbl", "p", "subList", "rect", "ellipse", "polygon"):
            continue
        if tag == "t" and child.text:
            parts.append(child.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "lineBreak":
            parts.append("\n")
        else:
            _extract_hwpx_own_text(child, parts)


def _walk_hwpx_node(node: ET.Element, lines: list[str]) -> None:
    """Walk HWPX XML cleanly: handles nested tables inside <hp:p> with zero duplication and cell separation."""
    tag = _local_tag(node)
    if tag == "tr":
        row_cells: list[str] = []
        for child in node:
            if _local_tag(child) == "tc":
                cell_lines: list[str] = []
                _walk_hwpx_node(child, cell_lines)
                if cell_lines:
                    row_cells.append(" ".join(cell_lines))
        if row_cells:
            lines.append(" | ".join(row_cells))
        return
    if tag == "p":
        parts: list[str] = []
        _extract_hwpx_own_text(node, parts)
        text = "".join(parts).strip()
        if text:
            lines.append(text)
        for child in node:
            _walk_hwpx_nested_containers(child, lines)
        return
    for child in node:
        _walk_hwpx_node(child, lines)


def _walk_hwpx_nested_containers(node: ET.Element, lines: list[str]) -> None:
    tag = _local_tag(node)
    if tag in ("tbl", "subList"):
        _walk_hwpx_node(node, lines)
        return
    for child in node:
        _walk_hwpx_nested_containers(child, lines)


def extract_hwpx(path: Path) -> str:
    sections: list[str] = []
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        section_files = sorted(
            [n for n in names if re.fullmatch(r"Contents/section\d+\.xml", n, flags=re.IGNORECASE)],
            key=_natural_key,
        )
        for sec in section_files:
            root = ET.fromstring(zf.read(sec))
            lines: list[str] = []
            _walk_hwpx_node(root, lines)
            if lines:
                sections.append("\n".join(lines))
    return "\n\n".join(sections).strip()


def extract_html(path: Path, encoding_hint: str | None = None) -> str:
    raw = _read_text_with_fallback(path, encoding_hint=encoding_hint)
    parser = _HTMLTextExtractor()
    parser.feed(raw)
    parser.close()
    return parser.get_text()


def extract_pdf(path: Path) -> tuple[str, str | None]:
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(str(path))
        pages = []
        for idx, page in enumerate(reader.pages, start=1):
            txt = (page.extract_text() or "").strip()
            if txt:
                pages.append(f"--- Page {idx} ---\n{txt}")
        if pages:
            return "\n\n".join(pages), None
        return "", (
            f"PDF_NATIVE_READ_REQUIRED: '{path.name}' yielded no selectable text (likely image/design-based PDF). "
            "Read this PDF natively with Antigravity read_file and append key text/captions to the candidate snapshot."
        )
    except ImportError:
        pass

    try:
        import fitz  # type: ignore

        doc = fitz.open(str(path))
        pages = []
        for idx, page in enumerate(doc, start=1):
            txt = page.get_text("text").strip()
            if txt:
                pages.append(f"--- Page {idx} ---\n{txt}")
        doc.close()
        if pages:
            return "\n\n".join(pages), None
        return "", (
            f"PDF_NATIVE_READ_REQUIRED: '{path.name}' yielded no selectable text (likely image/design-based PDF). "
            "Read this PDF natively with Antigravity read_file and append key text/captions to the candidate snapshot."
        )
    except ImportError:
        return "", (
            f"PDF_NATIVE_READ_REQUIRED: Neither pypdf nor PyMuPDF is installed for '{path.name}'. "
            "Read this PDF natively with Antigravity read_file and save/append extracted text to the candidate snapshot."
        )


def extract_file(path: Path, encoding_hint: str | None = None) -> tuple[str, str | None]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    ext = path.suffix.lower()
    if ext in UNSUPPORTED_BINARY_EXTENSIONS:
        raise UnsupportedBinaryFormatError(
            f"UNSUPPORTED_BINARY_FORMAT: Legacy binary format '{ext}' ('{path.name}') is not directly supported. "
            "Please save/export as .xlsx, .docx, .hwpx, .pdf, or .md and resubmit."
        )
    if ext in TEXT_EXTENSIONS:
        return _read_text_with_fallback(path, encoding_hint=encoding_hint).strip(), None
    if ext == ".docx":
        return extract_docx(path), None
    if ext == ".xlsx":
        return extract_xlsx(path), None
    if ext == ".pptx":
        return extract_pptx(path), None
    if ext == ".hwpx":
        return extract_hwpx(path), None
    if ext in HTML_EXTENSIONS:
        return extract_html(path, encoding_hint=encoding_hint), None
    if ext == ".pdf":
        return extract_pdf(path)
    return _read_text_with_fallback(path, encoding_hint=encoding_hint).strip(), f"Unknown extension '{ext}' treated as plain text."


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Extract and consolidate multilingual text from resume/portfolio/JD files (v2.1).")
    parser.add_argument("--inputs", nargs="*", default=[], help="One or more input file paths.")
    parser.add_argument("--out", required=True, help="Output consolidated UTF-8 text file path.")
    parser.add_argument(
        "--encoding",
        default="auto",
        help="Optional explicit text encoding hint (e.g., utf-8, cp949, gb18030, cp932). Default: auto.",
    )
    parser.add_argument(
        "--append-stdin",
        action="store_true",
        help="Also read additional text from stdin and append to the consolidated output.",
    )
    parser.add_argument("--stdin-label", default="Inline Pasted Input", help="Section label for stdin content.")
    args = parser.parse_args()

    sections: list[str] = []
    warnings: list[str] = []
    files_manifest: list[dict[str, Any]] = []

    for raw_path in args.inputs:
        p = Path(raw_path).resolve()
        text, warn = extract_file(p, encoding_hint=args.encoding)
        if warn:
            warnings.append(warn)
        files_manifest.append({"path": str(p), "chars": len(text), "warning": warn})
        if text:
            sections.append(f"=== SOURCE: {p.name} ===\n{text}")

    if args.append_stdin:
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            sections.append(f"=== SOURCE: {args.stdin_label} ===\n{stdin_text}")
            files_manifest.append({"path": f"<stdin:{args.stdin_label}>", "chars": len(stdin_text), "warning": None})

    combined = "\n\n".join(sections).strip() + ("\n" if sections else "")
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(combined, encoding="utf-8")

    summary = {
        "out_path": str(out_path),
        "total_chars": len(combined),
        "files_processed": files_manifest,
        "warnings": warnings,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
