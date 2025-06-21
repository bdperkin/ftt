"""
Language tests for file type detection based on content analysis and extensions.
"""

import re
from pathlib import Path
from typing import Dict, List, Pattern, Tuple

from ..types import FileType, FileTypeCategory, TestResult

# Programming language patterns: (extension, patterns, description)
LANGUAGE_PATTERNS: Dict[str, Tuple[List[Pattern[str]], str]] = {
    ".py": (
        [
            re.compile(r"^\s*#.*?coding[:=]\s*([-\w.]+)", re.MULTILINE),
            re.compile(r"^\s*import\s+\w+", re.MULTILINE),
            re.compile(r"^\s*from\s+\w+\s+import", re.MULTILINE),
            re.compile(r"^\s*def\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"^\s*class\s+\w+\s*(\(|\:)", re.MULTILINE),
            re.compile(r'^\s*if\s+__name__\s*==\s*["\']__main__["\']', re.MULTILINE),
        ],
        "Python script",
    ),
    ".js": (
        [
            re.compile(r"function\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"var\s+\w+\s*=", re.MULTILINE),
            re.compile(r"let\s+\w+\s*=", re.MULTILINE),
            re.compile(r"const\s+\w+\s*=", re.MULTILINE),
            re.compile(r"console\.log\s*\(", re.MULTILINE),
            re.compile(r'require\s*\(\s*["\']', re.MULTILINE),
        ],
        "JavaScript source",
    ),
    ".java": (
        [
            re.compile(r"public\s+class\s+\w+", re.MULTILINE),
            re.compile(r"private\s+\w+\s+\w+", re.MULTILINE),
            re.compile(r"public\s+static\s+void\s+main", re.MULTILINE),
            re.compile(r"import\s+java\.", re.MULTILINE),
            re.compile(r"System\.out\.print", re.MULTILINE),
        ],
        "Java source",
    ),
    ".c": (
        [
            re.compile(r"#include\s*<\w+\.h>", re.MULTILINE),
            re.compile(r"int\s+main\s*\(", re.MULTILINE),
            re.compile(r"printf\s*\(", re.MULTILINE),
            re.compile(r"void\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"#define\s+\w+", re.MULTILINE),
        ],
        "C source",
    ),
    ".cpp": (
        [
            re.compile(r"#include\s*<iostream>", re.MULTILINE),
            re.compile(r"std::", re.MULTILINE),
            re.compile(r"cout\s*<<", re.MULTILINE),
            re.compile(r"namespace\s+\w+", re.MULTILINE),
            re.compile(r"class\s+\w+\s*{", re.MULTILINE),
        ],
        "C++ source",
    ),
    ".h": (
        [
            re.compile(r"#ifndef\s+\w+", re.MULTILINE),
            re.compile(r"#define\s+\w+", re.MULTILINE),
            re.compile(r"#endif", re.MULTILINE),
            re.compile(r'extern\s+"C"', re.MULTILINE),
        ],
        "C header",
    ),
    ".rs": (
        [
            re.compile(r"fn\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"use\s+std::", re.MULTILINE),
            re.compile(r"let\s+\w+\s*=", re.MULTILINE),
            re.compile(r"impl\s+\w+", re.MULTILINE),
            re.compile(r"struct\s+\w+", re.MULTILINE),
        ],
        "Rust source",
    ),
    ".go": (
        [
            re.compile(r"package\s+\w+", re.MULTILINE),
            re.compile(r"import\s*\(", re.MULTILINE),
            re.compile(r"func\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"fmt\.Print", re.MULTILINE),
            re.compile(r"type\s+\w+\s+struct", re.MULTILINE),
        ],
        "Go source",
    ),
    ".rb": (
        [
            re.compile(r"def\s+\w+", re.MULTILINE),
            re.compile(r"class\s+\w+", re.MULTILINE),
            re.compile(r'require\s+["\']', re.MULTILINE),
            re.compile(r"puts\s+", re.MULTILINE),
            re.compile(r"end\s*$", re.MULTILINE),
        ],
        "Ruby script",
    ),
    ".php": (
        [
            re.compile(r"<\?php", re.MULTILINE),
            re.compile(r"function\s+\w+\s*\(", re.MULTILINE),
            re.compile(r"\$\w+\s*=", re.MULTILINE),
            re.compile(r"echo\s+", re.MULTILINE),
            re.compile(r"require_once\s+", re.MULTILINE),
        ],
        "PHP script",
    ),
    ".pl": (
        [
            re.compile(r"#!/usr/bin/perl", re.MULTILINE),
            re.compile(r"use\s+strict;", re.MULTILINE),
            re.compile(r"sub\s+\w+\s*{", re.MULTILINE),
            re.compile(r"my\s+\$\w+", re.MULTILINE),
            re.compile(r"print\s+", re.MULTILINE),
        ],
        "Perl script",
    ),
}

# Text file patterns by extension
TEXT_EXTENSIONS = {
    ".txt": "ASCII text",
    ".md": "Markdown text",
    ".rst": "reStructuredText text",
    ".tex": "LaTeX text",
    ".csv": "CSV text",
    ".tsv": "TSV text",
    ".json": "JSON text",
    ".xml": "XML text",
    ".yaml": "YAML text",
    ".yml": "YAML text",
    ".toml": "TOML text",
    ".ini": "INI configuration text",
    ".cfg": "configuration text",
    ".conf": "configuration text",
    ".log": "log text",
    ".sql": "SQL text",
    ".html": "HTML text",
    ".htm": "HTML text",
    ".css": "CSS text",
    ".scss": "SCSS text",
    ".sass": "Sass text",
    ".less": "LESS text",
    ".dockerfile": "Dockerfile text",
    ".makefile": "Makefile text",
    ".gitignore": "gitignore text",
    ".gitattributes": "gitattributes text",
    ".editorconfig": "EditorConfig text",
    ".bash_profile": "Bash profile text",
    ".bashrc": "Bash configuration text",
    ".zshrc": "Zsh configuration text",
    ".vimrc": "Vim configuration text",
}

# Content-based text detection patterns
TEXT_CONTENT_PATTERNS = [
    (re.compile(r"^\s*{[\s\S]*}\s*$", re.MULTILINE), "JSON text"),
    (re.compile(r"^\s*<\?xml", re.MULTILINE), "XML text"),
    (re.compile(r"^\s*<!DOCTYPE\s+html", re.MULTILINE | re.IGNORECASE), "HTML text"),
    (re.compile(r"^\s*<html", re.MULTILINE | re.IGNORECASE), "HTML text"),
    (
        re.compile(r"^\s*SELECT\s+.*\s+FROM\s+", re.MULTILINE | re.IGNORECASE),
        "SQL text",
    ),
    (re.compile(r"^\s*INSERT\s+INTO\s+", re.MULTILINE | re.IGNORECASE), "SQL text"),
    (
        re.compile(r"^\s*CREATE\s+(TABLE|DATABASE)", re.MULTILINE | re.IGNORECASE),
        "SQL text",
    ),
    (re.compile(r"^\s*#\s*[A-Za-z].*$", re.MULTILINE), "text with comments"),
    (re.compile(r"^\s*//.*$", re.MULTILINE), "source code text"),
    (re.compile(r"^\s*/\*[\s\S]*?\*/", re.MULTILINE), "source code text"),
]


def test_language(filepath: Path) -> TestResult:
    """
    Perform language-based tests on a file to detect programming languages and
    text types.

    Args:
        filepath: Path to the file to test

    Returns:
        TestResult indicating success or failure
    """
    try:
        # First, try to determine type based on file extension
        extension = filepath.suffix.lower()
        filename = filepath.name.lower()

        # Special handling for files without extensions but known names
        if not extension:
            if filename in ("makefile", "dockerfile", "rakefile", "gemfile"):
                file_type = FileType(
                    category=FileTypeCategory.TEXT,
                    description=f"{filename.title()} text",
                )
                return TestResult.success_result(file_type)
            elif filename.startswith("."):
                # Hidden configuration files
                file_type = FileType(
                    category=FileTypeCategory.TEXT, description="configuration text"
                )
                return TestResult.success_result(file_type)

        # Check for known text extensions
        if extension in TEXT_EXTENSIONS:
            file_type = FileType(
                category=FileTypeCategory.TEXT, description=TEXT_EXTENSIONS[extension]
            )
            return TestResult.success_result(file_type)

        # Read file content for analysis
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(4096)  # Read first 4KB for analysis
        except UnicodeDecodeError:
            # If we can't read as text, it's likely binary
            return TestResult(success=False)

        if not content.strip():
            # Empty or whitespace-only file
            return TestResult(success=False)

        # Check for programming language patterns
        if extension in LANGUAGE_PATTERNS:
            patterns, description = LANGUAGE_PATTERNS[extension]
            matches = sum(1 for pattern in patterns if pattern.search(content))

            # If we have at least 2 pattern matches, consider it a match
            if matches >= 2:
                file_type = FileType(
                    category=FileTypeCategory.TEXT, description=f"{description} text"
                )
                return TestResult.success_result(file_type)

        # Check for content-based patterns
        for pattern, description in TEXT_CONTENT_PATTERNS:
            if pattern.search(content):
                file_type = FileType(
                    category=FileTypeCategory.TEXT, description=description
                )
                return TestResult.success_result(file_type)

        # Check if content appears to be plain text
        if _is_plain_text(content):
            file_type = FileType(
                category=FileTypeCategory.TEXT, description="ASCII text"
            )
            return TestResult.success_result(file_type)

        # If we get here, language tests didn't identify the file
        return TestResult(success=False)

    except PermissionError:
        return TestResult.failure_result(f"Permission denied: {filepath}")
    except OSError as e:
        return TestResult.failure_result(f"OS error: {e}")
    except Exception as e:
        return TestResult.failure_result(f"Unexpected error: {e}")


def _is_plain_text(content: str) -> bool:
    """
    Determine if the content appears to be plain text.

    Checks for printable characters and reasonable line structure.
    """
    if not content:
        return False

    # Count printable characters
    printable_count = 0
    total_chars = len(content)

    for char in content:
        if char.isprintable() or char in ("\n", "\r", "\t"):
            printable_count += 1

    # If more than 95% of characters are printable, consider it text
    if total_chars > 0 and (printable_count / total_chars) > 0.95:
        # Additional check: reasonable line structure
        lines = content.split("\n")
        if len(lines) > 1:
            # Check average line length (shouldn't be too long for text files)
            avg_line_length = sum(len(line) for line in lines) / len(lines)
            if avg_line_length < 200:  # Reasonable line length
                return True
        elif len(lines) == 1 and len(content) < 1000:
            # Single line that's not too long
            return True

    return False
