# Resume LaTeX

A modular LaTeX resume system that generates professional PDF and JSON Resume formats.

## Features

- PDF generation using Charter font
- JSON Resume format (jsonresume.org compatible)
- Modular LaTeX sections (summary, projects, skills, education)
- Python scripts for automated JSON generation

## Prerequisites

- Python 3.12+
- LaTeX distribution (TeX Live or MiKTeX)  
- Make (optional)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure personal information
# Edit scripts/config.py with your details

# Build PDF
make build

# Build PDF + JSON Resume
make all

# Run tests
make test
```

## Windows Usage

```powershell
# Build PDF
latexmk -pdf -interaction=nonstopmode cv.tex

# Generate JSON Resume  
python scripts/generate_json.py

# Run tests
python tests/test_utils.py
```

## Project Structure

```
resume-latex/
├── cv.tex                # Main LaTeX file
├── Makefile             # Build automation
├── sections/            # Resume sections
│   ├── summary.tex
│   ├── projects.tex
│   ├── open_source.tex
│   ├── skills.tex
│   └── education.tex
├── style/               # LaTeX styling
│   ├── header.tex
│   └── macros.tex
├── scripts/             # Python scripts
│   ├── config.py
│   ├── utils.py
│   └── generate_json.py
├── tests/               # Test suite
└── docs/                # Generated output
    └── resume.json
```

## Customization

Edit `.tex` files in `sections/` directory or modify `style/header.tex` for styling changes. Update `scripts/config.py` for personal information used in JSON Resume generation.
