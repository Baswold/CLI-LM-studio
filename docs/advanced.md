# Advanced Features

This guide covers advanced usage patterns and features of CLI-LM-Studio.

## Table of Contents

- [Configuration Management](#configuration-management)
- [Scripting and Automation](#scripting-and-automation)
- [Custom Workflows](#custom-workflows)
- [Performance Optimization](#performance-optimization)
- [Advanced Model Settings](#advanced-model-settings)
- [Integration Patterns](#integration-patterns)

## Configuration Management

### Multiple Configurations

You can maintain different configurations for different purposes:

```bash
# Work configuration
lms --config ~/.lm_studio/work.yaml chat "..."

# Personal configuration
lms --config ~/.lm_studio/personal.yaml chat "..."

# Experimental configuration
lms --config ~/.lm_studio/experimental.yaml chat "..."
```

### Environment-Specific Settings

```bash
# Production
export LM_STUDIO_CONFIG=/etc/lm_studio/production.yaml
lms chat "..."

# Development
export LM_STUDIO_CONFIG=~/.lm_studio/dev.yaml
lms chat "..."

# Testing
export LM_STUDIO_CONFIG=/tmp/test.yaml
lms chat "..."
```

### Dynamic Configuration

Override settings programmatically:

```bash
# Use different model for code review
LM_STUDIO_DEFAULT_MODEL=codellama-34b \
LM_STUDIO_TEMPERATURE=0.3 \
lms chat "Review this code: $(cat script.py)"

# Use creative settings for writing
LM_STUDIO_TEMPERATURE=1.2 \
LM_STUDIO_MAX_TOKENS=4000 \
lms chat "Write a creative story about..."
```

## Scripting and Automation

### Batch Processing

Process multiple files:

```bash
#!/bin/bash
# analyze_codebase.sh

for file in src/**/*.py; do
    echo "Analyzing $file..."
    lms chat "Analyze this Python code: $(cat $file)" > "analysis/${file}.txt"
done
```

### Automated Code Review

```bash
#!/bin/bash
# code_review.sh

# Get git diff
diff=$(git diff main...HEAD)

# Get AI review
review=$(lms chat -s "You are a code reviewer" \
    "Review these changes: $diff")

# Post as PR comment (requires gh CLI)
echo "$review" | gh pr comment --body-file -
```

### Continuous Documentation

```bash
#!/bin/bash
# update_docs.sh

for file in src/**/*.py; do
    # Generate docstring
    docs=$(lms chat "Write comprehensive docstrings for: $(cat $file)")

    # TODO: Apply the docstrings (requires parsing)
    echo "$docs" > "docs/generated/${file}.md"
done
```

### Scheduled Tasks

Use with cron for scheduled tasks:

```bash
# Crontab entry
0 9 * * * /usr/local/bin/lms chat "Summarize today's news" > ~/daily_summary.txt
```

## Custom Workflows

### Multi-Step Refinement

```bash
#!/bin/bash
# refine_code.sh

code_file="$1"

# Step 1: Generate initial code
echo "Step 1: Generating initial code..."
lms chat "Write a Python class for $code_file" > v1.py

# Step 2: Get review
echo "Step 2: Getting review..."
review=$(lms chat "Review this code: $(cat v1.py)")

# Step 3: Improve based on review
echo "Step 3: Improving code..."
lms chat "Improve this code based on review:
CODE: $(cat v1.py)
REVIEW: $review" > v2.py

# Step 4: Add tests
echo "Step 4: Adding tests..."
lms chat "Write pytest tests for: $(cat v2.py)" > test_v2.py

echo "Complete! Check v2.py and test_v2.py"
```

### Interactive Decision Trees

```bash
#!/bin/bash
# decision_helper.sh

question="$1"

# Get initial answer
answer=$(lms chat "$question")
echo "Answer: $answer"

# Ask follow-up
read -p "Follow-up question: " followup
lms chat "Context: $question
Previous answer: $answer
Follow-up: $followup"
```

### Context-Aware Assistance

```bash
#!/bin/bash
# smart_assistant.sh

# Gather context
git_status=$(git status --short)
current_branch=$(git branch --show-current)
recent_commits=$(git log -3 --oneline)
open_files=$(lsof -c python | grep -v ".so$" | awk '{print $NF}' | sort -u)

# Build context
context="Project context:
- Branch: $current_branch
- Git status: $git_status
- Recent commits: $recent_commits
- Open files: $open_files

Question: $1"

# Get answer with context
lms chat "$context"
```

## Performance Optimization

### Optimizing Response Time

```yaml
# fast.yaml - Optimized for speed
api_timeout: 15
default_model: llama-2-7b  # Smaller model
max_tokens: 500  # Shorter responses
temperature: 0.3  # More deterministic
```

### Optimizing Quality

```yaml
# quality.yaml - Optimized for quality
api_timeout: 120
default_model: llama-2-70b  # Larger model
max_tokens: 4000  # Longer responses
temperature: 0.7  # Balanced creativity
```

### Caching Strategies

```bash
#!/bin/bash
# cached_query.sh

query="$1"
cache_file="cache/$(echo "$query" | md5sum | cut -d' ' -f1).txt"

if [ -f "$cache_file" ]; then
    # Use cached response
    cat "$cache_file"
else
    # Query and cache
    lms chat "$query" | tee "$cache_file"
fi
```

## Advanced Model Settings

### Temperature Profiles

```bash
# Factual (0.0-0.3)
alias lms-factual='lms chat -t 0.2'

# Balanced (0.4-0.7)
alias lms-balanced='lms chat -t 0.6'

# Creative (0.8-1.2)
alias lms-creative='lms chat -t 1.0'

# Experimental (1.3-2.0)
alias lms-experimental='lms chat -t 1.5'
```

### System Prompt Templates

```bash
# ~/.lm_studio/prompts/

# code_expert.txt
You are an expert software engineer with deep knowledge of best practices,
design patterns, and clean code principles.

# creative_writer.txt
You are a creative writer with a vivid imagination and excellent storytelling
abilities.

# teacher.txt
You are a patient teacher who explains complex concepts in simple terms with
clear examples.
```

Usage:

```bash
lms chat -s "$(cat ~/.lm_studio/prompts/code_expert.txt)" "..."
```

### Model-Specific Optimizations

```bash
# For code models
lms_code() {
    lms chat -m "codellama-34b" -t 0.3 -s "You are a code generator" "$@"
}

# For creative tasks
lms_creative() {
    lms chat -m "llama-2-70b" -t 1.2 --max-tokens 4000 "$@"
}

# For quick answers
lms_quick() {
    lms chat -m "llama-2-7b" -t 0.5 --max-tokens 500 "$@"
}
```

## Integration Patterns

### Git Integration

```bash
# ~/.gitconfig
[alias]
    ai-commit = "!f() { \
        diff=$(git diff --staged); \
        msg=$(lms chat \"Write a concise git commit message for: $diff\"); \
        git commit -m \"$msg\"; \
    }; f"

    ai-review = "!f() { \
        lms chat \"Review these changes: $(git diff)\"; \
    }; f"
```

### Editor Integration

For Vim:

```vim
" ~/.vimrc
" Send selection to LMS
vnoremap <leader>ai :!lms chat<CR>

" Explain selected code
vnoremap <leader>ex :!lms chat "Explain this code:"<CR>
```

For VS Code (via terminal):

```bash
# Create a task in .vscode/tasks.json
{
    "label": "Ask AI",
    "type": "shell",
    "command": "lms chat '${input:question}'"
}
```

### CI/CD Integration

GitHub Actions:

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install LMS CLI
        run: pip install cli-lm-studio

      - name: Run AI Review
        run: |
          diff=$(git diff origin/main...HEAD)
          lms chat "Review this code: $diff" > review.txt

      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### API Integration

```python
# Use as a library
from lm_studio_cli import LMStudioClient, Config

config = Config.load()
client = LMStudioClient(config)

# Make requests
response = client.chat_completion(
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response["choices"][0]["message"]["content"])
```

### Webhook Integration

```python
# webhook_handler.py
from flask import Flask, request
from lm_studio_cli import LMStudioClient, Config

app = Flask(__name__)
client = LMStudioClient(Config.load())

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    question = data.get('question')

    response = client.chat_completion(
        messages=[{"role": "user", "content": question}]
    )

    return {'answer': response["choices"][0]["message"]["content"]}
```

## Best Practices

### 1. Error Handling

```bash
#!/bin/bash

query="$1"

# Try with timeout
if ! timeout 30 lms chat "$query" 2>/dev/null; then
    echo "Query timed out, trying with shorter response..."
    timeout 15 lms chat --max-tokens 500 "$query"
fi
```

### 2. Resource Management

```bash
#!/bin/bash

# Limit concurrent requests
max_jobs=3

for file in *.py; do
    while [ $(jobs -r | wc -l) -ge $max_jobs ]; do
        sleep 1
    done

    lms chat "Analyze: $(cat $file)" > "$file.analysis" &
done

wait  # Wait for all background jobs
```

### 3. Logging and Monitoring

```bash
#!/bin/bash

# Log all queries
LOG_FILE=~/.lm_studio/query_log.txt

log_query() {
    echo "[$(date)] $1" >> "$LOG_FILE"
}

query="$1"
log_query "Query: $query"

response=$(lms chat "$query")
log_query "Response length: ${#response}"

echo "$response"
```

## Troubleshooting

### Performance Issues

```bash
# Check model performance
time lms chat "Hello"

# Use smaller model
lms chat -m "llama-2-7b" "..."

# Reduce max tokens
lms chat --max-tokens 500 "..."
```

### Connection Issues

```bash
# Test connection
if lms models list >/dev/null 2>&1; then
    echo "Connected"
else
    echo "Not connected - is LM Studio running?"
fi
```

## Future Enhancements

- TODO: Plugin system for custom commands
- TODO: Conversation templates
- TODO: Multi-model ensemble responses
- TODO: Automatic model selection based on task
- TODO: Response quality scoring
- TODO: Conversation branching and exploration

