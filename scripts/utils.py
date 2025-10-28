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
    Handles nested braces properly.
    
    Args:
        text: The text to search in
        start_pos: Position after the opening brace
    
    Returns:
        Position of matching closing brace, or -1 if not found
    """
    count = 1
    pos = start_pos
    while pos < len(text) and count > 0:
        if pos > 0 and text[pos - 1] == '\\':
            # Skip escaped characters
            pos += 1
            continue
        if text[pos] == '{':
            count += 1
        elif text[pos] == '}':
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
    args = []
    pos = start
    
    for _ in range(num_args):
        # Skip whitespace
        while pos < len(text) and text[pos] in ' \n\t':
            pos += 1
        
        if pos >= len(text) or text[pos] != '{':
            logger.warning(f"Failed to extract LaTeX arg at position {pos}")
            return None, start
        
        # Find matching brace
        end = find_matching_brace(text, pos + 1)
        if end == -1:
            logger.warning(f"Unmatched brace at position {pos}")
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
    # Remove comments
    text = re.sub(r'%.*', '', text)
    
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


def parse_cventry(text: str) -> List[Dict[str, str]]:
    """
    Parse all \\cventry commands from LaTeX text.
    
    Returns:
        List of dicts with keys: title, tech, link, content
    """
    entries = []
    pos = 0
    
    while True:
        match = re.search(r'\\cventry', text[pos:])
        if not match:
            break
        
        # Extract 4 arguments
        args, end_pos = extract_latex_args(text, pos + match.end(), 4)
        
        if args and len(args) == 4:
            title, tech, link_content, content = args
            
            # Parse href from link if present
            link_match = re.search(r'\\href\{([^}]+)\}\{([^}]+)\}', link_content)
            if link_match:
                url = link_match.group(1)
                link_text = link_match.group(2)
            else:
                url = ""
                link_text = link_content
            
            entries.append({
                'title': title,
                'tech': tech,
                'link_url': url,
                'link_text': link_text,
                'content': content
            })
            pos = end_pos
        else:
            # Failed to parse, skip this occurrence
            pos += match.end()
    
    logger.debug(f"Parsed {len(entries)} cventry commands")
    return entries


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


def format_file_size(size_bytes: int) -> str:
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


def get_summary_text() -> str:
    """
    Parse summary text from sections/summary.tex.
    Returns the summary content without section header.
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
