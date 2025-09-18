from pathlib import Path
import importlib.util
import sys

def test_markdown_renderer_smoke():
    # Dynamically import src/main.py as a module to access helpers
    repo = Path(__file__).resolve().parents[1]
    main_py = repo / "src" / "main.py"

    spec = importlib.util.spec_from_file_location("paperlens_main", main_py)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["paperlens_main"] = mod
    spec.loader.exec_module(mod)  # type: ignore

    summary = {
        "title": "sample_paper",
        "sections": {
            "abstract": "Stub: abstract summary.",
            "background": "Stub: background summary.",
            "methods": "Stub: methods summary.",
            "results": "Stub: results summary.",
            "conclusion": "Stub: conclusion summary.",
        },
        "citations": ["[1] Smith et al., 2020", "[2] Doe, 2019"],
    }

    md = mod._to_markdown(summary)  # noqa: SLF001 (accessing internal helper)
    assert "# Summary: sample_paper" in md
    assert "## Abstract" in md
