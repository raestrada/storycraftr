# Running Tests

This document provides guidance on running the test suite for StoryCraftr.

## Running the Test Suite

Tests are managed using `pytest` and can be run via `poetry`. To run all tests, execute the following command from the root of the repository:

```bash
poetry run pytest
```

To run tests for a specific module, you can specify the path:

```bash
poetry run pytest tests/rag/
```

## Mocks

The test suite is configured to mock external services, such as the Hugging Face Hub and vector databases, to ensure that tests can run without network access or external dependencies. This allows for fast, reliable, and isolated testing of individual components.

## Integration Tests with LLM Providers

Some tests evaluate integration with LLM providers like OpenAI. These tests are skipped by default. To enable them, you must set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_BASE_URL` (optional): The base URL for a compatible API endpoint (e.g., Mistral AI).

You can set these variables in a `.env` file in the project root or export them in your shell:

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"  # pragma: allowlist secret
export OPENAI_BASE_URL="https://api.mistral.ai/v1/"
poetry run pytest
```

These tests will make live calls to the API provider and may incur costs.

## RAG Evaluation Tests

In addition to unit and integration tests, we have evaluation tests to measure the quality of our Retrieval-Augmented Generation (RAG) system. These tests use the [RAGAS framework](https://docs.ragas.io/) to score the faithfulness, relevancy, and context quality of generated answers.

### Running RAG Evaluation Tests

RAG evaluation tests make live calls to an LLM provider to "judge" the quality of the RAG pipeline's output. As such, they require API credentials and will incur costs.

These tests are located in `tests/rag/test_evaluation.py` and are marked to be skipped by default. To run them, you must provide an API key, similar to other integration tests:

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"  # pragma: allowlist secret
poetry run pytest tests/rag/test_evaluation.py
```

### Example Test

A typical RAG evaluation test involves:

1.  Defining a set of questions and (optionally) ground-truth answers.
2.  Running the RAG pipeline to generate an answer and retrieve contexts for each question.
3.  Using RAGAS to evaluate the generated answer against metrics like `faithfulness` and `answer_relevancy`.
4.  Asserting that the quality scores are above a defined threshold.

These tests ensure that our RAG system provides high-quality, contextually accurate responses.
