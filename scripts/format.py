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
        print("Format Python code using isort and black.")
        print()
        print("Options:")
        print("  check    Check formatting without making changes")
        print("  -h, --help    Show this help message")
        return 0

    check_only = len(sys.argv) > 1 and sys.argv[1] == "check"
    paths = ["src", "tests", "scripts"]

    if check_only:
        print("🔍 Checking code formatting...")
        print()

        # Check import sorting
        isort_exit = run_command(
            ["isort", "--check-only", "--diff"] + paths, "import sorting check"
        )

        # Check code formatting
        black_exit = run_command(
            ["black", "--check", "--diff"] + paths, "code formatting check"
        )

        if isort_exit == 0 and black_exit == 0:
            print("✅ All code is properly formatted!")
            return 0
        else:
            print("❌ Code formatting issues found. Run without 'check' to fix.")
            return 1

    else:
        print("🔧 Formatting code...")
        print()

        # Sort imports
        isort_exit = run_command(["isort"] + paths, "import sorting")

        # Format code
        black_exit = run_command(["black"] + paths, "code formatting")

        if isort_exit == 0 and black_exit == 0:
            print("✅ Code formatting completed successfully!")
            return 0
        else:
            print("❌ Some formatting operations failed.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
