#!/usr/bin/env python3
"""Zero-dependency document text extractor for resume-jd-coach (v1.1).

Supports:
  - Plain text / Markdown / structured text: .md, .markdown, .txt, .csv, .json, .yaml, .yml
  - Microsoft Word: .docx (nested textbox/table safe, skips mc:Fallback duplicates)
  - PowerPoint portfolio decks: .pptx (exact ppt/presentation.xml slide order + _rels speaker notes)
  - Korean Hancom Hangul XML: .hwpx (nested table/paragraph safe — zero duplication/mashing)
  - HTML pages: .html, .htm
  - PDF: uses pypdf or PyMuPDF (fitz) if installed; otherwise emits PDF_NATIVE_READ_REQUIRED
    warning guiding Antigravity native read_file inspection.
  - Rejects legacy binary formats (.hwp, .doc, .xls, .ppt, or null-byte binaries) loudly instead
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


def _read_text_with_fallback(path: Path) -> str:
    data = path.read_bytes()
    # Detect binary files early (allow UTF-16 BOM, reject arbitrary NUL-bearing binaries)
    has_utf16_bom = data.startswith((b"\xff\xfe", b"\xfe\xff"))
    if not has_utf16_bom and b"\x00" in data[:4096]:
        raise UnsupportedBinaryFormatError(
            f"UNSUPPORTED_BINARY_FORMAT: '{path.name}' appears to be a binary file and cannot be extracted as plain text. "
            "Please convert it to .docx, .hwpx, .pdf, or .md and resubmit."
        )
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr", "utf-16"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
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
        # Still visit nested containers (e.g. drawing/txbxContent/tbl inside a paragraph) separately
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


def _extract_pptx_xml_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for elem in root.iter():
        if _local_tag(elem) == "p":
            parts: list[str] = []
            for sub in elem.iter():
                sub_local = _local_tag(sub)
                if sub_local == "t" and sub.text:
                    parts.append(sub.text)
                elif sub_local == "br":
                    parts.append("\n")
            line = "".join(parts).strip()
            if line:
                paragraphs.append(line)
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
        # Visit nested structural containers (tables/textboxes inside runs of this paragraph) separately
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


def extract_html(path: Path) -> str:
    raw = _read_text_with_fallback(path)
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


def extract_file(path: Path) -> tuple[str, str | None]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    ext = path.suffix.lower()
    if ext in UNSUPPORTED_BINARY_EXTENSIONS:
        raise UnsupportedBinaryFormatError(
            f"UNSUPPORTED_BINARY_FORMAT: Legacy binary format '{ext}' ('{path.name}') is not directly supported. "
            "Please save/export as .hwpx, .docx, .pdf, or .md and resubmit."
        )
    if ext in TEXT_EXTENSIONS:
        return _read_text_with_fallback(path).strip(), None
    if ext == ".docx":
        return extract_docx(path), None
    if ext == ".pptx":
        return extract_pptx(path), None
    if ext == ".hwpx":
        return extract_hwpx(path), None
    if ext in HTML_EXTENSIONS:
        return extract_html(path), None
    if ext == ".pdf":
        return extract_pdf(path)
    return _read_text_with_fallback(path).strip(), f"Unknown extension '{ext}' treated as plain text."


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Extract and consolidate text from resume/portfolio/JD files.")
    parser.add_argument("--inputs", nargs="*", default=[], help="One or more input file paths.")
    parser.add_argument("--out", required=True, help="Output consolidated UTF-8 text file path.")
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
        text, warn = extract_file(p)
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
