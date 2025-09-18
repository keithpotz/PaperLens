import click
from pathlib import Path

@click.command()
@click.argument("pdf_path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["md", "json", "html"]),
    default="md",
    help="Output format for the summary.",
)
def cli(pdf_path, fmt):
    """
    PaperLens CLI (Pre-Alpha Stub)

    Accepts a PDF file and outputs a placeholder summary in the chosen format.
    """
    pdf_path = Path(pdf_path)

    # Placeholder structured summary
    summary = {
        "title": pdf_path.stem,
        "sections": {
            "abstract": "Stub: abstract summary.",
            "background": "Stub: background summary.",
            "methods": "Stub: methods summary.",
            "results": "Stub: results summary.",
            "conclusion": "Stub: conclusion summary.",
        },
        "citations": [
            "[1] Smith et al., 2020",
            "[2] Doe, 2019",
        ],
    }

    # Render output
    if fmt == "json":
        import json
        output = json.dumps(summary, indent=2)
    elif fmt == "html":
        output = _to_html(summary)
    else:
        output = _to_markdown(summary)

    click.echo(output)


def _to_markdown(s):
    """Render summary as Markdown."""
    parts = [
        f"# Summary: {s['title']}",
        "## Abstract",
        s["sections"]["abstract"],
        "## Background",
        s["sections"]["background"],
        "## Methods",
        s["sections"]["methods"],
        "## Results",
        s["sections"]["results"],
        "## Conclusion",
        s["sections"]["conclusion"],
        "## Citations",
        "\n".join(s["citations"]),
    ]
    return "\n\n".join(parts)


def _to_html(s):
    """Render summary as HTML (very minimal)."""
    return f"""
    <html>
      <head><title>Summary: {s['title']}</title></head>
      <body>
        <h1>{s['title']}</h1>
        <h2>Abstract</h2><p>{s['sections']['abstract']}</p>
        <h2>Background</h2><p>{s['sections']['background']}</p>
        <h2>Methods</h2><p>{s['sections']['methods']}</p>
        <h2>Results</h2><p>{s['sections']['results']}</p>
        <h2>Conclusion</h2><p>{s['sections']['conclusion']}</p>
        <h2>Citations</h2><ul>{"".join(f"<li>{c}</li>" for c in s['citations'])}</ul>
      </body>
    </html>
    """


if __name__ == "__main__":
    cli()
