from pathlib import Path
import importlib.util
import sys

def test_markdown_renderer_smoke():
    repo = Path(__file__).resolve().parents[1]
    main_py = repo / "src" / "main.py"

    spec = importlib.util.spec_from_file_location("paperlens_main", main_py)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["paperlens_main"] = mod
    spec.loader.exec_module(mod)  # type: ignore

    summary = {
        "title": "sample_paper",
        "sections": {
            "abstract": "A short abstract. Sentence two.",
            "background": "Background text.",
            "methods": "Methods text.",
            "results": "Results text.",
            "conclusion": "Conclusion text.",
        },
        "citations": ["[1] Example ref"],
    }

    md = mod._to_markdown(summary)  # noqa: SLF001 (access internal helper)
    assert "# Summary: sample_paper" in md
    assert "## Abstract" in md
    assert "## Citations" in md
