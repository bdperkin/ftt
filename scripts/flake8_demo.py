#!/usr/bin/env python3
"""
Flake8 demonstration and utility script for FTT project.

This script demonstrates flake8's linting capabilities and provides
utilities for working with flake8 code analysis.

Copyright (c) 2025 Brandon Perkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess  # nosec
import sys
from typing import List, Optional


def run_flake8_command(args: List[str], description: str) -> int:
    """Run a flake8 command and return the exit code."""
    cmd = ["flake8"] + args
    print(f"Running: {' '.join(cmd)}")
    print(f"Description: {description}")
    result = subprocess.run(cmd)  # nosec
    print(f"Exit code: {result.returncode}")
    print()
    return result.returncode


def show_flake8_info() -> None:
    """Show flake8 version and configuration information."""
    print("🔍 Flake8 Code Linter Information")
    print("=" * 40)

    # Show version
    result = subprocess.run(
        ["flake8", "--version"], capture_output=True, text=True
    )  # nosec
    if result.returncode == 0:
        print(f"Version: {result.stdout.strip()}")

    # Show configuration
    print("\nConfiguration (from .flake8):")
    print("- Max line length: 88 characters (black compatible)")
    print("- Ignored codes: E203, E501, W503, W504 (black conflicts)")
    print("- Max complexity: 15 (McCabe complexity)")
    print("- Docstring convention: Google style")
    print("- Exclude: build dirs, .venv, .git, etc.")
    print("- Per-file ignores: __init__.py imports, test assertions")
    print()


def lint_code(paths: Optional[List[str]] = None) -> int:
    """Run flake8 linting on specified paths."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🔍 Running flake8 linting...")
    return run_flake8_command(paths, "Lint code for style and errors")


def show_statistics(paths: Optional[List[str]] = None) -> int:
    """Show flake8 statistics."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("📊 Showing flake8 statistics...")
    return run_flake8_command(["--statistics"] + paths, "Show error statistics")


def check_complexity(paths: Optional[List[str]] = None) -> int:
    """Check code complexity only."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🧮 Checking code complexity...")
    return run_flake8_command(["--select=C901"] + paths, "Check McCabe complexity only")


def show_ignored_errors(paths: Optional[List[str]] = None) -> int:
    """Show what errors are being ignored."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🔇 Showing ignored errors...")
    return run_flake8_command(
        ["--extend-ignore="] + paths, "Show all errors (nothing ignored)"
    )


def main() -> int:
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/flake8_demo.py <command> [paths...]")
        print()
        print("Commands:")
        print("  info        Show flake8 version and configuration")
        print("  lint        Run standard linting")
        print("  stats       Show error statistics")
        print("  complexity  Check code complexity only")
        print("  ignored     Show what errors are being ignored")
        print()
        print("Examples:")
        print("  python scripts/flake8_demo.py info")
        print("  python scripts/flake8_demo.py lint")
        print("  python scripts/flake8_demo.py complexity src/")
        print("  python scripts/flake8_demo.py stats tests/")
        return 1

    command = sys.argv[1]
    paths = sys.argv[2:] if len(sys.argv) > 2 else None

    if command == "info":
        show_flake8_info()
        return 0
    elif command == "lint":
        return lint_code(paths)
    elif command == "stats":
        return show_statistics(paths)
    elif command == "complexity":
        return check_complexity(paths)
    elif command == "ignored":
        return show_ignored_errors(paths)
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
