# Contributing to CLI-LM-Studio

Thank you for your interest in contributing to CLI-LM-Studio! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please:

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- LM Studio (for testing)
- Familiarity with command-line tools

### Areas for Contribution

We welcome contributions in many areas:

- **Bug fixes** - Help us squash bugs
- **New features** - Add functionality
- **Documentation** - Improve guides and examples
- **Tests** - Increase code coverage
- **Examples** - Add usage examples
- **Performance** - Optimize code
- **UI/UX** - Improve user experience

## Development Setup

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/CLI-LM-studio.git
cd CLI-LM-studio
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies:**

```bash
pip install -e ".[dev]"
```

4. **Verify the setup:**

```bash
pytest
```

## Making Changes

### 1. Create a Branch

Create a descriptive branch name:

```bash
git checkout -b feature/add-export-feature
git checkout -b fix/streaming-bug
git checkout -b docs/improve-readme
```

### 2. Make Your Changes

- Write clear, readable code
- Add comments for complex logic
- Update documentation as needed
- Add tests for new functionality

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lm_studio_cli

# Run specific test file
pytest tests/test_client.py

# Run linting
ruff check src/

# Format code
black src/
```

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- **Line length:** 100 characters (enforced by Black)
- **Imports:** Organized by isort
- **Type hints:** Required for all functions
- **Docstrings:** Required for all public functions/classes

### Example

```python
def chat_completion(
    self,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Create a chat completion.

    Args:
        messages: List of message dictionaries
        model: Model to use (optional)
        temperature: Sampling temperature (optional)

    Returns:
        Response dictionary

    Raises:
        APIError: If the API request fails
    """
    # Implementation here
    pass
```

### Code Quality Tools

We use several tools to maintain code quality:

- **Black** - Code formatting
- **Ruff** - Fast linting
- **mypy** - Type checking
- **pytest** - Testing

Run all checks:

```bash
# Format
black src/

# Lint
ruff check src/

# Type check
mypy src/

# Test
pytest
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

Example test:

```python
def test_get_models_success(self, mock_request, client):
    """Test successfully getting models."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [{"id": "model-1"}]
    }
    mock_request.return_value = mock_response

    models = client.get_models()
    assert len(models) == 1
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_client.py

# Specific test
pytest tests/test_client.py::TestClientInitialization::test_client_creation

# With coverage
pytest --cov=lm_studio_cli --cov-report=html
```

## Submitting Changes

### 1. Commit Your Changes

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add streaming support for chat completions"
git commit -m "Fix timeout error handling in client"
git commit -m "Update installation documentation"

# Not so good
git commit -m "fix bug"
git commit -m "updates"
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

- Go to the original repository
- Click "New Pull Request"
- Select your fork and branch
- Fill in the PR template:
  - Description of changes
  - Related issues
  - Testing performed
  - Screenshots (if applicable)

### 4. Code Review

- Respond to feedback promptly
- Make requested changes
- Keep the conversation focused and professional

### Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def function_name(arg1: str, arg2: int) -> bool:
    """
    Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When something goes wrong
    """
```

### Updating Documentation

When adding features, update:

- Code docstrings
- README.md (if user-facing)
- docs/ files (usage, examples, etc.)
- CHANGELOG.md

## Feature Requests

Have an idea for a new feature?

1. Check existing issues to avoid duplicates
2. Open a new issue with:
   - Clear description
   - Use case
   - Proposed implementation (if any)
   - Examples

## Bug Reports

Found a bug?

1. Check if it's already reported
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Python version, etc.)
   - Error messages/logs

## Questions?

- Open a Discussion on GitHub
- Check existing documentation
- Look at example code

## Recognition

Contributors will be:

- Listed in the project's contributors
- Mentioned in release notes (for significant contributions)
- Appreciated forever! 🎉

Thank you for contributing to CLI-LM-Studio!
