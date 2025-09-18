# src/summarizer/citation_mapper.py
"""
Lightweight citation extraction for pre-alpha.

Goals:
- Detect numeric citations like: [1], [1,3], [2–4], [2-4, 7]
- Detect author–year citations like: (Smith, 2020), (Smith & Doe, 2019),
  (Smith et al., 2018), and multiple within one pair of parentheses separated
  by ';' or ','.
- Optionally map numeric citations to reference entries if the references_text
  contains numbered items.

This is intentionally heuristic. We’ll replace/augment with a proper parser later.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List

# Matches blocks like [1], [1,3], [2-4], [2–4, 7]
BRACKET_BLOCK = re.compile(r"\[([0-9,\-\s–]+)\]")

# Matches items like (Smith, 2020), (Smith & Doe, 2019), (Smith et al., 2018)
# and will pull out the inner chunk. We later split on ';' or ',' between author-year pairs carefully.
AUTHORYEAR_BLOCK = re.compile(r"\(([^()]*\b\d{4}[^()]*)\)")

# A single author-year pattern (liberal but biased toward common academic styles)
SINGLE_AUTHORYEAR = re.compile(
    r"""
    ^\s*
    (?P<author>[A-Z][A-Za-z\-]+                                   # First surname
       (?:\s*&\s*[A-Z][A-Za-z\-]+                                 #  & Second
        |(?:\s+et\s+al\.)                                         #  et al.
        |(?:\s*,\s*[A-Z][A-Za-z\-]+)*)                            #  , Additional
    )
    \s*,\s*
    (?P<year>(19|20)\d{2}[a-z]?)                                   # 2020 or 2020a
    \s*$
    """,
    re.X,
)

# Reference-line matcher for numbered references (very loose):
# [1] Foo..., or 1. Foo..., or 1) Foo...
REF_LINE_NUM = re.compile(r"^\s*(?:\[(?P<b>\d{1,3})\]|(?P<p>\d{1,3})[.)])\s+(?P<rest>.+)$")


def _expand_bracket_block(block: str) -> Iterable[int]:
    """
    Expand content inside a numeric citation block into individual integers.
    e.g., "1,3, 5-7" -> [1,3,5,6,7]
    """
    # normalize en-dash to hyphen
    block = block.replace("–", "-")
    pieces = [p.strip() for p in block.split(",") if p.strip()]
    for piece in pieces:
        if "-" in piece:
            try:
                start_s, end_s = [s.strip() for s in piece.split("-", 1)]
                start, end = int(start_s), int(end_s)
                if start <= end and 1 <= start <= 999 and 1 <= end <= 999 and (end - start) < 500:
                    for n in range(start, end + 1):
                        yield n
                else:
                    # fall back to individual parse if range is weird
                    for n_s in (start_s, end_s):
                        if n_s.isdigit():
                            n = int(n_s)
                            if 1 <= n <= 999:
                                yield n
            except Exception:
                # ignore malformed range
                continue
        else:
            if piece.isdigit():
                n = int(piece)
                if 1 <= n <= 999:
                    yield n


def _parse_reference_index(references_text: str) -> Dict[int, str]:
    """
    Build a simple index {number: reference line} from references_text.

    This is a naive single-line parser; multi-line entries will be improved later.
    """
    index: Dict[int, str] = {}
    if not references_text:
        return index

    for line in references_text.splitlines():
        m = REF_LINE_NUM.match(line)
        if not m:
            continue
        num = m.group("b") or m.group("p")
        rest = (m.group("rest") or "").strip()
        if num and rest:
            try:
                n = int(num)
                if 1 <= n <= 999 and n not in index:
                    index[n] = rest
            except ValueError:
                continue
    return index


def _extract_author_year_pairs(block_text: str) -> List[str]:
    """
    Given the inner text of parentheses that includes a year, attempt to split
    into distinct author-year pairs. We split on ';' first; if none, try commas
    but only when they appear to separate complete pairs (heuristic).
    """
    # First split by semicolons which commonly separate distinct citations
    parts = [p.strip() for p in block_text.split(";") if p.strip()]
    results: List[str] = []

    # If there was only one part, try splitting by '), (' pattern already handled by AUTHORYEAR_BLOCK
    # Otherwise each part should look like an author-year pair or a list of authors with a single year.
    for p in parts:
        # If comma-separated multiple citations are jammed together, try conservative splitting:
        candidates = [c.strip() for c in re.split(r"\s*,\s*(?=[A-Z][A-Za-z\-]+\s*,\s*(?:19|20)\d{2})", p)] or [p]
        for cand in candidates:
            m = SINGLE_AUTHORYEAR.match(cand)
            if m:
                author = m.group("author")
                year = m.group("year")
                results.append(f"{author}, {year}")
    # If nothing matched, try a last-chance direct match
    if not results:
        m = SINGLE_AUTHORYEAR.match(block_text.strip())
        if m:
            results.append(f"{m.group('author')}, {m.group('year')}")
    return results


def map_citations(raw_text: str, references_text: str) -> List[str]:
    """
    Extract citations from the raw body text and map numeric ones to references when possible.

    Returns:
        A sorted list of human-readable citation strings, e.g.:
        ["[1] Full reference if available...", "[3]", "(Smith et al., 2020)"]
    """
    results: List[str] = []
    seen: set[str] = set()

    # 1) Numeric citations
    ref_index = _parse_reference_index(references_text)
    nums_found: set[int] = set()

    for m in BRACKET_BLOCK.finditer(raw_text):
        for n in _expand_bracket_block(m.group(1)):
            nums_found.add(n)

    for n in sorted(nums_found):
        if n in ref_index:
            s = f"[{n}] {ref_index[n]}"
        else:
            s = f"[{n}]"
        if s not in seen:
            seen.add(s)
            results.append(s)

    # 2) Author–year citations
    # Find each parentheses block that appears to contain a year, then split into pairs
    for blk in AUTHORYEAR_BLOCK.finditer(raw_text):
        pairs = _extract_author_year_pairs(blk.group(1))
        for p in pairs:
            s = f"({p})"
            if s not in seen:
                seen.add(s)
                results.append(s)

    # Sort: numeric citations first (by number), then author-year alphabetically
    def _sort_key(item: str):
        if item.startswith("["):
            try:
                num = int(item.split("]", 1)[0][1:])
                return (0, num, "")
            except Exception:
                return (0, 10**6, item)
        return (1, 10**6, item)

    results.sort(key=_sort_key)
    return results
