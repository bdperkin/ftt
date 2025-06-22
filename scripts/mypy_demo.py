#!/usr/bin/env python3
"""
MyPy demonstration and utility script for FTT project.

This script demonstrates mypy's type checking capabilities and provides
utilities for working with static type analysis.

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


def run_mypy_command(args: List[str], description: str) -> int:
    """Run a mypy command and return the exit code."""
    cmd = ["mypy"] + args
    print(f"Running: {' '.join(cmd)}")
    print(f"Description: {description}")
    result = subprocess.run(cmd)  # nosec
    print(f"Exit code: {result.returncode}")
    print()
    return result.returncode


def show_mypy_info() -> None:
    """Show mypy version and configuration information."""
    print("🔍 MyPy Static Type Checker Information")
    print("=" * 45)

    # Show version
    result = subprocess.run(
        ["mypy", "--version"], capture_output=True, text=True
    )  # nosec
    if result.returncode == 0:
        print(f"Version: {result.stdout.strip()}")

    # Show configuration
    print("\nConfiguration (from pyproject.toml):")
    print("- Python version: 3.8+ compatibility")
    print("- Strict mode: enabled (comprehensive type checking)")
    print("- Files: src/, tests/, scripts/")
    print("- Namespace packages: supported")
    print("- Error output: codes, columns, context, pretty formatting")
    print("- Import handling: ignore missing imports for external libs")
    print("- Test relaxation: allow untyped defs in tests/")
    print()


def check_types(paths: Optional[List[str]] = None) -> int:
    """Run mypy type checking on specified paths."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🔍 Running mypy type checking...")
    return run_mypy_command(paths, "Check static types")


def check_strict(paths: Optional[List[str]] = None) -> int:
    """Run mypy with extra strict checking."""
    if paths is None:
        paths = ["src"]

    print("🔒 Running strict mypy type checking...")
    return run_mypy_command(
        ["--strict"] + paths, "Strict type checking (extra rigorous)"
    )


def show_coverage(paths: Optional[List[str]] = None) -> int:
    """Show type coverage report."""
    if paths is None:
        paths = ["src"]

    print("📊 Showing mypy type coverage...")
    return run_mypy_command(
        ["--html-report", "mypy-report"] + paths, "Generate HTML coverage report"
    )


def check_specific_errors(paths: Optional[List[str]] = None) -> int:
    """Check for specific error types."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("🎯 Checking for specific error types...")
    return run_mypy_command(
        ["--show-error-codes", "--show-column-numbers"] + paths,
        "Show detailed error information",
    )


def daemon_start() -> int:
    """Start mypy daemon for faster subsequent runs."""
    print("🚀 Starting mypy daemon...")
    return run_mypy_command(["--dmypy", "start"], "Start mypy daemon")


def daemon_run(paths: Optional[List[str]] = None) -> int:
    """Run mypy using daemon for faster checking."""
    if paths is None:
        paths = ["src", "tests", "scripts"]

    print("⚡ Running mypy with daemon...")
    return run_mypy_command(
        ["--dmypy", "run"] + paths, "Fast type checking with daemon"
    )


def main() -> int:
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/mypy_demo.py <command> [paths...]")
        print()
        print("Commands:")
        print("  info       Show mypy version and configuration")
        print("  check      Run standard type checking")
        print("  strict     Run strict type checking")
        print("  coverage   Generate HTML coverage report")
        print("  errors     Show detailed error information")
        print("  daemon     Start mypy daemon")
        print("  fast       Run with daemon (faster)")
        print()
        print("Examples:")
        print("  python scripts/mypy_demo.py info")
        print("  python scripts/mypy_demo.py check")
        print("  python scripts/mypy_demo.py strict src/")
        print("  python scripts/mypy_demo.py coverage")
        return 1

    command = sys.argv[1]
    paths = sys.argv[2:] if len(sys.argv) > 2 else None

    if command == "info":
        show_mypy_info()
        return 0
    elif command == "check":
        return check_types(paths)
    elif command == "strict":
        return check_strict(paths)
    elif command == "coverage":
        return show_coverage(paths)
    elif command == "errors":
        return check_specific_errors(paths)
    elif command == "daemon":
        return daemon_start()
    elif command == "fast":
        return daemon_run(paths)
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
