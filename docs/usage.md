# Usage Guide

This guide covers all the features and commands available in CLI-LM-Studio.

## Table of Contents

- [Basic Commands](#basic-commands)
- [Chat Commands](#chat-commands)
- [Model Management](#model-management)
- [History Management](#history-management)
- [Configuration](#configuration)

## Basic Commands

### Getting Help

Show general help:
```bash
lms --help
```

Show help for a specific command:
```bash
lms chat --help
lms models --help
```

### Version Information

```bash
lms --version
```

### Initialize Configuration

```bash
lms init
```

Creates a default configuration file if none exists.

## Chat Commands

### Single Message

Send a single message and get a response:

```bash
lms chat "What is Python?"
```

### Interactive Mode

Start an interactive chat session:

```bash
lms chat -i
# or
lms chat --interactive
```

In interactive mode, you can use these commands:
- `/exit` or `/quit` - Exit the chat
- `/clear` - Clear conversation history
- `/save` - Save conversation to file
- `/help` - Show help message

### Custom Model

Use a specific model (overrides config):

```bash
lms chat -m "llama-2-7b" "Tell me about AI"
```

### Custom Temperature

Adjust the temperature (0.0 = deterministic, 2.0 = very random):

```bash
lms chat -t 0.3 "Write a formal letter"
lms chat -t 1.5 "Write a creative story"
```

### Custom System Prompt

Override the system prompt:

```bash
lms chat -s "You are a Python expert" "How do I use decorators?"
```

### Disable Streaming

Get the complete response at once instead of streaming:

```bash
lms chat --no-stream "Explain quantum computing"
```

### Complex Example

Combine multiple options:

```bash
lms chat \
  -m "gpt-4" \
  -s "You are a helpful coding assistant" \
  -t 0.5 \
  --max-tokens 1000 \
  "Write a Python function to parse JSON"
```

## Model Management

### List All Models

```bash
lms models list
```

### List Models with Details

```bash
lms models list --detailed
# or
lms models list -d
```

### Get Model Information

```bash
lms models info llama-2-7b
```

### Set Default Model

```bash
lms models set-default llama-2-7b
```

This updates your configuration to use this model by default.

## History Management

### Show Recent History

Show last 10 conversations:
```bash
lms history show
```

Show last 20 conversations:
```bash
lms history show -n 20
```

Show all history:
```bash
lms history show --all
```

### Search History

Search for conversations containing a keyword:

```bash
lms history search "python"
```

### Clear History

Clear all conversation history:

```bash
lms history clear
```

Skip confirmation:
```bash
lms history clear -y
```

## Configuration

### Show Current Configuration

```bash
lms config-show
```

Displays all current settings in a formatted table.

### Edit Configuration

Edit the configuration file directly:

```bash
# Linux/macOS
nano ~/.lm_studio/config.yaml

# Windows
notepad %USERPROFILE%\.lm_studio\config.yaml
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `api_url` | LM Studio API URL | `http://localhost:1234` |
| `api_timeout` | Request timeout (seconds) | `30` |
| `default_model` | Default model name | `local-model` |
| `system_prompt` | Default system prompt | `You are a helpful AI assistant.` |
| `temperature` | Sampling temperature | `0.7` |
| `max_tokens` | Maximum tokens to generate | `2000` |
| `top_p` | Nucleus sampling parameter | `0.9` |
| `history_enabled` | Enable history tracking | `true` |
| `history_path` | History storage path | `~/.lm_studio/history` |
| `log_level` | Logging level | `INFO` |

## Tips and Best Practices

### 1. Choose the Right Temperature

- **0.0-0.3**: Factual, deterministic responses (good for code, facts)
- **0.4-0.7**: Balanced creativity and accuracy (general use)
- **0.8-1.2**: More creative, varied responses (creative writing)
- **1.3-2.0**: Very creative, potentially random (experimental)

### 2. Use System Prompts

System prompts help set the behavior:

```bash
# Code assistance
lms chat -s "You are an expert programmer" "..."

# Writing help
lms chat -s "You are a professional editor" "..."

# Teaching
lms chat -s "You are a patient teacher explaining to a beginner" "..."
```

### 3. Manage Context Length

If you hit token limits:
- Use shorter prompts
- Increase `max_tokens` in config
- Use `/clear` in interactive mode to reset context

### 4. Save Important Conversations

In interactive mode, use `/save` to save conversations for later reference.

### 5. Search History Efficiently

Use specific keywords when searching:

```bash
# Good
lms history search "fibonacci algorithm"

# Less effective
lms history search "code"
```

## Advanced Usage

### Piping Input

You can pipe text into the chat command:

```bash
echo "Explain this concept simply" | lms chat
```

```bash
cat document.txt | lms chat "Summarize this:"
```

### Using with Scripts

CLI-LM-Studio can be used in shell scripts:

```bash
#!/bin/bash

# Get code review
response=$(lms chat "Review this code: $(cat mycode.py)")
echo "$response" > review.txt
```

### Batch Processing

Process multiple prompts:

```bash
while read -r prompt; do
  lms chat "$prompt" >> results.txt
done < prompts.txt
```

## Troubleshooting

### Slow Responses

- Use a smaller model
- Reduce `max_tokens`
- Check your system resources
- Ensure no other heavy processes are running

### Empty or Weird Responses

- Check temperature setting (try 0.7)
- Verify model is loaded in LM Studio
- Try a different model
- Check prompt clarity

### Connection Issues

- Verify LM Studio is running
- Check API URL in config
- Ensure firewall isn't blocking
- Try restarting LM Studio

## Next Steps

- Explore [Examples](./examples.md)
- Learn about [Advanced Features](./advanced.md)
- Check the [API Reference](./api.md)
