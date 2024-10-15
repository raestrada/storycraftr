import os
import pytest
from unittest.mock import patch, MagicMock
from storycraftr.agent.worldbuilding import (
    generate_geography, generate_history, generate_culture, 
    generate_magic_system, generate_technology, save_to_markdown
)
from storycraftr.utils.core import get_config, file_has_more_than_three_lines


# Test for generate_geography
@patch("storycraftr.worldbuilding.create_message")
@patch("storycraftr.worldbuilding.get_thread")
@patch("storycraftr.worldbuilding.create_or_get_assistant")
@patch("storycraftr.worldbuilding.get_config")
@patch("storycraftr.worldbuilding.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.worldbuilding.save_to_markdown")
def test_generate_geography(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_file_lines.return_value = False
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Geography Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_geography("my_book", "Geography of a fantastic world")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "worldbuilding", "geography.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate the geography details for the book's world based on this prompt: Geography of a fantastic world. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "geography.md", "Geography", "Generated Geography Content")
    assert result == "Generated Geography Content"

# Test for generate_history
@patch("storycraftr.worldbuilding.create_message")
@patch("storycraftr.worldbuilding.get_thread")
@patch("storycraftr.worldbuilding.create_or_get_assistant")
@patch("storycraftr.worldbuilding.get_config")
@patch("storycraftr.worldbuilding.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.worldbuilding.save_to_markdown")
def test_generate_history(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = True
    mock_file_lines.return_value = True
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated History Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_history("my_book", "Ancient history of the world")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "worldbuilding", "history.md"))
    mock_file_lines.assert_called_once_with(os.path.join("my_book", "worldbuilding", "history.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Use the attached history file to evolve the content based on this prompt: Ancient history of the world. Write it in en.",
        assistant="assistant_object",
        file_path=os.path.join("my_book", "worldbuilding", "history.md")
    )
    mock_save.assert_called_once_with("my_book", "history.md", "History", "Generated History Content")
    assert result == "Generated History Content"

# Test for generate_culture
@patch("storycraftr.worldbuilding.create_message")
@patch("storycraftr.worldbuilding.get_thread")
@patch("storycraftr.worldbuilding.create_or_get_assistant")
@patch("storycraftr.worldbuilding.get_config")
@patch("storycraftr.worldbuilding.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.worldbuilding.save_to_markdown")
def test_generate_culture(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_file_lines.return_value = False
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Culture Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_culture("my_book", "Culture of the people")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "worldbuilding", "culture.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate the culture details for the book's world based on this prompt: Culture of the people. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "culture.md", "Culture", "Generated Culture Content")
    assert result == "Generated Culture Content"

# Test for generate_magic_system
@patch("storycraftr.worldbuilding.create_message")
@patch("storycraftr.worldbuilding.get_thread")
@patch("storycraftr.worldbuilding.create_or_get_assistant")
@patch("storycraftr.worldbuilding.get_config")
@patch("storycraftr.worldbuilding.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.worldbuilding.save_to_markdown")
def test_generate_magic_system(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = True
    mock_file_lines.return_value = True
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Magic System Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_magic_system("my_book", "Complex magic system")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "worldbuilding", "magic_system.md"))
    mock_file_lines.assert_called_once_with(os.path.join("my_book", "worldbuilding", "magic_system.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Use the attached magic/science system file to evolve the content based on this prompt: Complex magic system. Write it in en.",
        assistant="assistant_object",
        file_path=os.path.join("my_book", "worldbuilding", "magic_system.md")
    )
    mock_save.assert_called_once_with("my_book", "magic_system.md", "Magic/Science System", "Generated Magic System Content")
    assert result == "Generated Magic System Content"

# Test for generate_technology
@patch("storycraftr.worldbuilding.create_message")
@patch("storycraftr.worldbuilding.get_thread")
@patch("storycraftr.worldbuilding.create_or_get_assistant")
@patch("storycraftr.worldbuilding.get_config")
@patch("storycraftr.worldbuilding.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.worldbuilding.save_to_markdown")
def test_generate_technology(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_file_lines.return_value = False
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Technology Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_technology("my_book", "Advanced technology of the world")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "worldbuilding", "technology.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate the technology details for the book's world based on this prompt: Advanced technology of the world. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "technology.md", "Technology", "Generated Technology Content")
    assert result == "Generated Technology Content"
