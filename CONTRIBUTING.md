# Contributing to FTT (File Type Tester)

Thank you for your interest in contributing to FTT! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Making Changes](#making-changes)
- [Submitting Contributions](#submitting-contributions)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic familiarity with command-line tools

### Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ftt.git
   cd ftt
   ```
3. **Set up development environment** (see [Development Setup](#development-setup))
4. **Create a feature branch** for your changes
5. **Make your changes** following our [Code Standards](#code-standards)
6. **Test your changes** thoroughly
7. **Submit a pull request**

## Development Setup

### 1. Create Virtual Environment

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
# Install the package in development mode with all dependencies
pip install -e ".[dev]"

# Or install dependencies manually
pip install -e .
pip install pytest pytest-cov black flake8 mypy isort bandit pre-commit
```

### 3. Set Up Pre-commit Hooks

```bash
# Install pre-commit hooks (REQUIRED)
pre-commit install

# Test the setup
pre-commit run --all-files
```

### 4. Verify Installation

```bash
# Test that ftt works
ftt --version
ftt examples/hello.py

# Run tests
pytest
```

## Code Standards

We maintain high code quality standards. All contributions must follow these guidelines:

### Code Formatting

- **Black** for code formatting (88 character line limit)
- **isort** for import sorting
- Run before committing: `black src/ tests/ && isort src/ tests/`

### Code Quality

- **Flake8** for linting
- **MyPy** for type checking
- **Bandit** for security scanning
- All functions must have type annotations
- Comprehensive docstrings required

### Pre-commit Hooks

Our pre-commit configuration automatically enforces:

- Trailing whitespace removal
- End-of-file fixing
- YAML/JSON/TOML validation
- Python code formatting and linting
- Type checking
- Security scanning

**Important**: Pre-commit hooks will run automatically on commit and may modify your files. Review changes before pushing.

### Code Style Guidelines

```python
# Good: Type annotations and docstrings
def test_file(filepath: Union[str, Path]) -> TestResult:
    """
    Test a file to determine its type.

    Args:
        filepath: Path to the file to test

    Returns:
        TestResult containing classification or error
    """
    # Implementation here
    pass

# Good: Error handling
try:
    result = some_operation()
    return TestResult.success_result(result)
except SpecificError as e:
    return TestResult.failure_result(f"Operation failed: {e}")

# Good: Clear variable names and logic
is_executable = stat.S_ISREG(mode) and mode & stat.S_IXUSR
if is_executable:
    return create_executable_result()
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/ftt

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_detect_python_script_with_shebang()`
- Test both success and failure cases
- Include edge cases and error conditions
- Use temporary files for file-based tests

Example test structure:

```python
def test_new_feature(self) -> None:
    """Test description of what this test validates."""
    # Arrange
    test_data = create_test_data()

    # Act
    result = tester.test_file(test_data)

    # Assert
    assert result.success
    assert result.file_type is not None
    assert "expected" in result.file_type.description
```

### Testing Guidelines

- **Unit tests** for individual functions and methods
- **Integration tests** for complete workflows
- **Edge case testing** for error conditions
- **Cross-platform considerations** when applicable
- **Performance testing** for large files or many files

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-rust-language-detection`
- `fix/handle-symlink-errors`
- `docs/update-installation-guide`
- `refactor/improve-magic-number-detection`

### Commit Messages

Follow conventional commit format:

```
type(scope): brief description

Longer description if needed explaining what and why.

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

Examples:
- `feat(magic): add support for WebP image detection`
- `fix(filesystem): handle broken symlinks gracefully`
- `docs(readme): add installation troubleshooting section`
- `test(core): add tests for empty file detection`

### Adding New File Format Support

When adding support for new file formats:

1. **Magic signatures**: Add to `src/ftt/tests/magic.py`
2. **Language patterns**: Add to `src/ftt/tests/language.py`
3. **Test cases**: Create test files and unit tests
4. **Documentation**: Update README and CHANGELOG

Example magic signature addition:

```python
# In MAGIC_SIGNATURES list
(0, b'\x89PNG\r\n\x1a\n', 'PNG image data', FileTypeCategory.DATA, 'image/png'),
```

### Adding New Programming Languages

1. Add patterns to `LANGUAGE_PATTERNS` in `language.py`
2. Include multiple detection patterns for reliability
3. Add test cases with real code samples
4. Update documentation

## Submitting Contributions

### Pull Request Process

1. **Ensure your fork is up to date**:
   ```bash
   git remote add upstream https://github.com/original-owner/ftt.git
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following all guidelines above

4. **Test thoroughly**:
   ```bash
   # Run all checks
   pre-commit run --all-files
   pytest
   ftt examples/*  # Manual testing
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create pull request** on GitHub with:
   - Clear title and description
   - Reference any related issues
   - Include testing instructions
   - Add screenshots for UI changes

### Pull Request Requirements

- [ ] All pre-commit hooks pass
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] No merge conflicts
- [ ] Clear commit messages

## Issue Reporting

### Bug Reports

Include:

- **Environment details** (OS, Python version)
- **FTT version** (`ftt --version`)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Sample files** that trigger the issue (if safe to share)
- **Error messages** and stack traces

### Feature Requests

Include:

- **Use case description** - what problem does this solve?
- **Proposed solution** - how should it work?
- **Alternative solutions** considered
- **Examples** of the desired behavior
- **Impact assessment** - who benefits from this feature?

### Security Issues

For security vulnerabilities:

- **Do not** create public issues
- Email maintainers directly
- Include detailed reproduction steps
- Allow time for patch development before disclosure

## Development Workflow

### Architecture Overview

FTT uses a three-tier testing system:

1. **Filesystem tests** (`src/ftt/tests/filesystem.py`)
   - File properties and permissions
   - Special file types (directories, symlinks, devices)

2. **Magic tests** (`src/ftt/tests/magic.py`)
   - File signature detection
   - Binary content analysis

3. **Language tests** (`src/ftt/tests/language.py`)
   - Programming language detection
   - Text format identification

### Key Design Principles

- **Early termination**: First successful test determines result
- **Memory efficiency**: Read only necessary file portions
- **Error resilience**: Graceful handling of edge cases
- **Extensibility**: Easy to add new formats and languages
- **Unix compatibility**: Maintain expected output format

### Performance Considerations

- Limit file reading to first 1-4KB for analysis
- Use compiled regex patterns for efficiency
- Avoid loading entire files into memory
- Consider impact on batch processing

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes to API or behavior
- **MINOR** (x.Y.0): New features, backward compatible
- **PATCH** (x.y.Z): Bug fixes, backward compatible

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Run full test suite
4. Create release tag
5. Update documentation if needed

---

## Questions?

- **Documentation**: Check README.md and docstrings
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Code**: Read the source code - it's well-documented!

Thank you for contributing to FTT! 🎉
