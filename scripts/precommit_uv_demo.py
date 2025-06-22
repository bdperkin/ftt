#!/usr/bin/env python3

"""
Pre-commit-UV Demo Script for FTT Project

This script demonstrates the integration of pre-commit-uv, which combines the power
of pre-commit's comprehensive hook system with UV's ultra-fast dependency installation.

Pre-commit-UV provides:
- 10-100x faster hook environment creation
- Lightning-fast dependency installation for Python hooks
- Full compatibility with existing pre-commit workflows
- Reduced CI/CD build times for pre-commit checks
- Better developer experience with faster hook execution

Usage:
    python scripts/precommit_uv_demo.py
    python scripts/precommit_uv_demo.py --help
    python scripts/precommit_uv_demo.py --benchmark
    python scripts/precommit_uv_demo.py --hooks
    python scripts/precommit_uv_demo.py --compare

"""

import argparse
import subprocess  # nosec B404
import sys
import time
from typing import Dict, List, Optional, Tuple


def run_command(
    cmd: List[str], description: str, capture_output: bool = True
) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")

    try:
        if capture_output:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True  # nosec
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
        else:
            subprocess.run(cmd, check=True)  # nosec
            output = "Command executed successfully"

        print(output)
        print(f"✅ {description} completed successfully")
        return True, output
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Error running {description}\nExit code: {e.returncode}"
        if hasattr(e, "stdout") and e.stdout:
            error_msg += f"\nSTDOUT: {e.stdout}"
        if hasattr(e, "stderr") and e.stderr:
            error_msg += f"\nSTDERR: {e.stderr}"
        print(error_msg)
        return False, error_msg
    except FileNotFoundError:
        error_msg = f"❌ Command not found: {cmd[0]}"
        print(error_msg)
        return False, error_msg


def check_precommit_uv_installed() -> bool:
    """Check if pre-commit-uv is installed and available."""
    try:
        result = subprocess.run(
            ["pre-commit", "--version"],
            capture_output=True,
            text=True,
            check=True,  # nosec
        )
        output = result.stdout
        if "pre-commit-uv" in output:
            print("✅ Pre-commit-UV plugin is installed and available")
            print(f"Version info: {output.strip()}")
            return True
        else:
            print("❌ Pre-commit-UV plugin not found in pre-commit installation")
            print("Install with: uv add --dev pre-commit-uv")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pre-commit is not installed or not in PATH")
        print("Install with: uv add --dev pre-commit pre-commit-uv")
        return False


def list_precommit_hooks() -> bool:
    """List all available pre-commit hooks."""
    print("\n📋 Pre-commit Hook Configuration Analysis:")

    # Define known hooks from .pre-commit-config.yaml
    uv_hooks = ["uv-lock", "uv-export"]
    standard_hooks = [
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-json",
        "check-toml",
        "check-merge-conflict",
        "check-added-large-files",
        "debug-statements",
        "check-docstring-first",
        "isort",
        "black",
        "flake8",
        "mypy",
        "bandit",
        "pytest-cov",
    ]

    print(f"UV-specific hooks: {len(uv_hooks)}")
    print(f"Standard hooks (UV accelerated): {len(standard_hooks)}")

    print("\n🚀 UV-Specific Hooks:")
    for hook in uv_hooks:
        print(f"  • {hook}")

    print("\n🔧 Standard Hooks (using UV for environments):")
    for hook in standard_hooks:
        print(f"  • {hook}")

    # Test if we can run a simple hook to verify configuration
    print("\n🔍 Testing hook configuration...")
    success, _ = run_command(
        ["pre-commit", "run", "uv-lock", "--all-files"],
        "Testing uv-lock hook",
        capture_output=True,
    )

    if success or "files were modified" in _.lower():
        print("✅ Hook configuration is working correctly")
        return True
    else:
        print("⚠️  Hook configuration may have issues")
        return False


def run_uv_hooks() -> bool:
    """Run UV-specific hooks."""
    hooks = ["uv-lock", "uv-export"]
    results = []

    for hook in hooks:
        print(f"\n🔍 Running {hook} hook")
        print("-" * 40)

        start_time = time.time()
        success, _ = run_command(
            ["pre-commit", "run", hook, "--all-files"],
            f"Running {hook}",
            capture_output=True,
        )
        duration = time.time() - start_time

        if success or "files were modified" in _.lower():
            # uv-export typically "fails" because it modifies files
            results.append((hook, duration, True))
            print(f"✅ {hook}: {duration: .2f}s")
        else:
            results.append((hook, duration, False))
            print(f"❌ {hook}: Failed")

    return len([r for r in results if r[2]]) > 0


