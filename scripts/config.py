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
    "json": "docs/resume.json",
    "latest_pr": "sections/latest_pr.tex"
}

# Resume Content Summary - parsed from sections/summary.tex by utils.get_summary_text()
# Fallback if parsing fails:
SUMMARY_TEXT = "Backend developer specializing in Java and Spring Boot with expertise in building production-grade distributed systems."

# Fallback text for latest PR (if API fails)
FALLBACK_PR_TEXT = r"\item \textbf{Active Contributor:} Ongoing contributions to open-source projects."

# Open Source Contributions - used by JSON Resume generator
OPEN_SOURCE_CONTRIBUTIONS = [
    {
        "organization": "HackSquad by Novu",
        "position": "Open Source Contributor",
        "url": "https://github.com/novuhq/novu",
        "startDate": "2024",
        "endDate": "2024",
        "summary": "Winner of HackSquad open-source program. Developed new features and improved code quality through testing and documentation.",
        "highlights": []
    },
    {
        "organization": "Social Summer of Code",
        "position": "Open Source Contributor",
        "url": "",
        "startDate": "2024",
        "endDate": "2024",
        "summary": "Winner of Social Summer of Code. Enhanced frontend UX and modularized Python programs.",
        "highlights": []
    },
    {
        "organization": "Innogeeks Winter of Code",
        "position": "Open Source Contributor",
        "url": "",
        "startDate": "2023",
        "endDate": "2023",
        "summary": "Winner of Innogeeks Winter of Code. Implemented features and resolved bugs in web applications.",
        "highlights": []
    }
]

# API Configuration
GITHUB_API_TIMEOUT = 10  # seconds
GITHUB_API_BASE = "https://api.github.com"
