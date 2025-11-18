# CLI-LM-Studio Project Overview

## Introduction

CLI-LM-Studio is a comprehensive, production-ready command-line interface for interacting with LM Studio's local language models. Built with Python, it provides a rich set of features for chat, model management, and conversation history tracking.

## Project Structure

```
CLI-LM-studio/
├── src/
│   └── lm_studio_cli/          # Main package
│       ├── __init__.py          # Package initialization
│       ├── main.py              # CLI entry point (Click commands)
│       ├── client.py            # LM Studio API client
│       ├── config.py            # Configuration management
│       ├── chat.py              # Chat session handling
│       ├── models.py            # Model management
│       ├── history.py           # Conversation history
│       ├── utils.py             # Utility functions
│       └── exceptions.py        # Custom exceptions
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_client.py          # Client tests
│   └── test_config.py          # Config tests
├── docs/                        # Documentation
│   ├── installation.md         # Installation guide
│   ├── usage.md                # Usage guide
│   ├── examples.md             # Examples
│   ├── advanced.md             # Advanced features
│   └── PROJECT_OVERVIEW.md     # This file
├── examples/                    # Example files
│   └── config.example.yaml     # Example configuration
├── scripts/                     # Helper scripts
│   └── shell-completion.bash   # Bash completion
├── .github/
│   └── workflows/
│       └── tests.yml           # CI/CD workflow
├── pyproject.toml              # Project metadata & dependencies
├── setup.py                    # Setup script
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── TODO.md                     # Future enhancements
├── Makefile                    # Development commands
└── .gitignore                  # Git ignore rules
```

## Architecture

### Core Components

#### 1. CLI Interface (`main.py`)
- Built with Click framework
- Provides commands: chat, models, history, config-show, init
- Handles command-line argument parsing
- Orchestrates other components

#### 2. API Client (`client.py`)
- Manages communication with LM Studio server
- Implements retry logic and error handling
- Supports both streaming and non-streaming responses
- Provides health checks and model queries

#### 3. Configuration (`config.py`)
- Uses Pydantic for validation
- Supports YAML files and environment variables
- Provides sensible defaults
- Handles configuration persistence

#### 4. Chat Session (`chat.py`)
- Manages conversation state
- Handles interactive and single-shot modes
- Implements streaming display with Rich
- Supports conversation commands (/exit, /clear, /save)

#### 5. Model Management (`models.py`)
- Lists available models
- Displays model information
- Manages default model selection
- Provides model validation

#### 6. History (`history.py`)
- Stores conversations in JSON format
- Supports searching and filtering
- Provides conversation statistics
- Implements history cleanup

#### 7. Utilities (`utils.py`)
- Logging configuration
- Error handling helpers
- Text formatting functions
- File operations

### Data Flow

```
User Input → CLI Parser → Command Handler → API Client → LM Studio
                ↓                              ↓
           Config Manager                  History Manager
                ↓                              ↓
            YAML File                      JSON Storage
```

### Dependencies

**Core Dependencies:**
- `requests` - HTTP client for API communication
- `pyyaml` - Configuration file parsing
- `rich` - Beautiful terminal output
- `click` - CLI framework
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management

**Development Dependencies:**
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `ruff` - Fast linting
- `mypy` - Type checking

## Key Features

### 1. Chat System
- **Interactive Mode**: Full conversational sessions
- **Single-Shot Mode**: Quick queries
- **Streaming**: Real-time response display
- **Commands**: In-chat commands for control
- **Customization**: Temperature, tokens, system prompts

### 2. Configuration
- **Multiple Sources**: Files, environment variables
- **Validation**: Type-checked with Pydantic
- **Profiles**: Support for different configs
- **Defaults**: Sensible out-of-the-box settings

### 3. Model Management
- **Discovery**: List available models
- **Information**: Detailed model metadata
- **Selection**: Set and switch default models
- **Validation**: Verify model availability

### 4. History Tracking
- **Persistence**: JSON-based storage
- **Search**: Find past conversations
- **Statistics**: Usage analytics
- **Management**: Clear, view, export

### 5. Developer Experience
- **Type Hints**: Full type annotation
- **Documentation**: Comprehensive docstrings
- **Testing**: Extensive test coverage
- **Logging**: Detailed logging support

## Design Principles

### 1. Readability
- Clear naming conventions
- Comprehensive documentation
- Logical code organization
- Minimal complexity

### 2. Extensibility
- Modular architecture
- Plugin-ready structure
- Configuration-driven behavior
- Clear interfaces

### 3. Reliability
- Robust error handling
- Retry mechanisms
- Input validation
- Graceful degradation

### 4. Performance
- Efficient API usage
- Minimal dependencies
- Lazy loading
- Streaming responses

### 5. User Experience
- Beautiful terminal output
- Helpful error messages
- Intuitive commands
- Sensible defaults

## Development Workflow

### Setup
```bash
# Clone repository
git clone <repo-url>
cd CLI-LM-studio

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
pytest tests/test_client.py
```

### Code Quality
```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Run all checks
make check-all
```

### Building
```bash
# Build distribution
make build

# Clean artifacts
make clean
```

## Configuration

### File Locations
- **Config**: `~/.lm_studio/config.yaml`
- **History**: `~/.lm_studio/history/`
- **Logs**: Optional, configured per user

### Environment Variables
```bash
LM_STUDIO_API_URL       # API endpoint
LM_STUDIO_DEFAULT_MODEL # Default model
LM_STUDIO_TEMPERATURE   # Sampling temperature
LM_STUDIO_CONFIG        # Config file path
# ... and more
```

## API Integration

### LM Studio API
- Compatible with OpenAI-style API
- Endpoints: `/v1/models`, `/v1/chat/completions`
- Supports streaming via SSE
- Local-only (no cloud)

### Request Flow
1. User issues command
2. CLI validates input
3. Client formats request
4. Request sent to LM Studio
5. Response processed and displayed
6. History updated (if enabled)

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Test success and failure cases
- High coverage (target: 90%+)

### Integration Tests
- End-to-end workflows
- Real API interactions (optional)
- Configuration loading
- File operations

### Test Organization
```
tests/
├── test_client.py      # API client tests
├── test_config.py      # Configuration tests
├── test_chat.py        # Chat session tests
├── test_models.py      # Model management tests
├── test_history.py     # History tests
└── conftest.py         # Shared fixtures
```

## Future Roadmap

See [TODO.md](../TODO.md) for detailed future plans.

### Short Term (v0.2.0)
- Plugin system
- Shell completion
- Export functionality
- Conversation branching

### Medium Term (v0.3.0)
- Web UI
- Multi-model support
- Enhanced search
- Editor plugins

### Long Term (v1.0.0)
- Production hardening
- Performance optimization
- Full documentation
- Community features

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Start
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards
- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests
- Update documentation

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: docs/ directory
- **Examples**: examples/ directory

## Acknowledgments

Built with:
- Python 3.8+
- Click (CLI framework)
- Rich (terminal formatting)
- Pydantic (validation)
- Requests (HTTP client)

Inspired by:
- LM Studio's excellent local LLM platform
- Modern CLI design principles
- Open source community

---

**Last Updated**: 2024
**Version**: 0.1.0
**Status**: Active Development
