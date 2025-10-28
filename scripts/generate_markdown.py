#!/usr/bin/env python3
"""
Generate Markdown resume from LaTeX sections.
Clean, readable format for GitHub READMEs and plain-text sharing.
"""

import os
import re
from datetime import datetime

# Import configuration and utilities
from config import PERSONAL_INFO, OUTPUT_FILES, SECTIONS_DIR
from utils import (
    logger, read_file_safe, write_file_safe,
    parse_cventry
)

OUTPUT_FILE = OUTPUT_FILES['markdown']


def clean_latex(text):
    """Remove LaTeX commands and convert to Markdown."""
    if not text:
        return ""
    
    # Remove comments
    text = re.sub(r'%.*', '', text)
    
    # Process all \cventry commands using the parser from utils
    entries = parse_cventry(text)
    
    if entries:
        # Remove original \cventry commands
        text = re.sub(r'\\cventry\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', text)
        
        entries_md = []
        for entry in entries:
            link_md = f'[{entry["link_text"]}]({entry["link_url"]})' if entry['link_url'] else entry['link_text']
            content_md = clean_latex_simple(entry['content'])
            
            entry_md = f'\n### {entry["title"]}\n\n*{entry["tech"]}* | {link_md}\n\n{content_md}\n'
            entries_md.append(entry_md)
        
        text = text + '\n'.join(entries_md)
    
    # Convert LaTeX commands to Markdown
    text = clean_latex_simple(text)
    
    return text


def clean_latex_simple(text):
    """Convert basic LaTeX commands to Markdown."""
    if not text:
        return ""
    
    # Convert LaTeX commands to Markdown
    text = re.sub(r'\\section\{([^}]+)\}', r'## \1\n', text)
    text = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'*\1*', text)
    text = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'[\2](\1)', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\\\(\[\d+pt\])?', '\n', text)
    text = re.sub(r'\\item', '-', text)
    text = re.sub(r'\\quad', ' ', text)
    text = re.sub(r'\\par', '\n', text)
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\textbar\{\}', '|', text)
    text = re.sub(r'\\hfill', '', text)
    
    # Remove environment markers
    text = re.sub(r'\\begin\{itemizecompact\}', '', text)
    text = re.sub(r'\\end\{itemizecompact\}', '', text)
    text = re.sub(r'\\begin\{itemize\}(\[[^\]]*\])?', '', text)
    text = re.sub(r'\\end\{itemize\}', '', text)
    text = re.sub(r'\\input\{[^}]+\}', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = text.strip()
    
    return text


def parse_section(filename):
    """Parse a LaTeX section file and return cleaned Markdown."""
    filepath = os.path.join(SECTIONS_DIR, filename)
    content = read_file_safe(filepath)
    
    if not content:
        logger.warning(f"Section file {filename} is empty or unreadable")
        return ""
    
    return clean_latex(content)


def generate_markdown():
    """Generate complete Markdown resume."""
    
    logger.info("Generating Markdown resume...")
    
    # Parse sections
    summary = parse_section("summary.tex")
    projects = parse_section("projects.tex")
    open_source = parse_section("open_source.tex")
    education = parse_section("education.tex")
    skills = parse_section("skills.tex")
    
    # Get personal info from config
    name = PERSONAL_INFO['name']
    title = PERSONAL_INFO['title']
    email = PERSONAL_INFO['email']
    linkedin = PERSONAL_INFO['linkedin']
    github = PERSONAL_INFO['github']
    website = PERSONAL_INFO['website']
    
    # Build timestamp
    timestamp = datetime.now().strftime("%B %d, %Y")
    
    markdown = f"""# {name}

**{title}**

📧 [{email}](mailto:{email}) | 
💼 [LinkedIn]({linkedin}) | 
💻 [GitHub]({github}) | 
🌐 [Website]({website})

---

{summary}

---

{projects}

---

{open_source}

---

{education}

---

{skills}

---

## 📄 Download

- **[PDF Resume](cv.pdf)** (Recommended)
- **[JSON Resume](resume.json)** (Machine-readable)
- **[HTML Version](index.html)** (Web-friendly)

---

*Last updated: {timestamp}*

*This resume is auto-generated from LaTeX source files using GitHub Actions.*

"""
    
    # Write Markdown file
    success = write_file_safe(OUTPUT_FILE, markdown)
    
    if success:
        logger.info(f"Markdown resume generated successfully")
    else:
        logger.error("Failed to generate Markdown resume")
        return None
    
    return OUTPUT_FILE


if __name__ == "__main__":
    generate_markdown()
