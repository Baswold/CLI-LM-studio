# Examples

This document provides practical examples of using CLI-LM-Studio for various tasks.

## Quick Start Examples

### Example 1: Simple Question

```bash
lms chat "What is machine learning?"
```

### Example 2: Code Generation

```bash
lms chat "Write a Python function to calculate fibonacci numbers"
```

### Example 3: Interactive Conversation

```bash
lms chat -i
# Then type your messages interactively
```

## Real-World Use Cases

### 1. Code Review

```bash
# Review a Python file
lms chat "Review this code for bugs and improvements: $(cat script.py)"

# Get specific feedback
lms chat -s "You are a senior Python developer" \
  "Review this code: $(cat app.py)"
```

### 2. Documentation Writing

```bash
# Generate docstrings
lms chat "Write a docstring for this function: $(cat function.py)"

# Create README sections
lms chat "Write a clear README introduction for a project that does: ..."
```

### 3. Learning and Education

```bash
# Learn a concept
lms chat -s "You are a patient teacher" \
  "Explain recursion with simple examples"

# Step-by-step tutorial
lms chat "Teach me how to use Python decorators with examples"
```

### 4. Creative Writing

```bash
# Story generation
lms chat -t 1.2 "Write a short sci-fi story about AI"

# Brainstorming
lms chat -t 1.0 "Give me 10 creative blog post ideas about technology"
```

### 5. Data Analysis Help

```bash
# Get analysis suggestions
lms chat "I have a CSV with sales data. Suggest Python code to analyze it"

# Explain results
lms chat "Explain what this pandas code does: $(cat analysis.py)"
```

### 6. Translation and Rewriting

```bash
# Simplify text
lms chat "Rewrite this in simple terms: $(cat technical_doc.txt)"

# Professional tone
lms chat "Rewrite this email professionally: I want my money back ASAP"
```

## Advanced Examples

### 1. Multi-Step Workflow

```bash
#!/bin/bash

# Generate code
echo "Creating initial code..."
lms chat "Write a Python class for a simple TODO app" > todo.py

# Get review
echo "Reviewing code..."
lms chat "Review this code: $(cat todo.py)" > review.txt

# Improve based on review
echo "Improving code..."
lms chat "Improve this code based on review:
CODE: $(cat todo.py)
REVIEW: $(cat review.txt)" > todo_improved.py
```

### 2. Batch Processing

Process multiple files:

```bash
#!/bin/bash

for file in *.py; do
  echo "Analyzing $file..."
  lms chat "Analyze this Python code: $(cat $file)" > "${file}.analysis.txt"
done
```

### 3. Template-Based Generation

```bash
#!/bin/bash

template="Write a Python function named {NAME} that {DESCRIPTION}"

# Generate multiple functions
echo "$template" | \
  sed 's/{NAME}/add_numbers/g; s/{DESCRIPTION}/adds two numbers/g' | \
  lms chat

echo "$template" | \
  sed 's/{NAME}/calculate_average/g; s/{DESCRIPTION}/calculates average of a list/g' | \
  lms chat
```

### 4. Interactive Knowledge Base

Create a script for domain-specific queries:

```bash
#!/bin/bash

# knowledge_assistant.sh
SYSTEM_PROMPT="You are an expert in Python programming and data science."

while true; do
  read -p "Question: " question
  [ -z "$question" ] && break

  lms chat -s "$SYSTEM_PROMPT" "$question"
done
```

### 5. Code Refactoring

```bash
# Refactor for readability
lms chat -s "You are a code refactoring expert" \
  "Refactor this for better readability: $(cat messy_code.py)"

# Convert between styles
lms chat "Convert this imperative code to functional style: $(cat code.py)"
```

## Model-Specific Examples

### Using Different Models for Different Tasks

```bash
# Use a larger model for complex tasks
lms chat -m "llama-2-70b" "Explain quantum computing in detail"

# Use a smaller model for simple tasks
lms chat -m "llama-2-7b" "What is 2+2?"

# Use a code-specific model
lms chat -m "codellama-13b" "Write a sorting algorithm"
```

## Temperature Examples

Demonstrating different temperature settings:

```bash
# Very factual (low temperature)
lms chat -t 0.1 "What is the capital of France?"

# Balanced
lms chat -t 0.7 "Write a short poem about coding"

# Very creative (high temperature)
lms chat -t 1.5 "Write a bizarre short story"
```

## System Prompt Examples

