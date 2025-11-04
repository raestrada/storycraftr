# LangChain Refactor Plan

## Purpose & Scope
This refactor removes all direct usage of the legacy OpenAI SDK and re-centers StoryCraftr’s automation on LangChain primitives. Every large-language-model call must pass through a LangChain interface with first-class support for OpenAI, OpenRouter, and Ollama providers. We will not maintain backward compatibility with the existing assistants or vector-store workflows and will trim any dead code that relied on the OpenAI Assistants API.

## Current Pain Points
- `storycraftr/agent/agents.py` orchestrates threads, vector stores, and assistant runs via `openai` and `OpenAI`, making extensions impossible without OpenAI parity.
- Configuration objects (`BookConfig`, CLI flags, init templates) assume OpenAI-only concepts (`openai_url`, `openai_model`, API key discovery).
- Utilities (`cleanup_vector_stores`, markdown helpers) are coupled to OpenAI vector stores.
- Tests and fixtures are built around OpenAI responses, hampering provider diversification.

## Target Architecture
- **LLM service layer**: Introduce `storycraftr/llm/` with a `LangChainClient` factory that reads CLI options and environment variables to build one of:
  - `ChatOpenAI` (`langchain-openai`) for OpenAI with `OPENAI_API_KEY`.
  - `ChatOpenRouter` (`langchain_community.chat_models`) with `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL`.
  - `ChatOllama` (`langchain_community.chat_models`) with optional `OLLAMA_BASE_URL`.
- **Configuration changes**: Replace `openai_url`/`openai_model` fields with `llm_provider`, `llm_model`, `llm_endpoint`, `temperature`, and `request_timeout`. Update `BookConfig` and persisted JSON templates accordingly.
- **Prompt handling**: Migrate prompt assembly to LangChain `Runnable` chains so formatting, hashing, and multi-turn chat operate through structured `Messages`.
- **Retrieval**: Replace OpenAI vector stores with an embedded ChromaDB instance stored under each project (for example, `<book>/vector_store/`). Populate it via LangChain’s `Chroma` integration using `BAAI/bge-large-en-v1.5` as the default embedding model, which produces results closest to OpenAI’s text-embedding-3 series while running locally. Offer a fallback like `sentence-transformers/all-MiniLM-L6-v2` for low-resource setups. Define a shared loader for Markdown knowledge bases and centralize chunking parameters.
- **Streaming & multi-part answers**: Implement LangChain callbacks to stream tokens and manage multi-part responses without the bespoke `END_OF_RESPONSE` sentinel workarounds.

## Workstreams & Sequencing
1. **Foundation**
   - Remove `openai` dependency from `pyproject.toml`.
   - Add `langchain`, `langchain-core`, `langchain-community`, `langchain-openai`, `chromadb`, and embedding-model backends (`sentence-transformers`, `huggingface-hub`, `torch` or `onnxruntime` depending on CPU/GPU targets).
   - Preconfigure Poetry optional groups for heavy embedding dependencies (e.g., `[tool.poetry.group.embeddings]`) to keep installs manageable.
   - Create `storycraftr/llm/__init__.py` and `storycraftr/llm/factory.py` with provider-specific constructors and environment resolution rules.
2. **Configuration & CLI**
   - Update CLI options: `--llm-provider`, `--llm-model`, `--llm-endpoint`, `--llm-api-key-env`, defaulting from environment variables (`STORYCRAFTR_LLM_PROVIDER`, etc.).
   - Add embedding flags: `--embed-model`, `--embed-device`, `--embed-cache-dir`; read defaults from env vars (`STORYCRAFTR_EMBED_MODEL`, `STORYCRAFTR_EMBED_DEVICE`, `STORYCRAFTR_EMBED_CACHE`).
   - Rewrite `load_openai_api_key` into a generic credentials loader supporting `{OPENAI,OPENROUTER,OLLAMA}_API_KEY` plus optional config files under `.storycraftr/`.
   - Modify scaffolding commands (`init_structure_*`) to generate new config fields and drop OpenAI-only keys.
   - Adjust `BookConfig` and `load_book_config` to reflect new schema, including migration fallback when encountering legacy fields.
