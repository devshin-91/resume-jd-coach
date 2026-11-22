#!/usr/bin/env python3
"""Deterministic scoring, rubric lock, negation-aware ATS audit, and round-diff engine for resume-jd-coach (v1.1)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CATEGORY_ORDER = ("must_have", "portfolio_impact", "preferred", "ats_framing")

CATEGORY_LABELS = {
    "ko": {
        "must_have": "필수 자격 & 핵심 직무",
        "portfolio_impact": {
            "portfolio": "포트폴리오 증빙 & 성과",
            "resume_only": "직무 증빙 & 정량 성과",
        },
        "preferred": "우대 사항",
        "ats_framing": "JD 키워드 & 포지셔닝",
    },
    "en": {
        "must_have": "Must-Have & Core Duties",
        "portfolio_impact": {
            "portfolio": "Portfolio Proof & Impact",
            "resume_only": "Work Proof & Measurable Impact",
        },
        "preferred": "Preferred & Bonus",
        "ats_framing": "ATS Keywords & Role Framing",
    },
}

DEFAULT_WEIGHTS = {
    "must_have": Decimal("45"),
    "portfolio_impact": Decimal("25"),
    "preferred": Decimal("15"),
    "ats_framing": Decimal("15"),
}

GRADE_MULTIPLIERS: dict[str, Decimal] = {
    "FULL": Decimal("1.00"),
    "STRONG_PARTIAL": Decimal("0.75"),
    "PARTIAL": Decimal("0.50"),
    "WEAK": Decimal("0.25"),
    "MISSING": Decimal("0.00"),
}

GRADE_SEQUENCE = ("MISSING", "WEAK", "PARTIAL", "STRONG_PARTIAL", "FULL")
KNOCKOUT_RISK_GRADES = {"MISSING", "WEAK"}
VALID_GAP_TYPES = {"expression_gap", "transferable_gap", "true_gap"}
VALID_KEYWORD_TIERS = {"must": Decimal("2"), "preferred": Decimal("1")}
VALID_LANGUAGES = {"ko", "en"}
VALID_DOMAIN_MODES = {"portfolio", "resume_only"}

OVERLY_BROAD_ALIASES = {"자동화", "취득", "상실", "업무", "관리", "개발", "분석", "협업", "운영", "automation"}

HANGUL_OR_CJK_RE = re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af\u4e00-\u9fff\u3040-\u30ff]")
PURE_HANGUL_RE = re.compile(r"^[\uac00-\ud7af\s]+$")
ASCII_ALNUM_RE = re.compile(r"[A-Za-z0-9]")

NEGATED_HEADING_RE = re.compile(
    r"(아직\s*해\s*보지\s*않은|해보지\s*않은|미경험|미보유|부족한\s*부분|한계\s*및\s*미경험|"
    r"what\s+i\s+haven'?t\s+done|not\s+yet\s+experienced|missing\s+skills|skill\s+gaps)",
    flags=re.IGNORECASE,
)

SECTION_RESET_HEADING_RE = re.compile(
    r"^(=== SOURCE:|#{1,4}\s+\S|\[.{2,30}\]$|경력|학력|프로젝트|포트폴리오|기술\s*스택|사용\s*기술|요약|프로필|자격|관련\s*배경|"
    r"experience|education|projects?|skills?|summary|background)\b",
    flags=re.IGNORECASE,
)

LOCAL_NEGATION_RE = re.compile(
    r"(미경험|미보유|경험\s*(?:이|은|는)?\s*없|해\s*보지\s*않|해보지\s*않|사용\s*(?:해\s*보지\s*)?않|"
    r"사용\s*안|다뤄\s*보지\s*않|적용\s*안|부재|없음|불가|아직\s*없|배우지\s*않|"
    r"no\s+experience|not\s+experienced|never\s+used|not\s+used|haven'?t\s+used|"
    r"unfamiliar\s+with|lack\s+of|without\s+\w+\s+experience|do\s+not\s+have)",
    flags=re.IGNORECASE,
)


def _dec(val: Any) -> Decimal:
    return Decimal(str(val))


def _round1(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def _round2(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _fmt1(val: Any) -> str:
    """Format number to 1 decimal place strictly using Decimal ROUND_HALF_UP (never IEEE Banker's Rounding)."""
    return f"{_round1(_dec(val)):.1f}"


def _category_label(cat: str, lang: str, domain_mode: str) -> str:
    entry = CATEGORY_LABELS[lang][cat]
    if isinstance(entry, dict):
        return entry[domain_mode]
    return entry


def _display_score_safe(exact_score: Decimal, threshold: Decimal) -> tuple[Decimal, bool]:
    """Round score to 1 decimal while preventing contradiction with pass/fail threshold."""
    passed = exact_score >= threshold
    rounded = _round1(exact_score)
    if not passed and rounded >= threshold:
        floored = exact_score.quantize(Decimal("0.1"), rounding=ROUND_DOWN)
        return floored, False
    return rounded, passed


def _dec_norm(val: Any) -> str:
    """Canonical Decimal string without trailing zeros or scientific notation (e.g., 80.0 == 80 -> '80')."""
    d = _dec(val).normalize()
    if d == d.to_integral_value():
        return str(d.to_integral_value())
    return format(d, "f")


def compute_rubric_hash(rubric: dict[str, Any]) -> str:
    """Compute canonical SHA-256 hash over locked rubric fields (excluding lock metadata)."""
    canonical = {
        "role_title": rubric.get("role_title", ""),
        "company": rubric.get("company", ""),
        "language": str(rubric.get("language", "ko")).lower(),
        "domain_mode": str(rubric.get("domain_mode", "portfolio")).lower(),
        "pass_threshold": _dec_norm(rubric.get("pass_threshold", 80.0)),
        "ats_lexical_share": _dec_norm(rubric.get("ats_lexical_share", 0.5)),
        "category_weights": {
            cat: _dec_norm(rubric.get("category_weights", DEFAULT_WEIGHTS).get(cat, DEFAULT_WEIGHTS[cat]))
            for cat in CATEGORY_ORDER
        },
        "categories": {
            cat: [
                {
                    "id": str(item["id"]),
                    "title": str(item["title"]),
                    "weight": _dec_norm(item.get("weight", 1)),
                    "is_knockout": bool(item.get("is_knockout", False)),
                }
                for item in rubric.get("categories", {}).get(cat, [])
            ]
            for cat in CATEGORY_ORDER
        },
        "keywords": [
            {
                "term": str(kw["term"]),
                "aliases": [str(a) for a in kw.get("aliases", [])],
                "tier": str(kw.get("tier", "must")).lower(),
                "linked_item_id": str(kw["linked_item_id"]) if kw.get("linked_item_id") else None,
            }
            for kw in rubric.get("keywords", [])
        ],
    }
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def validate_rubric(rubric: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Validate rubric schema and return (normalized_item_map, advisory_warnings)."""
    warnings: list[str] = []

    lang = str(rubric.get("language", "ko")).lower()
    if lang not in VALID_LANGUAGES:
        raise ValueError(f"Invalid language '{lang}'. Valid: {sorted(VALID_LANGUAGES)}")

    domain_mode = str(rubric.get("domain_mode", "portfolio")).lower()
    if domain_mode not in VALID_DOMAIN_MODES:
        raise ValueError(f"Invalid domain_mode '{domain_mode}'. Valid: {sorted(VALID_DOMAIN_MODES)}")

    threshold = _dec(rubric.get("pass_threshold", 80.0))
    if threshold <= Decimal("0") or threshold > Decimal("100"):
        raise ValueError(f"pass_threshold must be in (0, 100], got {threshold}")

    ats_share = _dec(rubric.get("ats_lexical_share", 0.5))
    if ats_share < Decimal("0") or ats_share > Decimal("1"):
        raise ValueError(f"ats_lexical_share must be in [0, 1], got {ats_share}")

    raw_weights = rubric.get("category_weights", DEFAULT_WEIGHTS)
    for cat in CATEGORY_ORDER:
        w = _dec(raw_weights.get(cat, DEFAULT_WEIGHTS[cat]))
        if w < Decimal("0"):
            raise ValueError(f"Category weight for '{cat}' cannot be negative: {w}")

    categories = rubric.get("categories")
    if not isinstance(categories, dict):
        raise ValueError("rubric.json must contain a 'categories' object.")

    unknown_cats = set(categories.keys()) - set(CATEGORY_ORDER)
    if unknown_cats:
        raise ValueError(f"Unknown categories in rubric.json: {sorted(unknown_cats)}")

    item_map: dict[str, dict[str, Any]] = {}
    for cat in CATEGORY_ORDER:
        items = categories.get(cat, [])
        if not isinstance(items, list):
            raise ValueError(f"Category '{cat}' must be a list of items.")
        for item in items:
            if not isinstance(item, dict) or "id" not in item or "title" not in item:
                raise ValueError(f"Every item in '{cat}' must have 'id' and 'title': {item}")
            item_id = str(item["id"]).strip()
            if not item_id:
                raise ValueError(f"Empty item id in category '{cat}'.")
            if item_id in item_map:
                raise ValueError(f"Duplicate item id '{item_id}' across rubric.")
            weight = _dec(item.get("weight", 1))
            if weight <= Decimal("0"):
                raise ValueError(f"Item '{item_id}' weight must be > 0, got {weight}")
            is_ko = bool(item.get("is_knockout", False))
            if is_ko and cat != "must_have":
                raise ValueError(f"Item '{item_id}' has is_knockout=true outside 'must_have'.")
            if is_ko and weight < Decimal("2"):
                raise ValueError(
                    f"KNOCKOUT_WEIGHT_ERROR: Knockout item '{item_id}' must have weight >= 2 (got {weight}) "
                    "so core screening gates cannot be artificially minimized."
                )
            item_map[item_id] = {
                "id": item_id,
                "category": cat,
                "title": str(item["title"]),
                "description": str(item.get("description", "")),
                "weight": weight,
                "is_knockout": is_ko,
            }

    keywords = rubric.get("keywords", [])
    if not isinstance(keywords, list):
        raise ValueError("'keywords' must be a list.")
    for kw in keywords:
        if not isinstance(kw, dict) or not str(kw.get("term", "")).strip():
            raise ValueError(f"Invalid keyword entry: {kw}")
        term = str(kw["term"]).strip()
        tier = str(kw.get("tier", "must")).lower()
        if tier not in VALID_KEYWORD_TIERS:
            raise ValueError(f"Keyword '{term}' has invalid tier '{tier}' (use 'must' or 'preferred').")
        linked = kw.get("linked_item_id")
        if linked and str(linked) not in item_map:
            raise ValueError(f"Keyword '{term}' references unknown linked_item_id '{linked}'.")
        for alias in kw.get("aliases", []):
            a_clean = str(alias).strip()
            if a_clean.lower() in OVERLY_BROAD_ALIASES and a_clean.lower() != term.lower():
                warnings.append(
                    f"BROAD_ALIAS_WARNING: Keyword '{term}' uses overly broad alias '{a_clean}' which may cause false ATS matches."
                )

    if not item_map and not keywords:
        raise ValueError("Rubric has zero items and zero keywords.")

    return item_map, warnings


def _build_term_regex(term: str) -> re.Pattern[str]:
    cleaned = term.strip()
    if not cleaned:
        raise ValueError("Cannot build regex for empty keyword term.")

    has_cjk = bool(HANGUL_OR_CJK_RE.search(cleaned))
    tokens = re.split(r"\s+", cleaned)
    if has_cjk:
        core = r"\s*".join(re.escape(tok) for tok in tokens)
        if ASCII_ALNUM_RE.match(cleaned[0]):
            left = r"(?<![A-Za-z0-9])"
        elif PURE_HANGUL_RE.match(cleaned) and len(cleaned.replace(" ", "")) <= 2:
            # Prevent 1-2 char Hangul terms like "인사"/"취득" from matching inside unrelated words ("개인사정", "확인사항")
            left = r"(?<![\uac00-\ud7af])"
        else:
            left = ""
        right = r"(?![A-Za-z0-9+#])" if ASCII_ALNUM_RE.match(cleaned[-1]) else ""
        return re.compile(f"{left}{core}{right}", flags=re.IGNORECASE)

    core = r"\s+".join(re.escape(tok) for tok in tokens)
    if cleaned.startswith("."):
        # Allow both standalone ".NET" and compound "ASP.NET"
        left = ""
    elif ASCII_ALNUM_RE.match(cleaned[0]):
        left = r"(?<![A-Za-z0-9])"
    else:
        left = r"(?<![A-Za-z0-9+#])"

    last_ch = cleaned[-1]
    if last_ch in ("+", "#"):
        right = r"(?![A-Za-z+#])"
    elif len(cleaned) == 1 and ASCII_ALNUM_RE.match(last_ch):
        # Single-letter tech terms ("C", "R") must not match "C-level", "R&D", "C++", "C#"
        right = r"(?![A-Za-z0-9+#&\-])"
    elif ASCII_ALNUM_RE.match(last_ch):
        right = r"(?![A-Za-z0-9+#])"
    else:
        right = r"(?![A-Za-z0-9])"
    return re.compile(f"{left}{core}{right}", flags=re.IGNORECASE)


def _compute_negated_line_flags(lines: list[str]) -> list[bool]:
    """Identify lines inside explicit negative-experience sections (e.g., '아직 해 보지 않은 것')."""
    flags: list[bool] = []
    in_negated_section = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            flags.append(in_negated_section)
            continue
        is_bullet_or_sentence = (
            bool(re.match(r"^([-•*·]|\d+[.)])\s*", stripped))
            or stripped.endswith(".")
            or ";" in stripped
            or "," in stripped
        )
        if (not is_bullet_or_sentence) and len(stripped) <= 45 and NEGATED_HEADING_RE.search(stripped):
            in_negated_section = True
            flags.append(True)
            continue
        if in_negated_section and SECTION_RESET_HEADING_RE.search(stripped):
            in_negated_section = False
        flags.append(in_negated_section)
    return flags


CLAUSE_SPLIT_RE = re.compile(
    r"[.;|]|(?:이지만|이나|지만|하지만|이며|이고|는데|반면|(?:\bbut\b|\bhowever\b))",
    flags=re.IGNORECASE,
)


def _is_match_negated(line: str, start: int, end: int, line_in_neg_section: bool) -> bool:
    if line_in_neg_section:
        return True
    clause_left = max(0, start - 35)
    clause_right = min(len(line), end + 35)
    prefix = CLAUSE_SPLIT_RE.split(line[clause_left:start])[-1]
    suffix = CLAUSE_SPLIT_RE.split(line[end:clause_right])[0]
    window = f"{prefix}{line[start:end]}{suffix}"
    return bool(LOCAL_NEGATION_RE.search(window))


def audit_ats_keywords(keywords: list[dict[str, Any]], candidate_text: str) -> dict[str, Any]:
    """Run deterministic Korean/English boundary-aware & negation-aware lexical keyword matching."""
    lines = candidate_text.splitlines()
    neg_section_flags = _compute_negated_line_flags(lines)

    results: list[dict[str, Any]] = []
    total_w = Decimal("0")
    matched_w = Decimal("0")

    for kw in keywords:
        term = str(kw["term"]).strip()
        aliases = [str(a).strip() for a in kw.get("aliases", []) if str(a).strip()]
        tier = str(kw.get("tier", "must")).lower()
        linked_item_id = str(kw["linked_item_id"]) if kw.get("linked_item_id") else None
        weight = VALID_KEYWORD_TIERS[tier]
        total_w += weight

        matched_surface: str | None = None
        saw_negated = False

        # Scan full text across term & aliases so contradictory positive+negative mentions are always detected
        for surface in [term, *aliases]:
            pattern = _build_term_regex(surface)
            for line, in_neg_sec in zip(lines, neg_section_flags):
                for m in pattern.finditer(line):
                    if _is_match_negated(line, m.start(), m.end(), in_neg_sec):
                        saw_negated = True
                    elif matched_surface is None:
                        matched_surface = m.group(0)

        is_matched = matched_surface is not None
        if is_matched:
            matched_w += weight

        results.append(
            {
                "term": term,
                "aliases": aliases,
                "tier": tier,
                "linked_item_id": linked_item_id,
                "weight": float(weight),
                "matched": is_matched,
                "matched_surface": matched_surface,
                "negated_mention": (not is_matched) and saw_negated,
                "contradictory_mention": is_matched and saw_negated,
            }
        )

    ratio = (matched_w / total_w) if total_w > Decimal("0") else Decimal("1")
    return {
        "checked": True,
        "total_count": len(results),
        "matched_count": sum(1 for r in results if r["matched"]),
        "total_weight": total_w,
        "matched_weight": matched_w,
        "ratio": ratio,
        "coverage_pct": float(_round1(ratio * Decimal("100"))),
        "details": results,
    }


def _normalize_for_quote_check(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z\uac00-\ud7af]+", " ", text.lower()).strip()


def verify_quote_grounding(quote: str, candidate_text: str) -> bool:
    """Verify that a claimed evidence_quote actually appears in candidate_text.

    Requires verbatim normalized substring match OR (for multi-token clauses) BOTH >= 70% unigram
    AND >= 45% contiguous bigram overlap — blocking scattered bag-of-words fabrication.
    """
    norm_cand = _normalize_for_quote_check(candidate_text)
    if not norm_cand:
        return False

    clauses = [c.strip() for c in re.split(r"\.{3}|…|\s+/\s+|\n+", quote) if c.strip()]
    if not clauses:
        return False

    cand_tokens_list = norm_cand.split()
    cand_tokens = set(cand_tokens_list)
    cand_bigrams = {
        (cand_tokens_list[i], cand_tokens_list[i + 1]) for i in range(len(cand_tokens_list) - 1)
    }

    verified_clauses = 0
    for clause in clauses:
        norm_clause = _normalize_for_quote_check(clause)
        if not norm_clause:
            continue
        if norm_clause in norm_cand:
            verified_clauses += 1
            continue

        tokens = norm_clause.split()
        if len(tokens) == 1:
            if tokens[0] in cand_tokens or tokens[0] in norm_cand:
                verified_clauses += 1
            continue

        meaningful = [t for t in tokens if len(t) >= 2]
        unigram_ratio = (
            sum(1 for t in meaningful if t in cand_tokens or t in norm_cand) / len(meaningful)
            if meaningful
            else 0.0
        )
        clause_bigrams = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
        bigram_ratio = (
            sum(1 for bg in clause_bigrams if bg in cand_bigrams or f"{bg[0]} {bg[1]}" in norm_cand)
            / len(clause_bigrams)
            if clause_bigrams
            else 0.0
        )
        if unigram_ratio >= 0.70 and bigram_ratio >= 0.45:
            verified_clauses += 1

    non_empty_clauses = sum(1 for c in clauses if _normalize_for_quote_check(c))
    return non_empty_clauses > 0 and verified_clauses == non_empty_clauses


def evaluate_round(
    rubric: dict[str, Any],
    eval_data: dict[str, Any],
    candidate_text: str | None = None,
    history: dict[str, Any] | None = None,
    *,
    require_locked: bool = True,
    strict_quotes: bool = False,
    lang_override: str | None = None,
    domain_mode_override: str | None = None,
) -> dict[str, Any]:
    """Compute exact weighted score, uplifts, round diff, quote audit, and Grace recommendation."""
    item_map, rubric_warnings = validate_rubric(rubric)
    current_hash = compute_rubric_hash(rubric)

    stamped_hash = rubric.get("rubric_hash")
    if require_locked and not stamped_hash:
        raise ValueError(
            "RUBRIC_UNLOCKED_ERROR: rubric.json is missing 'rubric_hash'. "
            "Run --init-rubric <rubric.json> before evaluating Round 1."
        )
    if stamped_hash and stamped_hash != current_hash:
        raise ValueError(
            f"RUBRIC_TAMPERED_ERROR: rubric.json hash mismatch (stamped={stamped_hash}, computed={current_hash}). "
            "Do not alter locked rubric mid-session."
        )

    if history and history.get("rubric_hash") and history["rubric_hash"] != current_hash:
        raise ValueError(
            f"RUBRIC_DRIFT_ERROR: history.json hash ({history['rubric_hash']}) != rubric.json hash ({current_hash}). "
            "Start a new session if the target JD changed."
        )

    if eval_data.get("rubric_hash") and eval_data["rubric_hash"] != current_hash:
        raise ValueError(
            f"RUBRIC_HASH_MISMATCH: eval file hash ({eval_data['rubric_hash']}) != rubric hash ({current_hash})."
        )

    lang = (lang_override or str(rubric.get("language", "ko"))).lower()
    if lang not in VALID_LANGUAGES:
        raise ValueError(f"Invalid language '{lang}'. Valid: {sorted(VALID_LANGUAGES)}")
    domain_mode = (domain_mode_override or str(rubric.get("domain_mode", "portfolio"))).lower()
    if domain_mode not in VALID_DOMAIN_MODES:
        raise ValueError(f"Invalid domain_mode '{domain_mode}'. Valid: {sorted(VALID_DOMAIN_MODES)}")

    keywords = rubric.get("keywords", [])
    if keywords and candidate_text is None:
        raise ValueError(
            "CANDIDATE_TEXT_REQUIRED_ERROR: rubric.json defines ATS 'keywords', so --candidate-text is required "
            "to keep ats_framing category weights consistent across rounds."
        )

    eval_items_raw = eval_data.get("items")
    if not isinstance(eval_items_raw, list):
        raise ValueError("eval JSON must contain an 'items' list.")

    eval_by_id: dict[str, dict[str, Any]] = {}
    unverified_quotes: list[dict[str, str]] = []

    for entry in eval_items_raw:
        if not isinstance(entry, dict) or "id" not in entry or "grade" not in entry:
            raise ValueError(f"Every eval item must include 'id' and 'grade': {entry}")
        iid = str(entry["id"]).strip()
        if iid not in item_map:
            raise ValueError(f"Unknown item id '{iid}' in eval JSON (not in rubric.json).")
        if iid in eval_by_id:
            raise ValueError(f"Duplicate item id '{iid}' in eval JSON.")
        grade = str(entry["grade"]).strip().upper()
        if grade not in GRADE_MULTIPLIERS:
            raise ValueError(f"Invalid grade '{grade}' for item '{iid}'. Valid: {list(GRADE_MULTIPLIERS)}")
        evidence_quote = str(entry.get("evidence_quote", "")).strip()
        if grade != "MISSING" and not evidence_quote:
            raise ValueError(
                f"Anti-hallucination violation: item '{iid}' graded '{grade}' must include non-empty 'evidence_quote'."
            )
        quote_verified: bool | None = None
        if grade != "MISSING" and candidate_text is not None:
            quote_verified = verify_quote_grounding(evidence_quote, candidate_text)
            if not quote_verified:
                unverified_quotes.append({"id": iid, "evidence_quote": evidence_quote})

        gap_type = entry.get("gap_type")
        if grade == "FULL":
            gap_type_norm = None
        else:
            gap_type_norm = str(gap_type).strip().lower() if gap_type else "expression_gap"
            if gap_type_norm not in VALID_GAP_TYPES:
                raise ValueError(
                    f"Invalid gap_type '{gap_type_norm}' for item '{iid}'. Valid: {sorted(VALID_GAP_TYPES)}"
                )
        eval_by_id[iid] = {
            "id": iid,
            "grade": grade,
            "multiplier": GRADE_MULTIPLIERS[grade],
            "evidence_quote": evidence_quote,
            "quote_verified": quote_verified,
            "source": str(entry.get("source", "")).strip(),
            "gap_type": gap_type_norm,
            "action_hint": str(entry.get("action_hint", "")).strip(),
        }

    missing_eval_ids = sorted(set(item_map.keys()) - set(eval_by_id.keys()))
    if missing_eval_ids:
        raise ValueError(f"Eval JSON is missing rubric item(s): {missing_eval_ids}")

    if strict_quotes and unverified_quotes:
        bad_ids = [q["id"] for q in unverified_quotes]
        raise ValueError(
            f"QUOTE_VERIFICATION_ERROR: Non-verbatim or ungrounded evidence_quote detected for item(s): {bad_ids}."
        )

    # ATS lexical audit
    if keywords and candidate_text is not None:
        ats_audit = audit_ats_keywords(keywords, candidate_text)
    else:
        ats_audit = {
            "checked": False,
            "total_count": 0,
            "matched_count": 0,
            "total_weight": Decimal("0"),
            "matched_weight": Decimal("0"),
            "ratio": Decimal("0"),
            "coverage_pct": None,
            "details": [],
        }

    raw_weights = {
        cat: _dec(rubric.get("category_weights", DEFAULT_WEIGHTS).get(cat, DEFAULT_WEIGHTS[cat]))
        for cat in CATEGORY_ORDER
    }
    cat_items: dict[str, list[dict[str, Any]]] = {cat: [] for cat in CATEGORY_ORDER}
    for meta in item_map.values():
        cat_items[meta["category"]].append(meta)

    active_cats: list[str] = []
    for cat in CATEGORY_ORDER:
        if cat == "ats_framing":
            if cat_items[cat] or (ats_audit["checked"] and ats_audit["total_weight"] > Decimal("0")):
                if raw_weights[cat] > Decimal("0"):
                    active_cats.append(cat)
        else:
            if cat_items[cat] and raw_weights[cat] > Decimal("0"):
                active_cats.append(cat)

    active_weight_sum = sum((raw_weights[c] for c in active_cats), Decimal("0"))
    if active_weight_sum <= Decimal("0"):
        raise ValueError("Active category weight sum must be > 0.")

    eff_weights: dict[str, Decimal] = {
        cat: ((raw_weights[cat] / active_weight_sum) * Decimal("100")) if cat in active_cats else Decimal("0")
        for cat in CATEGORY_ORDER
    }

    ats_lexical_share_cfg = _dec(rubric.get("ats_lexical_share", 0.5))

    category_results: dict[str, dict[str, Any]] = {}
    item_results: list[dict[str, Any]] = []
    total_exact = Decimal("0")

    for cat in CATEGORY_ORDER:
        items = cat_items[cat]
        w_eff = eff_weights[cat]
        label = _category_label(cat, lang, domain_mode)
        if cat not in active_cats:
            category_results[cat] = {
                "label": label,
                "label_ko": _category_label(cat, "ko", domain_mode),
                "active": False,
                "effective_weight": 0.0,
                "attainment_pct": None,
                "earned_points": 0.0,
                "max_points": 0.0,
                "item_count": 0,
            }
            continue

        item_weight_sum = sum((it["weight"] for it in items), Decimal("0"))
        if items:
            earned_item_w = sum((it["weight"] * eval_by_id[it["id"]]["multiplier"] for it in items), Decimal("0"))
            items_ratio = earned_item_w / item_weight_sum
        else:
            items_ratio = Decimal("0")

        if cat == "ats_framing":
            has_lex = ats_audit["checked"] and ats_audit["total_weight"] > Decimal("0")
            has_frame = bool(items)
            if has_lex and has_frame:
                lex_alpha = ats_lexical_share_cfg
                frame_beta = Decimal("1") - lex_alpha
                cat_ratio = frame_beta * items_ratio + lex_alpha * ats_audit["ratio"]
            elif has_lex:
                lex_alpha = Decimal("1")
                frame_beta = Decimal("0")
                cat_ratio = ats_audit["ratio"]
            else:
                lex_alpha = Decimal("0")
                frame_beta = Decimal("1")
                cat_ratio = items_ratio
        else:
            lex_alpha = Decimal("0")
            frame_beta = Decimal("1")
            cat_ratio = items_ratio

        earned_pts = w_eff * cat_ratio
        total_exact += earned_pts

        category_results[cat] = {
            "label": label,
            "label_ko": _category_label(cat, "ko", domain_mode),
            "active": True,
            "effective_weight": float(_round2(w_eff)),
            "effective_weight_exact": w_eff,
            "attainment_pct": float(_round1(cat_ratio * Decimal("100"))),
            "earned_points": float(_round2(earned_pts)),
            "earned_points_exact": earned_pts,
            "max_points": float(_round2(w_eff)),
            "item_count": len(items),
        }

        item_pool_pts = w_eff * frame_beta
        for it in items:
            ev = eval_by_id[it["id"]]
            max_item_pts = item_pool_pts * (it["weight"] / item_weight_sum) if item_weight_sum > 0 else Decimal("0")
            cur_item_pts = max_item_pts * ev["multiplier"]
            uplift_full = max_item_pts - cur_item_pts

            cur_idx = GRADE_SEQUENCE.index(ev["grade"])
            if cur_idx < len(GRADE_SEQUENCE) - 1:
                next_grade = GRADE_SEQUENCE[cur_idx + 1]
                uplift_step = max_item_pts * (GRADE_MULTIPLIERS[next_grade] - ev["multiplier"])
            else:
                next_grade = "FULL"
                uplift_step = Decimal("0")

            uplift_transferable_cap = (
                max(Decimal("0"), max_item_pts * Decimal("0.75") - cur_item_pts)
                if ev["gap_type"] == "transferable_gap"
                else Decimal("0")
            )

            item_results.append(
                {
                    "id": it["id"],
                    "category": cat,
                    "title": it["title"],
                    "is_knockout": it["is_knockout"],
                    "weight": float(it["weight"]),
                    "grade": ev["grade"],
                    "multiplier": float(ev["multiplier"]),
                    "max_points_pp": float(_round2(max_item_pts)),
                    "max_points_exact": max_item_pts,
                    "earned_points_pp": float(_round2(cur_item_pts)),
                    "earned_points_exact": cur_item_pts,
                    "uplift_to_full_pp": float(_round2(uplift_full)),
                    "uplift_to_full_exact": uplift_full,
                    "uplift_transferable_cap_pp": float(_round2(uplift_transferable_cap)),
                    "next_grade": next_grade,
                    "uplift_one_step_pp": float(_round2(uplift_step)),
                    "gap_type": ev["gap_type"],
                    "evidence_quote": ev["evidence_quote"],
                    "quote_verified": ev["quote_verified"],
                    "source": ev["source"],
                    "action_hint": ev["action_hint"],
                }
            )

        if cat == "ats_framing":
            kw_pool_pts = w_eff * lex_alpha
            for kw_detail in ats_audit["details"]:
                kw_w = _dec(kw_detail["weight"])
                kw_max = (
                    kw_pool_pts * (kw_w / ats_audit["total_weight"])
                    if ats_audit["total_weight"] > Decimal("0")
                    else Decimal("0")
                )
                kw_detail["uplift_pp"] = float(_round2(Decimal("0") if kw_detail["matched"] else kw_max))
                kw_detail["uplift_exact"] = Decimal("0") if kw_detail["matched"] else kw_max

    # Exact conservation invariant verification
    sum_item_uplifts = sum((r["uplift_to_full_exact"] for r in item_results), Decimal("0"))
    sum_kw_uplifts = sum((d.get("uplift_exact", Decimal("0")) for d in ats_audit["details"]), Decimal("0"))
    conservation_residual = abs((total_exact + sum_item_uplifts + sum_kw_uplifts) - Decimal("100"))
    if conservation_residual > Decimal("0.0001"):
        raise RuntimeError(f"Internal scoring conservation error: residual={conservation_residual}")

    threshold = _dec(rubric.get("pass_threshold", 80.0))
    display_score, passed_threshold = _display_score_safe(total_exact, threshold)

    # Human Calibration #1: Knockout risks trigger on MISSING or WEAK
    knockout_risks = [
        {
            "id": r["id"],
            "title": r["title"],
            "grade": r["grade"],
            "gap_type": r["gap_type"],
            "action_hint": r["action_hint"],
        }
        for r in item_results
        if r["is_knockout"] and r["grade"] in KNOCKOUT_RISK_GRADES
    ]

    if passed_threshold and not knockout_risks:
        pass_status = "PASS"
    elif passed_threshold and knockout_risks:
        pass_status = "PASS_WITH_RISK"
    else:
        pass_status = "REVISE"

    gap_to_pass = max(Decimal("0"), threshold - total_exact)

    # Human Calibration #3 & v1.2 Leak Fix: Dual honest projection range
    true_gap_ids = {r["id"] for r in item_results if r["gap_type"] == "true_gap"}
    expression_gap_ids = {r["id"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "expression_gap"}
    transferable_gap_ids = {r["id"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "transferable_gap"}

    expression_items_uplift = sum(
        (r["uplift_to_full_exact"] for r in item_results if r["grade"] != "FULL" and r["gap_type"] == "expression_gap"),
        Decimal("0"),
    )
    # Transferable gaps conservatively capped at STRONG_PARTIAL (0.75) rather than FULL (1.00)
    transferable_capped_uplift = sum(
        (
            max(Decimal("0"), r["max_points_exact"] * Decimal("0.75") - r["earned_points_exact"])
            for r in item_results
            if r["grade"] != "FULL" and r["gap_type"] == "transferable_gap"
        ),
        Decimal("0"),
    )

    # ATS missing keyword uplift: NEVER leak negated mentions or transferable_gap/true_gap keywords into expression-only projection
    expression_ats_uplift = Decimal("0")
    transferable_ats_uplift = Decimal("0")
    for kw_detail in ats_audit["details"]:
        if kw_detail["matched"] or kw_detail.get("negated_mention", False):
            continue
        linked_id = kw_detail.get("linked_item_id")
        kw_u = kw_detail.get("uplift_exact", Decimal("0"))
        if linked_id:
            if linked_id in true_gap_ids:
                continue
            elif linked_id in transferable_gap_ids:
                transferable_ats_uplift += kw_u
            elif linked_id in expression_gap_ids or linked_id not in true_gap_ids:
                expression_ats_uplift += kw_u
        elif not true_gap_ids:
            expression_ats_uplift += kw_u

    projected_expression_only = min(Decimal("100"), total_exact + expression_items_uplift + expression_ats_uplift)
    projected_with_transferable = min(
        Decimal("100"), projected_expression_only + transferable_capped_uplift + transferable_ats_uplift
    )
    actionable_ats_uplift = expression_ats_uplift
    actionable_uplift_total = (
        expression_items_uplift + expression_ats_uplift + transferable_capped_uplift + transferable_ats_uplift
    )

    # Round tracking & diff
    prior_rounds = list(history.get("rounds", [])) if history else []
    round_num = int(eval_data.get("round", len(prior_rounds) + 1))
    earlier_rounds = [r for r in prior_rounds if int(r["round"]) < round_num]
    later_rounds = [int(r["round"]) for r in prior_rounds if int(r["round"]) > round_num]
    prev_round = earlier_rounds[-1] if earlier_rounds else None

    grace_tier_used_current = eval_data.get("grace_tier_used")
    if grace_tier_used_current is not None:
        grace_tier_used_current = int(grace_tier_used_current)
        if grace_tier_used_current not in (1, 2, 3):
            raise ValueError(f"grace_tier_used must be 1, 2, or 3, got {grace_tier_used_current}")

    prev_items_map: dict[str, dict[str, Any]] = {}
    if prev_round:
        prev_items_map = {it["id"]: it for it in prev_round.get("items", [])}

    resolved_items: list[dict[str, Any]] = []
    improved_items: list[dict[str, Any]] = []
    regressed_items: list[dict[str, Any]] = []
    stalled_items: list[dict[str, Any]] = []
    actionable_stalled_items: list[dict[str, Any]] = []

    for r in item_results:
        mult = GRADE_MULTIPLIERS[r["grade"]]
        prev = prev_items_map.get(r["id"])
        if prev is None:
            streak = 1 if mult <= Decimal("0.50") else 0
            r["prev_grade"] = None
            r["stalled_streak"] = streak
        else:
            prev_grade = prev["grade"]
            prev_mult = GRADE_MULTIPLIERS[prev_grade]
            prev_streak = int(prev.get("stalled_streak", 1 if prev_mult <= Decimal("0.50") else 0))
            r["prev_grade"] = prev_grade

            if mult > prev_mult:
                delta_pts = _round2(r["earned_points_exact"] - _dec(prev.get("earned_points_pp", 0)))
                change = {
                    "id": r["id"],
                    "title": r["title"],
                    "from": prev_grade,
                    "to": r["grade"],
                    "delta_pp": float(delta_pts),
                }
                improved_items.append(change)
                if r["grade"] == "FULL":
                    resolved_items.append(change)
            elif mult < prev_mult:
                delta_pts = _round2(r["earned_points_exact"] - _dec(prev.get("earned_points_pp", 0)))
                regressed_items.append(
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "from": prev_grade,
                        "to": r["grade"],
                        "delta_pp": float(delta_pts),
                    }
                )

            if mult > Decimal("0.50"):
                streak = 0
            elif mult <= prev_mult:
                streak = prev_streak + 1
            else:
                streak = 1
            r["stalled_streak"] = streak

        if r["stalled_streak"] >= 2 and r["gap_type"] != "true_gap":
            stalled_entry = {
                "id": r["id"],
                "title": r["title"],
                "grade": r["grade"],
                "gap_type": r["gap_type"],
                "stalled_streak": r["stalled_streak"],
                "uplift_to_full_pp": r["uplift_to_full_pp"],
            }
            stalled_items.append(stalled_entry)
            actionable_stalled_items.append(stalled_entry)

    if prev_round:
        prev_total_exact = _dec(prev_round.get("total_score_exact", prev_round["total_score"]))
        prev_score_display = _dec(prev_round["total_score"])
        delta_score_exact = total_exact - prev_total_exact
        # Keep headline delta strictly consistent with displayed 1-decimal scoreboard (prev + delta == curr)
        delta_score_display = _round1(display_score - prev_score_display)
        cat_deltas: dict[str, float | None] = {}
        prev_cats = prev_round.get("categories", {})
        for cat in CATEGORY_ORDER:
            if category_results[cat]["active"] and prev_cats.get(cat, {}).get("active"):
                c_delta = _round1(
                    _round1(category_results[cat]["earned_points_exact"])
                    - _round1(_dec(prev_cats[cat]["earned_points"]))
                )
                cat_deltas[cat] = float(c_delta)
            else:
                cat_deltas[cat] = None
    else:
        delta_score_exact = None
        delta_score_display = None
        prev_score_display = None
        cat_deltas = {cat: None for cat in CATEGORY_ORDER}

    # Grace recommendation engine (never fires when 0 actionable gaps remain!)
    has_actionable_headroom = (expression_items_uplift > Decimal("0")) or (transferable_capped_uplift > Decimal("0"))
    honest_fit_advisory = (pass_status == "REVISE") and (not has_actionable_headroom)

    should_offer_grace = False
    grace_reasons: list[str] = []
    if pass_status == "REVISE" and round_num >= 2 and has_actionable_headroom:
        if actionable_stalled_items:
            should_offer_grace = True
            names = ", ".join(f"{it['id']}({it['title']})" for it in actionable_stalled_items[:3])
            if lang == "en":
                grace_reasons.append(f"Actionable item(s) stalled for 2+ rounds: {names}")
            else:
                grace_reasons.append(f"동일 보완 가능 항목이 2라운드 이상 정체됨: {names}")
        if delta_score_exact is not None and delta_score_exact < Decimal("3.0"):
            should_offer_grace = True
            d_str = f"{delta_score_display:+.1f}%p"
            if lang == "en":
                grace_reasons.append(f"Round-over-round gain below +3.0%p ({d_str})")
            else:
                grace_reasons.append(f"직전 라운드 대비 점수 상승폭이 +3.0%p 미만 ({d_str})")

    prior_grace_tiers = [int(r["grace_tier_used"]) for r in earlier_rounds if r.get("grace_tier_used")]
    if grace_tier_used_current:
        prior_grace_tiers.append(grace_tier_used_current)
    max_prior_grace = max(prior_grace_tiers, default=0)
    max_actionable_streak = max((it["stalled_streak"] for it in actionable_stalled_items), default=0)

    if not should_offer_grace:
        suggested_tier = None
    elif max_prior_grace >= 2 or max_actionable_streak >= 4:
        suggested_tier = 3
    elif max_prior_grace >= 1 or max_actionable_streak >= 3 or round_num >= 4:
        suggested_tier = 2
    else:
        suggested_tier = 1

    grace_recommendation = {
        "should_offer": should_offer_grace,
        "suggested_tier": suggested_tier,
        "honest_fit_advisory": honest_fit_advisory,
        "reasons": grace_reasons,
        "stalled_item_ids": [it["id"] for it in actionable_stalled_items],
    }

    # Priority ordering: Knockout risks (MISSING/WEAK) FIRST, then highest uplift, then gap_rank
    gap_rank = {"expression_gap": 0, "transferable_gap": 1, "true_gap": 2, None: 3}
    top_priorities = sorted(
        [r for r in item_results if r["grade"] != "FULL"],
        key=lambda r: (
            0 if (r["is_knockout"] and r["grade"] in KNOCKOUT_RISK_GRADES) else 1,
            -r["uplift_to_full_pp"],
            gap_rank.get(r["gap_type"], 3),
            r["id"],
        ),
    )

    clean_categories = {}
    for cat, data in category_results.items():
        clean_categories[cat] = {k: v for k, v in data.items() if not k.endswith("_exact")}
        clean_categories[cat]["delta_points_pp"] = cat_deltas[cat]

    clean_items = [{k: v for k, v in r.items() if not k.endswith("_exact")} for r in item_results]
    clean_priorities = [{k: v for k, v in r.items() if not k.endswith("_exact")} for r in top_priorities]
    clean_kw_details = [{k: v for k, v in d.items() if not k.endswith("_exact")} for d in ats_audit["details"]]

    result = {
        "session": {
            "company": rubric.get("company", ""),
            "role_title": rubric.get("role_title", ""),
            "language": lang,
            "domain_mode": domain_mode,
            "rubric_hash": current_hash,
        },
        "round": round_num,
        "grace_tier_used": grace_tier_used_current,
        "evaluated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pass_threshold": float(_round1(threshold)),
        "total_score": float(display_score),
        "total_score_2dp": float(_round2(total_exact)),
        "total_score_exact": str(total_exact.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)),
        "pass_status": pass_status,
        "passed_threshold": passed_threshold,
        "gap_to_pass_pp": float(_round1(gap_to_pass)) if gap_to_pass > Decimal("0") else 0.0,
        "must_have_attainment_pct": clean_categories["must_have"]["attainment_pct"],
        "projected_expression_only_score": float(_round1(projected_expression_only)),
        "projected_with_transferable_cap": float(_round1(projected_with_transferable)),
        "projected_score_without_true_gaps": float(_round1(projected_with_transferable)),
        "actionable_expression_uplift_pp": float(_round1(expression_items_uplift + actionable_ats_uplift)),
        "actionable_transferable_cap_uplift_pp": float(_round1(transferable_capped_uplift)),
        "actionable_uplift_total_pp": float(_round1(actionable_uplift_total)),
        "missing_ats_uplift_pp": float(_round1(sum_kw_uplifts)),
        "knockout_risks": knockout_risks,
        "unverified_quotes": unverified_quotes,
        "rubric_warnings": rubric_warnings,
        "invalidated_subsequent_rounds": later_rounds,
        "categories": clean_categories,
        "ats_keywords": {
            "checked": ats_audit["checked"],
            "total_count": ats_audit["total_count"],
            "matched_count": ats_audit["matched_count"],
            "coverage_pct": ats_audit["coverage_pct"],
            "missing_must": [d for d in clean_kw_details if not d["matched"] and d["tier"] == "must"],
            "missing_preferred": [d for d in clean_kw_details if not d["matched"] and d["tier"] == "preferred"],
            "negated_mentions": [d for d in clean_kw_details if d.get("negated_mention")],
            "contradictory_mentions": [d for d in clean_kw_details if d.get("contradictory_mention")],
            "details": clean_kw_details,
        },
        "round_diff": {
            "has_previous": prev_round is not None,
            "previous_round": prev_round["round"] if prev_round else None,
            "previous_score": float(prev_score_display) if prev_score_display is not None else None,
            "delta_score_pp": float(delta_score_display) if delta_score_display is not None else None,
            "delta_score_exact_2dp": float(_round2(delta_score_exact)) if delta_score_exact is not None else None,
            "resolved_items": resolved_items,
            "improved_items": improved_items,
            "regressed_items": regressed_items,
            "stalled_items": stalled_items,
        },
        "grace_recommendation": grace_recommendation,
        "top_priorities": clean_priorities,
        "items": clean_items,
    }
    return result


def _category_status_badge(attainment: float, lang: str) -> str:
    if attainment >= 85.0:
        return "우수" if lang == "ko" else "Strong"
    if attainment >= 70.0:
        return "양호" if lang == "ko" else "Solid"
    if attainment >= 50.0:
        return "보강 필요" if lang == "ko" else "Needs Work"
    return "취약" if lang == "ko" else "Weak"


def render_markdown_report(res: dict[str, Any]) -> str:
    """Render standardized Markdown report (ko or en) with strict ROUND_HALF_UP formatting and CTA."""
    lang = res["session"].get("language", "ko")
    company = res["session"]["company"]
    role = res["session"]["role_title"]
    header_target = " · ".join(p for p in (company, role) if p) or "Target JD"

    if lang == "en":
        badges = {
            "PASS": "✅ **PASS** (Ready to Apply)",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK** (Threshold Met · Knockout Requirement Risk)",
            "REVISE": "🔁 **REVISE** (Self-Revision Recommended)",
        }
        lines = [
            f"# JD Match Diagnostic — Round {res['round']} ({header_target})",
            "",
            f"- **Overall Match Score:** **{_fmt1(res['total_score'])}%** / Pass Threshold **{_fmt1(res['pass_threshold'])}%** — {badges[res['pass_status']]}",
        ]
        if res["round_diff"]["has_previous"]:
            d = res["round_diff"]["delta_score_pp"]
            sign = "+" if d >= 0 else ""
            lines.append(
                f"- **Round-over-Round (Round {res['round_diff']['previous_round']} → {res['round']}):** "
                f"`{_fmt1(res['round_diff']['previous_score'])}% → {_fmt1(res['total_score'])}% ({sign}{_fmt1(d)}%p)`"
            )
        if res["pass_status"] == "REVISE":
            lines.append(f"- **Gap to Pass:** `+{_fmt1(res['gap_to_pass_pp'])}%p`")
            lo = _fmt1(res["projected_expression_only_score"])
            hi = _fmt1(res["projected_with_transferable_cap"])
            if lo == hi:
                lines.append(f"- **Honest Reachable Score (Expression Fixes):** `{lo}%`")
            else:
                lines.append(
                    f"- **Honest Reachable Score Range:** `{lo}%` (expression fixes only) ~ `{hi}%` "
                    f"(incl. transferable skills capped at STRONG_PARTIAL)"
                )
        if res["must_have_attainment_pct"] is not None:
            lines.append(f"- **Must-Have Attainment:** `{_fmt1(res['must_have_attainment_pct'])}%`")
        if res["ats_keywords"]["checked"]:
            ak = res["ats_keywords"]
            lines.append(
                f"- **ATS Keyword Coverage:** `{ak['matched_count']}/{ak['total_count']}` (`{_fmt1(ak['coverage_pct'])}%`)"
            )
        lines.append(f"- **Rubric Lock Hash:** `{res['session']['rubric_hash']}`")
        lines.append("")
        lines.extend(
            [
                "## Category Breakdown",
                "",
                "| Category | Weight | Attainment | Earned / Max | Round Δ | Status |",
                "| :--- | :---: | :---: | :---: | :---: | :---: |",
            ]
        )
    else:
        badges = {
            "PASS": "✅ **PASS** (지원 준비 완료)",
            "PASS_WITH_RISK": "⚠️ **PASS_WITH_RISK** (80% 도달 · 핵심 필수요건 위험 경고)",
            "REVISE": "🔁 **REVISE** (보완 후 재검토 필요)",
        }
        lines = [
            f"# 채용공고 일치율 진단 — Round {res['round']} ({header_target})",
            "",
            f"- **종합 일치율:** **{_fmt1(res['total_score'])}%** / 합격 기준 **{_fmt1(res['pass_threshold'])}%** — {badges[res['pass_status']]}",
        ]
        if res["round_diff"]["has_previous"]:
            d = res["round_diff"]["delta_score_pp"]
            sign = "+" if d >= 0 else ""
            lines.append(
                f"- **직전 라운드 대비 (Round {res['round_diff']['previous_round']} → {res['round']}):** "
                f"`{_fmt1(res['round_diff']['previous_score'])}% → {_fmt1(res['total_score'])}% ({sign}{_fmt1(d)}%p)`"
            )
        if res["pass_status"] == "REVISE":
            lines.append(f"- **합격선까지 남은 점수:** `+{_fmt1(res['gap_to_pass_pp'])}%p`")
            lo = _fmt1(res["projected_expression_only_score"])
            hi = _fmt1(res["projected_with_transferable_cap"])
            if lo == hi:
                lines.append(f"- **표현·증빙 보강만으로 도달 가능 점수:** `{lo}%` (보강 가능 폭 `+{_fmt1(res['actionable_expression_uplift_pp'])}%p`)")
            else:
                lines.append(
                    f"- **정직한 도달 가능 점수 범위:** `{lo}%` (표현 보강 확실치) ~ `{hi}%` "
                    f"(유사·전이 역량 최대 `STRONG_PARTIAL` 반영 시)"
                )
        if res["must_have_attainment_pct"] is not None:
            lines.append(f"- **필수 자격(Must-Have) 충족률:** `{_fmt1(res['must_have_attainment_pct'])}%`")
        if res["ats_keywords"]["checked"]:
            ak = res["ats_keywords"]
            lines.append(
                f"- **ATS 핵심 키워드 커버리지:** `{ak['matched_count']}/{ak['total_count']}` (`{_fmt1(ak['coverage_pct'])}%`)"
            )
        lines.append(f"- **Rubric Lock Hash:** `{res['session']['rubric_hash']}`")
        lines.append("")
        lines.extend(
            [
                "## 영역별 상세 점수",
                "",
                "| 평가 영역 | 배점 비중 | 충족률 | 획득 점수 | Round Δ | 상태 |",
                "| :--- | :---: | :---: | :---: | :---: | :---: |",
            ]
        )

    for cat in CATEGORY_ORDER:
        c = res["categories"][cat]
        if not c["active"]:
            continue
        delta_str = "—"
        if c["delta_points_pp"] is not None:
            dsign = "+" if c["delta_points_pp"] >= 0 else ""
            delta_str = f"{dsign}{_fmt1(c['delta_points_pp'])}%p"
        status_txt = _category_status_badge(c["attainment_pct"], lang)
        lines.append(
            f"| {c['label']} (`{cat}`) | {_fmt1(c['effective_weight'])}% | "
            f"{_fmt1(c['attainment_pct'])}% | {_fmt1(c['earned_points'])} / {_fmt1(c['max_points'])} | {delta_str} | {status_txt} |"
        )
    lines.append("")

    # Knockout risk warning
    if res["knockout_risks"]:
        lines.append("> [!WARNING]")
        if lang == "en":
            lines.append("> **Critical Knockout Risk Detected (`MISSING` or `WEAK`):** High risk of automated/initial screening rejection unless substantiated.")
        else:
            lines.append("> **핵심 필수 요건(Knockout) 위험 감지 (`MISSING` 또는 `WEAK`):** 실제 보유 역량이라면 구체적 프로젝트 근거로 반드시 보강해 주세요.")
        for kr in res["knockout_risks"]:
            lines.append(f"> - **`{kr['id']}` {kr['title']}** (`{kr['grade']}` · `{kr['gap_type']}`): {kr['action_hint']}")
        lines.append("")

    # Unverified quote audit warning
    if res["unverified_quotes"]:
        lines.append("> [!NOTE]")
        ids = ", ".join(q["id"] for q in res["unverified_quotes"])
        if lang == "en":
            lines.append(f"> **Quote Verification Audit:** Item(s) `{ids}` had non-verbatim or paraphrased `evidence_quote` against candidate text.")
        else:
            lines.append(f"> **원문 근거 자동 검증 참고:** `{ids}` 항목의 `evidence_quote`가 제출 문서 원문과 완전히 일치하지 않습니다. 원문 그대로 발췌했는지 재확인하세요.")
        lines.append("")

    # Round diff section
    if res["round_diff"]["has_previous"]:
        rd = res["round_diff"]
        lines.append(
            f"## Round {rd['previous_round']} → Round {res['round']} "
            + ("Progress Summary" if lang == "en" else "변화 요약")
        )
        lines.append("")
        if rd["improved_items"]:
            lines.append("- **Improved / Resolved:**" if lang == "en" else "- **개선/해결된 항목:**")
            for it in rd["improved_items"]:
                badge = " ✅" if it["to"] == "FULL" else ""
                lines.append(
                    f"  - `{it['id']}` {it['title']}: `{it['from']} → {it['to']}` (`+{_fmt1(it['delta_pp'])}%p`){badge}"
                )
        else:
            lines.append("- **Improved / Resolved:** None" if lang == "en" else "- **개선/해결된 항목:** 없음")
        if rd["regressed_items"]:
            lines.append(
                "- **⚠️ Regressed Items (check for accidental deletions):**"
                if lang == "en"
                else "- **⚠️ 점수 하락 항목 (의도치 않은 삭제 여부 확인):**"
            )
            for it in rd["regressed_items"]:
                lines.append(
                    f"  - `{it['id']}` {it['title']}: `{it['from']} → {it['to']}` (`{_fmt1(it['delta_pp'])}%p`)"
                )
        if rd["stalled_items"] and res["pass_status"] != "PASS":
            lines.append(
                "- **Stalled Actionable Items (2+ consecutive rounds `<= PARTIAL`):**"
                if lang == "en"
                else "- **정체 항목 (보완 가능 항목 2라운드 이상 `<= PARTIAL` 유지):**"
            )
            for it in rd["stalled_items"]:
                lines.append(
                    f"  - `{it['id']}` {it['title']} (`{it['grade']}`, {it['stalled_streak']}R, `{it['gap_type']}`, max `+{_fmt1(it['uplift_to_full_pp'])}%p`)"
                )
        lines.append("")

    # Priority coaching guide
    if res["top_priorities"]:
        lines.append("## Priority Revision Guide (Coach-First)" if lang == "en" else "## 우선순위 보완 가이드 (직접 수정 포인트)")
        lines.append("")
        gap_sections = (
            [
                ("expression_gap", "🎯 Expression & Evidence Fixes (Fastest Score Gains)"),
                ("transferable_gap", "🌉 Transferable Experience Bridging"),
                ("true_gap", "🧭 True Capability Gaps (Zero Fabrication)"),
            ]
            if lang == "en"
            else [
                ("expression_gap", "🎯 표현·증빙 보강 (빠른 점수 상승 가능)"),
                ("transferable_gap", "🌉 유사·전이 역량 연결 필요"),
                ("true_gap", "🧭 실제 미보유 역량 점검 (창작·과장 금지)"),
            ]
        )
        for gtype, heading in gap_sections:
            group = [p for p in res["top_priorities"] if p["gap_type"] == gtype]
            if not group:
                continue
            lines.append(f"### {heading}")
            lines.append("")
            for idx, item in enumerate(group, start=1):
                ko_tag = " **[KNOCKOUT]**" if item["is_knockout"] else ""
                show_stall = (
                    item["stalled_streak"] >= 2
                    and res["pass_status"] != "PASS"
                    and item["gap_type"] != "true_gap"
                )
                stall_tag = (
                    f" *(⚠️ {item['stalled_streak']}R stalled)*"
                    if (show_stall and lang == "en")
                    else (f" *(⚠️ {item['stalled_streak']}R 정체)*" if show_stall else "")
                )
                if lang == "en":
                    lines.append(
                        f"{idx}. **`{item['id']}` {item['title']}**{ko_tag}{stall_tag} — "
                        f"Current `{item['grade']}` · Up to **`+{_fmt1(item['uplift_to_full_pp'])}%p`**"
                    )
                    if item["evidence_quote"]:
                        src = f" ({item['source']})" if item["source"] else ""
                        lines.append(f"   - **Current Evidence{src}:** \"{item['evidence_quote']}\"")
                    else:
                        lines.append("   - **Current Evidence:** Not found in submitted documents")
                    if item["action_hint"]:
                        lines.append(f"   - **Revision Direction:** {item['action_hint']}")
                else:
                    lines.append(
                        f"{idx}. **`{item['id']}` {item['title']}**{ko_tag}{stall_tag} — "
                        f"현재 `{item['grade']}` · 보완 시 최대 **`+{_fmt1(item['uplift_to_full_pp'])}%p`**"
                    )
                    if item["evidence_quote"]:
                        src = f" ({item['source']})" if item["source"] else ""
                        lines.append(f"   - **현재 근거{src}:** \"{item['evidence_quote']}\"")
                    else:
                        lines.append("   - **현재 근거:** 제출 문서에서 확인되지 않음")
                    if item["action_hint"]:
                        lines.append(f"   - **수정 포인트:** {item['action_hint']}")
            lines.append("")

    # ATS missing & contradictory keywords
    if res["ats_keywords"]["checked"]:
        mm = res["ats_keywords"]["missing_must"]
        mp = res["ats_keywords"]["missing_preferred"]
        neg = res["ats_keywords"]["negated_mentions"]
        contra = res["ats_keywords"].get("contradictory_mentions", [])
        if mm or mp or contra:
            lines.append("## JD Keywords Audit (ATS Lexical Scan)" if lang == "en" else "## JD 키워드 점검 (ATS 스캔)")
            lines.append("")
            if contra:
                c_terms = ", ".join(f"`{k['term']}`" for k in contra)
                lines.append("> [!WARNING]")
                lines.append(
                    f"> **Self-Contradictory Keyword Warning:** {c_terms} appeared in BOTH positive (skills/claims) and negative (unexperienced) sections of the document. Remove unverified claims to protect credibility."
                    if lang == "en"
                    else f"> **문서 내 자기모순 키워드 경고:** {c_terms} 키워드가 '보유/스킬' 문맥과 '미경험/부정' 문맥에 동시에 등장했습니다. 서류 신뢰도를 위해 실제 미보유 항목은 스킬란에서 제거하세요."
                )
                lines.append("")
            if mm:
                fmt = ", ".join(
                    f"`{k['term']}`" + (f" ({'/'.join(k['aliases'])})" if k["aliases"] else "")
                    for k in mm
                )
                lines.append(f"- **Missing Must Keywords:** {fmt}" if lang == "en" else f"- **필수 키워드 미반영:** {fmt}")
            if mp:
                fmt = ", ".join(
                    f"`{k['term']}`" + (f" ({'/'.join(k['aliases'])})" if k["aliases"] else "")
                    for k in mp
                )
                lines.append(f"- **Missing Preferred Keywords:** {fmt}" if lang == "en" else f"- **우대 키워드 미반영:** {fmt}")
            if neg:
                neg_terms = ", ".join(f"`{k['term']}`" for k in neg)
                lines.append(
                    f"- *Note: {neg_terms} appeared only inside negative/unexperienced phrasing and were correctly excluded.*"
                    if lang == "en"
                    else f"- *참고: {neg_terms} 키워드는 미경험/부정 문맥에서만 확인되어 매칭에서 정확히 제외되었습니다.*"
                )
            lines.append(
                "- *Include only verified terms inside real project context; bare skills-list stuffing is capped at `WEAK (0.25)`.*"
                if lang == "en"
                else "- *실제 경험·사용 사실이 있는 키워드만 구체적 프로젝트 맥락 안에 반영하세요. 근거 없는 스킬 나열은 `WEAK(0.25)` 상한이 적용됩니다.*"
            )
            lines.append("")

    # Next-step top-3 mission + CTA + optional Grace / honest-fit advisory
    gr = res["grace_recommendation"]
    if res["pass_status"] == "REVISE":
        actionable_top3 = [p for p in res["top_priorities"] if p["gap_type"] != "true_gap"][:3]
        if actionable_top3:
            can_reach = _dec(res["projected_with_transferable_cap"]) >= _dec(res["pass_threshold"])
            if lang == "en":
                mission_heading = (
                    "## Next Round Fastest Path Mission (Top 3)"
                    if can_reach
                    else f"## Highest-Impact Fixes (Threshold {_fmt1(res['pass_threshold'])}% Unlikely Without True Gaps)"
                )
            else:
                mission_heading = (
                    f"## 이번 라운드 핵심 미션 (최단 {_fmt1(res['pass_threshold'])}% 돌파 TOP 3)"
                    if can_reach
                    else f"## 최대 보강 가능 항목 (표현·유사경험 보강만으로 {_fmt1(res['pass_threshold'])}% 단독 도달 어려움)"
                )
            lines.append(mission_heading)
            lines.append("")
            for i, p in enumerate(actionable_top3, start=1):
                if p["gap_type"] == "transferable_gap" and p.get("uplift_transferable_cap_pp", 0) > 0:
                    gain_txt = (
                        f"realistic cap `+{_fmt1(p['uplift_transferable_cap_pp'])}%p` (full `+{_fmt1(p['uplift_to_full_pp'])}%p`)"
                        if lang == "en"
                        else f"유사경험 현실 상한 `+{_fmt1(p['uplift_transferable_cap_pp'])}%p` (FULL 기준 `+{_fmt1(p['uplift_to_full_pp'])}%p`)"
                    )
                else:
                    gain_txt = (
                        f"up to `+{_fmt1(p['uplift_to_full_pp'])}%p`"
                        if lang == "en"
                        else f"최대 `+{_fmt1(p['uplift_to_full_pp'])}%p`"
                    )
                lines.append(f"{i}. **`{p['id']}` {p['title']}** (`{p['grade']}` · {gain_txt})")
            lines.append("")
        if gr["honest_fit_advisory"]:
            lines.extend(
                [
                    "> [!IMPORTANT]",
                    (
                        "> **Honest Role-Fit Advisory:** All remaining gaps are `true_gap` items (zero actionable wording gaps left). "
                        "Rather than fabricating missing qualifications, consider building a small genuine portfolio proof or targeting better-aligned postings."
                        if lang == "en"
                        else "> **정직한 직무 적합도 안내:** 남은 미충족 항목이 모두 실제 미보유 역량(`true_gap`)입니다. "
                        "표현 수정만으로 80%를 인위적으로 맞추려 하기보다, 소규모 실전 포트폴리오 보강 또는 보유 강점이 더 잘 맞는 공고 병행 지원을 권장합니다."
                    ),
                    "",
                ]
            )
        elif gr["should_offer"]:
            lines.extend(
                [
                    "> [!TIP]",
                    (
                        f"> **Grace Assistance Available (Suggested: Tier {gr['suggested_tier']}):** " + " / ".join(gr["reasons"])
                        if lang == "en"
                        else f"> **보조 모드(Grace) 제안 (권장 시작: Tier {gr['suggested_tier']}):** " + " / ".join(gr["reasons"])
                    ),
                    (
                        "> Keep revising on your own, or opt in to **Tier 1 (Questions + Skeleton) / Tier 2 (Fact-Grounded Options A·B) / Tier 3 (Targeted Pair-Draft)** whenever you feel stuck."
                        if lang == "en"
                        else "> 직접 더 다듬어 보셔도 좋고, 막히는 항목이 있다면 **1단계(질문+뼈대) / 2단계(사실 기반 표현 A·B안) / 3단계(특정 항목 공동 초안)** 중 원하시는 단계로 바로 보조해 드릴 수 있습니다."
                    ),
                    "",
                ]
            )
        else:
            next_r = res["round"] + 1
            lines.append(
                f"*Revise your resume/portfolio based on the pointers above and submit for **Round {next_r}** re-evaluation. Ask for Grace coaching anytime if you get stuck.*"
                if lang == "en"
                else f"*위 포인트를 반영해 이력서/포트폴리오를 직접 수정하신 뒤 **Round {next_r}** 재평가를 요청해 주세요. 막히는 항목이 있으면 언제든 보조 모드(Grace 1~3단계)를 요청하실 수 있습니다.*"
            )
            lines.append("")
    elif res["pass_status"] == "PASS_WITH_RISK":
        lines.append(
            "*You cleared the overall threshold, but please review the Knockout Risk warning above before submitting.*"
            if lang == "en"
            else "*종합 점수는 합격선을 넘겼습니다. 다만 위 Knockout 필수요건 경고를 확인하신 뒤, 실제 보유 역량이라면 간단히 반영해 최종 재점검하시는 것을 권장합니다.*"
        )
        lines.append("")
    else:
        lines.append(
            "*Congratulations! Your application passed the locked rubric threshold with zero knockout risks.*"
            if lang == "en"
            else "*축하합니다! 잠금 루브릭 기준 합격선을 돌파했으며 핵심 Knockout 누락도 없습니다. 강점 항목을 면접 핵심 어필 포인트로 활용해 보세요.*"
        )
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def update_history(history_path: Path, result: dict[str, Any]) -> dict[str, Any]:
    """Persist round result idempotently; drops stale subsequent rounds if an earlier round is re-run."""
    if history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8-sig"))
    else:
        history = {
            "session": result["session"],
            "rubric_hash": result["session"]["rubric_hash"],
            "pass_threshold": result["pass_threshold"],
            "rounds": [],
        }

    cur_round = int(result["round"])
    # Keep strictly earlier rounds so re-running round N never leaves stale N+1.. rounds behind
    rounds = [r for r in history.get("rounds", []) if int(r["round"]) < cur_round]
    rounds.append(
        {
            "round": cur_round,
            "evaluated_at": result["evaluated_at"],
            "total_score": result["total_score"],
            "total_score_2dp": result["total_score_2dp"],
            "total_score_exact": result["total_score_exact"],
            "pass_status": result["pass_status"],
            "grace_tier_used": result.get("grace_tier_used"),
            "categories": result["categories"],
            "items": [
                {
                    "id": it["id"],
                    "grade": it["grade"],
                    "earned_points_pp": it["earned_points_pp"],
                    "gap_type": it["gap_type"],
                    "stalled_streak": it["stalled_streak"],
                }
                for it in result["items"]
            ],
            "grace_recommended": result["grace_recommendation"]["should_offer"],
        }
    )
    rounds.sort(key=lambda r: int(r["round"]))
    history["rounds"] = rounds

    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return history


def init_rubric_command(rubric_path: Path) -> int:
    rubric = json.loads(rubric_path.read_text(encoding="utf-8-sig"))
    item_map, warnings = validate_rubric(rubric)
    rhash = compute_rubric_hash(rubric)
    rubric["rubric_hash"] = rhash
    rubric["locked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rubric_path.write_text(json.dumps(rubric, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {cat: len(rubric.get("categories", {}).get(cat, [])) for cat in CATEGORY_ORDER}
    summary = {
        "status": "RUBRIC_LOCKED",
        "rubric_path": str(rubric_path.resolve()),
        "rubric_hash": rhash,
        "language": str(rubric.get("language", "ko")).lower(),
        "domain_mode": str(rubric.get("domain_mode", "portfolio")).lower(),
        "pass_threshold": float(_round1(_dec(rubric.get("pass_threshold", 80.0)))),
        "total_items": len(item_map),
        "category_item_counts": counts,
        "keyword_count": len(rubric.get("keywords", [])),
        "warnings": warnings,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Deterministic rubric lock & match scorer for resume-jd-coach (v1.2).")
    parser.add_argument("--init-rubric", help="Validate and stamp rubric_hash onto rubric.json, then exit.")
    parser.add_argument("--rubric", help="Path to locked rubric.json.")
    parser.add_argument("--eval", dest="eval_path", help="Path to round_NN_eval.json.")
    parser.add_argument("--candidate-text", help="Path to consolidated plain-text candidate resume+portfolio.")
    parser.add_argument("--history", help="Path to session history.json (read prior rounds & append current).")
    parser.add_argument("--report-out", help="Optional path to write rendered Markdown coaching report.")
    parser.add_argument("--lang", choices=["ko", "en"], help="Override report language (default from rubric.json or ko).")
    parser.add_argument(
        "--domain-mode",
        choices=["portfolio", "resume_only"],
        help="Override portfolio_impact category label mode (portfolio vs resume_only).",
    )
    parser.add_argument(
        "--strict-quotes",
        action="store_true",
        help="Fail with non-zero exit code if any evidence_quote cannot be verified against --candidate-text.",
    )
    args = parser.parse_args()

    if args.init_rubric:
        return init_rubric_command(Path(args.init_rubric))

    if not args.rubric or not args.eval_path:
        parser.error("Provide either --init-rubric <path> OR both --rubric <path> and --eval <path>.")

    rubric_path = Path(args.rubric)
    eval_path = Path(args.eval_path)
    rubric = json.loads(rubric_path.read_text(encoding="utf-8-sig"))
    eval_data = json.loads(eval_path.read_text(encoding="utf-8-sig"))

    candidate_text = None
    if args.candidate_text:
        candidate_text = Path(args.candidate_text).read_text(encoding="utf-8-sig")

    history = None
    history_path = Path(args.history) if args.history else None
    if history_path and history_path.exists():
        history = json.loads(history_path.read_text(encoding="utf-8-sig"))

    result = evaluate_round(
        rubric,
        eval_data,
        candidate_text=candidate_text,
        history=history,
        require_locked=True,
        strict_quotes=args.strict_quotes,
        lang_override=args.lang,
        domain_mode_override=args.domain_mode,
    )

    if history_path:
        update_history(history_path, result)

    if args.report_out:
        report_path = Path(args.report_out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_markdown_report(result), encoding="utf-8")
        result["report_path"] = str(report_path.resolve())

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
