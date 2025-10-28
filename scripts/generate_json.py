#!/usr/bin/env python3
"""
Generate JSON Resume from LaTeX sections.
Follows JSON Resume Schema: https://jsonresume.org/schema/
Parses data from LaTeX files instead of hardcoding.
"""

import json
import os
from datetime import datetime

# Import configuration and utilities
from config import PERSONAL_INFO, OUTPUT_FILES, SECTIONS_DIR
from utils import (
    logger, read_file_safe, write_file_safe,
    parse_cventry, clean_latex_to_plain, get_summary_text
)

OUTPUT_FILE = OUTPUT_FILES['json']


def parse_projects_from_latex():
    """Parse project data from projects.tex file."""
    filepath = os.path.join(SECTIONS_DIR, "projects.tex")
    content = read_file_safe(filepath)
    
    if not content:
        return []
    
    entries = parse_cventry(content)
    projects = []
    
    for entry in entries:
        # Extract bullet points from content
        highlights = []
        content_plain = clean_latex_to_plain(entry['content'])
        for line in content_plain.split('\n'):
            line = line.strip()
            if line and not line.startswith('\\'):
                highlights.append(line)
        
        # Extract tech keywords
        tech_keywords = [t.strip() for t in entry['tech'].split(',')]
        
        project = {
            "name": entry['title'],
            "description": highlights[0] if highlights else entry['title'],
            "highlights": highlights,
            "keywords": tech_keywords,
            "startDate": "",
            "endDate": "",
            "url": entry['link_url'] if entry['link_url'] else "",
            "roles": ["Developer"],
            "entity": "",
            "type": "application"
        }
        projects.append(project)
    
    return projects


def parse_open_source_from_latex():
    """Parse open source contributions from open_source.tex file."""
    # Return hardcoded structured data for JSON Resume format
    # Note: The actual LaTeX file uses a different format (paragraph + latest PR)
    # This structured data is specifically for JSON Resume schema compliance
    volunteer = [
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
    
    return volunteer
    
    return volunteer


def generate_json_resume():
    """Generate JSON Resume file."""
    
    logger.info("Generating JSON resume...")
    
    # Parse projects from LaTeX
    projects = parse_projects_from_latex()
    volunteer = parse_open_source_from_latex()
    
    # Get summary from summary.tex
    summary_text = get_summary_text()
    
    # Build resume data
    resume_data = {
        "basics": {
            "name": PERSONAL_INFO['name'],
            "label": PERSONAL_INFO['title'],
            "image": "",
            "email": PERSONAL_INFO['email'],
            "phone": PERSONAL_INFO.get('phone', ''),
            "url": PERSONAL_INFO['website'],
            "summary": summary_text,
            "location": {
                "address": "",
                "postalCode": "",
                "city": PERSONAL_INFO['location'].get('city', ''),
                "countryCode": PERSONAL_INFO['location'].get('country_code', 'IN'),
                "region": PERSONAL_INFO['location'].get('region', '')
            },
            "profiles": [
                {
                    "network": "LinkedIn",
                    "username": PERSONAL_INFO['linkedin'].split('/')[-1],
                    "url": PERSONAL_INFO['linkedin']
                },
                {
                    "network": "GitHub",
                    "username": PERSONAL_INFO['github'].split('/')[-1],
                    "url": PERSONAL_INFO['github']
                }
            ]
        },
        "work": [],
        "volunteer": volunteer,
        "education": [
            {
                "institution": "Maharshi Dayanand University",
                "url": "",
                "area": "Computer Science",
                "studyType": "B.Tech",
                "startDate": "",
                "endDate": "",
                "score": "8.2/10 CGPA",
                "courses": [
                    "Operating Systems",
                    "Database Management Systems",
                    "Computer Networks",
                    "Data Structures",
                    "Algorithms"
                ]
            }
        ],
        "awards": [],
        "certificates": [],
        "publications": [],
        "skills": [
            {
                "name": "Languages",
                "level": "",
                "keywords": ["Java", "C", "C++", "Python", "SQL", "JavaScript"]
            },
            {
                "name": "Frameworks & Libraries",
                "level": "",
                "keywords": ["Spring Boot", "Spring MVC", "Spring Data JPA", "Spring Security", "Hibernate", "Maven"]
            },
            {
                "name": "Databases",
                "level": "",
                "keywords": ["MySQL", "PostgreSQL", "MongoDB"]
            },
            {
                "name": "Tools & Technologies",
                "level": "",
                "keywords": ["Git", "Docker", "Postman", "Linux", "Swagger", "Firebase"]
            }
        ],
        "languages": [
            {
                "language": "English",
                "fluency": "Professional"
            }
        ],
        "interests": [],
        "references": [],
        "projects": projects
    }
    
    # Write JSON file
    success = write_file_safe(OUTPUT_FILE, json.dumps(resume_data, indent=2, ensure_ascii=False))
    
    if success:
        logger.info(f"JSON resume generated successfully")
        logger.info(f"  Projects parsed: {len(projects)}")
        logger.info(f"  Validate at: https://jsonresume.org/schema/")
    else:
        logger.error("Failed to generate JSON resume")
        return None
    
    return OUTPUT_FILE


if __name__ == "__main__":
    generate_json_resume()
