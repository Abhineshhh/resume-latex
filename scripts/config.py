#!/usr/bin/env python3
"""
Centralized configuration for resume generation scripts.
Update this file to change personal information across all formats.
"""

# Personal Information (used by all generators)
PERSONAL_INFO = {
    "name": "Abhinesh Jha",
    "title": "Backend Developer",
    "email": "jhaabhinesh977@gmail.com",
    "phone": "",
    "linkedin": "https://linkedin.com/in/abhineshjha",
    "github": "https://github.com/Abhineshhh",
    "website": "https://abhineshhh.me",
    "location": {
        "city": "",
        "country_code": "IN",
        "region": ""
    }
}

# GitHub Configuration
GITHUB_USERNAME = "Abhineshhh"

# File Paths
SECTIONS_DIR = "sections"
STYLE_DIR = "style"
DOCS_DIR = "docs"

# Output Files
OUTPUT_FILES = {
    "html": "docs/web/index.html",
    "json": "docs/resume.json",
    "markdown": "docs/README.md",
    "latest_pr": "sections/latest_pr.tex"
}

# Resume Content Summary - parsed from sections/summary.tex by utils.get_summary_text()
# Fallback if parsing fails:
SUMMARY_TEXT = "Backend developer specializing in Java and Spring Boot with expertise in building production-grade distributed systems."

# Fallback text for latest PR (if API fails)
FALLBACK_PR_TEXT = r"\item \textbf{Active Contributor:} Ongoing contributions to open-source projects."

# API Configuration
GITHUB_API_TIMEOUT = 10  # seconds
GITHUB_API_BASE = "https://api.github.com"
