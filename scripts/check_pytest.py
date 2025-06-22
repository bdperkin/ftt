#!/usr/bin/env python3
# Copyright (c) 2025 Brandon Perkins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Pytest Installation Checker and Troubleshooter

This script helps diagnose and fix pytest installation issues that can cause
"Executable 'pytest' not found" errors in CI/CD pipelines and local development.
"""

import os
import shutil
import subprocess  # nosec B404
import sys
from typing import List, Tuple

from pathlib import Path


def run_command(cmd: List[str], description: str) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(  # nosec B603
            cmd, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", f"Command timed out: {' '.join(cmd)}"
    except Exception as e:
        return 1, "", f"Error running command: {e}"


def check_python_environment() -> None:
    """Check Python environment details."""
    print("🐍 Python Environment Check")
    print("=" * 50)

    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path[:3]}...")  # First 3 entries

    # Check if we're in a virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Virtual environment detected")
        if "VIRTUAL_ENV" in os.environ:
            print(f"VIRTUAL_ENV: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️  Not in a virtual environment (recommended to use one)")

    print()


def check_pytest_installation() -> bool:
    """Check if pytest is installed and accessible."""
    print("🧪 Pytest Installation Check")
    print("=" * 50)

    # Check if pytest is importable
    try:
        import pytest

        print(f"✅ pytest module found: {pytest.__file__}")
        print(f"✅ pytest version: {pytest.__version__}")
        pytest_importable = True
    except ImportError as e:
        print(f"❌ pytest module not importable: {e}")
        pytest_importable = False

    # Check if pytest executable is in PATH
    pytest_path = shutil.which("pytest")
    if pytest_path:
        print(f"✅ pytest executable found: {pytest_path}")

        # Test pytest version command
        exit_code, stdout, stderr = run_command(
            ["pytest", "--version"], "pytest version"
        )
        if exit_code == 0:
            print(f"✅ pytest executable works: {stdout.strip()}")
            pytest_executable = True
        else:
            print(f"❌ pytest executable failed: {stderr}")
            pytest_executable = False
    else:
        print("❌ pytest executable not found in PATH")
        pytest_executable = False

    print()
    return pytest_importable and pytest_executable


def check_dev_dependencies() -> None:
    """Check if dev dependencies are installed."""
    print("📦 Development Dependencies Check")
    print("=" * 50)

    dev_packages = [
        "pytest",
        "pytest_cov",
        "black",
        "flake8",
        "mypy",
        "isort",
        "bandit",
        "pre_commit",
    ]

    missing_packages = []

    for package in dev_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    else:
        print("\n✅ All dev dependencies found")

    print()


def suggest_fixes() -> None:
    """Suggest fixes for common pytest issues."""
    print("🔧 Suggested Fixes")
    print("=" * 50)

    print("If pytest is not found, try these solutions:")
    print()

    print("1. Install dev dependencies:")
    print('   pip install -e ".[dev]"')
    print()

    print("2. Install pytest directly:")
    print("   pip install pytest pytest-cov")
    print()

    print("3. Verify installation:")
    print("   which pytest")
    print("   pytest --version")
    print()

    print("4. For virtual environment issues:")
    print("   source .venv/bin/activate  # Linux/Mac")
    print("   .venv\\Scripts\\activate     # Windows")
    print()

    print("5. For pre-commit hooks:")
    print("   pip install pre-commit")
    print("   pre-commit install --install-hooks")
    print()

    print("6. For CI/CD environments:")
    print('   - Ensure pip install -e ".[dev]" runs before pytest')
    print("   - Check that virtual environment is activated")
    print("   - Verify Python version compatibility (3.8-3.13)")
    print()


def run_test_command() -> None:
    """Try to run a simple pytest command."""
    print("🏃 Test Run")
    print("=" * 50)

    if not shutil.which("pytest"):
        print("❌ Cannot run test - pytest not found")
        return

    # Try to run pytest --help
    exit_code, stdout, stderr = run_command(["pytest", "--help"], "pytest help")
    if exit_code == 0:
        print("✅ pytest --help works")
    else:
        print(f"❌ pytest --help failed: {stderr}")
        return

    # Try to run pytest --collect-only
    if Path("tests").exists():
        exit_code, stdout, stderr = run_command(
            ["pytest", "--collect-only", "-q"], "collect tests"
        )
        if exit_code == 0:
            print("✅ Test collection works")
            print(f"Found tests: {len(stdout.splitlines())} items")
        else:
            print(f"❌ Test collection failed: {stderr}")
    else:
        print("⚠️  No tests directory found")

    print()


def main() -> None:
    """Main function to run all checks."""
    print("FTT Pytest Installation Checker")
    print("=" * 50)
    print()

    check_python_environment()
    pytest_ok = check_pytest_installation()
    check_dev_dependencies()

    if pytest_ok:
        run_test_command()
        print("🎉 Pytest is properly installed and working!")
    else:
        suggest_fixes()
        print("❌ Pytest installation issues detected")
        sys.exit(1)


if __name__ == "__main__":
    main()
