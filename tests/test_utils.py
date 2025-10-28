#!/usr/bin/env python3
"""
Unit tests for resume generation utilities.
Run with: python -m pytest tests/
Or: python tests/test_utils.py
"""

import sys
import os

# Add parent directory to path to import scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from utils import (
    find_matching_brace,
    extract_latex_args,
    escape_latex_chars,
    clean_latex_to_plain,
    parse_cventry,
    validate_url,
    validate_email
)


def test_find_matching_brace():
    """Test brace matching function."""
    text = "hello {world {nested} text} end"
    pos = find_matching_brace(text, 7)  # After first {
    assert pos == 27  # Position after matching } (function returns position after consuming)
    
    # Test unmatched brace
    text2 = "hello {world"
    pos2 = find_matching_brace(text2, 7)
    assert pos2 == -1


def test_extract_latex_args():
    """Test LaTeX argument extraction."""
    text = r"\cventry{Title}{Tech}{Link}{Content}"
    # Position should be after \cventry (length 8)
    args, pos = extract_latex_args(text, 8, 4)
    assert args == ['Title', 'Tech', 'Link', 'Content']
    assert len(args) == 4
    
    # Test with nested braces
    text2 = r"\cventry{Title}{Java, Python}{\href{http://link.com}{Demo}}{Some content}"
    args2, pos2 = extract_latex_args(text2, 8, 4)
    assert args2 is not None
    assert len(args2) == 4
    assert args2[0] == 'Title'
    assert r'\href{http://link.com}{Demo}' in args2[2]


def test_escape_latex_chars():
    """Test LaTeX character escaping."""
    text = "Test_with#special$chars&more%stuff"
    escaped = escape_latex_chars(text)
    assert r'\_' in escaped
    assert r'\#' in escaped
    assert r'\$' in escaped
    assert r'\&' in escaped
    assert r'\%' in escaped


def test_clean_latex_to_plain():
    """Test LaTeX to plain text conversion."""
    latex = r"\textbf{Bold} and \textit{italic} text"
    plain = clean_latex_to_plain(latex)
    assert plain == "Bold and italic text"
    
    latex2 = r"\href{http://example.com}{Link Text}"
    plain2 = clean_latex_to_plain(latex2)
    assert plain2 == "Link Text"


def test_parse_cventry():
    """Test parsing of \\cventry commands."""
    latex = r"""
    \cventry{Project One}{Java, Spring}{\href{https://github.com/user/proj}{GitHub}}{
    \begin{itemize}
      \item Feature one
      \item Feature two
    \end{itemize}
    }
    
    \cventry{Project Two}{Python}{\href{https://example.com}{Demo}}{Description here}
    """
    
    entries = parse_cventry(latex)
    assert len(entries) == 2
    assert entries[0]['title'] == 'Project One'
    assert entries[0]['tech'] == 'Java, Spring'
    assert entries[0]['link_url'] == 'https://github.com/user/proj'
    assert entries[1]['title'] == 'Project Two'


def test_validate_url():
    """Test URL validation."""
    assert validate_url("https://github.com/user/repo") == True
    assert validate_url("http://example.com") == True
    assert validate_url("not-a-url") == False
    assert validate_url("ftp://example.com") == False  # Only http/https


def test_validate_email():
    """Test email validation."""
    assert validate_email("test@example.com") == True
    assert validate_email("user.name+tag@example.co.uk") == True
    assert validate_email("invalid@") == False
    assert validate_email("@example.com") == False
    assert validate_email("notanemail") == False


def run_all_tests():
    """Run all tests and print results."""
    tests = [
        ("Brace Matching", test_find_matching_brace),
        ("Argument Extraction", test_extract_latex_args),
        ("LaTeX Escaping", test_escape_latex_chars),
        ("LaTeX to Plain", test_clean_latex_to_plain),
        ("CVEntry Parsing", test_parse_cventry),
        ("URL Validation", test_validate_url),
        ("Email Validation", test_validate_email),
    ]
    
    passed = 0
    failed = 0
    
    print("Running tests...\n")
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Error - {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
