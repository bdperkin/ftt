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

# Tox testing utilities
python scripts/tox_demo.py list        # List all tox environments
python scripts/tox_demo.py test        # Run basic tests
python scripts/tox_demo.py lint        # Run linting checks
python scripts/tox_demo.py type        # Run type checking
python scripts/tox_demo.py security    # Run security checks
python scripts/tox_demo.py coverage    # Run coverage analysis
python scripts/tox_demo.py all         # Run all quality checks
python scripts/tox_demo.py clean       # Clean build artifacts
python scripts/tox_demo.py format      # Format code
python scripts/tox_demo.py parallel    # Run tests in parallel

# Individual tools
isort src/ tests/ scripts/       # Sort imports
black src/ tests/ scripts/       # Format code
flake8 src/ tests/ scripts/      # Lint code
mypy src/ tests/ scripts/        # Type checking
bandit -r -s B101 src/ scripts/  # Security scanning (excludes tests)

# Tox commands
tox                              # Run default environments
tox -e py38,py39,py310          # Run specific Python versions
tox -e lint                     # Run linting only
tox -e type                     # Run type checking only
tox -e security                 # Run security scanning only
tox -e coverage                 # Run with coverage
tox -e all                      # Run all quality checks
tox -p auto                     # Run in parallel
tox -r                          # Recreate environments

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

### Multi-Environment Testing with Tox

FTT uses Tox for comprehensive testing across multiple Python versions and environments:

- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Quality environments**: lint, type, security, coverage
- **Utility environments**: format, clean, build, dev
- **Parallel execution**: Run tests across multiple versions simultaneously
- **Isolated builds**: Each environment uses isolated package builds

**Key Tox environments:**

```bash
# Testing environments
tox -e py38                 # Test on Python 3.8
tox -e py39                 # Test on Python 3.9
tox -e py310                # Test on Python 3.10
tox -e py311                # Test on Python 3.11
tox -e py312                # Test on Python 3.12
tox -e py313                # Test on Python 3.13

# Quality assurance environments
tox -e lint                 # Run all linting tools (black, isort, flake8)
tox -e type                 # Run type checking with mypy
tox -e security             # Run security scanning with bandit
tox -e coverage             # Run tests with full coverage reporting

# Utility environments
tox -e format               # Format code with black and isort
tox -e clean                # Clean build artifacts and cache files
tox -e build                # Build and validate package
tox -e dev                  # Set up development environment
tox -e all                  # Run all quality checks in sequence

# Convenience environments
tox -e quick                # Quick test run without coverage
tox -e verbose              # Verbose test run with detailed output
```

**Common Tox workflows:**

```bash
# Run all default environments (Python versions + quality)
tox

# Run tests in parallel across all Python versions
tox -p auto

# Run specific environments in parallel
tox -p auto -e py38,py39,py310,lint,type

# Run tests with specific pytest arguments
tox -e py39 -- --verbose --tb=short

# Recreate environments (useful after dependency changes)
tox -r

# List all available environments
tox list

# Run comprehensive quality checks
tox -e all

# Development workflow
tox -e format               # Format code
tox -e lint                 # Check formatting and linting
tox -e type                 # Check types
tox -e py311                # Test on your development Python version
```

**Tox configuration highlights:**

- **Isolated builds**: Each environment builds the package independently
- **Dependency management**: Each environment specifies its own dependencies
- **Skip missing interpreters**: Tests continue even if some Python versions are missing
- **Wheel packaging**: Uses modern wheel-based package installation
- **Coverage integration**: Coverage reports generated in htmlcov/ and coverage.xml
- **Security reports**: Bandit generates JSON and console reports

### Ultra-Fast Development with UV

FTT supports UV, the next-generation Python package manager written in Rust that's 10-100x faster than pip:

- **Lightning-fast installs**: Parallel downloads and efficient caching
- **Universal lockfiles**: Cross-platform reproducible builds with `uv.lock`
- **Python version management**: Install and manage Python versions automatically
- **Project management**: Modern pyproject.toml-based workflow
- **Tool execution**: Run tools in isolated environments with `uvx`
- **Workspace support**: Manage multiple related packages

**UV Installation:**

```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Verify installation
uv --version
```

**UV Workflow:**

```bash
# Project setup and dependency management
uv sync --dev                           # Install all dependencies (creates .venv)
uv add package_name                     # Add runtime dependency
uv add --dev package_name               # Add development dependency
uv remove package_name                  # Remove dependency
uv lock                                 # Update lock file
uv tree                                 # Show dependency tree

# Running commands in project environment
uv run pytest                          # Run tests
uv run black src tests scripts         # Format code
uv run flake8 src tests scripts        # Lint code
uv run mypy src tests scripts          # Type checking
uv run bandit -r src scripts           # Security scanning

# Python version management
uv python list                         # List available Python versions
uv python install 3.11                 # Install Python 3.11
uv python pin 3.11                     # Pin project to Python 3.11

# Tool execution (no installation needed)
uvx black .                            # Run black in temporary environment
uvx ruff check .                       # Run ruff linter
uvx mypy src/                          # Run mypy type checker

# Building and publishing
uv build                               # Build wheel and sdist
uv publish                             # Publish to PyPI (with credentials)

# Exporting for compatibility
uv export --format requirements-txt --output-file requirements.txt
uv export --dev --format requirements-txt --output-file requirements-dev.txt
```