def run_standard_hooks_sample() -> bool:
    """Run a sample of standard hooks to show UV acceleration."""
    hooks = ["trailing-whitespace", "end-of-file-fixer", "check-yaml", "black", "isort"]
    results = []

    for hook in hooks:
        print(f"\n🔍 Running {hook} hook (with UV acceleration)")
        print("-" * 50)

        start_time = time.time()
        success, output = run_command(
            ["pre-commit", "run", hook, "--all-files"],
            f"Running {hook}",
            capture_output=True,
        )
        duration = time.time() - start_time

        # Check if UV was used
        uv_used = "Using pre-commit with uv" in output

        if success:
            results.append((hook, duration, True, uv_used))
            uv_indicator = " (UV accelerated)" if uv_used else ""
            print(f"✅ {hook}: {duration: .2f}s{uv_indicator}")
        else:
            results.append((hook, duration, False, uv_used))
            print(f"❌ {hook}: Failed")

    return len([r for r in results if r[2]]) > 0


def benchmark_precommit_performance() -> None:
    """Benchmark pre-commit performance with UV acceleration."""
    print("\n" + "=" * 80)
    print("⚡ Pre-commit Performance with UV Acceleration")
    print("=" * 80)

    # Test a subset of hooks for performance
    test_hooks = [
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "isort",
        "black",
    ]

    results: Dict[str, float] = {}

    print("\n🚀 Running hooks with UV acceleration:")
    print("-" * 50)

    for hook in test_hooks:
        print(f"\n🔍 Testing {hook}")

        start_time = time.time()
        success, output = run_command(
            ["pre-commit", "run", hook, "--all-files"],
            f"Running {hook}",
            capture_output=True,
        )
        duration = time.time() - start_time

        if success:
            results[hook] = duration
            # Check if UV was mentioned in output
            uv_used = "Using pre-commit with uv" in output or "pre-commit-uv" in output
            uv_indicator = " ⚡" if uv_used else ""
            print(f"✅ {hook}: {duration: .2f}s{uv_indicator}")
        else:
            print(f"❌ {hook}: Failed")

    # Show summary
    if results:
        print("\n📊 Performance Summary:")
        total_time = sum(results.values())
        print(f"Total execution time: {total_time: .2f}s")
        print(f"Average per hook: {total_time / len(results): .2f}s")

        print("\n🏆 Fastest hooks:")
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        for hook, time_taken in sorted_results[:3]:
            print(f"  • {hook}: {time_taken: .2f}s")


def show_precommit_uv_features() -> None:
    """Show comprehensive pre-commit-uv features and capabilities."""
    print("\n" + "=" * 80)
    print("🚀 Pre-commit-UV Features and Capabilities")
    print("=" * 80)

    features = [
        ("🏃 Speed", "10-100x faster hook environment creation"),
        ("🔧 Compatibility", "Drop-in replacement for standard pre-commit"),
        ("📦 Environments", "UV-accelerated Python hook environments"),
        ("🔒 Reliability", "Uses UV's robust dependency resolution"),
        ("⚡ CI/CD", "Dramatically reduces pre-commit execution times"),
        ("🛠️ Development", "Faster hook iterations and feedback"),
        ("🌍 Cross-platform", "Works on Linux, macOS, and Windows"),
        ("🔄 Caching", "Intelligent environment and dependency caching"),
    ]

    for icon, description in features:
        print(f"{icon} {description}")

    print("\n💡 Key Benefits:")
    print("  • Faster virtual environment creation for hooks")
    print("  • Parallel dependency downloads")
    print("  • Efficient caching mechanisms")
    print("  • Reduced memory usage")
    print("  • Better error messages")
    print("  • Seamless integration with existing workflows")
    print("  • Automatic UV detection and usage")


def show_usage_examples() -> None:
    """Show practical usage examples for pre-commit-uv."""
    print("\n" + "=" * 80)
    print("📚 Pre-commit-UV Usage Examples")
    print("=" * 80)

    examples = [
        (
            "Install pre-commit with UV",
            "uv tool install pre-commit --with pre-commit-uv",
        ),
        ("Check version", "pre-commit --version"),
        ("Install hooks", "pre-commit install --install-hooks"),
        ("Run all hooks", "pre-commit run --all-files"),
        ("Run specific hook", "pre-commit run black --all-files"),
        ("Run UV-specific hooks", "pre-commit run uv-lock uv-export --all-files"),
        ("Update hook repos", "pre-commit autoupdate"),
        ("Clean hook environments", "pre-commit clean"),
        ("Show hook info", "pre-commit run --help"),
        ("Bypass hooks", "git commit --no-verify"),
    ]

    for description, command in examples:
        print(f"\n🔧 {description}:")  # noqa: E231
        print(f"   {command}")

    print("\n🎯 Pro Tips:")
    print("  • UV acceleration is automatic when pre-commit-uv is installed")
    print("  • Hook environments are cached for subsequent runs")
    print("  • Use uv-lock and uv-export hooks for dependency management")
    print("  • UV provides better error messages for dependency issues")


