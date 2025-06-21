"""
Test modules for file type detection.
"""

from .filesystem import test_filesystem
from .magic import test_magic
from .language import test_language

__all__ = ["test_filesystem", "test_magic", "test_language"] 