"""
Type definitions for the FTT file type tester.

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

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FileTypeCategory(Enum):
    """Primary file type categories."""

    TEXT = "text"
    EXECUTABLE = "executable"
    DATA = "data"


@dataclass
class FileType:
    """Represents a detected file type."""

    category: FileTypeCategory
    description: str
    mime_type: Optional[str] = None
    confidence: float = 1.0

    def __str__(self) -> str:
        """Return a human-readable description."""
        if self.category.value in self.description:
            return self.description
        return f"{self.description} {self.category.value}"


@dataclass
class TestResult:
    """Result of a file type test."""

    success: bool
    file_type: Optional[FileType] = None
    error: Optional[str] = None

    @classmethod
    def success_result(cls, file_type: FileType) -> "TestResult":
        """Create a successful test result."""
        return cls(success=True, file_type=file_type)

    @classmethod
    def failure_result(cls, error: str) -> "TestResult":
        """Create a failed test result."""
        return cls(success=False, error=error)
