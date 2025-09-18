# src/summarizer/summarizer_basic.py
import re
from typing import Dict

SECTION_ORDER = ["abstract", "background", "methods", "results", "conclusion"]

# Heuristics for detecting common section headers (case-insensitive)
_HEADER_HINTS = {
    "abstract": re.compile(r"^\s*(abstract)\s*$", re.I),
    "background": re.compile(r"^\s*((introduction|background))\s*$", re.I),
    "methods": re.compile(r"^\s*(methods?|materials\s+and\s+methods?)\s*$", re.I),
    "results": re.compile(r"^\s*(results?|findings?)\s*$", re.I),
    "conclusion": re.compile(r"^\s*(conclusions?|discussion|discussion\s+and\s+conclusion[s]?)\s*$", re.I),
}

# Also support numbered headers like:
# "1 Introduction", "I. INTRODUCTION", "2. Methods", "III Results", etc.
_NUMBERED_HEADER = re.compile(
    r"""^\s*(
            (\d+|[IVXLCDM]+)      # decimal or roman numeral
            [.)]?
            \s+
        )?
        ([A-Z][A-Za-z][A-Za-z \-/&]+?)   # header words
        \s*$
    """,
    re.X,
)


def _pick_section(header: str) -> str | None:
    """Map a candidate header line to a canonical section name."""
    h = header.strip()

    # Direct match against known headers
    for name, pat in _HEADER_HINTS.items():
        if pat.match(h):
            return name

    # Try numbered header heuristic -> strip number prefix then test again
    m = _NUMBERED_HEADER.match(h)
    if m:
        tail = m.group(3).strip()
        for name, pat in _HEADER_HINTS.items():
            if pat.match(tail):
                return name

    # Fallback: keyword contains (looser)
    low = h.lower()
    if "abstract" in low:
        return "abstract"
    if "introduction" in low or "background" in low:
        return "background"
    if "method" in low or "materials" in low:
        return "methods"
    if "result" in low or "finding" in low:
        return "results"
    if "conclusion" in low or "discussion" in low:
        return "conclusion"

    return None


def _normalize(text: str) -> list[str]:
    """Split into non-empty paragraphs with trimmed whitespace."""
    # Normalize Windows/Mac line endings and collapse excessive blank lines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Split by blank lines to get paragraphs
    chunks = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return chunks


def split_sections(raw_text: str) -> Dict[str, str]:
    """Greedy single-pass assignment of paragraphs to detected sections."""
    paras = _normalize(raw_text)
    sections: Dict[str, list[str]] = {k: [] for k in SECTION_ORDER}
    current: str | None = None

    for p in paras:
        # Treat short, header-like paragraphs as potential section headers
        # Keep a reasonable length to avoid matching full paragraphs
        if len(p) < 140:
            sec = _pick_section(p)
            if sec:
                current = sec
                continue

        if current:
            sections[current].append(p)

    # Join paragraphs; keep empty string if none found
    return {k: "\n\n".join(v) if v else "" for k, v in sections.items()}


def extractive_summary(text: str, max_sents: int = 3) -> str:
    """Very simple extractive baseline: take the first N sentences of the section."""
    if not text:
        return ""
    # Split on sentence boundaries; keep things simple for now
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    # Filter out ultra-short fragments
    sents = [s.strip() for s in sents if len(s.strip()) > 1]
    return " ".join(sents[:max_sents]) if sents else ""


def summarize_sections(raw_text: str, max_sents: int = 3) -> Dict[str, str]:
    """Produce short per-section summaries."""
    chunks = split_sections(raw_text)
    return {
        "abstract": extractive_summary(chunks["abstract"], max_sents),
        "background": extractive_summary(chunks["background"], max_sents),
        "methods": extractive_summary(chunks["methods"], max_sents),
        "results": extractive_summary(chunks["results"], max_sents),
        "conclusion": extractive_summary(chunks["conclusion"], max_sents),
    }
