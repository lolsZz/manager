# Makefile for Dify Installer

.PHONY: install install-dev test clean build publish

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

run-web:
	dify-web-install

run-cli:
	dify-install install

verify:
	dify-install verify

help:
	@echo "Available targets:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install the package with development dependencies"
	@echo "  test        Run tests"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build package distributions"
	@echo "  publish     Publish package to PyPI"
	@echo "  run-web     Start web installer"
	@echo "  run-cli     Run CLI installer"
	@echo "  verify      Verify installation"
	@echo "  help        Show this help message"