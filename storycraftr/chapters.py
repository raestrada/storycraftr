import os
from storycraftr.agents import create_or_get_assistant, get_thread, create_message
from storycraftr.core import get_config

# Function to save content to a markdown file
def save_to_markdown(book_name, file_name, header, content):
    """Save the generated content to the specified markdown file."""
    file_path = os.path.join(book_name, 'chapters', file_name)
    with open(file_path, 'w') as f:
        f.write(f"# {header}\n\n{content}")
    return file_path  # Return the path for potential reuse

# Function to generate a new chapter based on a prompt
def generate_chapter(book_name, prompt, chapter_number):
    """Generate a new chapter based on a prompt."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Prepare the chapter file path
    chapter_file = f"chapter-{chapter_number}.md"
    file_path = os.path.join(book_name, 'chapters', chapter_file)

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path):
        content = f"Use the attached chapter file as a reference to evolve and improve the content based on this prompt: {prompt}. Write it in {get_config(book_name).primary_language}."
        chapter_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Write a detailed chapter for the following book premise: {prompt}. Write it in {get_config(book_name).primary_language}."
        chapter_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save the updated chapter content to markdown
    save_to_markdown(book_name, chapter_file, f"Chapter {chapter_number}", chapter_content)
    return chapter_content

def generate_cover(book_name, prompt):
    """
    Generate a professional book cover in markdown format using the book's metadata 
    and a prompt for additional guidance.
    """
    # Obtener los datos del archivo de configuración
    config = get_config(book_name)
    language = config.primary_language
    title = config.book_name
    author = config.default_author
    genre = config.genre
    alternate_languages = ', '.join(config.alternate_languages)

    # Crear o obtener el asistente
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Prompt para generar la portada completa en markdown, incluyendo todos los datos relevantes
    prompt_content = (
        f"Create a professional book cover in markdown format for the book titled '{title}'. "
        f"Include the title, author (which is '{author}'), genre ('{genre}'), "
        f"and alternate languages ('{alternate_languages}'). Use this information to format a typical "
        f"book cover with a detailed description. Use this prompt as additional context: {prompt}. "
        f"Write the content in {language}."
    )

    # Generar el contenido completo de la portada
    cover_content = create_message(
        thread_id=thread.id,
        content=prompt_content,
        assistant=assistant
    )

    # Guardar el contenido en el archivo markdown
    save_to_markdown(book_name, "cover.md", "Cover", cover_content)

    return cover_content


# Function to generate the back cover page
def generate_back_cover(book_name, prompt):
    """Generate the back cover page for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Generate the back cover content
    back_cover_content = create_message(
        thread_id=thread.id,
        content=f"Generate a detailed synopsis for the back cover of the book based on this prompt: {prompt}. Write it in {get_config(book_name).primary_language}.",
        assistant=assistant
    )

    # Save to markdown
    save_to_markdown(book_name, "back_cover.md", "Back Cover", back_cover_content)
    return back_cover_content

# Function to generate the epilogue of the book
def generate_epilogue(book_name, prompt):
    """Generate the epilogue for the book."""
    assistant = create_or_get_assistant(book_name, book_name)
    thread = get_thread()

    # Prepare the epilogue file path
    file_path = os.path.join(book_name, 'chapters', "epilogue.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path):
        content = f"Use the attached epilogue file as a reference to evolve and improve the content based on this prompt: {prompt}. Write it in {get_config(book_name).primary_language}."
        epilogue_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path
        )
    else:
        content = f"Generate the epilogue for the book based on this prompt: {prompt}. Write it in {get_config(book_name).primary_language}."
        epilogue_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant
        )

    # Save the updated epilogue content to markdown
    save_to_markdown(book_name, "epilogue.md", "Epilogue", epilogue_content)
    return epilogue_content