### 1. Code Expert

```bash
lms chat -s "You are an expert programmer who writes clean, efficient code" \
  "Write a binary search implementation"
```

### 2. Teacher

```bash
lms chat -s "You are a patient teacher who explains concepts simply" \
  "What is async/await in JavaScript?"
```

### 3. Critic

```bash
lms chat -s "You are a constructive code reviewer" \
  "Review this code: $(cat app.py)"
```

### 4. Creative Writer

```bash
lms chat -s "You are a creative writer who uses vivid descriptions" \
  "Describe a futuristic city"
```

### 5. Business Analyst

```bash
lms chat -s "You are a business analyst who provides actionable insights" \
  "Analyze this sales data: $(cat sales.csv)"
```

## Integration Examples

### 1. Git Commit Messages

```bash
#!/bin/bash

# Generate commit message from diff
diff=$(git diff --staged)
message=$(lms chat "Write a concise git commit message for: $diff")
git commit -m "$message"
```

### 2. Automated Testing Ideas

```bash
# Generate test cases
lms chat "Generate pytest test cases for this function: $(cat function.py)" > test_function.py
```

### 3. API Documentation

```bash
# Document API endpoints
for endpoint in api/*.py; do
  lms chat "Document this API endpoint: $(cat $endpoint)" > "docs/$(basename $endpoint .py).md"
done
```

### 4. Log Analysis

```bash
# Analyze error logs
lms chat "Analyze these errors and suggest fixes: $(tail -100 app.log)"
```

### 5. Configuration Generation

```bash
# Generate config files
lms chat "Create a nginx config for a Python Flask app on port 5000" > nginx.conf
```

## History Usage Examples

### 1. Find Past Solutions

```bash
# Search for previous coding solutions
lms history search "fibonacci"
lms history search "sorting algorithm"
```

### 2. Review Learning Progress

```bash
# See all past conversations
lms history show --all

# See recent learning topics
lms history show -n 50
```

### 3. Extract Useful Code

```bash
# Search and extract
lms history search "Python class" > past_classes.txt
```

## Productivity Tips

### 1. Create Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
alias ask="lms chat"
alias code-review="lms chat -s 'You are a code reviewer'"
alias explain="lms chat -s 'You are a teacher'"
```

Usage:
```bash
ask "What is Docker?"
code-review "$(cat app.py)"
explain "What is a closure?"
```

### 2. Create Reusable Functions

```bash
# Add to your shell config
ask_about_code() {
  lms chat "Explain this code: $(cat $1)"
}

improve_code() {
  lms chat "Improve this code: $(cat $1)"
}

# Usage
ask_about_code script.py
improve_code messy.py
```

### 3. Quick Scripts

Create a scripts directory:

```bash
~/bin/summarize
#!/bin/bash
lms chat "Summarize this: $(cat $1)"

~/bin/translate
#!/bin/bash
lms chat "Translate to $1: $2"
```

## Best Practices

### 1. Be Specific

```bash
# ❌ Vague
lms chat "Write code"

# ✅ Specific
lms chat "Write a Python function that reads a CSV file and returns a pandas DataFrame"
```

### 2. Provide Context

```bash
# ❌ No context
lms chat "Fix this bug"

# ✅ With context
lms chat "This Python function should return even numbers but returns odd. Fix it: $(cat function.py)"
```

### 3. Use Appropriate Temperature

```bash
# For facts and code: low temperature
lms chat -t 0.3 "Write a unit test"

# For creative tasks: higher temperature
lms chat -t 1.0 "Write a creative product description"
```

### 4. Iterate and Refine

```bash
# Start simple
lms chat "Write a TODO app"

# Then refine
lms chat "Add database support to this TODO app: $(cat todo.py)"

# Keep improving
lms chat "Add user authentication to: $(cat todo.py)"
```

## Troubleshooting Examples

### Model Not Responding

```bash
# Check if model is loaded
lms models list

# Test with simple prompt
lms chat "Hi"

# Try different model
lms chat -m "different-model" "Test"
```

### Getting Better Responses

```bash
# If response is too short
lms chat --max-tokens 4000 "Explain in detail..."

# If response is too creative
lms chat -t 0.3 "Give me the facts about..."

# If response is too boring
lms chat -t 1.2 "Write something creative about..."
```

## Next Steps

- Read the [Advanced Features](./advanced.md) guide
- Check out the [API Reference](./api.md)
- Join the community discussions
