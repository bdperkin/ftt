#!/usr/bin/env python3
"""
Bandit demonstration and utility script for FTT project.

This script demonstrates bandit's security scanning capabilities and provides
utilities for working with security analysis.

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


def run_bandit_command(args: List[str], description: str) -> int:
    """Run a bandit command and return the exit code."""
    cmd = ["bandit"] + args
    print(f"Running: {' '.join(cmd)}")
    print(f"Description: {description}")
    result = subprocess.run(cmd)  # nosec
    print(f"Exit code: {result.returncode}")
    print()
    return result.returncode


def show_bandit_info() -> None:
    """Show bandit version and configuration information."""
    print("🔒 Bandit Security Scanner Information")
    print("=" * 40)

    # Show version
    result = subprocess.run(
        ["bandit", "--version"], capture_output=True, text=True
    )  # nosec
    if result.returncode == 0:
        print(f"Version: {result.stdout.strip()}")

    # Show configuration
    print("\nConfiguration (from pyproject.toml):")
    print("- Target directories: src, scripts (excludes tests)")
    print("- Confidence level: MEDIUM (filters low-confidence issues)")
    print("- Severity level: MEDIUM (focuses on important issues)")
    print("- Output format: screen (human-readable)")
    print("- Recursive scanning: enabled")
    print("- Context lines: 3 (shows code context)")
    print("- Excluded directories: .git, .venv, __pycache__, build dirs, tests")
    print("- Skipped tests: B101 (assert_used), B603 (subprocess_without_shell)")
    print("- Focus: Production code security (src/) and utility scripts")
    print()


def scan_security(paths: Optional[List[str]] = None) -> int:
    """Run bandit security scanning on specified paths."""
    if paths is None:
        paths = ["src", "scripts"]

    print("🔒 Running bandit security scan...")
    return run_bandit_command(
        ["-r", "-s", "B101"] + paths, "Scan code for security vulnerabilities"
    )


def scan_with_confidence(confidence: str, paths: Optional[List[str]] = None) -> int:
    """Run bandit with specific confidence level."""
    if paths is None:
        paths = ["src", "scripts"]

    print(f"🔒 Running bandit security scan with {confidence} confidence...")
    return run_bandit_command(
        ["-r", "-i", confidence.lower(), "-s", "B101"] + paths,
        f"Scan with {confidence} confidence level",
    )


def scan_with_severity(severity: str, paths: Optional[List[str]] = None) -> int:
    """Run bandit with specific severity level."""
    if paths is None:
        paths = ["src", "scripts"]

    print(f"🔒 Running bandit security scan with {severity} severity...")
    return run_bandit_command(
        ["-r", "-l", severity.lower(), "-s", "B101"] + paths,
        f"Scan with {severity} severity level",
    )


def generate_json_report(paths: Optional[List[str]] = None) -> int:
    """Generate JSON security report."""
    if paths is None:
        paths = ["src", "scripts"]

    print("🔒 Generating JSON security report...")
    return run_bandit_command(
        ["-r", "-f", "json", "-o", "bandit-report.json", "-s", "B101"] + paths,
        "Generate JSON security report",
    )


def generate_html_report(paths: Optional[List[str]] = None) -> int:
    """Generate HTML security report."""
    if paths is None:
        paths = ["src", "scripts"]

    print("🔒 Generating HTML security report...")
    return run_bandit_command(
        ["-r", "-f", "html", "-o", "bandit-report.html", "-s", "B101"] + paths,
        "Generate HTML security report",
    )


def show_baseline(paths: Optional[List[str]] = None) -> int:
    """Generate baseline for future comparisons."""
    if paths is None:
        paths = ["src", "scripts"]

    print("🔒 Generating security baseline...")
    return run_bandit_command(
        ["-r", "-f", "json", "-o", "bandit-baseline.json", "-s", "B101"] + paths,
        "Generate security baseline",
    )


def scan_specific_tests(test_ids: str, paths: Optional[List[str]] = None) -> int:
    """Run specific security tests only."""
    if paths is None:
        paths = ["src", "scripts"]

    print(f"🔒 Running specific security tests: {test_ids}")
    return run_bandit_command(
        ["-r", "-t", test_ids] + paths, f"Run specific tests: {test_ids}"
    )


def show_available_tests() -> int:
    """Show all available bandit tests."""
    print("🔒 Available bandit security tests:")
    return run_bandit_command(
        ["--help"], "Show help and list all available security tests"
    )


def main() -> int:
    """Main function for bandit demo."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/bandit_demo.py <command> [args]")
        print()
        print("Commands:")
        print("  info              Show bandit version and configuration")
        print("  scan              Run security scan on default paths")
        print("  high              Scan with HIGH confidence level")
        print("  medium            Scan with MEDIUM confidence level")
        print("  low               Scan with LOW confidence level")
        print("  severe            Scan with HIGH severity level")
        print("  json              Generate JSON report")
        print("  html              Generate HTML report")
        print("  baseline          Generate security baseline")
        print("  tests             Show available security tests")
        print("  specific <ids>    Run specific test IDs (e.g., B101,B102)")
        print()
        print("Examples:")
        print("  python scripts/bandit_demo.py info")
        print("  python scripts/bandit_demo.py scan")
        print("  python scripts/bandit_demo.py high")
        print("  python scripts/bandit_demo.py json")
        print("  python scripts/bandit_demo.py specific B101,B102")
        return 1

    command = sys.argv[1].lower()

    if command == "info":
        show_bandit_info()
        return 0
    elif command == "scan":
        return scan_security()
    elif command == "high":
        return scan_with_confidence("HIGH")
    elif command == "medium":
        return scan_with_confidence("MEDIUM")
    elif command == "low":
        return scan_with_confidence("LOW")
    elif command == "severe":
        return scan_with_severity("HIGH")
    elif command == "json":
        return generate_json_report()
    elif command == "html":
        return generate_html_report()
    elif command == "baseline":
        return show_baseline()
    elif command == "tests":
        return show_available_tests()
    elif command == "specific":
        if len(sys.argv) < 3:
            print("Error: Please specify test IDs (e.g., B101,B102)")
            return 1
        return scan_specific_tests(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
