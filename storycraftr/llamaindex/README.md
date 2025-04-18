# LlamaIndex Integration for StoryCraftr

This module integrates LlamaIndex with StoryCraftr to provide powerful semantic search capabilities for your book content.

## Features

- **Semantic Search**: Search your book content with natural language queries
- **Indexing**: Automatically index your book content for fast retrieval
- **Context Retrieval**: Get relevant context from your book to enhance AI responses
- **CLI Commands**: Command-line interface for LlamaIndex operations
- **Chat Integration**: Use LlamaIndex directly from the chat interface

## System Architecture

The LlamaIndex integration is designed to work seamlessly with StoryCraftr's existing architecture:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  StoryCraftr    │     │    LlamaIndex   │     │  OpenAI API     │
│  CLI Interface  │─────▶   Integration   │─────▶  (or similar)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Book Content   │     │  Vector Store   │     │    Embeddings   │
│   Directories   │─────▶      Index      │─────▶      API        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Integration Points

1. **CLI Commands**: Commands added to the existing StoryCraftr CLI
2. **Chat Integration**: New commands for the chat interface
3. **Agent Enhancement**: Context enrichment for StoryCraftr's agent
4. **Storage**: Vector indices stored in the book's directory structure

## CLI Usage

### Building an Index

Build a semantic index of your book content:

```bash
storycraftr llamaindex build-index --book-path /path/to/your/book
```

You can also specify which directories to index:

```bash
storycraftr llamaindex build-index --book-path /path/to/your/book -d worldbuilding -d chapters
```

### Querying the Index

Query your book content with natural language:

```bash
storycraftr llamaindex query --book-path /path/to/your/book "What are the main characters in my story?"
```

For raw results without agent processing:

```bash
storycraftr llamaindex query --book-path /path/to/your/book --raw "Tell me about the protagonist's backstory"
```

### Getting Raw Context

Retrieve raw context from your book:

```bash
storycraftr llamaindex context --book-path /path/to/your/book "What is the magic system in my world?"
```

## Chat Integration

LlamaIndex can also be used directly from the StoryCraftr chat interface:

1. Start a chat session:
   ```bash
   storycraftr chat --book-path /path/to/your/book
   ```

2. Use LlamaIndex commands with the `!llamaindex` prefix:
   - `!llamaindex build` - Build a semantic index
   - `!llamaindex query "What are the main themes in my story?"` - Query your book content
   - `!llamaindex context "Tell me about the protagonist"` - Get raw context
   - `!llamaindex help` - Show LlamaIndex help

## Development Setup

To set up the environment for development:

1. Create a Python 3.11 virtual environment:
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   mkdir -p ~/.storycraftr/
   echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt
   ```

See [DEVELOPMENT.md](../../DEVELOPMENT.md) for more detailed setup instructions.

## How It Works

LlamaIndex integration works by:

1. **Document Loading**: Loads your book content (markdown, text, and JSON files) from key directories
2. **Chunking**: Splits documents into manageable chunks (default: 512 tokens with 20 token overlap)
3. **Embedding**: Converts text chunks to vector embeddings using OpenAI's embedding models
4. **Indexing**: Creates a vector store index for semantic search
5. **Retrieval**: Finds relevant content based on query similarity
6. **Response Generation**: Uses retrieved context to generate accurate responses through StoryCraftr's agent

The indexed content is stored in the `indexes/llamaindex` directory within your book project.

## Data Flow

When you query the LlamaIndex integration, the following process occurs:

1. User input → CLI or Chat interface
2. Query → Vector Index retrieval
3. Relevant documents → Agent context enrichment
4. Enhanced context → LLM processing
5. Processed response → User display

## Environmental Configuration

The LlamaIndex integration is configurable through environment variables:

```
# In .env file or environment variables
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o  # or another compatible model
OPENAI_API_URL=https://api.openai.com/v1  # or another compatible API

LLAMA_INDEX_CHUNK_SIZE=512  # Customize chunking
LLAMA_INDEX_CHUNK_OVERLAP=20
```

## Benefits

- **Enhanced Context**: The AI assistant can reference your book content accurately
- **Better Answers**: Get more relevant and accurate responses based on your specific book
- **Time Saving**: Quickly find information across your entire book project
- **Consistency**: Maintain consistency in your story by easily referencing previous content

## Technical Implementation

This integration uses:

- **llama-index-core**: For the core vector indexing and retrieval
- **llama-index-llms-openai**: For OpenAI LLM integration
- **llama-index-embeddings-openai**: For embedding generation
- **llama-index-readers-file**: For file loading and processing
- **llama-index-readers-web**: For potential web content integration 