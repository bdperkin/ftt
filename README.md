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
# Format code and sort imports (includes flake8 linting + mypy type checking + bandit security)
python scripts/format.py        # Apply formatting + lint + type check + security scan
python scripts/format.py check  # Check formatting + linting + types + security

# Black code formatter utilities
python scripts/black_demo.py info      # Show black version and config
python scripts/black_demo.py check     # Check formatting
python scripts/black_demo.py format    # Apply formatting
python scripts/black_demo.py diff      # Show formatting differences

# Flake8 linting utilities
python scripts/flake8_demo.py info        # Show flake8 version and config
python scripts/flake8_demo.py lint        # Run standard linting
python scripts/flake8_demo.py stats       # Show error statistics
python scripts/flake8_demo.py complexity  # Check code complexity only
python scripts/flake8_demo.py ignored     # Show ignored errors

# MyPy type checking utilities
python scripts/mypy_demo.py info       # Show mypy version and config
python scripts/mypy_demo.py check      # Run standard type checking
python scripts/mypy_demo.py strict     # Run strict type checking
python scripts/mypy_demo.py coverage   # Generate HTML coverage report
python scripts/mypy_demo.py errors     # Show detailed error information
python scripts/mypy_demo.py daemon     # Start mypy daemon
python scripts/mypy_demo.py fast       # Run with daemon (faster)

# Bandit security scanning utilities
python scripts/bandit_demo.py info     # Show bandit version and config
python scripts/bandit_demo.py scan     # Run standard security scan
python scripts/bandit_demo.py high     # Scan with HIGH confidence level
python scripts/bandit_demo.py medium   # Scan with MEDIUM confidence level
python scripts/bandit_demo.py low      # Scan with LOW confidence level
python scripts/bandit_demo.py severe   # Scan with HIGH severity level
python scripts/bandit_demo.py json     # Generate JSON security report
python scripts/bandit_demo.py html     # Generate HTML security report
python scripts/bandit_demo.py baseline # Generate security baseline
python scripts/bandit_demo.py tests    # Show available security tests

# Individual tools
isort src/ tests/ scripts/       # Sort imports
black src/ tests/ scripts/       # Format code
flake8 src/ tests/ scripts/      # Lint code
mypy src/ tests/ scripts/        # Type checking
bandit -r -s B101 src/ scripts/  # Security scanning (excludes tests)

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

### Code Formatting

FTT uses Black for consistent Python code formatting:

- **Line length**: 88 characters (PEP 8 compliant)
- **Target version**: Python 3.8+ compatibility
- **File types**: Python source (.py) and stub (.pyi) files
- **Preview mode**: Disabled for stable formatting
- **Exclusions**: Build directories, .venv, .git, and other artifacts

Black automatically handles:
- String quote normalization
- Trailing comma insertion
- Line length optimization
- Consistent indentation and spacing

### Code Linting

FTT uses Flake8 for comprehensive Python code linting:

- **Configuration**: Centralized in `pyproject.toml` (via flake8-pyproject plugin)
- **Line length**: 88 characters (compatible with Black)
- **Ignored codes**: E203, E501, W503, W504 (conflicts with Black)
- **Complexity**: McCabe complexity threshold of 15
- **Docstring style**: Google convention
- **Exclusions**: Build directories, .venv, .git, and cache folders

Flake8 checks for:
- PEP 8 style violations
- Logical errors and unused imports
- Code complexity (McCabe)
- Docstring presence and format
- Security issues (with bandit integration)

### Static Type Checking

FTT uses MyPy for comprehensive static type analysis:

- **Configuration**: Centralized in `pyproject.toml` with strict mode enabled
- **Python version**: 3.8+ compatibility with modern type hints
- **Strict mode**: Comprehensive type checking with all warnings enabled
- **Files**: src/, tests/, scripts/ with namespace package support
- **Error output**: Detailed with codes, columns, context, and pretty formatting
- **HTML reports**: Type coverage reports generated in `mypy-report/`
- **Daemon mode**: Fast incremental checking for development

MyPy checks for:
- Type annotation completeness and correctness
- Function signature compatibility
- Variable type consistency
- Generic type usage and bounds
- Import resolution and module structure
- Unreachable code and logical errors

### Security Scanning

FTT uses Bandit for comprehensive security vulnerability scanning:

- **Configuration**: Centralized in `pyproject.toml` with MEDIUM confidence/severity
- **Target directories**: src/, scripts/ with recursive scanning (excludes tests/)
- **Confidence levels**: LOW, MEDIUM, HIGH (filters noise vs thoroughness)
- **Severity levels**: LOW, MEDIUM, HIGH (focuses on important issues)
- **Output formats**: screen (human-readable), JSON, HTML, XML, CSV
- **Context lines**: 3 lines of code context for each issue
- **Exclusions**: Build directories, .venv, .git, and cache folders
- **Report generation**: JSON and HTML reports for CI/CD integration

Bandit checks for:
- Hardcoded passwords and secrets
- SQL injection vulnerabilities
- Shell injection risks
- Insecure random number generation
- Unsafe file operations and permissions
- Cryptographic weaknesses
- Network security issues
- Input validation problems

Security reports are generated as:
- **bandit-report.json**: Machine-readable format for CI/CD
- **bandit-report.html**: Human-readable format for review
- **bandit-baseline.json**: Baseline for tracking new issues

## License

MIT License - see LICENSE file for details.
