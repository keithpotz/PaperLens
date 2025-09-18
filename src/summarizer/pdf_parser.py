# src/summarizer/pdf_parser.py
from pathlib import Path
import fitz  # PyMuPDF


SECTION_HINTS = [
    "abstract",
    "introduction",
    "background",
    "methods",
    "results",
    "discussion",
    "conclusion",
    "references",
]


def parse_pdf(pdf_path: Path) -> dict:
    """
    Parse a PDF into plain text with minimal structure.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        dict: {
            "title": str,
            "raw_text": str,
            "references_text": str
        }
    """
    doc = fitz.open(pdf_path)

    # Extract all text
    pages = [page.get_text("text") for page in doc]
    text = "\n".join(p.strip() for p in pages if p).strip()

    # Try to extract title
    meta_title = (doc.metadata.get("title") or "").strip()
    if meta_title:
        title = meta_title
    else:
        # fallback: first non-empty line of first page
        first_page_lines = pages[0].splitlines() if pages else []
        title = next((line.strip() for line in first_page_lines if line.strip()), pdf_path.stem)

    # Find references section (last occurrence)
    lower = text.lower()
    idx = lower.rfind("references")
    references_text = text[idx:].strip() if idx != -1 else ""

    return {
        "title": title,
        "raw_text": text,
        "references_text": references_text,
    }
