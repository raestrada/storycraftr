import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message
from storycraftr.core import get_config, file_has_more_than_three_lines

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'outline', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")
    return file_path  # Return the path for reuse

# Function to generate the general outline of the book
def generate_general_outline(book_name, prompt):
    """Generate the general outline of the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the general outline
    file_path = os.path.join(book_name, 'outline', "general_outline.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached general outline file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        general_outline_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Create a general outline for a book based on this prompt: {prompt}. Write it in {language}."
        general_outline_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "general_outline.md", "General Outline", general_outline_content)
    return general_outline_content

# Function to generate the character summary of the book
def generate_character_summary(book_name, prompt):
    """Generate the character summary for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the character summary
    file_path = os.path.join(book_name, 'outline', "character_summary.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached character summary file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        character_summary_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate a character summary for the book based on this prompt: {prompt}. Write it in {language}."
        character_summary_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "character_summary.md", "Character Summary", character_summary_content)
    return character_summary_content

# Function to generate the main plot points of the book
def generate_plot_points(book_name, prompt):
    """Generate the main plot points for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the plot points
    file_path = os.path.join(book_name, 'outline', "plot_points.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached plot points file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        plot_points_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the main plot points for the book based on this prompt: {prompt}. Write it in {language}."
        plot_points_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "plot_points.md", "Main Plot Points", plot_points_content)
    return plot_points_content

# Function to generate the chapter-by-chapter synopsis of the book
def generate_chapter_synopsis(book_name, prompt):
    """Generate the chapter-by-chapter synopsis for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the chapter synopsis
    file_path = os.path.join(book_name, 'outline', "chapter_synopsis.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached chapter-by-chapter synopsis file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        chapter_synopsis_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate a chapter-by-chapter synopsis for the book based on this prompt: {prompt}. Write it in {language}."
        chapter_synopsis_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "chapter_synopsis.md", "Chapter Synopsis", chapter_synopsis_content)
    return chapter_synopsis_content
