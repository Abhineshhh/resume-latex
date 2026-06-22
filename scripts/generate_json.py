#!/usr/bin/env python3
"""
Generate JSON Resume from LaTeX sections.
Follows JSON Resume Schema: https://jsonresume.org/schema/
Parses data from LaTeX files and config.
"""

import json
import os
import sys

# Import configuration and utilities
from config import PERSONAL_INFO, OUTPUT_FILES, SECTIONS_DIR, OPEN_SOURCE_CONTRIBUTIONS
from utils import (
    logger, read_file_safe, write_file_safe,
    parse_cventry, clean_latex_to_plain, get_summary_text, parse_skills_from_latex,
    parse_experience_from_latex, parse_education_from_latex,
)

OUTPUT_FILE = OUTPUT_FILES['json']

# Fallback skills only if sections/skills.tex cannot be parsed at all
_FALLBACK_SKILLS = [
    {"name": "Languages", "level": "", "keywords": ["Java", "Go", "C", "SQL"]},
    {"name": "Backend & Frameworks", "level": "", "keywords": ["Spring Boot", "Spring MVC", "Spring Security", "FastAPI", "Hibernate"]},
    {"name": "Databases", "level": "", "keywords": ["MySQL", "PostgreSQL", "MongoDB", "Redis"]},
    {"name": "DevOps & Tools", "level": "", "keywords": ["Git", "Maven", "Docker", "Linux", "Postman", "Swagger", "CI/CD (GitHub Actions)"]},
]


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

        # Extract tech keywords (drop empties from trailing commas)
        tech_keywords = [t.strip() for t in entry['tech'].split(',') if t.strip()]

        # Use first highlight as description but don't duplicate in highlights
        description = highlights[0] if highlights else entry['title']

        project = {
            "name": entry['title'],
            "description": description,
            "highlights": highlights[1:] if len(highlights) > 1 else [],
            "keywords": tech_keywords,
            "startDate": "",
            "endDate": "",
            "url": entry['link_url'] or "",
            "roles": ["Developer"],
            "entity": "",
            "type": "application",
        }
        projects.append(project)

    return projects


def generate_json_resume():
    """Generate JSON Resume file. Returns output path on success, None on failure."""

    logger.info("Generating JSON resume...")

    try:
        projects = parse_projects_from_latex()
        volunteer = OPEN_SOURCE_CONTRIBUTIONS
        work = parse_experience_from_latex()
        education = parse_education_from_latex()
        summary_text = get_summary_text()

        skills = parse_skills_from_latex()
        if not skills:
            logger.warning("No skills parsed from LaTeX, using fallback aligned with skills.tex")
            skills = _FALLBACK_SKILLS
    except Exception as e:
        logger.error(f"Error during data parsing: {e}")
        return None

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
                "region": PERSONAL_INFO['location'].get('region', ''),
            },
            "profiles": [
                {
                    "network": "LinkedIn",
                    "username": PERSONAL_INFO['linkedin'].rstrip('/').split('/')[-1],
                    "url": PERSONAL_INFO['linkedin'],
                },
                {
                    "network": "GitHub",
                    "username": PERSONAL_INFO['github'].rstrip('/').split('/')[-1],
                    "url": PERSONAL_INFO['github'],
                },
            ],
        },
        "work": work,
        "volunteer": volunteer,
        "education": education,
        "awards": [],
        "certificates": [],
        "publications": [],
        "skills": skills,
        "languages": [
            {
                "language": "English",
                "fluency": "Professional",
            }
        ],
        "interests": [],
        "references": [],
        "projects": projects,
    }

    try:
        json_content = json.dumps(resume_data, indent=2, ensure_ascii=False)
        success = write_file_safe(OUTPUT_FILE, json_content)

        if success:
            logger.info("JSON resume generated successfully")
            logger.info(f"  Work experience entries: {len(work)}")
            logger.info(f"  Projects parsed: {len(projects)}")
            logger.info(f"  Skills categories: {len(skills)}")
            logger.info(f"  Education entries: {len(education)}")
            logger.info("  Validate at: https://jsonresume.org/schema/")
        else:
            logger.error("Failed to write JSON resume")
            return None
    except (TypeError, ValueError) as e:
        logger.error(f"JSON serialization error: {e}")
        return None

    return OUTPUT_FILE


if __name__ == "__main__":
    result = generate_json_resume()
    sys.exit(0 if result else 1)
