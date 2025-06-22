# FTT - File Type Tester

A modern Python 3 implementation of file type detection and classification.

## Overview

FTT (File Type Tester) tests each file argument in an attempt to classify it. There are three sets of tests, performed in this order:

1. **Filesystem tests** - Check file properties and permissions
2. **Magic tests** - Analyze file signatures and magic numbers
3. **Language tests** - Detect programming languages and text formats

The first test that succeeds causes the file type to be printed.

## Installation

```bash
# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Test a single file
ftt myfile.txt

# Test multiple files
ftt file1.py file2.jpg file3.txt

# Get help
ftt --help
```

## Output Format

The type printed will usually contain one of these keywords:

- **text** - The file contains only printing characters and common control characters, safe to read on an ASCII terminal
- **executable** - The file contains compiled program code understandable to UNIX kernels
- **data** - Anything else (usually binary or non-printable)

Special exceptions are made for well-known file formats (core files, tar archives) that are known to contain binary data.

## Examples

```bash
$ ftt hello.py
hello.py: Python script text

$ ftt /bin/ls
/bin/ls: ELF executable

$ ftt image.jpg
image.jpg: JPEG image data

$ ftt document.pdf
document.pdf: PDF document data
```

## Development

### Running Tests

FTT uses pytest for testing with coverage reporting:

```bash
# Run all tests with coverage
pytest

# Run tests without coverage (faster)
pytest --no-cov

# Run with verbose output
pytest -v

# Run specific test
pytest -k test_python_script

# Generate HTML coverage report
pytest --cov-report=html

# Using the test runner script
python scripts/test.py all          # All tests with coverage
python scripts/test.py fast         # Tests without coverage
python scripts/test.py html         # Generate HTML coverage report
python scripts/test.py specific test_name  # Run specific test
python scripts/test.py clean        # Clean test artifacts
```

### Code Quality

```bash
# Format code and sort imports
python scripts/format.py        # Apply formatting
python scripts/format.py check  # Check formatting only

# Individual tools
isort src/ tests/ scripts/       # Sort imports
black src/ tests/ scripts/       # Format code
mypy src/                        # Type checking
flake8 src/                      # Linting

# Run pre-commit hooks
pre-commit run --all-files
```

### Test Coverage

Current test coverage focuses on core functionality:
- File type detection (filesystem, magic, language tests)
- Multiple file processing
- Error handling
- Result formatting

Coverage reports are generated in `htmlcov/index.html` and can be viewed in a web browser.

### Import Sorting

FTT uses isort to maintain consistent import ordering:

- **Standard library imports** first
- **Third-party imports** second (separated by blank line)
- **First-party imports** last (separated by blank line)
- **Black-compatible** configuration for seamless integration

Import sections are automatically sorted alphabetically within each group.

## License

MIT License - see LICENSE file for details.
