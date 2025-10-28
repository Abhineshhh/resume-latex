LATEXMK := latexmk
LATEXMKFLAGS := -pdf -interaction=nonstopmode -silent
PYTHON := python

.PHONY: build clean fetch-pr all-formats serve

fetch-pr:
	@echo "Fetching latest merged PR..."
	$(PYTHON) scripts/fetch_latest_pr.py

build: fetch-pr
	$(LATEXMK) $(LATEXMKFLAGS) cv.tex

all-formats: build
	@echo "Generating all resume formats..."
	$(PYTHON) scripts/generate_html.py
	$(PYTHON) scripts/generate_json.py
	$(PYTHON) scripts/generate_markdown.py
	@$(PYTHON) -c "import os; os.makedirs('docs', exist_ok=True)"
	@$(PYTHON) -c "import shutil; shutil.copy('cv.pdf', 'docs/cv.pdf')"
	@echo "✓ All formats generated in docs/ folder"

serve: all-formats
	@echo "Starting local web server at http://localhost:8000"
	@echo "Open http://localhost:8000/docs/ in your browser"
	$(PYTHON) -m http.server 8000

clean:
	$(LATEXMK) -c
	@$(PYTHON) -c "import os; [os.remove(f) for f in ['sections/latest_pr.tex'] if os.path.exists(f)]"
	@$(PYTHON) -c "import os, glob; [os.remove(f) for f in glob.glob('docs/*.html') + glob.glob('docs/*.json') + glob.glob('docs/*.md') + glob.glob('docs/*.pdf') if os.path.exists(f)]"

