# StoryCraftr Migration Action Plan

Do not commit this file. Do not mention it in .gitignore, etc.

Generally keep the code complexity low. Refactor common code into one place. Keep modules
to reasonable lengths (e.g. 500 lines) if possible.

## 1. Executive Summary

This document outlines the action plan for migrating StoryCraftr from its current dependency on OpenAI's Assistants API to a more flexible architecture using the Chat Completions API and a custom Retrieval-Augmented Generation (RAG) system.

**Goal:** Achieve provider independence, enabling compatibility with OpenAI-compatible endpoints like Mistral.ai, thereby addressing vendor lock-in and aligning with creative and legal requirements (e.g., EU AI Act).

**Key Findings:**
- **High Dependency:** The codebase, particularly `storycraftr/agent/agents.py`, is tightly coupled with the OpenAI Assistants API, including its proprietary file search and thread management.
- **No Unit Tests:** The repository currently lacks a test suite. This presents a significant risk of regressions during the refactoring process. Introducing tests for new and modified components will be a critical part of this migration.

## 2. Migration Plan

The migration is broken down into three phases to manage complexity and risk.

### Phase 1: Foundational RAG Implementation

**Goal:** Build the core components for a provider-agnostic RAG system without modifying the existing OpenAI integration. This allows for isolated development and testing.

IMPORTANT general policy for tests:
- they should provide as much coverage as possible, mock external services as needed.
- they can integrate with LLM API providers conditionally if well documented API access variables are set (document them in a top level file TESTS.md)
- use the time when you have access to API keys to capture mock content.
- avoid using adhoc tests, consider if the test suite could be improved by adding a test that tests what you want to test in an adhoc manner.
- provide pauses for the user to do reviews of your changes.
- new Python code should follow ReST documentation conventions for docstrings.

**Estimated Effort:** 3-5 days.

| Task ID | Description | Key Actions | Status |
|---|---|---|---|
| **1.1** | **Add Dependencies** | Modify `pyproject.toml` to include: `chromadb`, `sentence-transformers`, `pypdf`, and `unstructured`. Ensure CPU-only versions of `torch` and `onnxruntime` are used to avoid CUDA dependencies. | **Done** |
| **1.2** | **Create RAG Core Modules** | Create a new `storycraftr/rag/` directory with the following modules: <br> - `document_processor.py`: Functions to load and chunk Markdown files from the book path. <br> - `embeddings.py`: A class/module to handle embedding generation. Start with a local CPU-based model from `sentence-transformers`. <br> - `vector_store.py`: An abstraction layer for ChromaDB to handle storing and retrieving document chunks. | **Done** |
| **1.3** | **Establish Test Suite** | Create a `tests/` directory and configure `pytest`. Write unit tests for the new RAG modules (`document_processor`, `embeddings`, `vector_store`) to ensure they function correctly before integration. | **Done** |
| **1.4** | build quality measurement tests for the RAG. | | To Do |
| **1.5** | evaluate the RAG. | | To Do |

### Phase 2: Core Logic Migration

**Goal:** Replace the Assistants API calls with the new RAG system and the universal Chat Completions API.

**Estimated Effort:** 5-8 days.

| Task ID | Description | Key Actions | Status |
|---|---|---|---|
| **2.1** | **Refactor Agent Logic** | Heavily modify `storycraftr/agent/agents.py`: <br> - Remove functions related to OpenAI Assistants, vector stores, and threads (`create_or_get_assistant`, `get_vector_store_id_by_name`, `get_thread`, etc.). <br> - Create a new data ingestion function that uses the RAG modules from Phase 1 to process and store book files in ChromaDB. <br> - Rewrite the main chat/message function (`create_message`) to orchestrate the new flow: <br>   1. Receive user prompt. <br>   2. Query ChromaDB for relevant context. <br>   3. Construct a new prompt including the context. <br>   4. Call the `client.chat.completions.create()` endpoint. <br>   5. Implement manual conversation history management. | To Do |
| **2.2** | **Update Configuration** | Modify `storycraftr/utils/core.py` (`load_book_config`) and the `storycraftr.json` structure to support multiple providers. Add fields for `api_base_url`, `api_key`, and `model_name` to allow easy switching to Mistral.ai or other providers. | To Do |
| **2.3** | **Update CLI Commands** | Refactor the `storycraftr chat` command (and any others that use the agent) to work with the new agent logic. This includes updating how the agent is initialized and how messages are sent. | To Do |

### Phase 3: Integration Testing and Validation

**Goal:** Ensure the new system works end-to-end and is ready for use.

**Estimated Effort:** 2-3 days.

| Task ID | Description | Key Actions | Status |
|---|---|---|---|
| **3.1** | **End-to-End Testing** | Manually test the full user workflow using the `storycraftr chat` command. Validate against: <br> - OpenAI's API. <br> - A Mistral.ai compatible endpoint. <br> Ensure that context from the book is correctly retrieved and used in responses. | To Do |
| **3.2** | **Write Integration Tests** | Add integration tests to the new test suite that cover the main chat workflow, mocking the API calls but testing the RAG pipeline and prompt construction. | To Do |

## 3. Timeline and Resource Assessment

- **Total Estimated Effort:** **10-16 working days**.
- **Assigned Resources:** 1 Senior Python Developer with AI experience
- **Primary Risk:** The complete absence of an existing test suite significantly increases the risk of introducing regressions. The timeline includes a buffer for manual testing and building a foundational test suite for the new components, which is non-negotiable for a refactoring of this scale.
