#!/usr/bin/env python3
"""
Test runner script for FTT project.

This script provides convenient commands for running different types of tests
using pytest and pytest-cov.

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

import os
import subprocess  # nosec
import sys
from typing import List

from pathlib import Path


def run_command(cmd: List[str]) -> int:
    """Run a command and return the exit code."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode  # nosec


def main() -> int:
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/test.py <command>")
        print()
        print("Available commands:")
        print("  all          - Run all tests with coverage")
        print("  fast         - Run tests without coverage")
        print("  coverage     - Run tests with detailed coverage report")
        print("  unit         - Run only unit tests")
        print("  integration  - Run only integration tests")
        print("  verbose      - Run tests with verbose output")
        print(
            "  specific     - Run specific test (provide test name as additional arg)"
        )
        print("  html         - Generate HTML coverage report")
        print("  clean        - Clean test artifacts")
        return 1

    command = sys.argv[1]

    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    if command == "all":
        return run_command(["pytest", "-v"])

    elif command == "fast":
        return run_command(["pytest", "-v", "--no-cov"])

    elif command == "coverage":
        return run_command(
            ["pytest", "-v", "--cov-report=term-missing", "--cov-report=html:htmlcov"]
        )

    elif command == "unit":
        return run_command(["pytest", "-v", "-m", "unit"])

    elif command == "integration":
        return run_command(["pytest", "-v", "-m", "integration"])

    elif command == "verbose":
        return run_command(["pytest", "-vvv", "--tb=long"])

    elif command == "specific":
        if len(sys.argv) < 3:
            print("Error: Please provide test name")
            print("Example: python scripts/test.py specific test_python_script")
            return 1
        test_name = sys.argv[2]
        return run_command(["pytest", "-v", "-k", test_name])

    elif command == "html":
        exit_code = run_command(
            ["pytest", "-v", "--cov-report=html:htmlcov", "--cov-report=term"]
        )
        if exit_code == 0:
            print("\nHTML coverage report generated in htmlcov/index.html")
        return exit_code

    elif command == "clean":
        print("Cleaning test artifacts...")
        artifacts = [
            ".pytest_cache",
            "htmlcov",
            ".coverage",
            "coverage.xml",
            "__pycache__",
        ]

        for artifact in artifacts:
            path = Path(artifact)
            if path.exists():
                if path.is_dir():
                    import shutil

                    shutil.rmtree(path)
                    print(f"Removed directory: {artifact}")
                else:
                    path.unlink()
                    print(f"Removed file: {artifact}")

        # Also clean __pycache__ directories recursively
        for pycache in Path(".").rglob("__pycache__"):
            if pycache.is_dir():
                import shutil

                shutil.rmtree(pycache)
                print(f"Removed: {pycache}")

        print("Test artifacts cleaned.")
        return 0

    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
