# Resume - LaTeX

> Automated resume system with multi-format generation and auto-updating GitHub contributions.

## 🚀 Features

- **Multi-format output**: PDF, HTML, JSON Resume, Markdown
- **Auto-updates**: Fetches latest merged PR from GitHub weekly
- **GitHub Pages**: Deployed automatically at `https://resume.abhineshhh.me/`
- **Modular structure**: Easy to customize sections
- **CI/CD**: Builds and deploys on every push

## 📦 Quick Start

### Prerequisites

- **Python 3.x** with `requests` library
- **LaTeX distribution** (MiKTeX or TeX Live)

### Local Build

```bash
# Fetch latest PR and compile PDF
make build

# Generate all formats (PDF, HTML, JSON, MD)
make all-formats

# Preview HTML resume locally
make serve
```

### Edit Content

Edit files in `sections/` directory:
- `summary.tex` - Professional summary
- `projects.tex` - Projects with tech stack
- `skills.tex` - Technical skills
- `education.tex` - Academic background
- `open_source.tex` - Open source contributions (+ auto-fetched latest PR)

### Deploy

```bash
git add .
git commit -m "Update resume"
git push
```

GitHub Actions automatically:
1. Fetches your latest merged PR
2. Compiles PDF
3. Generates HTML, JSON, Markdown
4. Deploys to GitHub Pages

## 🔗 Resume Links

After deployment, your resume will be available at:

- **PDF (Main)**: `https://resume.abhineshhh.me/` → Direct PDF view
- **HTML Version**: `https://resume.abhineshhh.me/web/` → Interactive HTML
- **JSON Resume**: `https://resume.abhineshhh.me/resume.json` → JSON Resume schema
- **Markdown**: `https://resume.abhineshhh.me/README.md` → GitHub-style markdown

## 📂 Structure

```
resume-latex/
├── cv.tex                    # Main LaTeX file
├── sections/                 # Modular content
│   ├── summary.tex
│   ├── projects.tex
│   ├── open_source.tex
│   ├── skills.tex
│   ├── education.tex
│   └── latest_pr.tex        # Auto-generated
├── style/
│   ├── header.tex           # Document setup
│   └── macros.tex           # Custom commands
├── scripts/                 # Python automation
│   ├── fetch_latest_pr.py
│   ├── generate_html.py
│   ├── generate_json.py
│   ├── generate_markdown.py
│   ├── config.py           # Personal configuration
│   └── utils.py            # Helper functions
├── docs/                    # Generated output (deployed)
│   ├── index.pdf           # PDF at root
│   ├── web/
│   │   └── index.html      # HTML version
│   ├── resume.json
│   └── README.md
└── .github/workflows/
    └── build.yml           # CI/CD automation
```

## ⚙️ Configuration

Update personal info in `scripts/config.py`:

```python
PERSONAL_INFO = {
    "name": "Abhinesh Jha",
    "email": "jhaabhinesh977@gmail.com",
    "github": "https://github.com/Abhineshhh",
    "linkedin": "https://linkedin.com/in/abhineshjha",
    "website": "https://abhineshhh.me"
}

GITHUB_USERNAME = "Abhineshhh"
```

Update header info in `style/header.tex` for the PDF version.

## 🔄 Auto-Update Schedule

The workflow automatically fetches your latest GitHub PR:
- **Scheduled**: Every Sunday at midnight UTC
- **Manual**: Click "Run workflow" in GitHub Actions tab
- **On push**: Automatically when you update any file

## 🛠️ Tech Stack

- **LaTeX** - Document typesetting
- **Python** - Build automation and format generation
- **GitHub Actions** - CI/CD pipeline
- **GitHub Pages** - Static hosting

## 📄 License

Feel free to fork and customize for your own resume!

---

**Built with ❤️ using LaTeX, Python, and GitHub Actions**
```
├── style/                # theme & formatting
│   ├── header.tex
│   └── macros.tex
│
├── scripts/              # automation scripts
│   ├── fetch_latest_pr.py     # fetches latest merged PR
│   ├── generate_html.py       # LaTeX → HTML
│   ├── generate_json.py       # LaTeX → JSON Resume
│   └── generate_markdown.py   # LaTeX → Markdown
│
├── docs/                 # generated files (GitHub Pages)
│   ├── index.pdf        # PDF at root URL
│   ├── web/
│   │   └── index.html   # HTML version at /web/
│   ├── resume.json      # JSON Resume format
│   └── README.md        # Markdown version
│
├── Makefile              # for local build
├── .github/
│   └── workflows/
│       └── build.yml     # CI/CD pipeline
│
└── README.md
```

## 🚀 Quick Start

#### Prerequisites

**1. Python 3.x**
```powershell
python --version
pip install requests
```

**2. TeX Distribution** (for PDF generation)

