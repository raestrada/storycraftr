import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'outline', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")

# Function to generate the general outline of the book
def generate_general_outline(book_name, prompt, language):
    """Generate the general outline of the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the general outline content
    general_outline_content = create_message(
        thread_id=thread.id,
        content=f"Create a general outline for a book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "general_outline.md", "General Outline", general_outline_content)
    return general_outline_content

# Function to generate the character summary of the book
def generate_character_summary(book_name, prompt, language):
    """Generate the character summary for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the character summary content
    character_summary_content = create_message(
        thread_id=thread.id,
        content=f"Generate a character summary for the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "character_summary.md", "Character Summary", character_summary_content)
    return character_summary_content

# Function to generate the main plot points of the book
def generate_plot_points(book_name, prompt, language):
    """Generate the main plot points for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the plot points content
    plot_points_content = create_message(
        thread_id=thread.id,
        content=f"Generate the main plot points for the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "plot_points.md", "Main Plot Points", plot_points_content)
    return plot_points_content

# Function to generate the chapter-by-chapter synopsis of the book
def generate_chapter_synopsis(book_name, prompt, language):
    """Generate the chapter-by-chapter synopsis for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the chapter synopsis content
    chapter_synopsis_content = create_message(
        thread_id=thread.id,
        content=f"Generate a chapter-by-chapter synopsis for the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "chapter_synopsis.md", "Chapter Synopsis", chapter_synopsis_content)
    return chapter_synopsis_content
