"""
Command-line interface for the FTT file type tester.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from . import __version__
from .core import FileTypeTester


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='ftt',
        description='File Type Tester - Classify files by type',
        epilog='Examples:\n'
               '  ftt myfile.txt              # Test a single file\n'
               '  ftt file1.py file2.jpg      # Test multiple files\n'
               '  ftt /path/to/directory/*    # Test all files in directory',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'files',
        nargs='*',
        help='Files to test (if none provided, reads from stdin)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--mime-type',
        action='store_true',
        help='Also output MIME type if available'
    )
    
    return parser


def read_files_from_stdin() -> List[str]:
    """Read file paths from stdin, one per line."""
    files = []
    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                files.append(line)
    except KeyboardInterrupt:
        pass
    return files


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Get list of files to test
    files_to_test = []
    if args.files:
        files_to_test = args.files
    else:
        # Read from stdin
        files_to_test = read_files_from_stdin()
    
    if not files_to_test:
        parser.print_help()
        return 1
    
    # Initialize the file type tester
    tester = FileTypeTester()
    exit_code = 0
    
    # Test each file
    for filepath in files_to_test:
        try:
            path = Path(filepath)
            result = tester.test_file(path)
            
            # Format output
            if args.mime_type and result.file_type and result.file_type.mime_type:
                output = f"{filepath}: {result.file_type}; charset=unknown; {result.file_type.mime_type}"
            else:
                output = tester.format_result(filepath, result)
            
            print(output)
            
            # Set exit code if there was an error
            if result.error:
                exit_code = 1
                
        except KeyboardInterrupt:
            print("\nInterrupted", file=sys.stderr)
            return 130
        except Exception as e:
            print(f"{filepath}: Error - {e}", file=sys.stderr)
            exit_code = 1
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main()) 