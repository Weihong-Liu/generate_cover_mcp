#!/bin/bash
# Quick setup script for generate-cover-mcp

set -e

echo "🚀 Setting up generate-cover-mcp..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the generate-cover-mcp directory"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install package in development mode
echo "⚙️ Installing package..."
pip install -e ".[dev]"

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install chromium

# Run tests
echo "🧪 Running tests..."
pytest

echo "✅ Setup complete!"
echo ""
echo "To use the MCP server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Set HTML template path: export COVER_HTML_PATH=/path/to/CoverMaster2.html"
echo "3. Start server: generate-cover-mcp"
echo ""
echo "Or run the example: python examples/usage_example.py"