### Option A: MiKTeX (recommended for Windows)

**Using Chocolatey (easiest):**

1. Open PowerShell as Administrator
2. Install MiKTeX:

```powershell
choco install miktex
```

3. **IMPORTANT:** Close PowerShell completely and open a new window
   - The PATH won't update in the current terminal session
   - MiKTeX binaries are added to PATH during installation
   - New terminal = fresh PATH with MiKTeX included
4. Verify installation:

```powershell
pdflatex --version
latexmk --version
```

**Manual installation:**

1. Download MiKTeX installer from [miktex.org](https://miktex.org/download)
2. Run installer and follow prompts (use defaults)
3. After installation, restart your terminal
4. Verify installation as above

### Option B: TeX Live

1. Download TeX Live installer from [tug.org/texlive](https://tug.org/texlive/acquire-netinstall.html)
2. Run `install-tl-windows.exe`
3. Follow installation wizard (basic scheme is sufficient)
4. Add TeX Live bin directory to PATH if not automatic
5. Restart terminal and verify

---

## 📦 Build Commands

### Build PDF Only
```powershell
make build
# OR
python scripts\fetch_latest_pr.py
latexmk -pdf -interaction=nonstopmode cv.tex
```

### Build All Formats (PDF + HTML + JSON + Markdown)
```powershell
make all-formats
```

This generates:
- `cv.pdf` - LaTeX-compiled PDF (source)
- `docs/index.pdf` - PDF for root URL
- `docs/web/index.html` - HTML version at /web/
- `docs/resume.json` - JSON Resume format
- `docs/README.md` - Markdown version

### Preview HTML Resume Locally
```powershell
make serve
```

Then open `http://localhost:8000/docs/` in your browser.

### Clean Build Artifacts
```powershell
make clean
```

---

## 🌐 GitHub Pages Deployment

Your resume will be automatically deployed to GitHub Pages on every push to `main` or `master`.

### Setup Steps:

1. **Enable GitHub Pages** in your repository:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` / `(root)`
   - Save

2. **Update Personal Info**:
   - Edit `scripts/generate_html.py` (lines 12-17)
   - Edit `scripts/generate_json.py` (lines 13-18)
   - Edit `scripts/generate_markdown.py` (lines 12-17)
   - Replace placeholder values with your actual info

3. **Push to GitHub**:
   ```powershell
   git add .
   git commit -m "Enable multi-format resume generation"
   git push origin main
   ```

4. **Access Your Resume**:
   - **PDF (Main)**: `https://yourusername.github.io/resume-latex/` → Direct PDF
   - **HTML Version**: `https://yourusername.github.io/resume-latex/web/`
   - **JSON Resume**: `https://yourusername.github.io/resume-latex/resume.json`

---

## ⚙️ Configuration

### Dynamic Latest PR Feature

Edit `scripts/fetch_latest_pr.py` line 12:
```python
GITHUB_USERNAME = "Abhineshhh"  # Replace with YOUR GitHub username
```

### Personal Information

Update these files with your actual info:
- `style/header.tex` - Name, contact links
- `scripts/generate_html.py` - HTML generator config
- `scripts/generate_json.py` - JSON Resume data
- `scripts/generate_markdown.py` - Markdown generator config

### Content Sections

Edit files in `sections/`:
- `summary.tex` - Professional summary
- `projects.tex` - Your projects
- `open_source.tex` - Open-source contributions
- `education.tex` - Education history
- `skills.tex` - Technical skills

---

## 🔄 How It Works

1. **On every push**, GitHub Actions:
   - Fetches your latest merged PR
   - Compiles LaTeX → PDF
   - Generates HTML version
   - Creates JSON Resume
   - Builds Markdown format
   - Deploys everything to GitHub Pages

2. **Dynamic PR Integration**:
   - Script queries GitHub API for your latest merged PR
   - Generates `sections/latest_pr.tex`
   - Automatically included in all formats

3. **Multi-Format Pipeline**:
   ```
   LaTeX Source → PDF (latexmk)
                ↓
   Python Scripts → HTML + JSON + Markdown
                ↓
   GitHub Pages → Live Website
   ```

---

## 📋 Features Included

✅ Modular LaTeX structure (easy to edit)  
✅ Dynamic latest PR integration  
✅ Multi-format output (PDF, HTML, JSON, Markdown)  
✅ Responsive HTML design  
✅ JSON Resume schema compliance  
✅ GitHub Actions CI/CD  
✅ GitHub Pages deployment  
✅ Local development server  
✅ One-command builds  

---

## 🤝 Contributing

Feel free to fork this repository and customize it for your own resume!

## 📄 License

MIT License - feel free to use this template for your own resume.

---

*Last updated: Auto-generated on every build via GitHub Actions*
