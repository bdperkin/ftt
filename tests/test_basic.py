"""
Basic tests for the FTT file type tester.
"""

import tempfile
from pathlib import Path

import pytest

from ftt import FileTypeTester, FileTypeCategory


class TestFileTypeTester:
    """Test the main FileTypeTester class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tester = FileTypeTester()
    
    def test_python_script(self):
        """Test detection of Python script."""
        content = """#!/usr/bin/env python3
import os
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            f.flush()
            
            result = self.tester.test_file(f.name)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "Python" in result.file_type.description
            
        Path(f.name).unlink()
    
    def test_binary_file(self):
        """Test detection of binary file."""
        # Create a file with binary content
        binary_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(binary_content)
            f.flush()
            
            result = self.tester.test_file(f.name)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "PNG" in result.file_type.description
            
        Path(f.name).unlink()
    
    def test_text_file(self):
        """Test detection of plain text file."""
        content = """This is a plain text file.
It contains multiple lines of text.
Each line contains readable ASCII characters.
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            
            result = self.tester.test_file(f.name)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "text" in result.file_type.description.lower()
            
        Path(f.name).unlink()
    
    def test_empty_file(self):
        """Test detection of empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.flush()
            
            result = self.tester.test_file(f.name)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "empty" in result.file_type.description
            
        Path(f.name).unlink()
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent file."""
        result = self.tester.test_file("/path/to/nonexistent/file")
        
        assert not result.success
        assert result.error is not None
        assert "does not exist" in result.error
    
    def test_directory(self):
        """Test detection of directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.tester.test_file(tmpdir)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.DATA
            assert "directory" in result.file_type.description
    
    def test_json_file(self):
        """Test detection of JSON file."""
        content = """{
    "name": "test",
    "version": "1.0.0",
    "description": "A test JSON file"
}"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(content)
            f.flush()
            
            result = self.tester.test_file(f.name)
            
            assert result.success
            assert result.file_type is not None
            assert result.file_type.category == FileTypeCategory.TEXT
            assert "JSON" in result.file_type.description
            
        Path(f.name).unlink()
    
    def test_multiple_files(self):
        """Test testing multiple files at once."""
        files = []
        
        # Create a Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("Hello")')
            files.append(f.name)
        
        # Create a text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Hello world')
            files.append(f.name)
        
        try:
            results = self.tester.test_files(files)
            
            assert len(results) == 2
            assert all(result.success for result in results)
            assert all(result.file_type is not None for result in results)
            
        finally:
            for filepath in files:
                Path(filepath).unlink()
    
    def test_format_result(self):
        """Test result formatting."""
        content = "Hello, world!"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            
            result = self.tester.test_file(f.name)
            formatted = self.tester.format_result(f.name, result)
            
            assert f.name in formatted
            assert "text" in formatted.lower()
            
        Path(f.name).unlink() 