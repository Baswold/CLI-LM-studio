# Installation Guide

Welcome to CLI-LM-Studio! This guide will help you install and configure the tool.

## Prerequisites

Before installing CLI-LM-Studio, ensure you have:

- **Python 3.8 or higher** installed on your system
- **LM Studio** installed and running (download from [lmstudio.ai](https://lmstudio.ai))
- **pip** package manager (usually comes with Python)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Baswold/CLI-LM-studio.git
   cd CLI-LM-studio
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```

4. **Install development dependencies (optional):**
   ```bash
   pip install -e ".[dev]"
   ```

### Method 2: Install from PyPI (Coming Soon)

Once published to PyPI, you'll be able to install with:

```bash
pip install cli-lm-studio
```

## Initial Configuration

After installation, initialize the configuration:

```bash
lms init
```

This creates a configuration file at `~/.lm_studio/config.yaml` with default settings.

## Verify Installation

1. **Check version:**
   ```bash
   lms --version
   ```

2. **Ensure LM Studio is running:**
   - Open LM Studio
   - Start the local server (usually on port 1234)
   - Load a model

3. **Test connection:**
   ```bash
   lms models list
   ```

   You should see a list of available models.

## Configuration

### Configuration File Location

The configuration file is located at:
- **Linux/macOS:** `~/.lm_studio/config.yaml`
- **Windows:** `%USERPROFILE%\.lm_studio\config.yaml`

### Basic Configuration

Edit your config file to customize settings:

```yaml
# API Configuration
api_url: http://localhost:1234
api_timeout: 30

# Model Settings
default_model: your-model-name
temperature: 0.7
max_tokens: 2000

# History
history_enabled: true
history_path: ~/.lm_studio/history
```

### Environment Variables

You can also configure using environment variables:

```bash
export LM_STUDIO_API_URL=http://localhost:1234
export LM_STUDIO_DEFAULT_MODEL=llama-2-7b
export LM_STUDIO_TEMPERATURE=0.7
```

Environment variables take precedence over config file settings.

## Troubleshooting

### Common Issues

**Issue: "Could not connect to LM Studio"**
- Solution: Ensure LM Studio is running and the server is started
- Check that the API URL is correct (default: http://localhost:1234)

**Issue: "Model not found"**
- Solution: Load a model in LM Studio before using the CLI
- List available models with `lms models list`

**Issue: "Permission denied" when creating config**
- Solution: Ensure you have write permissions to your home directory
- Try running with appropriate permissions

**Issue: Command not found: lms**
- Solution: Ensure the package is installed: `pip install -e .`
- Check that your Python scripts directory is in PATH

### Getting Help

If you encounter issues:

1. Check the [documentation](./README.md)
2. Enable verbose logging: `lms --verbose chat "test"`
3. Report issues on [GitHub](https://github.com/Baswold/CLI-LM-studio/issues)

## Next Steps

- Read the [Usage Guide](./usage.md)
- Explore [Examples](./examples.md)
- Learn about [Advanced Features](./advanced.md)
