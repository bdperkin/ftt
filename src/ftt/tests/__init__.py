"""
Test modules for file type detection.
"""

from .filesystem import test_filesystem
from .language import test_language
from .magic import test_magic

__all__ = ["test_filesystem", "test_magic", "test_language"]
