# Changelog

All notable changes to the FTT (File Type Tester) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### UV Integration
- **UV package manager support** for ultra-fast Python development
- **UV configuration** in pyproject.toml with dev-dependencies and workspace setup
- **Universal lock file** (uv.lock) for reproducible cross-platform builds
- **UV demo script** (scripts/uv_demo.py) with interactive CLI for UV operations
- **UV workflow script** (scripts/uv_workflow.sh) demonstrating typical development workflow
- **UV CI/CD integration** with GitHub Actions for multi-Python testing
- **Comprehensive UV documentation** in README.md covering installation, usage, and workflows

#### UV Features
- **Lightning-fast dependency installation** (10-100x faster than pip)
- **Python version management** with automatic installation
- **Tool execution** with uvx for ephemeral environments
- **Project management** with modern pyproject.toml workflow
- **Build and publish** capabilities with uv build/publish
- **Cache management** for efficient storage and cleanup
- **Export functionality** for requirements.txt compatibility

#### UV Development Workflow
- **One-command setup** with `uv sync --dev`
- **Fast test execution** with `uv run pytest`
- **Quality checks** with `uv run` for black, flake8, mypy, bandit
- **Package building** with `uv build`
- **Dependency management** with `uv add/remove`
- **Performance benchmarking** tools for pip vs uv comparison

#### Tox-UV Integration
- **Tox-UV plugin integration** combining tox's multi-environment testing with UV's speed
- **UV-enhanced test environments** for all Python versions (uv-py38 through uv-py313)
- **UV-enhanced quality environments** (uv-lint, uv-type, uv-coverage, uv-security, uv-all)
- **UV-enhanced utility environments** (uv-dev, uv-quick, uv-verbose, uv-benchmark)
- **Performance benchmarking** environment to compare UV vs standard tox speed
- **Comprehensive tox-uv demo script** (scripts/tox_uv_demo.py) with interactive CLI
- **CI/CD integration** with GitHub Actions for tox-uv testing
- **Parallel execution support** for UV-enhanced environments
- **Backward compatibility** maintained with standard tox environments

#### Tox-UV Features
- **10-100x faster** virtual environment creation compared to standard tox
- **Lightning-fast dependency installation** using UV's parallel downloads
- **Full compatibility** with existing tox configurations and workflows
- **Reduced CI/CD build times** for faster development feedback
- **Better developer experience** with faster test iterations
- **Intelligent caching** mechanisms for dependency management
- **Cross-platform support** on Linux, macOS, and Windows
- **Seamless integration** with existing development workflows

## [1.0.0] - 2025-06-21

### Added

#### Core Features
- **Three-tier file classification system** implementing filesystem, magic, and language tests
- **Filesystem tests** for file properties, permissions, and special file types
  - Directory detection
  - Symbolic link handling with target resolution
  - Special file detection (character/block devices, pipes, sockets)
  - Executable bit detection
  - Empty file handling
- **Magic tests** for file signature and content analysis
  - Support for 50+ file format signatures
  - Executable format detection (ELF, Mach-O, MS-DOS)
  - Archive format detection (ZIP, tar, gzip, bzip2, 7z, RAR, XZ)
  - Image format detection (PNG, JPEG, GIF, BMP, WebP)
  - Audio/video format detection (MP3, Ogg, MP4)
  - Document format detection (PDF, Microsoft Office)
  - Binary content heuristics
  - Script detection via shebang processing
- **Language tests** for programming language and text format detection
  - Support for 10+ programming languages (Python, JavaScript, Java, C/C++, Rust, Go, Ruby, PHP, Perl)
  - Text format detection (JSON, XML, HTML, YAML, TOML, CSV, etc.)
  - Configuration file detection
  - Plain text analysis with printability heuristics

#### File Type Categories
- **"text"** - Files safe to read on ASCII terminals
- **"executable"** - Compiled programs understandable to UNIX kernels
- **"data"** - Binary or non-printable data (including well-known formats)

#### Command-Line Interface
- **Multiple file processing** with single command
- **Help and version information** (`--help`, `--version`)
- **MIME type output** option (`--mime-type`)
- **Standard input support** for file path lists
- **Comprehensive error handling** with meaningful messages
- **Exit codes** indicating success/failure status

#### Project Infrastructure
- **Modern Python packaging** with pyproject.toml
- **MIT License** for open source usage
- **Comprehensive documentation** with README, examples, and inline comments
- **Example files** for testing and demonstration
- **Unit test suite** with pytest framework
- **Type annotations** throughout codebase
- **Clean project structure** with proper module organization

### Development & Code Quality

#### Pre-commit Configuration
- **Automated code quality checks** on every commit
- **Code formatting** with black (88 character line length)
- **Import sorting** with isort (black-compatible profile)
- **Linting** with flake8 (Python code analysis)
- **Type checking** with mypy (static type analysis)
- **Security scanning** with bandit
- **File validation** (YAML, JSON, TOML syntax checking)
- **General file hygiene** (trailing whitespace, end-of-file fixing)

#### Code Quality Improvements
- **Full type annotation coverage** for all functions and methods
- **Python 3.8+ compatibility** using Union types instead of newer syntax
- **Removed unused imports** and variables
- **Fixed line length violations** (88 character limit)
- **Proper error handling** for filesystem operations
- **Consistent code formatting** via black
- **Sorted imports** for better organization
- **Security compliance** verified by bandit

#### Testing & Validation
- **Unit tests** for all major functionality
- **Example file validation** ensuring tool works correctly
- **Cross-platform compatibility** considerations
- **Error case coverage** (nonexistent files, permissions, etc.)

### Technical Details

#### Architecture
- **Modular design** with separate test modules
- **Plugin-like test system** allowing easy extension
- **Clean separation** between CLI, core logic, and test implementations
- **Comprehensive type system** with custom data classes
- **Robust error handling** with structured error types

#### Performance
- **Efficient file reading** (limited to first 1-4KB for analysis)
- **Early termination** on first successful test
- **Memory-conscious** binary content detection
- **Fast pattern matching** with compiled regular expressions

#### Compatibility
- **Python 3.8+** support
- **Cross-platform** filesystem handling
- **Unicode-aware** text processing
- **Robust binary detection** preventing crashes on binary data

## [0.0.0] - Project Initialization

### Added
- Initial project setup
- Git repository initialization
- Basic project structure

---

## Release Notes

### Version 1.0.0
This is the initial stable release of FTT (File Type Tester), providing a comprehensive, modern Python implementation of file type detection. The tool successfully identifies hundreds of file formats across three categories (text, executable, data) using a robust three-tier testing system.

Key highlights:
- **Production-ready** file type detection
- **Extensive format support** (50+ magic signatures, 10+ programming languages)
- **Modern Python practices** (type hints, proper packaging, comprehensive testing)
- **Developer-friendly** (pre-commit hooks, code quality tools, clear documentation)
- **Unix-compatible** output format maintaining compatibility expectations

The tool is suitable for both command-line usage and integration into larger Python applications.
