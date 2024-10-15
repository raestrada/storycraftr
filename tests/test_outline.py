import os
import pytest
from unittest.mock import patch, MagicMock
from storycraftr.agent.outline import (
    generate_general_outline, generate_character_summary, 
    generate_plot_points, generate_chapter_synopsis, save_to_markdown
)
from storycraftr.utils.core import get_config, file_has_more_than_three_lines

# Test for generate_general_outline
@patch("storycraftr.outline.create_message")
@patch("storycraftr.outline.get_thread")
@patch("storycraftr.outline.create_or_get_assistant")
@patch("storycraftr.outline.get_config")
@patch("storycraftr.outline.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.outline.save_to_markdown")
def test_generate_general_outline(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_file_lines.return_value = False
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated General Outline Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_general_outline("my_book", "Outline for a new book")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "outline", "general_outline.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Create a general outline for a book based on this prompt: Outline for a new book. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "general_outline.md", "General Outline", "Generated General Outline Content")
    assert result == "Generated General Outline Content"

# Test for generate_character_summary
@patch("storycraftr.outline.create_message")
@patch("storycraftr.outline.get_thread")
@patch("storycraftr.outline.create_or_get_assistant")
@patch("storycraftr.outline.get_config")
@patch("storycraftr.outline.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.outline.save_to_markdown")
def test_generate_character_summary(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = True
    mock_file_lines.return_value = True
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Character Summary Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_character_summary("my_book", "Summary of main characters")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "outline", "character_summary.md"))
    mock_file_lines.assert_called_once_with(os.path.join("my_book", "outline", "character_summary.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Use the attached character summary file to evolve the content based on this prompt: Summary of main characters. Write it in en.",
        assistant="assistant_object",
        file_path=os.path.join("my_book", "outline", "character_summary.md")
    )
    mock_save.assert_called_once_with("my_book", "character_summary.md", "Character Summary", "Generated Character Summary Content")
    assert result == "Generated Character Summary Content"

# Test for generate_plot_points
@patch("storycraftr.outline.create_message")
@patch("storycraftr.outline.get_thread")
@patch("storycraftr.outline.create_or_get_assistant")
@patch("storycraftr.outline.get_config")
@patch("storycraftr.outline.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.outline.save_to_markdown")
def test_generate_plot_points(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_file_lines.return_value = False
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Plot Points Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_plot_points("my_book", "Plot points for the story")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "outline", "plot_points.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate the main plot points for the book based on this prompt: Plot points for the story. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "plot_points.md", "Main Plot Points", "Generated Plot Points Content")
    assert result == "Generated Plot Points Content"

# Test for generate_chapter_synopsis
@patch("storycraftr.outline.create_message")
@patch("storycraftr.outline.get_thread")
@patch("storycraftr.outline.create_or_get_assistant")
@patch("storycraftr.outline.get_config")
@patch("storycraftr.outline.file_has_more_than_three_lines")
@patch("os.path.exists")
@patch("storycraftr.outline.save_to_markdown")
def test_generate_chapter_synopsis(mock_save, mock_exists, mock_file_lines, mock_get_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = True
    mock_file_lines.return_value = True
    mock_get_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Chapter Synopsis Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"

    # Call function
    result = generate_chapter_synopsis("my_book", "Chapter by chapter synopsis")

    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "outline", "chapter_synopsis.md"))
    mock_file_lines.assert_called_once_with(os.path.join("my_book", "outline", "chapter_synopsis.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Use the attached chapter-by-chapter synopsis file to evolve the content based on this prompt: Chapter by chapter synopsis. Write it in en.",
        assistant="assistant_object",
        file_path=os.path.join("my_book", "outline", "chapter_synopsis.md")
    )
    mock_save.assert_called_once_with("my_book", "chapter_synopsis.md", "Chapter Synopsis", "Generated Chapter Synopsis Content")
    assert result == "Generated Chapter Synopsis Content"
