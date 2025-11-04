import os
from pathlib import Path
from unittest import mock

import pytest
from click import ClickException

from storycraftr.cli import (
    verify_book_path,
    is_initialized,
    project_not_initialized_error,
)
from storycraftr.llm.credentials import load_local_credentials


@pytest.fixture(autouse=True)
def reset_env():
    original = dict(os.environ)
    for var in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "OLLAMA_API_KEY"):
        os.environ.pop(var, None)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


@pytest.fixture
def mock_console():
    with mock.patch("storycraftr.cli.console") as console:
        yield console


def test_verify_book_path_success(mock_console):
    with mock.patch("os.path.exists", return_value=True):
        assert verify_book_path("my_project") == "my_project"


def test_verify_book_path_failure(mock_console):
    with mock.patch("os.path.exists", return_value=False):
        with pytest.raises(ClickException):
            verify_book_path("missing_project")


def test_is_initialized_true(mock_console):
    with mock.patch("os.path.exists", return_value=True):
        assert is_initialized("my_project")


def test_is_initialized_false(mock_console):
    with mock.patch("os.path.exists", return_value=False):
        assert not is_initialized("my_project")


def test_project_not_initialized_error(mock_console):
    project_not_initialized_error("demo")
    mock_console.print.assert_called_once()


def test_load_local_credentials(tmp_path):
    config_dir = tmp_path / ".storycraftr"
    config_dir.mkdir()
    key_file = config_dir / "openai_api_key.txt"
    key_file.write_text("placeholder-token", encoding="utf-8")

    with mock.patch("pathlib.Path.home", return_value=tmp_path):
        load_local_credentials()

    expected = "placeholder-token"  # pragma: allowlist secret
    assert os.environ["OPENAI_API_KEY"] == expected
