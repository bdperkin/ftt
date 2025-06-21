"""
FTT - File Type Tester

A modern Python implementation of file type detection and classification.
"""

__version__ = "1.0.0"
__author__ = "User"

from .core import FileTypeTester
from .types import FileType, TestResult

__all__ = ["FileTypeTester", "FileType", "TestResult"] 