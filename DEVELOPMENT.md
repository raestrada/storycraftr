# StoryCraftr Development Guide

This guide explains how to set up a development environment for StoryCraftr using Python 3.11 and venv.

## Requirements

- Python 3.11+
- Git

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/raestrada/storycraftr.git
cd storycraftr
```

### 2. Create a Python 3.11 Virtual Environment

```bash
# Create a new virtual environment
python3.11 -m venv .venv

# Activate the virtual environment
# On macOS/Linux
source .venv/bin/activate
# On Windows
# .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install LlamaIndex specific dependencies
pip install llama-index llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file llama-index-readers-web tiktoken
```

### 4. Set Up Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

Alternatively, you can configure the API key in the StoryCraftr standard location:

```bash
mkdir -p ~/.storycraftr/
echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt
```

### 5. Verify Installation

Run the test script to verify the installation:

```bash
python test_llamaindex.py
```

## Development Workflow

### Running StoryCraftr in Development Mode

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run StoryCraftr commands
python -m storycraftr --help
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_specific.py
```

## LlamaIndex Integration

The LlamaIndex integration provides semantic search capabilities for StoryCraftr. 

### Key Components

- `storycraftr/llamaindex/core.py`: Core functionality for document indexing and retrieval
- `storycraftr/llamaindex/agent_integration.py`: Integration with the StoryCraftr agent system
- `storycraftr/llamaindex/cli.py`: CLI commands for LlamaIndex features
- `storycraftr/llamaindex/chat_integration.py`: Integration with the chat interface

### Example Usage

```bash
# Build a semantic index
python -m storycraftr llamaindex build-index

# Query the index
python -m storycraftr llamaindex query "What are the main characters in my story?"
```

## Troubleshooting

### ImportError Issues

If you encounter import errors, check that you're using the correct Python version and your virtual environment is activated.

```bash
# Check Python version
python --version

# Install missing dependencies
pip install -r requirements.txt
```

### API Key Issues

If you encounter API key errors, make sure your OpenAI API key is correctly set in either:

1. The `.env` file
2. The `~/.storycraftr/openai_api_key.txt` file
3. Or as an environment variable: `export OPENAI_API_KEY=your_key_here` 