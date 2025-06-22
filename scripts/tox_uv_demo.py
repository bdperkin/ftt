#!/usr/bin/env python3
"""
Tox-UV Demo Script for FTT Project

This script demonstrates the integration of tox-uv, which combines the power
of tox's multi-environment testing with UV's ultra-fast dependency installation.

Tox-UV provides:
- 10-100x faster virtual environment creation
- Lightning-fast dependency installation
- Full compatibility with existing tox workflows
- Reduced CI/CD build times
- Better developer experience with faster test iterations

Usage:
    python scripts/tox_uv_demo.py
    python scripts/tox_uv_demo.py --help
    python scripts/tox_uv_demo.py --benchmark
    python scripts/tox_uv_demo.py --compare

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
    print()

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


def check_tox_uv_installed() -> bool:
    """Check if tox-uv is installed and available."""
    try:
        result = subprocess.run(
            ["tox", "--version"], capture_output=True, text=True, check=True  # nosec
        )
        output = result.stdout
        if "tox-uv" in output:
            print("✅ Tox-UV plugin is installed and available")
            print(f"Version info: {output.strip()}")
            return True
        else:
            # Check if UV environments are available even without tox-uv plugin
            list_result = subprocess.run(
                ["tox", "list"], capture_output=True, text=True, check=True  # nosec
            )
            if "uv-" in list_result.stdout:
                print("✅ UV-enhanced environments are available")
                print("Note: Using UV backend without tox-uv plugin")
                print("For full tox-uv features, install with: uv add --dev tox-uv")
                return True
            else:
                print("❌ Tox-UV plugin not found and no UV environments available")
                print("Install with: uv add --dev tox-uv")
                return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tox is not installed or not in PATH")
        print("Install with: uv add --dev tox tox-uv")
        return False


def list_tox_environments() -> bool:
    """List all available tox environments."""
    success, output = run_command(
        ["tox", "list"], "List all tox environments (standard and UV-enhanced)"
    )

    if success:
        print("\n📋 Environment Analysis:")
        lines = output.split("\n")
        standard_envs = []
        uv_envs = []

        for line in lines:
            if line.strip():
                if line.startswith("uv-"):
                    uv_envs.append(line.strip())
                else:
                    standard_envs.append(line.strip())

        print(f"Standard environments: {len(standard_envs)}")
        print(f"UV-enhanced environments: {len(uv_envs)}")

        if uv_envs:
            print("\n🚀 UV-Enhanced Environments:")
            for env in uv_envs:
                print(f"  • {env}")

    return success


def run_uv_environment_test() -> bool:
    """Run a test using UV-enhanced environment."""
    return run_command(["tox", "-e", "uv-quick"], "Run quick tests with UV backend")[0]


def run_standard_environment_test() -> bool:
    """Run a test using standard tox environment."""
    return run_command(["tox", "-e", "quick"], "Run quick tests with standard backend")[
        0
    ]


def benchmark_uv_vs_standard() -> None:
    """Benchmark UV vs standard tox performance."""
    print("\n" + "=" * 80)
    print("⚡ Tox-UV vs Standard Tox Performance Benchmark")
    print("=" * 80)

    # Test environments to benchmark
    test_cases = [
        ("uv-quick", "UV Backend - Quick Test"),
        ("quick", "Standard Backend - Quick Test"),
        ("uv-lint", "UV Backend - Linting"),
        ("lint", "Standard Backend - Linting"),
    ]

    results: Dict[str, float] = {}

    for env_name, description in test_cases:
        print(f"\n🔍 {description}")
        print("-" * 40)

        start_time = time.time()
        success, _ = run_command(
            ["tox", "-e", env_name], f"Running {env_name}", capture_output=True
        )
        duration = time.time() - start_time

        if success:
            results[env_name] = duration
            print(f"✅ {description}: {duration: .2f}s")
        else:
            print(f"❌ {description}: Failed")

    # Compare results
    if "uv-quick" in results and "quick" in results:
        uv_time = results["uv-quick"]
        standard_time = results["quick"]
        speedup = standard_time / uv_time if uv_time > 0 else 0

        print("\n📊 Performance Comparison:")
        print(f"Standard tox: {standard_time: .2f}s")
        print(f"UV tox:      {uv_time: .2f}s")
        print(f"Speedup:     {speedup: .1f}x faster")

    if "uv-lint" in results and "lint" in results:
        uv_lint_time = results["uv-lint"]
        standard_lint_time = results["lint"]
        lint_speedup = standard_lint_time / uv_lint_time if uv_lint_time > 0 else 0

        print("\n📊 Linting Performance:")
        print(f"Standard lint: {standard_lint_time: .2f}s")
        print(f"UV lint:       {uv_lint_time: .2f}s")
        print(f"Speedup:       {lint_speedup: .1f}x faster")


def show_tox_uv_features() -> None:
    """Show comprehensive tox-uv features and capabilities."""
    print("\n" + "=" * 80)
    print("🚀 Tox-UV Features and Capabilities")
    print("=" * 80)

    features = [
        ("🏃 Speed", "10-100x faster dependency installation"),
        ("🔧 Compatibility", "Drop-in replacement for standard tox"),
        ("📦 Environments", "Supports all tox environment types"),
        ("🔒 Reliability", "Uses UV's robust dependency resolution"),
        ("⚡ CI/CD", "Dramatically reduces build times"),
        ("🛠️ Development", "Faster test iterations and feedback"),
        ("🌍 Cross-platform", "Works on Linux, macOS, and Windows"),
        ("🔄 Caching", "Intelligent dependency caching"),
    ]

    for icon, description in features:
        print(f"{icon} {description}")

    print("\n💡 Key Benefits:")
    print("  • Faster virtual environment creation")
    print("  • Parallel dependency downloads")
    print("  • Efficient caching mechanisms")
    print("  • Reduced memory usage")
    print("  • Better error messages")
    print("  • Seamless integration with existing workflows")


def show_usage_examples() -> None:
    """Show practical usage examples for tox-uv."""
    print("\n" + "=" * 80)
    print("📚 Tox-UV Usage Examples")
    print("=" * 80)

    examples = [
        ("Basic UV test run", "tox -e uv-py311"),
        ("All UV environments", "tox -e uv-py{38,39,310,311,312,313}"),
        ("UV linting", "tox -e uv-lint"),
        ("UV type checking", "tox -e uv-type"),
        ("UV coverage", "tox -e uv-coverage"),
        ("UV all checks", "tox -e uv-all"),
        ("UV development env", "tox -e uv-dev"),
        ("UV quick test", "tox -e uv-quick"),
        ("UV verbose test", "tox -e uv-verbose"),
        ("UV benchmark", "tox -e uv-benchmark"),
        ("Parallel UV testing", "tox -p auto -e uv-py{310,311,312}"),
        ("Force standard backend", "tox --runner virtualenv -e py311"),
    ]

    for description, command in examples:
        print(f"\n🔧 {description}:")  # noqa: E231
        print(f"   {command}")

    print("\n🎯 Pro Tips:")
    print("  • Use 'uv-' prefixed environments for speed")
    print("  • Standard environments remain available for compatibility")
    print("  • UV environments are especially fast for large dependency sets")
    print("  • Combine with parallel execution for maximum speed")


def interactive_menu() -> None:
    """Show interactive menu for tox-uv operations."""
    while True:
        print("\n" + "=" * 60)
        print("🚀 FTT Tox-UV Demo - Interactive Menu")
        print("=" * 60)
        print("1.  Check tox-uv installation")
        print("2.  List all environments")
        print("3.  Run UV quick test")
        print("4.  Run UV linting")
        print("5.  Run UV type checking")
        print("6.  Run UV coverage")
        print("7.  Run UV all checks")
        print("8.  Performance benchmark")
        print("9.  Show tox-uv features")
        print("10. Show usage examples")
        print("11. Environment comparison")
        print("0.  Exit")

        try:
            choice = input("\nEnter your choice (0-11): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            check_tox_uv_installed()
        elif choice == "2":
            list_tox_environments()
        elif choice == "3":
            run_command(["tox", "-e", "uv-quick"], "UV Quick Test")
        elif choice == "4":
            run_command(["tox", "-e", "uv-lint"], "UV Linting")
        elif choice == "5":
            run_command(["tox", "-e", "uv-type"], "UV Type Checking")
        elif choice == "6":
            run_command(["tox", "-e", "uv-coverage"], "UV Coverage")
        elif choice == "7":
            run_command(["tox", "-e", "uv-all"], "UV All Checks")
        elif choice == "8":
            benchmark_uv_vs_standard()
        elif choice == "9":
            show_tox_uv_features()
        elif choice == "10":
            show_usage_examples()
        elif choice == "11":
            print("\n🔍 Environment Comparison:")
            print("Standard: tox -e py311")
            print("UV:       tox -e uv-py311")
            print("\nBoth run the same tests, UV is just faster!")
        else:
            print("❌ Invalid choice. Please try again.")

        if choice != "0":
            input("\nPress Enter to continue...")


def main() -> Optional[int]:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Tox-UV Demo Script - Showcase tox-uv integration for FTT project"
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run performance benchmark and exit"
    )
    parser.add_argument(
        "--compare", action="store_true", help="Compare UV vs standard environments"
    )
    parser.add_argument(
        "--features", action="store_true", help="Show tox-uv features and exit"
    )

    # Add examples to help
    parser.epilog = """
