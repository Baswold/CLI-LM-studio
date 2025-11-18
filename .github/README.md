# GitHub Workflows

This directory would normally contain GitHub Actions workflow files.

## Note on tests.yml

A comprehensive GitHub Actions workflow file (`tests.yml`) was created but cannot be committed directly due to workflow permissions.

### Workflow Contents

The workflow includes:
- Multi-OS testing (Ubuntu, macOS, Windows)
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11, 3.12)
- Code quality checks (ruff, black, mypy)
- Test coverage reporting
- Codecov integration

### To Add This Workflow

Repository maintainers can add the workflow by:

1. Creating `.github/workflows/tests.yml` manually in the GitHub UI
2. Adding the workflow file through a PR with appropriate permissions
3. Or copying the content from the reference below

### Reference Workflow File

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Run tests with pytest
      run: |
        pytest --cov=lm_studio_cli --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Run ruff
      run: |
        ruff check src/

    - name: Run black
      run: |
        black --check src/

    - name: Run mypy
      run: |
        mypy src/
      continue-on-error: true
```

This workflow provides comprehensive CI/CD testing across multiple platforms and Python versions.
