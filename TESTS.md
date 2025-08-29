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

You can set these variables in a `.env` file in the project root or export them in your shell:

```bash
export OPENAI_API_KEY="sk-..."
poetry run pytest
```

These tests will make live calls to the API provider and may incur costs.