3. **Agent Pipeline**
   - Replace `initialize_openai_client` and all direct assistant calls with LangChain chains:
     - Build a conversation chain combining system behavior, user prompts, and configurable memory.
     - Use LangChain retrievers for knowledge ingestion instead of vector store APIs.
   - Refactor file upload & cleanup utilities to operate on the embedded Chroma store (persist under `vector_store/` with metadata per document) and expose rebuild commands.
   - Implement a reusable embedding service that boots the configured HuggingFace model, handles device placement (CPU/GPU/MPS), and exposes batched encode helpers.
   - Ensure CLI commands (`chat`, `outline`, etc.) request completions exclusively through the shared LangChain service.
4. **Testing**
   - Update unit tests to mock LangChain interfaces (use `langchain_core` `FakeListLLM` or patch the factory).
   - Add integration tests validating provider selection (environment overrides, CLI flags) and retrieval pipeline behavior.
5. **Documentation & Samples**
   - Refresh `README.md`, `CONTRIBUTING.md`, and `AGENTS.md` references to configuration keys and commands.
   - Provide example `.env` snippets showcasing OpenAI, OpenRouter, Ollama, and local embedding configuration (default `BAAI/bge-large-en-v1.5`, optional fallback).
   - Document migration notes in `docs/` summarizing breaking changes.
6. **Cleanup**
   - Delete obsolete modules (`cleanup_vector_stores`, assistants helpers) if functionality is superseded.
   - Sweep for any `openai` imports or legacy constants via `rg`.

## Provider Support Matrix
| Provider   | Required Env Vars                 | CLI Overrides                        | LangChain Class             |
|------------|-----------------------------------|--------------------------------------|-----------------------------|
| OpenAI     | `OPENAI_API_KEY`                  | `--llm-provider=openai`              | `ChatOpenAI`                |
| OpenRouter | `OPENROUTER_API_KEY`, optional `OPENROUTER_BASE_URL` | `--llm-provider=openrouter` | `ChatOpenRouter` (base URL set to `https://openrouter.ai/api/v1`) |
| Ollama     | *(none by default)*, optional `OLLAMA_BASE_URL` | `--llm-provider=ollama`             | `ChatOllama`                |
| Embeddings | `STORYCRAFTR_EMBED_MODEL` (defaults to `BAAI/bge-large-en-v1.5`), optional `STORYCRAFTR_EMBED_DEVICE` | `--embed-model`, `--embed-device` | `HuggingFaceEmbeddings` (defaulting to `bge-large-en-v1.5`) feeding Chroma |

## Risks & Mitigations
- **Parity gaps vs Assistants API**: Re-implement multi-turn orchestration with LangChain memory and ensure prompts encode behavior.txt instructions. Prototype with a fake LLM to validate flows before depending on remote providers.
- **Vector-store migration**: Chroma runs locally; manage index size with configurable chunking and offer maintenance commands (`storycraftr vector rebuild`) to regenerate embeddings when prompts change.
- **Embedding model footprint**: `bge-large-en-v1.5` requires PyTorch and ~1.3 GB of RAM; document hardware expectations and keep the fallback model flag well surfaced.
- **Provider divergence**: Each provider has different model names and token limits. Centralize mapping logic and expose validation errors early in CLI argument parsing.

## Acceptance Criteria
- No Python module imports `openai` or `OpenAI`.
- `storycraftr` CLI selects providers via configuration or flags and fails gracefully when required env vars are missing.
- Embedded Chroma vector store initializes automatically and can be rebuilt via CLI; embeddings leverage the configured local model.
- Integration tests simulate at least one run per provider using LangChain test doubles.
- Documentation clearly describes the new configuration schema and breaking changes, including embedding model guidance.
- Project builds and tests succeed with updated dependencies.
