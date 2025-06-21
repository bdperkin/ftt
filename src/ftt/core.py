"""
Core functionality for the FTT file type tester.
"""

from pathlib import Path
from typing import List, Optional

from .tests import test_filesystem, test_magic, test_language
from .types import FileType, FileTypeCategory, TestResult


class FileTypeTester:
    """
    Main class for testing and classifying file types.
    
    Performs three sets of tests in order:
    1. Filesystem tests - Check file properties and permissions
    2. Magic tests - Analyze file signatures and magic numbers  
    3. Language tests - Detect programming languages and text formats
    
    The first test that succeeds determines the file type.
    """
    
    def __init__(self) -> None:
        """Initialize the file type tester."""
        pass
    
    def test_file(self, filepath: str | Path) -> TestResult:
        """
        Test a single file to determine its type.
        
        Args:
            filepath: Path to the file to test
            
        Returns:
            TestResult containing the detected file type or error information
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)
        
        # Perform tests in order: filesystem, magic, language
        test_functions = [
            ("filesystem", test_filesystem),
            ("magic", test_magic),  
            ("language", test_language),
        ]
        
        for test_name, test_func in test_functions:
            try:
                result = test_func(filepath)
                if result.success and result.file_type:
                    return result
                elif result.error:
                    # If there's an error, return it immediately
                    return result
            except Exception as e:
                return TestResult.failure_result(f"Error in {test_name} test: {e}")
        
        # If none of the tests succeeded, return a default classification
        return TestResult.success_result(
            FileType(
                category=FileTypeCategory.DATA,
                description="data"
            )
        )
    
    def test_files(self, filepaths: List[str | Path]) -> List[TestResult]:
        """
        Test multiple files to determine their types.
        
        Args:
            filepaths: List of file paths to test
            
        Returns:
            List of TestResult objects, one for each file
        """
        results = []
        for filepath in filepaths:
            result = self.test_file(filepath)
            results.append(result)
        return results
    
    def format_result(self, filepath: str | Path, result: TestResult) -> str:
        """
        Format a test result for display.
        
        Args:
            filepath: Path to the file that was tested
            result: TestResult from testing the file
            
        Returns:
            Formatted string suitable for display
        """
        filepath_str = str(filepath)
        
        if result.error:
            return f"{filepath_str}: {result.error}"
        elif result.file_type:
            return f"{filepath_str}: {result.file_type}"
        else:
            return f"{filepath_str}: unknown"
    
    def classify_file(self, filepath: str | Path) -> Optional[FileType]:
        """
        Classify a single file and return just the FileType.
        
        Args:
            filepath: Path to the file to classify
            
        Returns:
            FileType object if successful, None if failed
        """
        result = self.test_file(filepath)
        return result.file_type if result.success else None 