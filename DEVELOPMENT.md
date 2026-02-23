# Development Guide

## Setup Development Environment

1. Clone the repository:
```bash
git clone <your-repo-url>
cd generate-cover-mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=generate_cover_mcp

# Run specific test file
pytest tests/test_generator.py
```

## Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Lint code
flake8 src/ tests/
```

## Testing the MCP Server

1. Start the server in development mode:
```bash
python -m generate_cover_mcp.server
```

2. Test with MCP client or use the example script:
```bash
python examples/usage_example.py
```

## Building and Publishing

1. Build the package:
```bash
python -m build
```

2. Check the package:
```bash
twine check dist/*
```

3. Upload to PyPI (test first):
```bash
# Test PyPI
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Project Structure

```
generate_cover_mcp/
├── src/generate_cover_mcp/
│   ├── __init__.py
│   ├── generator.py      # Core cover generation logic
│   └── server.py         # MCP server implementation
├── tests/
│   ├── __init__.py
│   └── test_generator.py
├── examples/
│   ├── mcp_config.json
│   ├── sample_articles.json
│   └── usage_example.py
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
└── .gitignore
```

## Adding New Features

1. Add functionality to `generator.py`
2. Add corresponding MCP tools to `server.py`
3. Update the tool schemas in `server.py`
4. Add tests in `tests/`
5. Update documentation in `README.md`

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. Build and publish to PyPI