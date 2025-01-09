# Developer Setup Guide

This guide provides detailed instructions for setting up OnHax for development.

## Prerequisites

1. Python 3.8 or higher
2. Git
3. pip or uv package manager

## Initial Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/onhax.git
   cd onhax
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix
   venv\Scripts\activate     # Windows
   ```

3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

## Development Tools

### Code Quality

We use several tools to maintain code quality:

1. **Black**: Code formatting

   ```bash
   black .
   ```

2. **isort**: Import sorting

   ```bash
   isort .
   ```

3. **mypy**: Type checking

   ```bash
   mypy .
   ```

4. **flake8**: Linting

   ```bash
   flake8 .
   ```

### Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=onhax

# Run specific test file
pytest tests/test_app.py
```

## Project Structure

- `onhax/`: Main package code
  - `app.py`: Core application logic
  - `client.py`: DeepSeek API client
  - `config.py`: Configuration management
  - `installer/`: Installation utilities
- `tests/`: Test suite
- `docs/`: Documentation
- `examples/`: Usage examples

## Making Changes

1. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and ensure tests pass:

   ```bash
   pytest
   ```

3. Commit changes:

   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. Push changes and create pull request:

   ```bash
   git push origin feature/your-feature-name
   ```

## Documentation

Update documentation when making changes:

1. Add docstrings to new code
2. Update API reference if needed
3. Add examples for new features
4. Update relevant guides
