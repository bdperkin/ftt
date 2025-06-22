#!/usr/bin/env python3
"""
Tox Demo Script for FTT Project

This script demonstrates how to use tox for testing and quality assurance
in the FTT (File Type Tester) project.

Usage:
    python scripts/tox_demo.py [command]

Commands:
    list        - List all available tox environments
    test        - Run basic tests
    lint        - Run linting checks
    type        - Run type checking
    security    - Run security checks
    coverage    - Run coverage analysis
    all         - Run all quality checks
    clean       - Clean up build artifacts
    help        - Show this help message
"""

import subprocess  # nosec B404
import sys
from typing import List

from pathlib import Path


def run_command(cmd: List[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    try:
        subprocess.run(cmd, check=True, cwd=Path.cwd())  # nosec B603, B607
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print("Make sure tox is installed: pip install tox")
        return False


def check_tox_installed() -> bool:
    """Check if tox is installed."""
    try:
        result = subprocess.run(  # nosec B603, B607
            ["tox", "--version"], capture_output=True, text=True, check=True
        )
        print(f"Tox version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tox is not installed or not in PATH")
        print("Install with: pip install tox")
        return False


def list_environments() -> bool:
    """List all available tox environments."""
    return run_command(["tox", "list"], "List tox environments")


def run_tests() -> bool:
    """Run basic tests."""
    return run_command(["tox", "-e", "py"], "Run basic tests")


def run_lint() -> bool:
    """Run linting checks."""
    return run_command(["tox", "-e", "lint"], "Run linting checks")


def run_type_check() -> bool:
    """Run type checking."""
    return run_command(["tox", "-e", "type"], "Run type checking")


def run_security() -> bool:
    """Run security checks."""
    return run_command(["tox", "-e", "security"], "Run security checks")


def run_coverage() -> bool:
    """Run coverage analysis."""
    return run_command(["tox", "-e", "coverage"], "Run coverage analysis")


def run_all_checks() -> bool:
    """Run all quality checks."""
    return run_command(["tox", "-e", "all"], "Run all quality checks")


def clean_artifacts() -> bool:
    """Clean up build artifacts."""
    return run_command(["tox", "-e", "clean"], "Clean build artifacts")


def format_code() -> bool:
    """Format code with black and isort."""
    return run_command(["tox", "-e", "format"], "Format code")


def run_parallel_tests() -> bool:
    """Run tests in parallel across multiple Python versions."""
    return run_command(
        ["tox", "-p", "auto"], "Run tests in parallel (multiple Python versions)"
    )


def show_help() -> None:
    """Show help message."""
    print(__doc__)
    print("\nCommon tox commands:")
    print("  tox                    - Run default environments")
    print("  tox -e py38            - Run tests on Python 3.8")
    print("  tox -e lint            - Run linting")
    print("  tox -e type            - Run type checking")
    print("  tox -e security        - Run security checks")
    print("  tox -e coverage        - Run with coverage")
    print("  tox -e all             - Run all checks")
    print("  tox -e clean           - Clean artifacts")
    print("  tox -p auto            - Run in parallel")
    print("  tox list               - List environments")
    print("  tox -r                 - Recreate environments")
    print("  tox -- --verbose       - Pass args to pytest")


def main() -> None:
    """Main function."""
    print("FTT Tox Demo Script")
    print("==================")

    # Check if tox is installed
    if not check_tox_installed():
        sys.exit(1)

    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    commands = {
        "list": list_environments,
        "test": run_tests,
        "lint": run_lint,
        "type": run_type_check,
        "security": run_security,
        "coverage": run_coverage,
        "all": run_all_checks,
        "clean": clean_artifacts,
        "format": format_code,
        "parallel": run_parallel_tests,
        "help": show_help,
    }

    if command in commands:
        if command == "help":
            commands[command]()
        else:
            success = commands[command]()
            if not success:
                sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
