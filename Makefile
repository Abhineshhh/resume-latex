LATEXMK := latexmk
LATEXMKFLAGS := -pdf -interaction=nonstopmode -silent
PYTHON := python

.PHONY: build clean all test help json

# Default target
help:
	@echo "Available targets:"
	@echo "  make build        - Compile PDF"
	@echo "  make json         - Generate JSON Resume only"
	@echo "  make all          - Build PDF and generate JSON Resume"
	@echo "  make test         - Run test suite"
	@echo "  make clean        - Remove generated files"

# Run test suite
test:
	@echo "Running tests..."
	$(PYTHON) tests/test_utils.py

# Build PDF only
build:
	@echo "Compiling LaTeX to PDF..."
	$(LATEXMK) $(LATEXMKFLAGS) cv.tex
	@echo "✓ PDF generated: cv.pdf"

# Generate JSON Resume only (no LaTeX compile)
json:
	@echo "Generating JSON Resume..."
	@$(PYTHON) -c "import os; os.makedirs('docs', exist_ok=True)"
	$(PYTHON) scripts/generate_json.py

# Build all formats (PDF + JSON)
all: build json
	@$(PYTHON) -c "import shutil; shutil.copy('cv.pdf', 'docs/index.pdf')"
	@echo "✓ All formats generated:"
	@echo "  - cv.pdf (source PDF)"
	@echo "  - docs/index.pdf (for deployment)"
	@echo "  - docs/resume.json (JSON Resume)"

# Clean all generated files
clean:
	@echo "Cleaning generated files..."
	$(LATEXMK) -c
	@$(PYTHON) -c "import os; [os.remove(f) for f in ['cv.pdf'] if os.path.exists(f)]"
	@$(PYTHON) -c "import os, glob; [os.remove(f) for f in glob.glob('docs/*.json') + glob.glob('docs/*.pdf') if os.path.exists(f)]"
	@echo "✓ Cleaned successfully"
