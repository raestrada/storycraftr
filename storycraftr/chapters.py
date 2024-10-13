import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'chapters', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")

# Function to generate a new chapter based on a prompt
def generate_chapter(book_name, prompt, language, chapter_number):
    """Generate a new chapter based on a prompt."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the chapter content
    chapter_content = create_message(
        thread_id=thread.id,
        content=f"Write a detailed chapter for the following book premise: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    chapter_file = f"chapter-{chapter_number}.md"
    save_to_markdown(book_name, chapter_file, f"Chapter {chapter_number}", chapter_content)
    return chapter_content

# Function to generate the cover page
def generate_cover(book_name, prompt, language):
    """Generate the cover page for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the cover content
    cover_content = create_message(
        thread_id=thread.id,
        content=f"Generate a detailed description for the cover of the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "cover.md", "Cover", cover_content)
    return cover_content

# Function to generate the back cover page
def generate_back_cover(book_name, prompt, language):
    """Generate the back cover page for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the back cover content
    back_cover_content = create_message(
        thread_id=thread.id,
        content=f"Generate a detailed synopsis for the back cover of the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "back_cover.md", "Back Cover", back_cover_content)
    return back_cover_content

# Function to generate the epilogue of the book
def generate_epilogue(book_name, prompt, language):
    """Generate the epilogue for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the epilogue content
    epilogue_content = create_message(
        thread_id=thread.id,
        content=f"Generate the epilogue for the book based on this prompt: {prompt}. Write it in {language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "epilogue.md", "Epilogue", epilogue_content)
    return epilogue_content