**UV Performance Benefits:**

```bash
# UV Demo Script - Interactive exploration
python scripts/uv_demo.py              # Interactive menu
python scripts/uv_demo.py --info       # Show UV information
python scripts/uv_demo.py --benchmark  # Performance comparison

# UV utilities
python scripts/uv_demo.py list         # List UV environments
python scripts/uv_demo.py sync         # Sync dependencies
python scripts/uv_demo.py test         # Run tests with UV
python scripts/uv_demo.py lint         # Run linting with UV
python scripts/uv_demo.py build        # Build with UV
python scripts/uv_demo.py clean        # Clean UV cache
```

**UV vs Traditional Tools:**

| Traditional | UV Equivalent | Speed Improvement |
|-------------|---------------|-------------------|
| `pip install package` | `uv add package` | 10-100x faster |
| `pip install -r requirements.txt` | `uv sync` | 10-50x faster |
| `python -m venv .venv` | `uv venv` | 10x faster |
| `pip freeze > requirements.txt` | `uv export` | Instant |
| `pyenv install 3.11` | `uv python install 3.11` | 5x faster |
| `pipx run tool` | `uvx tool` | 5-10x faster |

**UV Configuration:**

The project includes UV configuration in `pyproject.toml`:

```toml
[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=6.0",
    # ... other dev tools
]

[tool.uv.workspace]
members = ["."]
```

**UV Lock File:**

The `uv.lock` file ensures reproducible builds:
- **Cross-platform**: Works on Linux, macOS, Windows
- **Version-specific**: Locks exact versions of all dependencies
- **Transitive dependencies**: Includes all indirect dependencies
- **Integrity checks**: SHA256 hashes for security
- **Kept in version control**: Ensures consistent environments

**UV Cache Management:**

```bash
uv cache dir                           # Show cache directory
uv cache clean                         # Clean all cache
uv cache prune                         # Remove unused cache entries
```

**UV Development Workflow:**

1. **Setup**: `uv sync --dev` (one-time, creates .venv)
2. **Development**: `uv run command` (runs in project environment)
3. **Testing**: `uv run pytest` (fast test execution)
4. **Quality**: `uv run black .` (instant formatting)
5. **Build**: `uv build` (fast wheel creation)

UV makes Python development faster, more reliable, and more enjoyable!
- **Cleanup utilities**: Comprehensive artifact cleaning across all cache directories

### Pre-commit Hooks

FTT uses pre-commit hooks to automatically enforce code quality standards:

```bash
# Install pre-commit hooks (run once after cloning)
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black
pre-commit run pytest-check
```

**Configured hooks:**

- **File hygiene**: trailing whitespace, end-of-file fixing, YAML/JSON/TOML validation
- **Python quality**: isort (import sorting), black (formatting), flake8 (linting), mypy (type checking)
- **Security**: bandit (vulnerability scanning)
- **Testing**: pytest (unit tests), pytest-cov (coverage testing)

**Hook stages:**

- **pre-commit**: Runs on every commit (includes all quality checks + pytest)
- **pre-push**: Runs on push (includes pytest with coverage requirements)

The hooks automatically format code, catch issues early, and ensure consistent quality across all commits.

### CI/CD Pipeline

FTT includes a comprehensive GitHub Actions CI/CD pipeline:

```yaml
# Triggers: push to main/develop, pull requests, manual dispatch
- Test Matrix: Python 3.8-3.13 on Ubuntu
- Code Quality: formatting, linting, type checking, security
- Pre-commit: all hooks validation
- Build: package building and validation
```

**CI Jobs:**

- **test**: Runs pytest with coverage on all supported Python versions
- **quality**: Code quality checks (isort, black, flake8, mypy, bandit)
- **pre-commit**: Validates all pre-commit hooks
- **build**: Builds and validates the package

**Troubleshooting "pytest not found" errors:**

If you encounter `Executable 'pytest' not found` errors:

```bash
# Install dev dependencies (includes pytest)
pip install -e ".[dev]"

# Or install pytest directly
pip install pytest pytest-cov

# Verify installation
which pytest
pytest --version

# For pre-commit hooks
pip install pre-commit
pre-commit install

# Use the pytest checker script for diagnosis
python scripts/check_pytest.py
```

**Pytest Checker Utility:**

Use the included `scripts/check_pytest.py` script to diagnose pytest installation issues:

```bash
python scripts/check_pytest.py
```

This script checks:
- Python environment and virtual environment status
- Pytest module importability and executable availability
- All development dependencies installation status
- Provides specific troubleshooting suggestions

The CI pipeline automatically installs all dependencies and runs tests with proper coverage reporting.

## License

MIT License - see LICENSE file for details.
