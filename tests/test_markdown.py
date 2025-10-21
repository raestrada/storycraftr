import os
import pytest
import shutil
import tempfile
from pathlib import Path
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
    with mock.patch("storycraftr.utils.markdown.console") as mock_console:
        yield mock_console


@pytest.fixture
def temp_book_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# Test para save_to_markdown
@mock.patch("shutil.copyfile")
def test_save_to_markdown_backup(mock_copy, mock_console, temp_book_dir):
    book_path = temp_book_dir
    file_name = "test.md"
    header = "Test Header"
    content = "Test content"
    file_path = book_path / file_name
    file_path.write_text("initial content")

    save_to_markdown(book_path, file_name, header, content)

    # Verificar que se realizó una copia de seguridad
    mock_copy.assert_called_with(file_path, Path(f"{file_path}.back"))
    assert file_path.read_text() == f"# {header}\n\n{content}"


def test_save_to_markdown_no_backup(mock_console, temp_book_dir):
    book_path = temp_book_dir
    file_name = "test.md"
    header = "Test Header"
    content = "Test content"
    file_path = book_path / file_name

    save_to_markdown(book_path, file_name, header, content)

    assert not (book_path / (file_name + ".back")).exists()
    assert file_path.read_text() == f"# {header}\n\n{content}"


# Test para append_to_markdown
def test_append_to_markdown_success(mock_console, temp_book_dir):
    book_path = temp_book_dir
    folder_name = "test_folder"
    file_name = "test.md"
    content = "Appended content"
    initial_content = "Initial content"

    folder_path = book_path / folder_name
    folder_path.mkdir()
    file_path = folder_path / file_name
    file_path.write_text(initial_content)

    append_to_markdown(book_path, folder_name, file_name, content)

    assert file_path.read_text() == f"{initial_content}\n\n{content}"


def test_append_to_markdown_file_not_found(mock_console, temp_book_dir):
    book_path = temp_book_dir
    folder_name = "test_folder"
    file_name = "test.md"
    content = "Appended content"

    with pytest.raises(FileNotFoundError):
        append_to_markdown(book_path, folder_name, file_name, content)


# Test para read_from_markdown
def test_read_from_markdown_success(mock_console, temp_book_dir):
    book_path = temp_book_dir
    folder_name = "test_folder"
    file_name = "test.md"
    file_content = "File content"

    folder_path = book_path / folder_name
    folder_path.mkdir()
    (folder_path / file_name).write_text(file_content)

    content = read_from_markdown(book_path, folder_name, file_name)

    assert content == file_content


def test_read_from_markdown_file_not_found(mock_console, temp_book_dir):
    book_path = temp_book_dir
    folder_name = "test_folder"
    file_name = "test.md"

    with pytest.raises(FileNotFoundError):
        read_from_markdown(book_path, folder_name, file_name)
