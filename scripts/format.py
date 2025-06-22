#!/usr/bin/env python3
"""
Code formatting script for FTT project.

This script runs black and isort to format Python code consistently.

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
from typing import List


def run_command(cmd: List[str], description: str) -> int:
    """Run a command and return the exit code."""
    print(f"Running {description}...")
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd)  # nosec
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
    else:
        print(f"❌ {description} failed with exit code {result.returncode}")
    print()
    return result.returncode


def main() -> int:
    """Main formatting function."""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("Usage: python scripts/format.py [check]")
        print()
        print("Format Python code using isort, black, flake8, mypy, and bandit.")
        print()
        print("Options:")
        print(
            "  check    Check formatting, linting, types, and security "
            "without making changes"
        )
        print("  -h, --help    Show this help message")
        return 0

    check_only = len(sys.argv) > 1 and sys.argv[1] == "check"
    paths = ["src", "tests", "scripts"]

    if check_only:
        print("🔍 Checking code formatting, linting, types, and security...")
        print()

        # Check import sorting
        isort_exit = run_command(
            ["isort", "--check-only", "--diff"] + paths, "import sorting check"
        )

        # Check code formatting
        black_exit = run_command(
            ["black", "--check", "--diff"] + paths, "code formatting check"
        )

        # Check linting
        flake8_exit = run_command(["flake8"] + paths, "code linting check")

        # Check types
        mypy_exit = run_command(["mypy"] + paths, "static type checking")

        # Check security (exclude tests directory, skip B101)
        bandit_exit = run_command(
            ["bandit", "-r", "-s", "B101", "src", "scripts"], "security scanning"
        )

        if (
            isort_exit == 0
            and black_exit == 0
            and flake8_exit == 0
            and mypy_exit == 0
            and bandit_exit == 0
        ):
            print("✅ All code is properly formatted, linted, type-checked, and secure!")
            return 0
        else:
            print("❌ Code quality issues found. Run without 'check' to fix formatting.")
            return 1

    else:
        print("🔧 Formatting code...")
        print()

        # Sort imports
        isort_exit = run_command(["isort"] + paths, "import sorting")

        # Format code
        black_exit = run_command(["black"] + paths, "code formatting")

        # Lint code (informational only, doesn't fix issues)
        print("🔍 Running linting check...")
        flake8_exit = run_command(["flake8"] + paths, "code linting")

        # Check types (informational only, doesn't fix issues)
        print("🔍 Running type check...")
        mypy_exit = run_command(["mypy"] + paths, "static type checking")

        # Check security (informational only, doesn't fix issues)
        print("🔍 Running security scan...")
        bandit_exit = run_command(
            ["bandit", "-r", "-s", "B101", "src", "scripts"], "security scanning"
        )

        if isort_exit == 0 and black_exit == 0:
            print("✅ Code formatting completed successfully!")
            if flake8_exit != 0:
                print("⚠️  Some linting issues found (see above)")
            if mypy_exit != 0:
                print("⚠️  Some type checking issues found (see above)")
            if bandit_exit != 0:
                print("⚠️  Some security issues found (see above)")
            return 0
        else:
            print("❌ Some formatting operations failed.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
