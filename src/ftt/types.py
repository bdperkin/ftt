"""
Type definitions for the FTT file type tester.
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