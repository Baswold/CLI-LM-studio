# Makefile for CLI-LM-Studio
# Provides convenient commands for development and testing

.PHONY: help install dev-install test lint format type-check clean docs build publish

# Default target
.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "CLI-LM-Studio Development Commands"
	@echo "==================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in production mode
	pip install .

dev-install:  ## Install package in development mode with dev dependencies
	pip install -e ".[dev]"

test:  ## Run test suite
	pytest -v

test-cov:  ## Run tests with coverage report
	pytest --cov=lm_studio_cli --cov-report=html --cov-report=term-missing

test-watch:  ## Run tests in watch mode
	pytest-watch

lint:  ## Run linting checks
	ruff check src/

lint-fix:  ## Run linting with auto-fix
	ruff check --fix src/

format:  ## Format code with black
	black src/ tests/

format-check:  ## Check code formatting
	black --check src/ tests/

type-check:  ## Run type checking with mypy
	mypy src/

check-all: lint format-check type-check test  ## Run all checks (lint, format, type, test)

clean:  ## Clean up build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:  ## Generate documentation (TODO: Add sphinx or mkdocs)
	@echo "Documentation generation not yet implemented"
	@echo "See docs/ directory for existing documentation"

build:  ## Build distribution packages
	python -m build

publish-test:  ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI (use with caution!)
	python -m twine upload dist/*

init-config:  ## Initialize default configuration
	lms init

run-chat:  ## Run interactive chat (requires LM Studio)
	lms chat -i

run-models:  ## List available models
	lms models list

setup-hooks:  ## Setup git hooks (if pre-commit is used)
	pre-commit install

update-deps:  ## Update dependencies
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"

# TODO: Add more targets
# - benchmark: Run performance benchmarks
# - security: Run security checks
# - docker-build: Build Docker image
# - docker-run: Run in Docker container
