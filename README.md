# CLI-LM-Studio

> A powerful, feature-rich command-line interface for LM Studio

[![Tests](https://github.com/Baswold/CLI-LM-studio/workflows/Tests/badge.svg)](https://github.com/Baswold/CLI-LM-studio/actions)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

CLI-LM-Studio is a beautiful, intuitive command-line interface for interacting with [LM Studio](https://lmstudio.ai), allowing you to chat with local language models directly from your terminal.

## ✨ Features

- 🚀 **Fast & Lightweight** - Minimal overhead, maximum performance
- 💬 **Interactive Chat** - Full-featured chat sessions with streaming responses
- 🎨 **Beautiful Output** - Rich formatting with syntax highlighting and markdown rendering
- 📊 **Model Management** - List, inspect, and switch between models effortlessly
- 📝 **History Tracking** - Save, search, and review conversation history
- ⚙️ **Highly Configurable** - Extensive configuration options with sensible defaults
- 🔌 **Scriptable** - Perfect for automation and integration with other tools
- 🧪 **Well Tested** - Comprehensive test suite for reliability
- 📚 **Excellent Documentation** - Detailed guides and examples

## 🎥 Quick Demo

```bash
# Start an interactive chat
$ lms chat -i

# Ask a quick question
$ lms chat "What is Python?"

# List available models
$ lms models list

# Search conversation history
$ lms history search "python"
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- [LM Studio](https://lmstudio.ai) installed and running
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Baswold/CLI-LM-studio.git
cd CLI-LM-studio

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Initialize configuration
lms init
```

### Install from PyPI (Coming Soon)

```bash
pip install cli-lm-studio
lms init
```

## 🚀 Quick Start

### 1. Start LM Studio

1. Open LM Studio
2. Start the local server (usually port 1234)
3. Load a model

### 2. Initialize Configuration

```bash
lms init
```

This creates `~/.lm_studio/config.yaml` with default settings.

### 3. Verify Setup

```bash
# Check available models
lms models list

# Test a simple query
lms chat "Hello, how are you?"
```

### 4. Start Chatting!

```bash
# Interactive mode
lms chat -i

# Single question
lms chat "Explain quantum computing"

# Use a specific model
lms chat -m "llama-2-70b" "Write a poem about coding"
```

## 📖 Documentation

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Usage Guide](docs/usage.md) - Complete command reference
- [Examples](docs/examples.md) - Real-world usage examples
- [API Reference](docs/api.md) - API documentation

## 💡 Usage Examples

### Interactive Chat

Start a conversational session:

```bash
lms chat -i
```

Commands in interactive mode:
- `/exit` or `/quit` - Exit the chat
- `/clear` - Clear conversation history
- `/save` - Save conversation to file
- `/help` - Show help message

### Single-Shot Queries

```bash
# Simple question
lms chat "What is machine learning?"

# Code generation
lms chat "Write a Python function to calculate fibonacci numbers"

# With custom settings
lms chat -m "codellama-13b" -t 0.3 "Review this code: $(cat script.py)"
```

### Model Management

```bash
# List all models
lms models list

# Show detailed model info
lms models list --detailed

# Get info about a specific model
lms models info llama-2-7b

# Set default model
lms models set-default llama-2-13b
```

### History Management

```bash
# Show recent conversations
lms history show

# Show last 20 entries
lms history show -n 20

# Search history
lms history search "python tutorial"

# Clear all history
lms history clear
```

### Configuration

```bash
# Show current configuration
lms config-show

# Configuration is stored at ~/.lm_studio/config.yaml
# Edit it directly or use environment variables
```

## ⚙️ Configuration

### Configuration File

Located at `~/.lm_studio/config.yaml`:

```yaml
# API Configuration
api_url: http://localhost:1234
api_timeout: 30

# Model Settings
default_model: llama-2-7b
temperature: 0.7
max_tokens: 2000
system_prompt: You are a helpful AI assistant.

# History
history_enabled: true
history_path: ~/.lm_studio/history
history_max_entries: 1000

# Display
color_enabled: true
markdown_enabled: true
```

### Environment Variables

Override config with environment variables:

```bash
export LM_STUDIO_API_URL=http://localhost:1234
export LM_STUDIO_DEFAULT_MODEL=llama-2-13b
export LM_STUDIO_TEMPERATURE=0.5
```

## 🎨 Advanced Features

### Temperature Control

Control response creativity:

```bash
# Very factual (low temperature)
lms chat -t 0.1 "What is the capital of France?"

# Creative (high temperature)
lms chat -t 1.2 "Write a creative story"
```

### System Prompts

Set the assistant's behavior:

```bash
lms chat -s "You are an expert Python programmer" "Explain decorators"
```

### Streaming vs Non-Streaming

```bash
# Streaming (default) - see response as it's generated
lms chat "Write a long essay"

# Non-streaming - wait for complete response
lms chat --no-stream "Write a long essay"
```

### Piping and Scripting

```bash
# Pipe input
echo "Summarize this text" | lms chat

# Use in scripts
response=$(lms chat "What is 2+2?")
echo "Response: $response"

# Process files
lms chat "Review this code: $(cat script.py)" > review.txt
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Baswold/CLI-LM-studio.git
cd CLI-LM-studio

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=lm_studio_cli --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LM Studio](https://lmstudio.ai) - For the amazing local LLM platform
- [Rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
- [Click](https://click.palletsprojects.com/) - For the excellent CLI framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For robust data validation

## 📮 Support

- 📫 [Report Issues](https://github.com/Baswold/CLI-LM-studio/issues)
- 💬 [Discussions](https://github.com/Baswold/CLI-LM-studio/discussions)
- 📖 [Documentation](docs/)

## 🗺️ Roadmap

- [ ] Plugin system for extensibility
- [ ] Conversation templates
- [ ] Multi-model conversations
- [ ] Export conversations to various formats
- [ ] Shell completion scripts
- [ ] Docker support
- [ ] Web UI companion

## 📊 Project Status

This project is actively maintained and under development. We welcome contributions and feedback!

---

**Made with ❤️ for the LM Studio community**

*Star ⭐ this repository if you find it helpful!*
