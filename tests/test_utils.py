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
    assert args is not None
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


def test_edge_cases():
    """Test edge cases and error handling."""
    # Test empty string
    assert find_matching_brace("", 0) == -1
    
    # Test escaped braces
    text = r"hello \{not a brace\} {real brace}"
    pos = find_matching_brace(text, text.index('{', 20) + 1)
    assert pos > 0
    
    # Test extract_latex_args with invalid input
    args, _ = extract_latex_args("", 0, 1)
    assert args is None
    
    # Test parse_cventry with empty string
    entries = parse_cventry("")
    assert entries == []


def test_config_import():
    """Test that config imports work correctly."""
    from config import PERSONAL_INFO, GITHUB_USERNAME, OPEN_SOURCE_CONTRIBUTIONS
    assert PERSONAL_INFO is not None
    assert GITHUB_USERNAME is not None
    assert isinstance(OPEN_SOURCE_CONTRIBUTIONS, list)
    assert len(OPEN_SOURCE_CONTRIBUTIONS) > 0


def test_format_file_size():
    """Test file size formatting function."""
    from utils import format_file_size
    
    assert format_file_size(500) == "500.0 B"
    assert format_file_size(1024) == "1.0 KB"
    assert format_file_size(1536) == "1.5 KB"
    assert format_file_size(1048576) == "1.0 MB"
    assert format_file_size(1073741824) == "1.0 GB"
    assert format_file_size(1099511627776) == "1.0 TB"


def test_get_summary_text():
    """Test summary text extraction from LaTeX."""
    from utils import get_summary_text
    
    summary = get_summary_text()
    assert summary is not None
    assert len(summary) > 0
    assert isinstance(summary, str)
    # Should not contain LaTeX commands
    assert "\\section" not in summary
    assert "\\noindent" not in summary


def test_latex_parser():
    """Test LatexParser class."""
    from utils import LatexParser
    
    latex_content = r"""
    \section{Test Section}
    Some content here
    \section{Another Section}
    More content
    """
    
    parser = LatexParser(latex_content)
    
    # Test section parsing
    section = parser.parse_section("Test Section")
    assert section is not None
    assert "Some content here" in section
    
    # Test non-existent section
    none_section = parser.parse_section("Non Existent")
    assert none_section is None
    
    # Test errors
    errors = parser.get_errors()
    assert isinstance(errors, list)


def test_double_backslash_braces():
    """Test find_matching_brace with double backslashes."""
    # Test that \\{ is not treated as escaped (the backslash is escaped, not the brace)
    text = r"hello \\{test} end"
    # Find the position after the {
    brace_pos = text.index('{') + 1
    pos = find_matching_brace(text, brace_pos)
    assert pos > 0
    assert text[pos-1] == '}'


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
        ("Edge Cases", test_edge_cases),
        ("Config Import", test_config_import),
        ("File Size Formatting", test_format_file_size),
        ("Summary Text Extraction", test_get_summary_text),
        ("LaTeX Parser", test_latex_parser),
        ("Double Backslash Braces", test_double_backslash_braces),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    print("="*60)
    print("Running Resume Generator Test Suite")
    print("="*60 + "\n")
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name:30s} PASSED")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name:30s} FAILED: {e}")
            errors.append((name, str(e)))
            failed += 1
        except Exception as e:
            print(f"✗ {name:30s} ERROR: {e}")
            errors.append((name, f"Error: {e}"))
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    
    if errors:
        print("\nFailed Tests:")
        for name, error in errors:
            print(f"  • {name}: {error}")
        print()
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("✓ All tests passed successfully!\n")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please fix the issues above.\n")
        sys.exit(1)
