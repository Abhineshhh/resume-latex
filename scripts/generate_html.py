#!/usr/bin/env python3
"""
Generate HTML resume from LaTeX sections.
Parses .tex files and generates a clean, responsive HTML page.
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

OUTPUT_FILE = OUTPUT_FILES['html']


def clean_latex(text):
    """Remove LaTeX commands and convert to plain text."""
    if not text:
        return ""
    
    # Remove comments
    text = re.sub(r'%.*', '', text)
    
    # Process all \cventry commands using the parser from utils
    entries = parse_cventry(text)
    
    if entries:
        # Remove original \cventry commands
        text = re.sub(r'\\cventry\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', text)
        
        entries_html = []
        for entry in entries:
            link_html = f'<a href="{entry["link_url"]}" target="_blank">{entry["link_text"]}</a>' if entry['link_url'] else entry['link_text']
            content_html = clean_latex_simple(entry['content'])
            
            entry_html = f'''<div class="entry">
<h3>{entry["title"]}</h3>
<p><em>{entry["tech"]}</em> | {link_html}</p>
{content_html}
</div>'''
            entries_html.append(entry_html)
        
        text = text + '\n'.join(entries_html)
    
    # Convert common LaTeX commands
    text = clean_latex_simple(text)
    
    return text


def clean_latex_simple(text):
    """Convert basic LaTeX commands to HTML."""
    if not text:
        return ""
    
    # Convert common LaTeX commands
    text = re.sub(r'\\section\{([^}]+)\}', r'<h2>\1</h2>', text)
    text = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'<a href="\1" target="_blank">\2</a>', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\\\(\[\d+pt\])?', '<br>', text)
    text = re.sub(r'\\item', '<li>', text)
    text = re.sub(r'\\quad', ' ', text)
    text = re.sub(r'\\par', '<br>', text)
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\textbar\{\}', '|', text)
    text = re.sub(r'\\hfill', '', text)
    
    # Remove environment markers
    text = re.sub(r'\\begin\{itemizecompact\}', '<ul class="compact">', text)
    text = re.sub(r'\\end\{itemizecompact\}', '</ul>', text)
    text = re.sub(r'\\begin\{itemize\}(\[[^\]]*\])?', '<ul>', text)
    text = re.sub(r'\\end\{itemize\}', '</ul>', text)
    text = re.sub(r'\\input\{[^}]+\}', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()
    
    return text


def parse_section(filename):
    """Parse a LaTeX section file and return cleaned HTML."""
    filepath = os.path.join(SECTIONS_DIR, filename)
    content = read_file_safe(filepath)
    
    if not content:
        logger.warning(f"Section file {filename} is empty or unreadable")
        return ""
    
    return clean_latex(content)


def generate_html():
    """Generate complete HTML resume."""
    
    logger.info("Generating HTML resume...")
    
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
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{name} - {title} | Resume">
    <meta name="author" content="{name}">
    <meta name="keywords" content="resume, {title}, {name}">
    <title>{name} | Resume</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        
        header {{
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.3em;
            color: #3498db;
            margin-bottom: 20px;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-align: center;
        }}
        
        .contact {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 0.95em;
        }}
        
        .contact a {{
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .contact a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        
        h2 {{
            font-size: 1.5em;
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #3498db;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul {{
            margin-left: 20px;
            margin-bottom: 20px;
        }}
        
        ul.compact {{
            margin-left: 25px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        .entry {{
            margin-bottom: 25px;
        }}
        
        .entry h3 {{
            font-size: 1.2em;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        em {{
            color: #7f8c8d;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .download-btn {{
            display: inline-block;
            margin: 20px auto;
            padding: 12px 24px;
            background: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s;
        }}
        
        .download-btn:hover {{
            background: #2980b9;
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .contact {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 0;
            }}
            
            .download-btn, .footer {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{name}</h1>
            <p class="subtitle">{title}</p>
            <div class="contact">
                <span>🔗 <a href="{linkedin}">LinkedIn</a></span>
                <span>💻 <a href="{github}">GitHub</a></span>
                <span>🌐 <a href="{website}">Website</a></span>
                <span>✉️ <a href="mailto:{email}">{email}</a></span>
            </div>
        </header>
        
        <div style="text-align: center; margin: 20px 0;">
            <a href="cv.pdf" class="download-btn" download>📄 Download PDF Resume</a>
        </div>
        
        <main>
            {summary}
            
            {projects}
            
            {open_source}
            
            {education}
            
            {skills}
        </main>
        
        <footer class="footer">
            <p>Last updated: {timestamp}</p>
            <p>Built with LaTeX → HTML automation | <a href="{github}">View Source on GitHub</a></p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    success = write_file_safe(OUTPUT_FILE, html)
    
    if success:
        logger.info(f"HTML resume generated successfully")
    else:
        logger.error("Failed to generate HTML resume")
        return None
    
    return OUTPUT_FILE


if __name__ == "__main__":
    generate_html()
