# PaperLens 🔍

![Status](https://img.shields.io/badge/status-pre--alpha-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/keithpotz/paperlens/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/paperlens/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

**PaperLens** is an open-source tool that ingests academic PDFs and produces **structured summaries** while preserving **in-text citations linked to references**.  

- 📑 Breaks papers into **Abstract, Background, Methods, Results, Conclusion**  
- 🔍 Preserves and maps **citations** for traceability  
- 🖥️ Works **offline-first**, with optional AI/LLM support  
- 📦 Exports summaries in **Markdown, JSON, HTML**  
- 🧑‍🤝‍🧑 Built for **students, researchers, educators, journalists**  

---

> ⚠️ **PaperLens is currently in pre-alpha.**  
> The CLI runs and produces placeholder summaries, but full PDF parsing and citation mapping are still in progress.  
> Try it, star it ⭐, and help us build an open tool for research!


## ✨ Why PaperLens?

Reading and skimming dozens of papers for a literature review is exhausting.  
Most existing summarization tools are **paywalled**, **strip citations**, or **require cloud upload**.  

PaperLens is:  
- **Open** → fully auditable  
- **Private** → runs offline by default  
- **Extensible** → add citation formats, output exporters, or custom summarizers  

---

## 🚀 Quick Start

```bash
# clone repo
git clone https://github.com/yourname/paperlens.git
cd paperlens

# create venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run on example paper
python src/main.py examples/sample_paper.pdf --format md --out summary.md
```

Expected output (pre-alpha): stub summaries with placeholder texts and citations.

## 🛠 Features & Roadmap

### ✅ Completed
- CLI scaffold with stub pipeline
- Basic placeholder summaries for Abstract, Background, Methods, Results, Conclusion

### 🚧 In Progress
- Parse PDFs (title, abstract, sections, references)
- Preserve and **link** in-text citations ([12], (Smith, 2020)) → References

### 🔜 Planned
- Section-based summaries (Abstract, Background, Methods, Results, Conclusion)
- Export formats: Markdown / JSON / HTML
- Bulk summarization (folders of PDFs)
- Optional LLM backend (local models or API integration)
- GUI drag-and-drop desktop app

### 🌟 Future Ideas
- Zotero / Mendeley plugin integration
- Multi-paper thematic clustering for literature reviews
- Export to LaTeX or Word with summary tables
- Dataset builder for summarization research


### Components
- **`pdf_parser.py`** → Extracts raw text, sections, and references from PDFs  
- **`citation_mapper.py`** → Maps in-text citations ([12], (Smith, 2020)) to reference list entries  
- **`summarizer_basic.py`** → Baseline extractive summarizer (frequency- or rule-based, offline)  
- **`summarizer_llm.py`** → Optional abstractive summarizer using LLMs (local or API)  
- **`main.py`** → CLI entry point, handles arguments, I/O, and pipeline coordination  

### Data Flow
1. **Input**: PDF file(s)  
2. **Parsing**: Extract sections + reference list  
3. **Citation Mapping**: Link inline markers to references  
4. **Summarization**: Generate per-section summaries  
5. **Export**: Save in Markdown, JSON, or HTML formats  



## 🛠 Development Setup

PaperLens uses **Python 3.9+**. We recommend setting up a virtual environment.

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/paperlens.git
cd paperlens
```
### 2. Create and Activate Virtual Environment
```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Tests to verify setup
```bash
pip install -r requirements.txt
```
## 🔌 Extension Points

PaperLens is designed to be **extensible** so contributors can add functionality without breaking the core.

### 📄 Parsers (`pdf_parser.py`)
- Improve PDF parsing accuracy  
- Add support for complex layouts (two-column, scanned PDFs with OCR)  
- Extract metadata (title, authors, keywords)  

### 🔍 Citation Mapping (`citation_mapper.py`)
- Enhance detection of in-text citations ([12], (Smith, 2020), Author-Year)  
- Map to multiple citation styles (APA, IEEE, ACM, Chicago)  
- Handle edge cases like missing or malformed references  

### ✂️ Summarizers (`summarizer_basic.py`, `summarizer_llm.py`)
- Add new extractive algorithms (frequency-based, TextRank, graph-based)  
- Integrate abstractive summarizers with local or API-based LLMs  
- Fine-tune summarization for specific disciplines (e.g., medicine, CS, psychology)  

### 📦 Exporters (new module welcome)
- Support new output formats (LaTeX, Word, CSV, Zotero/Mendeley imports)  
- Add custom Markdown templates for different academic needs  
- Provide HTML/JSON schema for integration with web apps  

---
## 🤝 Contributing

Contributions are welcome! 🎉  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, coding style, and how to get involved.
---

## 🌟 Acknowledgments

PaperLens is made possible thanks to the open-source ecosystem and the research community.  
Special thanks to:

- 📰 **Researchers, students, and educators** who inspired the need for open, transparent tools  
- 📑 [PyMuPDF](https://pymupdf.readthedocs.io/) and other libraries that make PDF parsing accessible  
- 🧑‍🤝‍🧑 The **open-source community** for sharing tools, feedback, and contributions  
- 💡 Everyone helping to make academic knowledge more approachable and equitable  

---


💡 **Tip:** If you’re looking for a good first issue, start with exporters or citation mapping — they’re modular and easy to test!

