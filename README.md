# Resume LaTeX Generator

A professional resume generation system that creates both PDF and JSON Resume formats from LaTeX source files. Automatically fetches your latest GitHub contributions and maintains up-to-date resume content.

## 🚀 Features

- **LaTeX to PDF**: Professional PDF generation using Charter font
- **JSON Resume**: Auto-generates JSON Resume format (jsonresume.org compatible)
- **Dynamic Parsing**: Automatically parses skills and content from LaTeX files
- **CI/CD Ready**: GitHub Actions workflow for automated builds
- **Vercel Deployment**: Optimized for Vercel hosting
- **Modular Architecture**: Easy to customize sections
- **Test Suite**: Comprehensive testing for all utilities

## 📋 Prerequisites

- **Python 3.12+** (for scripts)
- **LaTeX Distribution**: 
  - Linux/macOS: TeX Live
  - Windows: MiKTeX or TeX Live
- **Make** (optional, for automation)
  - Windows users: See [Windows Usage](#-windows-usage) below

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Abhineshhh/resume-latex.git
cd resume-latex
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Information

Edit `scripts/config.py` with your personal information:

```python
PERSONAL_INFO = {
    "name": "Your Name",
    "title": "Your Title",
    "email": "your.email@example.com",
    "linkedin": "https://linkedin.com/in/yourusername",
    "github": "https://github.com/yourusername",
    "website": "https://yourwebsite.com",
    # ... update all fields
}
```

## 🎯 Usage

### Linux/macOS/WSL

Use the Makefile for easy commands:

```bash
# Build PDF only
make build

# Build all formats (PDF + JSON)
make all

# Run tests
make test

# Clean generated files
make clean
```

### 💻 Windows Usage

**Option 1: Use PowerShell Scripts (Recommended)**

```powershell
# Run tests
python tests/test_utils.py

# Build PDF
latexmk -pdf -interaction=nonstopmode cv.tex

# Generate JSON Resume
python scripts/generate_json.py

# Build everything
latexmk -pdf -interaction=nonstopmode cv.tex; python scripts/generate_json.py
```

**Option 2: Use WSL (Windows Subsystem for Linux)**

Install WSL and use the Makefile commands as shown above.

**Option 3: Install Make for Windows**

- Install Chocolatey: https://chocolatey.org/
- Run: `choco install make`
- Use Makefile commands

### Clean Build Artifacts (Windows)

```powershell
# Clean LaTeX files
latexmk -c

# Remove generated files
Remove-Item cv.pdf -ErrorAction SilentlyContinue
Remove-Item docs/*.json -ErrorAction SilentlyContinue
Remove-Item docs/*.pdf -ErrorAction SilentlyContinue
```

## 📁 Project Structure

```
resume-latex/
├── cv.tex                  # Main LaTeX file
├── Makefile               # Build automation
├── requirements.txt       # Python dependencies
├── pyrightconfig.json     # Python type checking config
├── .github/
│   └── workflows/
│       └── build.yml      # CI/CD workflow
├── docs/                  # Generated output (for Vercel)
│   ├── index.pdf         # PDF copy for web
│   └── resume.json       # JSON Resume format
├── sections/             # LaTeX content sections
│   ├── summary.tex
│   ├── projects.tex
│   ├── open_source.tex
│   ├── skills.tex
│   └── education.tex
├── style/                # LaTeX styling
│   ├── header.tex
│   └── macros.tex
├── scripts/              # Python automation scripts
│   ├── config.py         # Configuration
│   ├── utils.py          # Utility functions
│   └── generate_json.py
└── tests/                # Test suite
    ├── __init__.py
    └── test_utils.py
```

## 🔧 Customization

### Edit Resume Sections

Edit the `.tex` files in the `sections/` directory:

- `summary.tex` - Professional summary
- `projects.tex` - Project entries
- `open_source.tex` - Open source contributions
- `skills.tex` - Technical skills
- `education.tex` - Education details

### Add/Remove Sections

Edit `cv.tex` to include/exclude sections:

```latex
\input{sections/summary.tex}
\input{sections/projects.tex}
% \input{sections/new_section.tex}  % Add new sections
```

### Modify Styling

Edit files in the `style/` directory:

- `header.tex` - Header and document setup
- `macros.tex` - Custom LaTeX commands

## 🚀 Deployment (Vercel)

### Setup

1. Push your repository to GitHub
2. Connect your repo to Vercel
3. Configure custom domain in Vercel dashboard (if needed)

### Automatic Deployment

The GitHub Actions workflow automatically:
1. Runs tests
2. Fetches latest PR
3. Compiles PDF
4. Generates JSON Resume
5. Commits to `docs/` folder

Vercel auto-deploys when changes are pushed to main branch.

### Manual Deployment

You can also deploy directly from Vercel dashboard or CLI:

```bash
vercel deploy
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python tests/test_utils.py

# Tests include:
# - LaTeX parsing
# - Brace matching
# - Argument extraction
# - URL/email validation
# - File operations
# - Configuration validation
```

## 📊 Output Formats

### PDF Resume (`cv.pdf`)
Professional LaTeX-compiled PDF resume.

### JSON Resume (`docs/resume.json`)
Follows JSON Resume Schema v1.0.0:
- https://jsonresume.org/schema/
- Compatible with JSON Resume tools and themes
- Machine-readable for ATS systems

## 🛡️ Error Handling

The scripts include comprehensive error handling:
- Safe file operations with validation
- LaTeX character escaping
- JSON serialization error handling
- Type checking with Pyright
- Fallback values for missing data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/test_utils.py`
5. Submit a pull request

## 📝 License

This project is open source and available for personal and commercial use.

## 🐛 Troubleshooting

### LaTeX compilation errors
Ensure you have a complete LaTeX distribution installed with required packages.

### Windows Makefile issues
Use PowerShell commands directly or install WSL/Make for Windows.

## 📧 Contact

- GitHub: [@Abhineshhh](https://github.com/Abhineshhh)
- LinkedIn: [abhineshjha](https://linkedin.com/in/abhineshjha)
- Portfolio: [abhineshhh.me](https://abhineshhh.me)

---

**Built with ❤️ using LaTeX, Python, and automation**
