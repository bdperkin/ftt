"""
Filesystem tests for file type detection.

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
import stat
from pathlib import Path

from ..types import FileType, FileTypeCategory, TestResult


def test_filesystem(filepath: Path) -> TestResult:
    """
    Perform filesystem-based tests on a file.

    Tests include:
    - File existence
    - Directory detection
    - Executable bit detection
    - Special file types (device files, pipes, etc.)

    Args:
        filepath: Path to the file to test

    Returns:
        TestResult indicating success or failure
    """
    try:
        if not filepath.exists():
            return TestResult.failure_result(f"File does not exist: {filepath}")

        # Get file stats
        file_stat = filepath.stat()
        mode = file_stat.st_mode

        # Test for directory
        if stat.S_ISDIR(mode):
            file_type = FileType(
                category=FileTypeCategory.DATA, description="directory"
            )
            return TestResult.success_result(file_type)

        # Test for symbolic link
        if filepath.is_symlink():
            try:
                target = os.readlink(str(filepath))
            except (OSError, AttributeError):
                target = None
            description = f"symbolic link to {target}" if target else "symbolic link"
            file_type = FileType(
                category=FileTypeCategory.DATA, description=description
            )
            return TestResult.success_result(file_type)

        # Test for special files
        if stat.S_ISCHR(mode):
            file_type = FileType(
                category=FileTypeCategory.DATA, description="character special device"
            )
            return TestResult.success_result(file_type)

        if stat.S_ISBLK(mode):
            file_type = FileType(
                category=FileTypeCategory.DATA, description="block special device"
            )
            return TestResult.success_result(file_type)

        if stat.S_ISFIFO(mode):
            file_type = FileType(
                category=FileTypeCategory.DATA, description="named pipe (FIFO)"
            )
            return TestResult.success_result(file_type)

        if stat.S_ISSOCK(mode):
            file_type = FileType(category=FileTypeCategory.DATA, description="socket")
            return TestResult.success_result(file_type)

        # Test for executable bit (but only for regular files)
        if stat.S_ISREG(mode) and mode & stat.S_IXUSR:
            # Additional check: ensure it's not just a script with shebang
            # This is a basic filesystem test, more detailed checks happen in
            # magic tests
            file_type = FileType(
                category=FileTypeCategory.EXECUTABLE, description="executable"
            )
            return TestResult.success_result(file_type)

        # Test for empty file
        if file_stat.st_size == 0:
            file_type = FileType(category=FileTypeCategory.DATA, description="empty")
            return TestResult.success_result(file_type)

        # If we get here, it's a regular file that needs further testing
        return TestResult(success=False)

    except PermissionError:
        return TestResult.failure_result(f"Permission denied: {filepath}")
    except OSError as e:
        return TestResult.failure_result(f"OS error: {e}")
    except Exception as e:
        return TestResult.failure_result(f"Unexpected error: {e}")
