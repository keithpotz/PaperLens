import json
from pathlib import Path

import click

# Pipeline imports (implementations live in src/summarizer/)
from summarizer.pdf_parser import parse_pdf
from summarizer.summarizer_basic import summarize_sections
from summarizer.citation_mapper import map_citations


@click.command()
@click.argument("pdf_path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["md", "json", "html"]),
    default="md",
    help="Output format for the summary.",
)
@click.option(
    "--max-sents",
    type=click.IntRange(1, 10),
    default=3,
    show_default=True,
    help="Max sentences per section for the basic summarizer.",
)
def cli(pdf_path, fmt, max_sents):
    """
    PaperLens CLI (Pre-Alpha)

    Accepts a PDF file and outputs a summary in the chosen format.
    Currently uses a naive parser + extractive summarizer and basic citation detection.
    """
    pdf_path = Path(pdf_path)

    # Basic validation
    if pdf_path.suffix.lower() != ".pdf":
        _fail(f"Expected a .pdf file, got: {pdf_path.name}")

    try:
        # 1) Parse PDF → raw text + references slice
        doc = parse_pdf(pdf_path)

        # 2) Summarize per section (extractive baseline)
        sections = summarize_sections(doc["raw_text"], max_sents=max_sents)

        # 3) Detect inline citations (numbers + author-year)
        citations = map_citations(doc["raw_text"], doc.get("references_text", ""))

        # Structured payload
        summary = {
            "title": doc.get("title") or pdf_path.stem,
            "sections": sections,
            "citations": citations,
        }

        # Render output
        if fmt == "json":
            output = json.dumps(summary, indent=2, ensure_ascii=False)
        elif fmt == "html":
            output = _to_html(summary)
        else:
            output = _to_markdown(summary)

        click.echo(output)

    except Exception as e:
        _fail(str(e))


def _to_markdown(s: dict) -> str:
    """Render summary as Markdown."""
    parts = [
        f"# Summary: {s.get('title', 'Untitled')}",
        "## Abstract",
        s["sections"].get("abstract", ""),
        "## Background",
        s["sections"].get("background", ""),
        "## Methods",
        s["sections"].get("methods", ""),
        "## Results",
        s["sections"].get("results", ""),
        "## Conclusion",
        s["sections"].get("conclusion", ""),
        "## Citations",
        "\n".join(s.get("citations", [])) or "_None detected_",
    ]
    return "\n\n".join(parts)


def _to_html(s: dict) -> str:
    """Render summary as minimal HTML (no external deps)."""
    def esc(t: str) -> str:
        return (
            t.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    title = esc(s.get("title", "Untitled"))
    sec = s.get("sections", {})
    cits = s.get("citations", [])

    li = "".join(f"<li>{esc(c)}</li>" for c in cits) or "<li><em>None detected</em></li>"

    return f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Summary: {title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; line-height: 1.6; padding: 24px; max-width: 900px; margin: auto; }}
      h1 {{ margin-top: 0; }}
      h2 {{ margin-top: 1.5em; }}
      code, pre {{ background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }}
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <h2>Abstract</h2><p>{esc(sec.get("abstract", ""))}</p>
    <h2>Background</h2><p>{esc(sec.get("background", ""))}</p>
    <h2>Methods</h2><p>{esc(sec.get("methods", ""))}</p>
    <h2>Results</h2><p>{esc(sec.get("results", ""))}</p>
    <h2>Conclusion</h2><p>{esc(sec.get("conclusion", ""))}</p>
    <h2>Citations</h2><ul>{li}</ul>
  </body>
</html>"""


def _fail(msg: str) -> None:
    click.echo(f"error: {msg}", err=True)
    raise SystemExit(1)


if __name__ == "__main__":
    cli()
