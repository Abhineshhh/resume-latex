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
    "phone": "+91 9334305214",
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
    "json": "docs/resume.json"
}

# Resume Content Summary
# Parsed from sections/summary.tex by utils.get_summary_text()
# Note: summary.tex is used for JSON Resume generation, NOT included in PDF
# Fallback if parsing fails:
SUMMARY_TEXT = "Backend developer specializing in Java and Spring Boot with expertise in building production-grade distributed systems."

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
