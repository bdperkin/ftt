#!/usr/bin/env python3
"""
Version bump utility for FTT.

This script helps manage version updates by updating the version in the
central location and optionally creating git tags.
"""

import argparse
import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get the current version from _version.py."""
    version_file = Path(__file__).parent.parent / "src" / "ftt" / "_version.py"

    with open(version_file, "r") as f:
        content = f.read()

    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find version in _version.py")

    return match.group(1)


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump version according to semantic versioning."""
    major, minor, patch = map(int, current_version.split("."))

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_file(new_version: str) -> None:
    """Update the version in _version.py."""
    version_file = Path(__file__).parent.parent / "src" / "ftt" / "_version.py"

    with open(version_file, "r") as f:
        content = f.read()

    # Replace the version
    new_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']', f'__version__ = "{new_version}"', content
    )

    with open(version_file, "w") as f:
        f.write(new_content)

    print(f"Updated version to {new_version} in {version_file}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bump FTT version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bump_version.py patch    # 1.0.0 -> 1.0.1
  python bump_version.py minor    # 1.0.0 -> 1.1.0
  python bump_version.py major    # 1.0.0 -> 2.0.0
  python bump_version.py --set 1.2.3  # Set specific version
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Type of version bump",
    )
    group.add_argument(
        "--set", metavar="VERSION", help="Set specific version (e.g., 1.2.3)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        if args.set:
            new_version = args.set
            # Validate version format
            if not re.match(r"^\d+\.\d+\.\d+$", new_version):
                raise ValueError("Version must be in format X.Y.Z")
        else:
            new_version = bump_version(current_version, args.bump_type)

        print(f"New version: {new_version}")

        if args.dry_run:
            print("Dry run - no changes made")
        else:
            update_version_file(new_version)
            print("✓ Version updated successfully")
            print("Don't forget to:")
            print("  1. Commit the version change")
            print("  2. Create a git tag: git tag v{new_version}")
            print("  3. Push with tags: git push --tags")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
