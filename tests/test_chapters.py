import os
import pytest
from unittest.mock import patch, MagicMock
from storycraftr.agent.agents import create_message, create_or_get_assistant, get_thread
from storycraftr.utils.core import load_book_config
from storycraftr.agent.chapters import generate_chapter, generate_cover, generate_back_cover, generate_epilogue, save_to_markdown

# Test for generate_chapter
@patch("storycraftr.chapters.create_message")
@patch("storycraftr.chapters.get_thread")
@patch("storycraftr.chapters.create_or_get_assistant")
@patch("storycraftr.chapters.load_book_config")
@patch("os.path.exists")
@patch("storycraftr.chapters.save_to_markdown")
def test_generate_chapter(mock_save, mock_exists, mock_load_book_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_load_book_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Chapter Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"
    
    # Call function
    result = generate_chapter("my_book", "A great chapter", 1)
    
    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "chapters", "chapter-1.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Write a detailed chapter for the following book premise: A great chapter. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "chapter-1.md", "Chapter 1", "Generated Chapter Content")
    assert result == "Generated Chapter Content"

# Test for generate_cover
@patch("storycraftr.chapters.create_message")
@patch("storycraftr.chapters.get_thread")
@patch("storycraftr.chapters.create_or_get_assistant")
@patch("storycraftr.chapters.load_book_config")
@patch("storycraftr.chapters.save_to_markdown")
def test_generate_cover(mock_save, mock_load_book_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_load_book_config.return_value = MagicMock(
        primary_language="en", 
        book_name="My Book", 
        default_author="Author Name", 
        genre="Science Fiction",
        alternate_languages=["es"]
    )
    mock_message.return_value = "Generated Cover Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"
    
    # Call function
    result = generate_cover("my_book", "A beautiful cover")
    
    # Assertions
    expected_prompt = (
        "Create a professional book cover in markdown format for the book titled 'My Book'. "
        "Include the title, author (which is 'Author Name'), genre ('Science Fiction'), "
        "and alternate languages ('es'). Use this information to format a typical "
        "book cover with a detailed description. Use this prompt as additional context: A beautiful cover. "
        "Write the content in en."
    )
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content=expected_prompt,
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "cover.md", "Cover", "Generated Cover Content")
    assert result == "Generated Cover Content"

# Test for generate_back_cover
@patch("storycraftr.chapters.create_message")
@patch("storycraftr.chapters.get_thread")
@patch("storycraftr.chapters.create_or_get_assistant")
@patch("storycraftr.chapters.load_book_config")
@patch("storycraftr.chapters.save_to_markdown")
def test_generate_back_cover(mock_save, mock_load_book_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_load_book_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Back Cover Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"
    
    # Call function
    result = generate_back_cover("my_book", "A short synopsis")
    
    # Assertions
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate a detailed synopsis for the back cover of the book based on this prompt: A short synopsis. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "back_cover.md", "Back Cover", "Generated Back Cover Content")
    assert result == "Generated Back Cover Content"

# Test for generate_epilogue
@patch("storycraftr.chapters.create_message")
@patch("storycraftr.chapters.get_thread")
@patch("storycraftr.chapters.create_or_get_assistant")
@patch("storycraftr.chapters.load_book_config")
@patch("os.path.exists")
@patch("storycraftr.chapters.save_to_markdown")
def test_generate_epilogue(mock_save, mock_exists, mock_load_book_config, mock_assistant, mock_thread, mock_message):
    # Mocks
    mock_exists.return_value = False
    mock_load_book_config.return_value = MagicMock(primary_language="en")
    mock_message.return_value = "Generated Epilogue Content"
    mock_thread.return_value.id = "thread_id"
    mock_assistant.return_value = "assistant_object"
    
    # Call function
    result = generate_epilogue("my_book", "A thrilling epilogue")
    
    # Assertions
    mock_exists.assert_called_once_with(os.path.join("my_book", "chapters", "epilogue.md"))
    mock_message.assert_called_once_with(
        thread_id="thread_id",
        content="Generate the epilogue for the book based on this prompt: A thrilling epilogue. Write it in en.",
        assistant="assistant_object"
    )
    mock_save.assert_called_once_with("my_book", "epilogue.md", "Epilogue", "Generated Epilogue Content")
    assert result == "Generated Epilogue Content"
