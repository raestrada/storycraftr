import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'worldbuilding', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")

# Function to generate the geography of the world
def generate_geography(book_name, prompt, language):
    """Generate the geography details for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the geography content
    geography_content = create_message(
        thread_id=thread.id,
        content=f"Generate the geography details for the book's world based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "geography.md", "Geography", geography_content)
    return geography_content

# Function to generate the history of the world
def generate_history(book_name, prompt, language):
    """Generate the history details for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the history content
    history_content = create_message(
        thread_id=thread.id,
        content=f"Generate the history details for the book's world based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "history.md", "History", history_content)
    return history_content

# Function to generate the culture of the world
def generate_culture(book_name, prompt, language):
    """Generate the culture details for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the culture content
    culture_content = create_message(
        thread_id=thread.id,
        content=f"Generate the culture details for the book's world based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "culture.md", "Culture", culture_content)
    return culture_content

# Function to generate the magic or science system of the world
def generate_magic_system(book_name, prompt, language):
    """Generate the magic/science system for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the magic system content
    magic_system_content = create_message(
        thread_id=thread.id,
        content=f"Generate the magic/science system for the book's world based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "magic_system.md", "Magic/Science System", magic_system_content)
    return magic_system_content

# Function to generate the technology of the world (if applicable)
def generate_technology(book_name, prompt, language):
    """Generate the technology details for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the technology content
    technology_content = create_message(
        thread_id=thread.id,
        content=f"Generate the technology details for the book's world based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "technology.md", "Technology", technology_content)
    return technology_content
