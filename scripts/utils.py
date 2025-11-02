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
                'title': title.strip(),
                'tech': tech.strip(),
                'link_url': url.strip(),
                'link_text': link_text.strip(),
                'content': content.strip()
            })
            pos = end_pos
            logger.debug(f"Successfully parsed cventry #{entry_num}: {title}")
        else:
            # Failed to parse, skip this occurrence
            logger.warning(f"Failed to parse cventry #{entry_num} at position {match_pos}")
            pos = match_pos + 1
    
    logger.info(f"Parsed {len(entries)} cventry commands successfully")
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
