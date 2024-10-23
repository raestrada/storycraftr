import os
import pytest
import shutil
from unittest import mock
from storycraftr.utils.markdown import (
    save_to_markdown,
    append_to_markdown,
    read_from_markdown,
    consolidate_book_md,
)


# Mocks comunes para todos los tests
@pytest.fixture
def mock_console():
    with mock.patch("storycraftr.cli.console") as mock_console:
        yield mock_console


# Test para save_to_markdown
@mock.patch("shutil.copyfile")
@mock.patch("os.path.exists", return_value=True)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_to_markdown_backup(mock_open, mock_exists, mock_copy, mock_console):
    book_path = "test_book"
    file_name = "test.md"
    header = "Test Header"
    content = "Test content"

    save_to_markdown(book_path, file_name, header, content)

    # Verificar que se realizó una copia de seguridad
    mock_copy.assert_called_with(
        os.path.join(book_path, file_name), os.path.join(book_path, file_name) + ".back"
    )
    mock_open.assert_called_with(
        os.path.join(book_path, file_name), "w", encoding="utf-8"
    )
    mock_open().write.assert_called_with(f"# {header}\n\n{content}")


@mock.patch("os.path.exists", return_value=False)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_to_markdown_no_backup(mock_open, mock_exists, mock_console):
    book_path = "test_book"
    file_name = "test.md"
    header = "Test Header"
    content = "Test content"

    save_to_markdown(book_path, file_name, header, content)

    # Verificar que no se hizo copia de seguridad
    mock_open.assert_called_with(
        os.path.join(book_path, file_name), "w", encoding="utf-8"
    )
    mock_open().write.assert_called_with(f"# {header}\n\n{content}")


# Test para append_to_markdown
@mock.patch("os.path.exists", return_value=True)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_append_to_markdown_success(mock_open, mock_exists, mock_console):
    book_path = "test_book"
    folder_name = "test_folder"
    file_name = "test.md"
    content = "Appended content"

    append_to_markdown(book_path, folder_name, file_name, content)

    mock_open.assert_called_with(
        os.path.join(book_path, folder_name, file_name), "a", encoding="utf-8"
    )
    mock_open().write.assert_called_with(f"\n\n{content}")


@mock.patch("os.path.exists", return_value=False)
def test_append_to_markdown_file_not_found(mock_console):
    book_path = "test_book"
    folder_name = "test_folder"
    file_name = "test.md"
    content = "Appended content"

    with pytest.raises(FileNotFoundError):
        append_to_markdown(book_path, folder_name, file_name, content)


# Test para read_from_markdown
@mock.patch("os.path.exists", return_value=True)
@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="File content")
def test_read_from_markdown_success(mock_open, mock_exists, mock_console):
    book_path = "test_book"
    folder_name = "test_folder"
    file_name = "test.md"

    content = read_from_markdown(book_path, folder_name, file_name)

    mock_open.assert_called_with(
        os.path.join(book_path, folder_name, file_name), "r", encoding="utf-8"
    )
    assert content == "File content"


@mock.patch("os.path.exists", return_value=False)
def test_read_from_markdown_file_not_found(mock_console):
    book_path = "test_book"
    folder_name = "test_folder"
    file_name = "test.md"

    with pytest.raises(FileNotFoundError):
        read_from_markdown(book_path, folder_name, file_name)
