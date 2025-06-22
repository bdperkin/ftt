#!/bin/bash
# UV Workflow Script for FTT Project
# Demonstrates a typical development workflow using UV

set -e  # Exit on any error

echo "🚀 FTT UV Development Workflow"
echo "================================="

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ UV version: $(uv --version)"
echo

# Step 1: Sync dependencies
echo "📦 Step 1: Syncing dependencies..."
uv sync --dev
echo "✅ Dependencies synced"
echo

# Step 2: Run tests
echo "🧪 Step 2: Running tests..."
uv run pytest --cov=src/ftt --cov-report=term-missing --cov-fail-under=50
echo "✅ Tests passed"
echo

# Step 3: Code quality checks
echo "🔍 Step 3: Running quality checks..."

echo "  - Checking code formatting..."
uv run black --check src tests scripts

echo "  - Checking import sorting..."
uv run isort --check-only src tests scripts

echo "  - Running linter..."
uv run flake8 src tests scripts

echo "  - Type checking..."
uv run mypy src tests scripts

echo "  - Security scanning..."
uv run bandit -r -s B101 src scripts

echo "✅ All quality checks passed"
echo

# Step 4: Build package
echo "📦 Step 4: Building package..."
uv build
echo "✅ Package built successfully"
echo

# Step 5: Show project info
echo "📊 Step 5: Project information"
echo "  - Dependency tree:"
uv tree --depth 1
echo
echo "  - Lock file status:"
if [ -f "uv.lock" ]; then
    echo "    ✅ uv.lock exists ($(stat -c%s uv.lock) bytes)"
else
    echo "    ❌ uv.lock missing"
fi
echo

echo "🎉 UV workflow completed successfully!"
echo
echo "Next steps:"
echo "  - Make changes to your code"
echo "  - Run 'uv run pytest' to test"
echo "  - Run 'uv run black .' to format"
echo "  - Run 'uv build' to build package"
echo "  - Run 'uv publish' to publish (when ready)"
