import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message
from storycraftr.core import get_config, file_has_more_than_three_lines

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'worldbuilding', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")
    return file_path  # Return the path for reuse

# Function to generate the geography of the world
def generate_geography(book_name, prompt):
    """Generate the geography details for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the geography details
    file_path = os.path.join(book_name, 'worldbuilding', "geography.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached geography file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        geography_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the geography details for the book's world based on this prompt: {prompt}. Write it in {language}."
        geography_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "geography.md", "Geography", geography_content)
    return geography_content

# Function to generate the history of the world
def generate_history(book_name, prompt):
    """Generate the history details for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the history details
    file_path = os.path.join(book_name, 'worldbuilding', "history.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached history file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        history_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the history details for the book's world based on this prompt: {prompt}. Write it in {language}."
        history_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "history.md", "History", history_content)
    return history_content

# Function to generate the culture of the world
def generate_culture(book_name, prompt):
    """Generate the culture details for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the culture details
    file_path = os.path.join(book_name, 'worldbuilding', "culture.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached culture file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        culture_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the culture details for the book's world based on this prompt: {prompt}. Write it in {language}."
        culture_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "culture.md", "Culture", culture_content)
    return culture_content

# Function to generate the magic or science system of the world
def generate_magic_system(book_name, prompt):
    """Generate the magic/science system for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the magic system
    file_path = os.path.join(book_name, 'worldbuilding', "magic_system.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached magic/science system file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        magic_system_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the magic/science system for the book's world based on this prompt: {prompt}. Write it in {language}."
        magic_system_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "magic_system.md", "Magic/Science System", magic_system_content)
    return magic_system_content

# Function to generate the technology of the world (if applicable)
def generate_technology(book_name, prompt):
    """Generate the technology details for the book."""
    language = get_config(book_name).primary_language
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # File path for the technology details
    file_path = os.path.join(book_name, 'worldbuilding', "technology.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        content = f"Use the attached technology file to evolve the content based on this prompt: {prompt}. Write it in {language}."
        technology_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the technology details for the book's world based on this prompt: {prompt}. Write it in {language}."
        technology_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_name, "technology.md", "Technology", technology_content)
    return technology_content
