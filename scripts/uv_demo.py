#!/usr/bin/env python3
"""
UV Demo Script for FTT Project

This script demonstrates UV (Ultra-fast Python package installer) features
and provides an interactive CLI for common UV operations.

UV is a modern Python package manager written in Rust that aims to replace
pip, pip-tools, virtualenv, pyenv, pipx, and more with a single, fast tool.

Key Features:
- 10-100x faster than pip
- Universal lockfiles with uv.lock
- Built-in Python version management
- Project management with pyproject.toml
- Workspace support
- Tool execution with uvx
- Compatible with existing pip workflows

Usage:
    python scripts/uv_demo.py
    python scripts/uv_demo.py --help
    python scripts/uv_demo.py --info
    python scripts/uv_demo.py --benchmark

"""

import argparse
import subprocess  # nosec B404
import sys
import time
from typing import List, Optional


def run_command(cmd: List[str], description: str) -> bool:
    """Run a command and display the output."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True  # nosec
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {description}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print("Make sure UV is installed: pip install uv")
        return False


def check_uv_installed() -> bool:
    """Check if UV is installed."""
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=True  # nosec
        )
        print(f"UV version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ UV is not installed or not in PATH")
        print("Install with: pip install uv")
        return False


def list_environments() -> bool:
    """List all available UV environments."""
    return run_command(["uv", "python", "list"], "List Python versions")


def sync_dependencies() -> bool:
    """Sync project dependencies."""
    return run_command(["uv", "sync", "--dev"], "Sync dependencies")


def run_tests() -> bool:
    """Run tests with UV."""
    return run_command(
        ["uv", "run", "pytest", "--cov=src/ftt", "--cov-report=term-missing"],
        "Run tests with coverage",
    )


def run_lint() -> bool:
    """Run linting with UV."""
    commands = [
        (["uv", "run", "black", "--check", "src", "tests", "scripts"], "Black check"),
        (
            ["uv", "run", "isort", "--check-only", "src", "tests", "scripts"],
            "isort check",
        ),
        (["uv", "run", "flake8", "src", "tests", "scripts"], "Flake8 lint"),
        (["uv", "run", "mypy", "src", "tests", "scripts"], "MyPy type check"),
        (
            ["uv", "run", "bandit", "-r", "-s", "B101", "src", "scripts"],
            "Bandit security",
        ),
    ]

    all_passed = True
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            all_passed = False

    return all_passed


def build_package() -> bool:
    """Build package with UV."""
    return run_command(["uv", "build"], "Build package")


def clean_cache() -> bool:
    """Clean UV cache."""
    return run_command(["uv", "cache", "clean"], "Clean UV cache")


def show_uv_info() -> None:
    """Show comprehensive UV information."""
    print("\n" + "=" * 80)
    print("🚀 UV (Ultra-fast Python Package Manager) Information")
    print("=" * 80)

    # UV version
    run_command(["uv", "--version"], "UV Version")

    # UV help
    run_command(["uv", "--help"], "UV Help Overview")

    # Dependency tree
    run_command(["uv", "tree"], "Dependency Tree")

    # Available Python versions
    run_command(["uv", "python", "list"], "Available Python Versions")

    # Lock file status
    try:
        import os

        if os.path.exists("uv.lock"):
            size = os.path.getsize("uv.lock")
            mtime = time.ctime(os.path.getmtime("uv.lock"))
            print("\n📦 Lock file exists: uv.lock")
            print(f"Size: {size: , } bytes")
            print(f"Modified: {mtime}")
        else:
            print("\n❌ No uv.lock file found")
    except Exception as e:
        print(f"\n❌ Error checking lock file: {e}")


def benchmark_uv_vs_pip() -> None:
    """Run performance benchmark comparing UV vs pip."""
    print("\n" + "=" * 80)
    print("⚡ UV vs pip Performance Benchmark")
    print("=" * 80)

    benchmarks = {
        "Dependency Resolution": {
            "uv": "uv tree --depth 1",
            "pip": "pip list",
        },
        "Show Version": {
            "uv": "uv --version",
            "pip": "pip --version",
        },
        "Cache Info": {
            "uv": "uv cache dir",
            "pip": "pip cache dir",
        },
    }

    for test_name, commands in benchmarks.items():
        print(f"\n🔍 {test_name}")
        print("-" * 40)

        for tool, cmd in commands.items():
            start_time = time.time()
            try:
                subprocess.run(cmd.split(), capture_output=True, check=True)  # nosec
                duration = time.time() - start_time
                print(f"{tool: >4}: {duration: .4f}s")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"{tool: >4}: ❌ Failed")

    print("\n💡 UV Performance Benefits:")
    print("  • 10-100x faster dependency installation")
    print("  • 5-10x faster virtual environment creation")
    print("  • Parallel downloads and efficient caching")
    print("  • Universal lockfiles for reproducible builds")


def interactive_menu() -> None:
    """Show interactive menu for UV operations."""
    while True:
        print("\n" + "=" * 60)
        print("🚀 FTT UV Demo - Interactive Menu")
        print("=" * 60)
        print("1.  List Python versions")
        print("2.  Sync dependencies")
        print("3.  Run tests")
        print("4.  Run linting")
        print("5.  Build package")
        print("6.  Clean cache")
        print("7.  Show UV info")
        print("8.  Performance benchmark")
        print("9.  Show dependency tree")
        print("10. Export requirements.txt")
        print("0.  Exit")

        try:
            choice = input("\nEnter your choice (0-10): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            list_environments()
        elif choice == "2":
            sync_dependencies()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            run_lint()
        elif choice == "5":
            build_package()
        elif choice == "6":
            clean_cache()
        elif choice == "7":
            show_uv_info()
        elif choice == "8":
            benchmark_uv_vs_pip()
        elif choice == "9":
            run_command(["uv", "tree"], "Show dependency tree")
        elif choice == "10":
            run_command(
                [
                    "uv",
                    "export",
                    "--format",
                    "requirements-txt",
                    "--output-file",
                    "requirements.txt",
                ],
                "Export requirements.txt",
            )
        else:
            print("❌ Invalid choice. Please try again.")

        if choice != "0":
            input("\nPress Enter to continue...")


def main() -> Optional[int]:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="UV Demo Script - Showcase UV features for FTT project"
    )
    parser.add_argument(
        "--info", action="store_true", help="Show UV information and exit"
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run performance benchmark and exit"
    )

    # Add examples to help
    parser.epilog = """
Examples:
    python scripts/uv_demo.py                    # Interactive menu
    python scripts/uv_demo.py --info            # Show UV information
    python scripts/uv_demo.py --benchmark       # Run performance benchmark

UV Quick Reference:
    uv sync --dev                               # Install all dependencies
    uv add package_name                         # Add dependency
    uv remove package_name                      # Remove dependency
    uv run command                              # Run command in project env
    uvx tool_name                               # Run tool in temp env
    uv python install 3.11                     # Install Python version
    uv build                                    # Build distributions
    uv export --format requirements-txt        # Export requirements
        """

    args = parser.parse_args()

    print("🚀 FTT UV Demo Script")
    print("=" * 40)

    # Check if UV is installed
    if not check_uv_installed():
        return 1

    if args.info:
        show_uv_info()
    elif args.benchmark:
        benchmark_uv_vs_pip()
    else:
        interactive_menu()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(130)
