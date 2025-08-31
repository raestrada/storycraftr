import os
import json
from unittest.mock import MagicMock, patch

import httpx
import pytest
from click.testing import CliRunner
from openai import APIError

from storycraftr.cmd.chat import chat


@pytest.fixture
def mock_dependencies():
    """Fixture to mock dependencies for the chat command."""
    with (
        patch("storycraftr.cmd.chat.load_book_config") as mock_load,
        patch("storycraftr.cmd.chat.ingest_book_data") as mock_ingest,
        patch("storycraftr.cmd.chat.create_message") as mock_create,
        patch("storycraftr.cmd.chat.PromptSession") as mock_session,
    ):
        # Simulate successful book config loading
        config = MagicMock()
        mock_load.return_value = config

        # Simulate user typing "hello" and then "exit()"
        mock_session_instance = MagicMock()
        mock_session_instance.prompt.side_effect = ["hello", "exit()"]
        mock_session.return_value = mock_session_instance

        # Mock create_message to return a simple response
        mock_create.return_value = "A mock response."

        yield {
            "load_config": mock_load,
            "ingest": mock_ingest,
            "create": mock_create,
            "session": mock_session,
        }


def test_chat_happy_path(mock_dependencies, tmp_path):
    """
    Test the normal flow of a chat session: ingest, prompt, response, exit.
    """
    runner = CliRunner()
    book_path = str(tmp_path)
    result = runner.invoke(chat, ["--book-path", book_path], catch_exceptions=False)

    assert result.exit_code == 0
    mock_dependencies["ingest"].assert_called_once_with(book_path)

    # Verify create_message call
    mock_dependencies["create"].assert_called_once()
    args, kwargs = mock_dependencies["create"].call_args
    assert (
        "Answer the next prompt formatted on markdown (text): hello"
        in kwargs["content"]
    )
    assert kwargs["history"] == []

    # Verify response is in output
    assert "A mock response." in result.output


def test_chat_api_error_handling(mock_dependencies, tmp_path):
    """
    Test that API errors are handled gracefully and history is managed correctly.
    """
    # Simulate an APIError on the first call, then successful exit
    mock_request = httpx.Request(
        method="POST", url="https://api.openai.com/v1/chat/completions"
    )
    mock_dependencies["create"].side_effect = [
        APIError("Test API Error", request=mock_request, body=None),
    ]
    mock_dependencies["session"].return_value.prompt.side_effect = [
        "first message",
        "exit()",
    ]

    runner = CliRunner()
    book_path = str(tmp_path)
    result = runner.invoke(chat, ["--book-path", book_path])

    assert result.exit_code == 0
    assert "API Error: Test API Error" in result.output

    # create_message should be called once
    assert mock_dependencies["create"].call_count == 1

    # Check that history was correct for the failed call
    args, kwargs = mock_dependencies["create"].call_args
    assert kwargs["history"] == []


@pytest.fixture
def mock_integration_dependencies(tmp_path, monkeypatch):
    """Fixture for chat command integration tests, mocking external services."""
    # Reset singleton cache to ensure our mock is used.
    monkeypatch.setattr("storycraftr.agent.agents._embedding_generator", None)

    # Use an absolute path for file setup
    abs_book_path = tmp_path
    chapters_dir = abs_book_path / "chapters"
    chapters_dir.mkdir()
    (chapters_dir / "chapter-1.md").write_text(
        "# Chapter 1\n\nZevid is a character from a distant planet."
    )
    (abs_book_path / "storycraftr.json").write_text(
        json.dumps(
            {
                "book_name": "Test Book",
                "author": "Test Author",
                "rag": {"distance_threshold": 0.5},
            }
        )
    )

    # Change to the parent directory to use a relative path for the book,
    # which is a valid ChromaDB collection name.
    monkeypatch.chdir(abs_book_path.parent)
    book_path = abs_book_path.name

    # This mock class satisfies ChromaDB's protocol for an embedding function.
    class MockEmbeddingGenerator:
        is_legacy = False

        def __call__(self, input):
            # The embedding vector can be simple, as it's not used in assertions.
            return [[0.1, 0.2, 0.3] for _ in input]

        def name(self):
            return "mock_embedding_generator"

    with patch("storycraftr.cmd.chat.PromptSession") as mock_session, patch(
        "storycraftr.agent.agents.OpenAI"
    ) as mock_openai, patch(
        "storycraftr.agent.agents.EmbeddingGenerator"
    ) as mock_embedding_generator:
        # Mock EmbeddingGenerator to return an instance of our compliant mock class.
        # This will be used by `ingest_book_data`.
        mock_embedding_generator.return_value = MockEmbeddingGenerator()

        # Mock session to simulate user input
        mock_session_instance = MagicMock()
        mock_session_instance.prompt.side_effect = ["Who is Zevid?", "exit()"]
        mock_session.return_value = mock_session_instance

        # Mock OpenAI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Zevid is a fictional character."
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        yield {
            "session": mock_session,
            "openai": mock_openai,
            "client": mock_client,
            "embedding_generator": mock_embedding_generator,
            "book_path": str(book_path),
        }


def test_chat_integration_with_rag(mock_integration_dependencies):
    """
    Integration test for the chat command with the RAG pipeline.
    Mocks embeddings and API calls, but tests document processing and prompt construction.
    """
    runner = CliRunner()
    book_path = mock_integration_dependencies["book_path"]
    result = runner.invoke(chat, ["--book-path", book_path], catch_exceptions=False)

    assert result.exit_code == 0
    assert "Zevid is a fictional character." in result.output

    # Verify that the OpenAI client was called with context from the RAG pipeline
    mock_client = mock_integration_dependencies["client"]
    mock_client.chat.completions.create.assert_called_once()

    # Check the content of the prompt sent to the LLM
    call_args, call_kwargs = mock_client.chat.completions.create.call_args

    # Extract system and user messages
    system_prompt = ""
    user_prompt = ""
    for message in call_kwargs["messages"]:
        if message["role"] == "system":
            system_prompt = message["content"]
        elif message["role"] == "user":
            user_prompt = message["content"]

    # Verify that the RAG context is in the system prompt
    assert "Zevid is a character from a distant planet." in system_prompt

    # Verify that the user's question is in the user prompt
    assert "Who is Zevid?" in user_prompt
