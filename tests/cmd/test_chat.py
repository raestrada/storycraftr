import os
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
    assert kwargs["history"] == [{"role": "user", "content": "hello"}]

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
        APIError("Test API Error", request=mock_request),
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
    assert kwargs["history"] == [{"role": "user", "content": "first message"}]
