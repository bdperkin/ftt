#!/usr/bin/env python3
"""
Black demonstration and utility script for FTT project.

This script demonstrates black's formatting capabilities and provides
utilities for working with black formatting.

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


def run_black_command(args: List[str], description: str) -> int:
    """Run a black command and return the exit code."""
    cmd = ["black"] + args
    print(f"Running: {' '.join(cmd)}")
    print(f"Description: {description}")
    result = subprocess.run(cmd)  # nosec
    print(f"Exit code: {result.returncode}")
    print()
    return result.returncode


def show_black_info() -> None:
    """Show black version and configuration information."""
    print("🖤 Black Code Formatter Information")
    print("=" * 40)

    # Show version
    result = subprocess.run(
        ["black", "--version"], capture_output=True, text=True
    )  # nosec
    if result.returncode == 0:
        print(f"Version: {result.stdout.strip()}")

    # Show configuration
    print("\nConfiguration (from pyproject.toml):")
    print("- Line length: 88 characters")
    print("- Target version: Python 3.8+")
    print("- Include: Python files (.py, .pyi)")
    print("- Preview mode: disabled (stable formatting)")
    print("- Exclude: build dirs, .venv, .git, etc.")
    print()


def check_formatting(paths: Optional[List[str]] = None) -> int:
    """Check if code is properly formatted."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🔍 Checking code formatting with black...")
    return run_black_command(
        ["--check", "--diff"] + paths, "Check formatting without making changes"
    )


def format_code(paths: Optional[List[str]] = None) -> int:
    """Format code using black."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🔧 Formatting code with black...")
    return run_black_command(paths, "Format code (makes changes)")


def show_diff(paths: Optional[List[str]] = None) -> int:
    """Show what changes black would make."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("📋 Showing formatting differences...")
    return run_black_command(
        ["--diff"] + paths, "Show formatting differences without making changes"
    )


def main() -> int:
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/black_demo.py <command> [paths...]")
        print()
        print("Commands:")
        print("  info     Show black version and configuration")
        print("  check    Check if code is properly formatted")
        print("  format   Format code (makes changes)")
        print("  diff     Show what changes would be made")
        print()
        print("Examples:")
        print("  python scripts/black_demo.py info")
        print("  python scripts/black_demo.py check")
        print("  python scripts/black_demo.py format src/")
        print("  python scripts/black_demo.py diff tests/")
        return 1

    command = sys.argv[1]
    paths = sys.argv[2:] if len(sys.argv) > 2 else None

    if command == "info":
        show_black_info()
        return 0
    elif command == "check":
        return check_formatting(paths)
    elif command == "format":
        return format_code(paths)
    elif command == "diff":
        return show_diff(paths)
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
