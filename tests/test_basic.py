"""
Basic tests for the FTT file type tester.

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

import tempfile

from pathlib import Path

from ftt import FileTypeTester
from ftt.types import FileTypeCategory


class TestFileTypeTester:
    """Test the main FileTypeTester class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.tester = FileTypeTester()

    def test_python_script(self) -> None:
        """Test detection of Python script."""
        content = """#!/usr/bin/env python3
import os
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            result = self.tester.test_file(f.name)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "Python" in result.file_type.description

        Path(f.name).unlink()

    def test_binary_file(self) -> None:
        """Test detection of binary file."""
        # Create a file with binary content
        binary_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(binary_content)
            f.flush()

            result = self.tester.test_file(f.name)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "PNG" in result.file_type.description

        Path(f.name).unlink()

    def test_text_file(self) -> None:
        """Test detection of plain text file."""
        content = """This is a plain text file.
It contains multiple lines of text.
Each line contains readable ASCII characters.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            f.flush()

            result = self.tester.test_file(f.name)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "text" in result.file_type.description.lower()

        Path(f.name).unlink()

    def test_empty_file(self) -> None:
        """Test detection of empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.flush()

            result = self.tester.test_file(f.name)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "empty" in result.file_type.description

        Path(f.name).unlink()

    def test_nonexistent_file(self) -> None:
        """Test handling of nonexistent file."""
        result = self.tester.test_file("/path/to/nonexistent/file")

        assert not result.success
        assert result.error is not None
        assert "does not exist" in result.error

    def test_directory(self) -> None:
        """Test detection of directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.tester.test_file(tmpdir)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "directory" in result.file_type.description

    def test_json_file(self) -> None:
        """Test detection of JSON file."""
        content = """{
    "name": "test",
    "version": "1.0.0",
    "description": "A test JSON file"
}"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(content)
            f.flush()

            result = self.tester.test_file(f.name)

            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "JSON" in result.file_type.description

        Path(f.name).unlink()

    def test_multiple_files(self) -> None:
        """Test testing multiple files at once."""
        files = []

        # Create a Python file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('print("Hello")')
            files.append(f.name)

        # Create a text file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello world")
            files.append(f.name)

        try:
            results = self.tester.test_files([Path(f) for f in files])

            assert len(results) == 2
            assert all(result.success for result in results)
            assert all(result.file_type is not None for result in results)

        finally:
            for filepath in files:
                Path(filepath).unlink()

    def test_format_result(self) -> None:
        """Test result formatting."""
        content = "Hello, world!"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            f.flush()

            result = self.tester.test_file(f.name)
            formatted = self.tester.format_result(f.name, result)

            assert f.name in formatted
            assert "text" in formatted.lower()

        Path(f.name).unlink()
