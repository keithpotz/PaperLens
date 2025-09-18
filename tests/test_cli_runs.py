import subprocess
import sys
from pathlib import Path

def test_cli_runs_and_outputs_markdown(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    examples = repo / "examples"
    examples.mkdir(exist_ok=True)

    pdf = examples / "sample_paper.pdf"
    if not pdf.exists():
        # Tiny placeholder "looks like" a PDF for the parser
        pdf.write_bytes(b"%PDF-1.4\n% PaperLens placeholder\n")

    cmd = [sys.executable, str(repo / "src" / "main.py"), str(pdf), "--format", "md"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    # New pipeline: assert structural headings instead of stub text
    assert out.startswith("# Summary:"), out
    assert "## Abstract" in out
    assert "## Background" in out
    assert "## Methods" in out
    assert "## Results" in out
    assert "## Conclusion" in out
    assert "## Citations" in out
