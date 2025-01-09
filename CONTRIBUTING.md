# Contributing to Dify Installer

We love your input! We want to make contributing to the Dify Installer as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

1. Fork the repo and create your branch from `main`.
1. If you've added code that should be tested, add tests.
1. If you've changed APIs, update the documentation.
1. Ensure the test suite passes.
1. Make sure your code lints.
1. Issue that pull request!

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dify-installer.git
cd dify-installer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install development dependencies:
```bash
make install-dev
```

4. Run tests:
```bash
make test
```

## Testing

We use `pytest` for testing. To run tests:

```bash
pytest tests/
```

## Code Style

We use `black` for code formatting and `flake8` for linting. Please ensure your code follows these standards.

## Pull Request Process

1. Update the README.md with details of changes to the interface.
2. Update the tests as needed.
3. The PR will be merged once you have the sign-off of one other developer.

## Issue Process

1. Go to the GitHub repository
2. Click the "Issues" tab
3. Click the green "New Issue" button
4. Choose the appropriate issue template
5. Fill in the template with all relevant information

Thank you for contributing!