## 🎨 Coding Style

To keep PaperLens consistent and contributor-friendly, please follow these guidelines:

### 📝 General
- Follow **PEP 8** style conventions  
- Use **type hints** (`def func(x: str) -> int:`) wherever possible  
- Keep functions and modules **small, focused, and testable**  
- Use **meaningful variable and function names**  
- Prefer **pure functions** (avoid side effects when possible)  


### 📚 Documentation
- Add **docstrings** for all public functions, classes, and modules  
- Use Google-style or NumPy-style docstrings (consistent across the repo)  
- Include examples where helpful  

### 🔄 Commits
- Write **clear, concise commit messages**  
- Prefer [Conventional Commits](https://www.conventionalcommits.org/) (not mandatory):  
  - `feat:` new feature  
  - `fix:` bug fix  
  - `docs:` documentation only  
  - `test:` add or improve tests  
  - `refactor:` code change that doesn’t affect behavior  
  - `chore:` build/config changes  

### 🧪 Testing
- Add tests for any new feature or bug fix  
- Keep tests deterministic (no randomness unless seeded)  
- Run `pytest -q` locally before opening a pull request  

### 🖋 Example
```python
def extract_references(text: str) -> list[str]:
    """
    Extracts reference entries from a paper's reference section.

    Args:
        text (str): Raw text of the References section.

    Returns:
        list[str]: A list of reference entries.
    """
    return [line.strip() for line in text.split("\n") if line.strip()]
```

# 🤝 Contributing to PaperLens

First off, thank you for considering contributing to **PaperLens**!  
Your help makes this project better for students, researchers, educators, and journalists everywhere.  

We welcome all contributions — whether it's fixing bugs, improving documentation, or adding major new features.

---

## 📋 How to Contribute

1. **Fork** the repo on GitHub  
2. **Clone** your fork locally  
   ```bash
   git clone https://github.com/<your-username>/paperlens.git
   cd paperlens
   ```
3. Create a branch for your feature or fix:

   ```bash
   git checkout -b feature/YourFeature
   ```
4. Make your changes, following the coding styles below
5. Commit your work with a clear message
 ```bash
  git commit -m "Add feature: short description"
 ```
6. Push your fork
  ```bash
git push origin feature/YourFeature
  ```
7. Open a pull request to the main branch of the repo!
## 🏷 Labels

We use GitHub issue labels to help contributors find tasks quickly:

- **good first issue** 🟢  
  Beginner-friendly tasks that are small, well-defined, and easy to start with.  

- **help wanted** 🟡  
  Issues where we’d love extra community input or support.  

- **enhancement** 🔵  
  Requests for new features, improvements, or extensions to existing functionality.  

- **bug** 🔴  
  Something isn’t working as expected — includes reproducible errors, crashes, or incorrect behavior.  

- **documentation** 📖  
  Improvements or fixes to README, comments, or overall project docs.  

- **discussion** 💬  
  Open-ended conversations around design choices, architecture, or potential new directions.  

---

💡 **Tip:** If you’re new, start with issues labeled **good first issue** or **help wanted**. They’re scoped to be approachable and well-documented.