Examples:
    python scripts/tox_uv_demo.py                    # Interactive menu
    python scripts/tox_uv_demo.py --benchmark       # Performance benchmark
    python scripts/tox_uv_demo.py --compare         # Environment comparison
    python scripts/tox_uv_demo.py --features        # Show features

Tox-UV Quick Reference:
    tox -e uv-py311                                 # Run tests with UV
    tox -e uv-lint                                  # Linting with UV
    tox -e uv-all                                   # All checks with UV
    tox -p auto -e uv-py{310,311,312}              # Parallel UV testing
    tox --runner virtualenv -e py311               # Force standard backend
        """

    args = parser.parse_args()

    print("🚀 FTT Tox-UV Demo Script")
    print("=" * 40)

    # Check if tox-uv is available
    if not check_tox_uv_installed():
        print("\n⚠️  Tox-UV is not installed. Install it with:")
        print("   uv sync --dev  # Install all dev dependencies including tox-uv")
        return 1

    if args.benchmark:
        benchmark_uv_vs_standard()
    elif args.compare:
        print("\n🔍 Environment Comparison:")
        list_tox_environments()
        print("\n⚡ Testing UV vs Standard:")
        run_uv_environment_test()
        run_standard_environment_test()
    elif args.features:
        show_tox_uv_features()
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