def show_uv_hooks_detail() -> None:
    """Show detailed information about UV-specific hooks."""
    print("\n" + "=" * 80)
    print("📋 UV-Specific Pre-commit Hooks")
    print("=" * 80)

    hooks = [
        {
            "name": "uv-lock",
            "description": "Update uv.lock when pyproject.toml changes",
            "purpose": "Keeps lock file in sync with dependencies",
            "example": "pre-commit run uv-lock --all-files",
        },
        {
            "name": "uv-export",
            "description": "Export uv.lock to requirements.txt",
            "purpose": "Maintains pip compatibility",
            "example": "pre-commit run uv-export --all-files",
        },
        {
            "name": "pip-compile",
            "description": "Compile requirements files with UV",
            "purpose": "Fast requirements compilation",
            "example": "# Configured in .pre-commit-config.yaml",
        },
    ]

    for hook in hooks:
        print(f"\n🔧 {hook['name']}")
        print(f"   Description: {hook['description']}")
        print(f"   Purpose: {hook['purpose']}")
        print(f"   Example: {hook['example']}")


def interactive_menu() -> None:
    """Show interactive menu for pre-commit-uv operations."""
    while True:
        print("\n" + "=" * 60)
        print("🚀 FTT Pre-commit-UV Demo - Interactive Menu")
        print("=" * 60)
        print("1.  Check pre-commit-uv installation")
        print("2.  List all hooks")
        print("3.  Run UV-specific hooks")
        print("4.  Run sample standard hooks")
        print("5.  Performance benchmark")
        print("6.  Show pre-commit-uv features")
        print("7.  Show usage examples")
        print("8.  Show UV hooks detail")
        print("9.  Hook comparison")
        print("0.  Exit")

        try:
            choice = input("\nEnter your choice (0-9): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            check_precommit_uv_installed()
        elif choice == "2":
            list_precommit_hooks()
        elif choice == "3":
            run_uv_hooks()
        elif choice == "4":
            run_standard_hooks_sample()
        elif choice == "5":
            benchmark_precommit_performance()
        elif choice == "6":
            show_precommit_uv_features()
        elif choice == "7":
            show_usage_examples()
        elif choice == "8":
            show_uv_hooks_detail()
        elif choice == "9":
            print("\n🔍 Hook Comparison:")
            print("Standard hooks: Accelerated by UV environments")
            print("UV hooks: Native UV functionality")
            print("\nBoth benefit from UV's speed!")
        else:
            print("❌ Invalid choice. Please try again.")

        if choice != "0":
            input("\nPress Enter to continue...")


def main() -> Optional[int]:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Pre-commit-UV Demo Script - "
        "Showcase pre-commit-uv integration for FTT project"
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run performance benchmark and exit"
    )
    parser.add_argument(
        "--hooks", action="store_true", help="Show UV hooks information and exit"
    )
    parser.add_argument(
        "--compare", action="store_true", help="Compare UV vs standard hook execution"
    )
    parser.add_argument(
        "--features", action="store_true", help="Show pre-commit-uv features and exit"
    )

    # Add examples to help
    parser.epilog = """
Examples:
    python scripts/precommit_uv_demo.py                  # Interactive menu
    python scripts/precommit_uv_demo.py --benchmark     # Performance benchmark
    python scripts/precommit_uv_demo.py --hooks         # UV hooks information
    python scripts/precommit_uv_demo.py --compare       # Hook comparison
    python scripts/precommit_uv_demo.py --features      # Show features

Pre-commit-UV Quick Reference:
    pre-commit run --all-files                          # Run all hooks with UV
    pre-commit run uv-lock --all-files                  # Update lock file
    pre-commit run uv-export --all-files                # Export requirements
    pre-commit install --install-hooks                  # Install with UV acceleration
    pre-commit autoupdate                               # Update hook repositories
        """

    args = parser.parse_args()

    print("🚀 FTT Pre-commit-UV Demo Script")
    print("=" * 40)

    # Check if pre-commit-uv is available
    if not check_precommit_uv_installed():
        print("\n⚠️  Pre-commit-UV is not installed. Install it with:")
        print(
            "   uv sync --dev  # Install all dev dependencies including pre-commit-uv"
        )
        return 1

    if args.benchmark:
        benchmark_precommit_performance()
    elif args.hooks:
        show_uv_hooks_detail()
        list_precommit_hooks()
    elif args.compare:
        print("\n🔍 Hook Comparison:")
        list_precommit_hooks()
        print("\n⚡ Testing UV hooks:")
        run_uv_hooks()
        print("\n⚡ Testing standard hooks (UV accelerated):")
        run_standard_hooks_sample()
    elif args.features:
        show_precommit_uv_features()
        show_usage_examples()
    else:
        interactive_menu()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(130)
