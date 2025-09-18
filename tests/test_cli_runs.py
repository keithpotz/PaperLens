import subprocess
import sys
from pathlib import Path

def test_cli_runs_and_outputs_markdown(tmp_path: Path):
    # Ensure examples/ exists with a tiny placeholder PDF
    repo = Path(__file__).resolve().parents[1]
    examples = repo / "examples"
    examples.mkdir(exist_ok=True)

    pdf = examples / "sample_paper.pdf"
    if not pdf.exists():
        # Minimal valid-looking PDF header so PyMuPDF (later) won’t choke
        pdf.write_bytes(b"%PDF-1.4\n% PaperLens placeholder\n")

    cmd = [sys.executable, str(repo / "src" / "main.py"), str(pdf), "--format", "md"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    assert proc.returncode == 0, proc.stderr
    assert "Stub: abstract summary." in proc.stdout
    assert "## Citations" in proc.stdout
