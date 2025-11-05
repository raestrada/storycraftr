# LangChain Graph Refactor Plan

## Objective
Replace the hand-rolled assistant pipeline (manual retriever/LLM coordination and custom fallbacks) with a LangChain graph that orchestrates retrieval, prompting, and tool execution in a single, testable workflow.

## Current Pain Points
- `storycraftr/agent/agents.py` manages state, retrieval, and retries manually; the logic is brittle and difficult to reason about.
- Retriever or vector-store errors surface late, leading to hallucinated answers when docs aren’t loaded.
- There is no separation between planning, tool-use, and output formatting; everything funnels through `create_message`.
- Automated testing for RAG responses is missing; QA requires manual CLI runs.

## Target Architecture
- Define a LangChain graph (LCEL or `langgraph`) with nodes for:
  - **Retriever**: Chroma-backed retriever node returning document context.
  - **Prompt**: Conversation/command prompt builder that merges behavior instructions with retrieved context.
  - **LLM**: Chat model node producing the final answer.
  - Optional **Tools**: Hooks for file edits, outline generation, or future agents.
- Replace the CLI `create_message` call with a simple graph invocation.
- Persist graph configuration separately, enabling reuse in tests and potential server/extension integrations.

## Workstreams
1. **Graph Skeleton**
   - Add `storycraftr/graph/__init__.py` with reusable graph factory functions.
   - Implement nodes for retriever, prompt assembly, and LLM invocation.
   - Ensure embeddings/vector-store are created before graph construction.
2. **CLI Integration**
   - Update `storycraftr/cmd/chat.py` and other command modules to call the graph instead of `create_message`.
   - Remove obsolete helper code in `storycraftr/agent/agents.py` once graph is proven.
3. **Testing**
   - Add integration tests that run the graph with a fixed project and assert that a seeded question (e.g., installation instructions) cites the documentation.
   - Provide fixtures to preload the Chroma index for tests.
4. **Documentation**
   - Document the graph design, configuration flags, and how to extend nodes (e.g., adding tool execution).
   - Update `README.md` / `docs/getting_started.md` with instructions on running the new pipeline.

## Risks & Mitigations
- **Backward compatibility**: CLI commands must behave identically; add feature flags during transition if needed.
- **Graph complexity**: Start with the simplest graph (Retriever → Prompt → LLM); iterate before adding tools or branching logic.
- **Testing overhead**: Ensure tests seed embeddings once to keep runtime manageable.

## Success Criteria
- `storycraftr` CLI uses a LangChain graph end-to-end.
- Reloaded documentation is visible in graph responses (verified via tests).
- Legacy `create_message` and manual retries are retired.
- Docs and README illustrate how contributors can extend the graph.
