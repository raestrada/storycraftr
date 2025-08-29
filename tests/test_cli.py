import os
import sys
import pytest
import requests
from unittest import mock
from pathlib import Path
from click import ClickException
from storycraftr.cli import (
    verify_book_path,
    is_initialized,
    project_not_initialized_error,
)
from storycraftr.init import download_file


# Mock the console object to avoid printing to the console during tests
@pytest.fixture
def mock_console():
    with mock.patch("storycraftr.cli.console") as mock_console:
        yield mock_console


# Test download_file function
@mock.patch("requests.get")
@mock.patch("storycraftr.init.console")
def test_download_file_success(mock_console, mock_get):
    mock_response = mock.Mock()
    mock_response.text = "file content"
    mock_response.raise_for_status = mock.Mock()
    mock_get.return_value = mock_response

    save_dir = "test_dir"
    filename = "test_file.txt"

    with mock.patch("pathlib.Path.mkdir") as mock_mkdir, mock.patch(
        "pathlib.Path.write_text"
    ) as mock_write:
        download_file("http://example.com", save_dir, filename)

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_write.assert_called_once_with("file content", encoding="utf-8")
        mock_console.print.assert_called_with(
            "[green]File downloaded successfully from http://example.com[/green]"
        )


@mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Error"))
@mock.patch("storycraftr.init.console")
def test_download_file_failure(mock_console, mock_get):
    with pytest.raises(SystemExit):
        download_file("http://example.com", "test_dir", "test_file.txt")

    mock_console.print.assert_called_with(
        "[red]Error downloading the file from http://example.com: Error[/red]"
    )


# Test verify_book_path function
@mock.patch("os.path.exists", return_value=True)
def test_verify_book_path_success(mock_exists):
    assert verify_book_path("test_path") == "test_path"


@mock.patch("os.path.exists", return_value=False)
def test_verify_book_path_failure(mock_exists):
    with pytest.raises(ClickException):
        verify_book_path("invalid_path")


# Test is_initialized function
@mock.patch("os.path.exists", return_value=True)
def test_is_initialized_true(mock_exists):
    assert is_initialized("test_path")


@mock.patch("os.path.exists", return_value=False)
def test_is_initialized_false(mock_exists):
    assert not is_initialized("test_path")


# Test project_not_initialized_error function
def test_project_not_initialized_error(mock_console):
    project_not_initialized_error("test_path")

    mock_console.print.assert_called_with(
        "[red]✖ Project 'test_path' is not initialized. Run 'storycraftr init {book_path}' first.[/red]"
    )
