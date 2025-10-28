#!/usr/bin/env python3
"""
Fetch the latest merged PR from GitHub and generate a LaTeX snippet.
Uses GitHub's public API (no authentication required for public data).
"""

import requests
import sys
import os

# Import configuration and utilities
from config import GITHUB_USERNAME, OUTPUT_FILES, FALLBACK_PR_TEXT, GITHUB_API_TIMEOUT
from utils import logger, write_file_safe, escape_latex_chars

OUTPUT_FILE = OUTPUT_FILES['latest_pr']
FALLBACK_TEXT = FALLBACK_PR_TEXT

def get_latest_merged_pr():
    """Fetch the latest merged PR using GitHub API."""
    url = f"https://api.github.com/search/issues?q=author:{GITHUB_USERNAME}+type:pr+is:merged&sort=updated&order=desc&per_page=1"
    
    try:
        logger.info(f"Fetching latest PR for: {GITHUB_USERNAME}")
        response = requests.get(url, timeout=GITHUB_API_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('items'):
            pr = data['items'][0]
            # Use the escape_latex_chars function from utils
            title = escape_latex_chars(pr['title'])
            
            pr_url = pr['html_url']
            
            # Extract repo name from repository_url (format: https://api.github.com/repos/owner/repo)
            repo_path = pr['repository_url'].split('/repos/')[-1]
            
            logger.info(f"Found PR: {repo_path} - {pr['title']}")
            return title, pr_url, repo_path
        else:
            logger.warning("No merged PRs found.")
            return None, None, None
            
    except requests.exceptions.Timeout:
        logger.error(f"API request timeout after {GITHUB_API_TIMEOUT}s")
        return None, None, None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching PR data: {e}")
        return None, None, None
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing PR data: {e}")
        return None, None, None


def generate_latex_snippet(title, url, repo):
    """Generate LaTeX snippet for the latest PR."""
    if title and url and repo:
        # Format: Latest merged PR — org/repo (Title of PR)
        latex = rf"\item \textbf{{Active Contributor:}} Latest merged PR — \href{{{url}}}{{{repo}}} (\textit{{{title}}})"
        return latex
    else:
        return FALLBACK_TEXT


def main():
    """Main function."""
    if GITHUB_USERNAME == "yourusername":
        logger.warning("Please update GITHUB_USERNAME in scripts/config.py")
        logger.info("Using fallback text instead.")
        title, url, repo = None, None, None
    else:
        title, url, repo = get_latest_merged_pr()
    
    latex_snippet = generate_latex_snippet(title, url, repo)
    
    # Write to file using safe write
    success = write_file_safe(OUTPUT_FILE, latex_snippet + '\n')
    
    if not success:
        logger.error(f"Failed to write {OUTPUT_FILE}")
        sys.exit(1)
    
    if title:
        logger.info(f"Latest PR: {repo} - {title}")
    else:
        logger.info("Using fallback text (no PR data available)")


if __name__ == "__main__":
    main()
