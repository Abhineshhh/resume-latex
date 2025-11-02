LATEXMK := latexmk
LATEXMKFLAGS := -pdf -interaction=nonstopmode -silent
PYTHON := python

.PHONY: build clean fetch-pr all test help

# Default target
help:
	@echo "Available targets:"
	@echo "  make build        - Fetch latest PR and compile PDF"
	@echo "  make all          - Build PDF and generate JSON Resume"
	@echo "  make test         - Run test suite"
	@echo "  make clean        - Remove generated files"
	@echo "  make fetch-pr     - Fetch latest GitHub PR only"

# Fetch latest merged PR from GitHub
fetch-pr:
	@echo "Fetching latest merged PR..."
	@$(PYTHON) -c "import os; f='sections/latest_pr.tex'; open(f, 'a').close() if not os.path.exists(f) else None"
	$(PYTHON) scripts/fetch_latest_pr.py

# Run test suite
test:
	@echo "Running tests..."
	$(PYTHON) tests/test_utils.py

# Build PDF only
build: fetch-pr
	@echo "Compiling LaTeX to PDF..."
	$(LATEXMK) $(LATEXMKFLAGS) cv.tex
	@echo "✓ PDF generated: cv.pdf"

# Build all formats (PDF + JSON)
all: build
	@echo "Generating JSON Resume..."
	@$(PYTHON) -c "import os; os.makedirs('docs', exist_ok=True)"
	$(PYTHON) scripts/generate_json.py
	@$(PYTHON) -c "import shutil; shutil.copy('cv.pdf', 'docs/index.pdf')"
	@echo "✓ All formats generated:"
	@echo "  - cv.pdf (source PDF)"
	@echo "  - docs/index.pdf (for deployment)"
	@echo "  - docs/resume.json (JSON Resume)"

# Clean all generated files
clean:
	@echo "Cleaning generated files..."
	$(LATEXMK) -c
	@$(PYTHON) -c "import os; [os.remove(f) for f in ['sections/latest_pr.tex', 'cv.pdf'] if os.path.exists(f)]"
	@$(PYTHON) -c "import os, glob; [os.remove(f) for f in glob.glob('docs/*.json') + glob.glob('docs/*.pdf') if os.path.exists(f)]"
	@echo "✓ Cleaned successfully"

