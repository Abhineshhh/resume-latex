#!/usr/bin/env python3
"""
Utility functions for resume generation scripts.
Includes logging, validation, and LaTeX parsing helpers.
"""

import os
import re
import sys
import logging
from typing import Optional, List, Tuple, Dict, Any

# Ensure scripts are run from project root
if os.path.basename(os.getcwd()) == 'scripts':
    os.chdir('..')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


def setup_logger(name: str, verbose: bool = False) -> logging.Logger:
    """Setup a logger with the given name."""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    return log


def ensure_dir_exists(filepath: str) -> None:
    """Ensure the directory for the given filepath exists."""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def validate_file_exists(filepath: str) -> bool:
    """Check if a file exists and log warning if not."""
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return False
    return True


def read_file_safe(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
    """Safely read a file and return its content, or None if error."""
    try:
        if not validate_file_exists(filepath):
            return None
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
        logger.debug(f"Successfully read: {filepath} ({len(content)} chars)")
        return content
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return None


def write_file_safe(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """Safely write content to a file."""
    try:
        ensure_dir_exists(filepath)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        logger.info(f"✓ Generated: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error writing {filepath}: {e}")
        return False


def find_matching_brace(text: str, start_pos: int) -> int:
    """
    Find the position of the matching closing brace.
    Handles nested braces and escaped characters properly.
    
    Args:
        text: The text to search in
        start_pos: Position after the opening brace
    
    Returns:
        Position of matching closing brace, or -1 if not found
    """
    if not text or start_pos >= len(text):
        return -1
    
    count = 1
    pos = start_pos
    
    while pos < len(text) and count > 0:
        char = text[pos]
        
        # Count consecutive backslashes before current position
        num_backslashes = 0
        temp_pos = pos - 1
        while temp_pos >= 0 and text[temp_pos] == '\\':
            num_backslashes += 1
            temp_pos -= 1
        
        # Character is escaped only if preceded by odd number of backslashes
        is_escaped = (num_backslashes % 2 == 1)
        
        # Check braces only if not escaped
        if not is_escaped:
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
        
        pos += 1
    
    return pos if count == 0 else -1


def extract_latex_args(text: str, start: int, num_args: int) -> Tuple[Optional[List[str]], int]:
    """
    Extract N arguments from a LaTeX command.
    
    Args:
        text: The text containing LaTeX
        start: Starting position (after command name)
        num_args: Number of arguments to extract
    
    Returns:
        Tuple of (list of arguments, end position) or (None, start) if failed
    """
    if not text or start >= len(text) or num_args <= 0:
        logger.warning(f"Invalid arguments for extract_latex_args: text_len={len(text) if text else 0}, start={start}, num_args={num_args}")
        return None, start
    
    args = []
    pos = start
    
    for arg_num in range(1, num_args + 1):
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \n\t':
            pos += 1
        
        if pos >= len(text):
            logger.warning(f"Unexpected end of text while extracting argument {arg_num}/{num_args}")
            return None, start
        
        if text[pos] != '{':
            logger.warning(f"Expected '{{' at position {pos} for argument {arg_num}/{num_args}, found '{text[pos]}'")
            return None, start
        
        # Find matching brace
        end = find_matching_brace(text, pos + 1)
        if end == -1:
            logger.warning(f"Unmatched brace at position {pos} for argument {arg_num}/{num_args}")
            return None, start
        
        args.append(text[pos + 1:end - 1])
        pos = end
    
    return args, pos


def escape_latex_chars(text: str) -> str:
    """Escape special LaTeX characters."""
    latex_escapes = {
        '\\': r'\textbackslash{}',
        '_': r'\_',
        '&': r'\&',
        '#': r'\#',
        '%': r'\%',
        '$': r'\$',
        '{': r'\{',
        '}': r'\}',
        '^': r'\^{}',
        '~': r'\textasciitilde{}'
    }
    for char, escape in latex_escapes.items():
        text = text.replace(char, escape)
    return text


def clean_latex_to_plain(text: str) -> str:
    """
    Convert LaTeX to plain text by removing/converting commands.
    Basic version - doesn't handle complex structures.
    """
    # Remove comments (but preserve escaped percent signs first)
    text = re.sub(r'(?<!\\)%.*', '', text)
    
    # Convert escaped LaTeX special characters to plain text
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'\\&', '&', text)
    text = re.sub(r'\\_', '_', text)
    text = re.sub(r'\\#', '#', text)
    text = re.sub(r'\\\$', '$', text)
    text = re.sub(r'\\\{', '{', text)
    text = re.sub(r'\\\}', '}', text)
    
    # Convert common commands
    text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'\2', text)
    text = re.sub(r'\\section\{([^}]+)\}', r'\1', text)
    
    # Remove common commands
    text = re.sub(r'\\(noindent|quad|hfill|par)', '', text)
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\\\(\[\d+pt\])?', '\n', text)
    text = re.sub(r'\\item', '', text)
    text = re.sub(r'\\textbar\{\}', '|', text)
    
    # Remove environments
    text = re.sub(r'\\begin\{[^}]+\}', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    
    # Clean whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    return text.strip()


def _extract_braced_arg(text: str, start: int) -> Tuple[Optional[str], int]:
    """
    Given start at an opening '{', return (inner_content, position_after_closing_brace).
    Returns (None, start) if not a valid braced arg.
    """
    if start >= len(text) or text[start] != '{':
        return None, start
    end = find_matching_brace(text, start + 1)
    if end == -1:
        return None, start
    return text[start + 1:end - 1], end


def extract_href(text: str) -> Tuple[str, str]:
    """
    Extract the first \\href{url}{label} from LaTeX text.
    Handles nested braces in the label (e.g. \\faIcon{github}).
    Returns (url, label) or ("", "") if not found.
    """
    if not text:
        return "", ""

    idx = 0
    while True:
        match = re.search(r'\\href\b', text[idx:])
        if not match:
            return "", ""
        pos = idx + match.end()
        while pos < len(text) and text[pos] in ' \t\n':
            pos += 1
        url, pos = _extract_braced_arg(text, pos)
        if url is None:
            idx = idx + match.end()
            continue
        while pos < len(text) and text[pos] in ' \t\n':
            pos += 1
        label, pos = _extract_braced_arg(text, pos)
        if label is None:
            idx = idx + match.end()
            continue
        return url.strip(), label.strip()


def strip_latex_commands_from_title(title: str) -> str:
    """
    Clean a cventry title that may embed \\href{...}{\\faIcon{...}} or similar.
    Keeps the human-readable project/job name only.
    """
    if not title:
        return ""

    # Remove all \\href{...}{...} blocks (brace-aware)
    cleaned = title
    while True:
        match = re.search(r'\\href\b', cleaned)
        if not match:
            break
        start = match.start()
        pos = match.end()
        while pos < len(cleaned) and cleaned[pos] in ' \t\n':
            pos += 1
        _, pos = _extract_braced_arg(cleaned, pos)
        while pos < len(cleaned) and cleaned[pos] in ' \t\n':
            pos += 1
        _, pos = _extract_braced_arg(cleaned, pos)
        if pos <= start:
            # Avoid infinite loop on malformed input
            cleaned = cleaned[:start] + cleaned[start + 5:]
            continue
        cleaned = cleaned[:start] + cleaned[pos:]

    cleaned = clean_latex_to_plain(cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(' |-')
    return cleaned.strip()


def parse_cventry(text: str) -> List[Dict[str, str]]:
    """
    Parse all \\cventry commands from LaTeX text.

    Args:
        text: LaTeX content containing cventry commands

    Returns:
        List of dicts with keys: title, tech, link_url, link_text, content
    """
    if not text:
        logger.warning("Empty text provided to parse_cventry")
        return []

    entries = []
    pos = 0
    entry_num = 0

    while True:
        match = re.search(r'\\cventry', text[pos:])
        if not match:
            break

        entry_num += 1
        match_pos = pos + match.end()

        # Extract 4 arguments
        args, end_pos = extract_latex_args(text, match_pos, 4)

        if args and len(args) == 4:
            title_raw, tech, link_content, content = args

            # Prefer explicit link arg; fall back to href embedded in the title
            # (common pattern: \cventry{Name \href{url}{\faIcon{github}}}{tech}{}{...})
            url, link_text = extract_href(link_content)
            if not url:
                url, link_text = extract_href(title_raw)

            title = strip_latex_commands_from_title(title_raw)

            entries.append({
                'title': title,
                'tech': tech.strip(),
                'link_url': url,
                'link_text': link_text,
                'content': content.strip(),
            })
            pos = end_pos
            logger.debug(f"Successfully parsed cventry #{entry_num}: {title}")
        else:
            # Failed to parse, skip this occurrence
            logger.warning(f"Failed to parse cventry #{entry_num} at position {match_pos}")
            pos = match_pos + 1

    logger.info(f"Parsed {len(entries)} cventry commands successfully")
    return entries


MONTH_MAP = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04',
    'May': '05', 'June': '06', 'July': '07', 'August': '08',
    'September': '09', 'October': '10', 'November': '11', 'December': '12',
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
}


def validate_url(url: str) -> bool:
    """Basic URL validation."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def validate_email(email: str) -> bool:
    """Basic email validation."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_pattern.match(email) is not None


class LatexParser:
    """Enhanced LaTeX parser with error handling."""
    
    def __init__(self, text: str):
        self.text = text
        self.errors = []
    
    def parse_section(self, section_name: str) -> Optional[str]:
        """Extract content from a specific section."""
        pattern = rf'\\section\{{{section_name}\}}(.*?)(?=\\section|\\end\{{document\}}|$)'
        match = re.search(pattern, self.text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def get_errors(self) -> List[str]:
        """Return any parsing errors encountered."""
        return self.errors


def format_file_size(size_bytes: float) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_info(filepath: str) -> Optional[Dict[str, Any]]:
    """Get information about a file."""
    try:
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        return {
            'path': filepath,
            'size': stat.st_size,
            'size_formatted': format_file_size(stat.st_size),
            'modified': stat.st_mtime
        }
    except Exception as e:
        logger.error(f"Error getting file info for {filepath}: {e}")
        return None


def parse_skills_from_latex() -> List[Dict[str, Any]]:
    """
    Parse skills from sections/skills.tex.
    Returns structured skills data for JSON Resume.
    """
    from config import SECTIONS_DIR
    
    filepath = os.path.join(SECTIONS_DIR, "skills.tex")
    content = read_file_safe(filepath)
    
    if not content:
        logger.warning(f"Could not read {filepath}")
        return []
    
    skills = []
    
    # Parse each skill category line by line
    # Format: \noindent\textbf{Category:} item1, item2, item3
    pattern = r'\\noindent\\textbf\{([^:]+):\}\s*([^\\\n]+)'
    matches = re.findall(pattern, content)
    
    for category, items_str in matches:
        # Clean LaTeX commands from category name
        category = clean_latex_to_plain(category).strip()
        items = [item.strip() for item in items_str.split(',')]
        skills.append({
            "name": category,
            "level": "",
            "keywords": items
        })
    
    logger.debug(f"Parsed {len(skills)} skill categories from {filepath}")
    return skills


def get_summary_text() -> str:
    """
    Parse summary text from sections/summary.tex.
    Returns the summary content without section header.

    Note: summary.tex is used for JSON Resume generation only,
    and is NOT included in the PDF output.

    Falls back to config.SUMMARY_TEXT if parsing fails.
    """
    from config import SUMMARY_TEXT, SECTIONS_DIR

    filepath = os.path.join(SECTIONS_DIR, "summary.tex")
    content = read_file_safe(filepath)

    if not content:
        logger.warning(f"Could not read {filepath}, using fallback summary")
        return SUMMARY_TEXT

    # Remove section header and LaTeX commands
    # Pattern: \section{Summary} followed by \noindent and the actual text
    pattern = r'\\section\{Summary\}\s*\\noindent\s+(.*?)(?=\\section|$)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        summary = match.group(1).strip()
        # Clean up LaTeX formatting
        summary = clean_latex_to_plain(summary)
        logger.debug(f"Parsed summary from {filepath}")
        return summary
    else:
        logger.warning(f"Could not parse summary from {filepath}, using fallback")
        return SUMMARY_TEXT


def parse_month_year_date(date_str: str) -> str:
    """
    Convert a human date fragment like "July 2025" or "Present" into JSON Resume style.
    Returns "YYYY-MM", "YYYY", "" (Present/current), or "" if unparseable.
    """
    if not date_str:
        return ""
    s = date_str.strip()
    if re.match(r'(?i)^(present|current|now)$', s):
        return ""  # JSON Resume uses empty endDate for current roles

    for month, num in MONTH_MAP.items():
        if month in s:
            parts = s.split()
            year = parts[-1] if parts else ""
            if re.fullmatch(r'\d{4}', year):
                return f"{year}-{num}"
            break

    # Bare year
    if re.fullmatch(r'\d{4}', s):
        return s
    return ""


def parse_date_range(dates: str) -> Tuple[str, str]:
    """
    Parse a date range string such as:
      "May 2026 - Present"
      "July 2025 - Oct 2025"
      "2022 - 2026"
    Returns (startDate, endDate) in JSON Resume format.
    """
    if not dates:
        return "", ""

    dates = dates.strip()
    # Prefer en-dash / em-dash / spaced hyphen separators over single hyphens inside words
    parts = re.split(r'\s*(?:--|–|—|\s-\s)\s*', dates)
    if len(parts) < 2:
        # Fallback: last hyphen split if looks like "May 2026 - Present"
        parts = re.split(r'\s+-\s+', dates)

    if len(parts) >= 2:
        return parse_month_year_date(parts[0]), parse_month_year_date(parts[1])
    if len(parts) == 1:
        return parse_month_year_date(parts[0]), ""
    return "", ""


def parse_experience_from_latex() -> List[Dict[str, Any]]:
    """
    Parse work experience entries from sections/experience.tex.

    Expected LaTeX shape (one block per role):
      \\noindent\\textbf{Position} \\textbar{} \\textit{Type} \\textbar{} \\textit{Company}
        \\hfill \\textit{Start - End}
      \\begin{itemizecompact}
        \\item ...
      \\end{itemizecompact}
    """
    from config import SECTIONS_DIR

    filepath = os.path.join(SECTIONS_DIR, "experience.tex")
    content = read_file_safe(filepath)
    if not content:
        return []

    # Header line: bold position, italic type, italic company, italic dates
    header_pattern = re.compile(
        r'\\noindent\\textbf\{([^}]+)\}\s*\\textbar\{\}\s*\\textit\{([^}]+)\}\s*\\textbar\{\}\s*\\textit\{([^}]+)\}'
        r'(?:\s*\\hfill\s*\\textit\{([^}]+)\})?',
        re.MULTILINE,
    )

    matches = list(header_pattern.finditer(content))
    if not matches:
        logger.warning(f"No experience entries matched in {filepath}")
        return []

    work_experiences: List[Dict[str, Any]] = []

    for i, match in enumerate(matches):
        position = match.group(1).strip()
        employment_type = match.group(2).strip()  # Contract / Internship / etc.
        company = match.group(3).strip()
        dates = (match.group(4) or "").strip()
        start_date, end_date = parse_date_range(dates)

        # Slice between this header and the next (or EOF) to collect bullets for this role only
        block_start = match.end()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[block_start:block_end]

        highlights = []
        for item_match in re.finditer(r'\\item\s+(.+?)(?=\n\s*\\item|\n\s*\\end\{|\Z)', block, re.DOTALL):
            item_text = clean_latex_to_plain(item_match.group(1)).strip()
            if item_text:
                highlights.append(item_text)

        if not (position and company and highlights):
            logger.warning(f"Skipping incomplete experience entry: {position!r} @ {company!r}")
            continue

        # Encode employment type in position when useful (Contract / Internship)
        display_position = position
        if employment_type and employment_type.lower() not in position.lower():
            display_position = f"{position} ({employment_type})"

        work_experiences.append({
            "name": company,
            "position": display_position,
            "url": "",
            "startDate": start_date,
            "endDate": end_date,
            "summary": highlights[0],
            "highlights": highlights,
        })

    logger.info(f"Parsed {len(work_experiences)} work experience entries from {filepath}")
    return work_experiences


def parse_education_from_latex() -> List[Dict[str, Any]]:
    """
    Parse education from sections/education.tex, with config.EDUCATION as fallback.
    """
    from config import SECTIONS_DIR, EDUCATION

    filepath = os.path.join(SECTIONS_DIR, "education.tex")
    content = read_file_safe(filepath)
    if not content:
        return [dict(EDUCATION)]

    institution = EDUCATION["institution"]
    inst_match = re.search(r'\\noindent\\textbf\{([^}]+)\}', content)
    if inst_match:
        institution = inst_match.group(1).strip()

    # Dates on first line: \hfill \textit{2022 - 2026}
    start_date, end_date = EDUCATION["startDate"], EDUCATION["endDate"]
    date_match = re.search(r'\\hfill\s*\\textit\{([^}]+)\}', content)
    if date_match:
        s, e = parse_date_range(date_match.group(1))
        if s:
            start_date = s
        if e:
            end_date = e

    # Degree line: \textit{Bachelor of Technology in Computer Science} \hfill \textbf{CGPA: 8.4/10}
    area = EDUCATION["area"]
    study_type = EDUCATION["studyType"]
    score = EDUCATION["score"]

    degree_match = re.search(r'\\textit\{([^}]+)\}', content)
    if degree_match:
        degree_text = degree_match.group(1).strip()
        # "Bachelor of Technology in Computer Science"
        if ' in ' in degree_text:
            study_part, area_part = degree_text.split(' in ', 1)
            study_type = study_part.replace('Bachelor of Technology', 'B.Tech').strip()
            area = area_part.strip()
        else:
            area = degree_text

    cgpa_match = re.search(r'\\textbf\{CGPA:\s*([^}]+)\}', content)
    if cgpa_match:
        score = f"{cgpa_match.group(1).strip()} CGPA"

    courses = list(EDUCATION.get("courses", []))
    focus_match = re.search(r'Academic Focus:\}\s*([^\n\\]+)', content)
    if focus_match:
        courses = [c.strip() for c in focus_match.group(1).split(',') if c.strip()]

    return [{
        "institution": institution,
        "url": EDUCATION.get("url", ""),
        "area": area,
        "studyType": study_type,
        "startDate": start_date,
        "endDate": end_date,
        "score": score,
        "courses": courses,
    }]
