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

```bash
# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/
```

## License

MIT License - see LICENSE file for details.
