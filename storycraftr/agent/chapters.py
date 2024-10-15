import os
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.core import load_book_config, load_book_config
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.chapters import (
    CHAPTER_PROMPT_NEW,
    CHAPTER_PROMPT_REFINE,
    COVER_PROMPT,
    BACK_COVER_PROMPT,
    EPILOGUE_PROMPT_NEW,
    EPILOGUE_PROMPT_REFINE,
)
from rich.console import Console

console = Console()


# Function to generate a new chapter based on a prompt
def generate_chapter(book_name, chapter_number, prompt):
    """Generate a new chapter based on a prompt."""
    console.print(
        f"[bold blue]Generating chapter {chapter_number}...[/bold blue]"
    )  # Progress message
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    # Prepare the chapter file path
    chapter_file = f"chapter-{chapter_number}.md"
    file_path = os.path.join(book_name, "chapters", chapter_file)

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path):
        console.print(
            f"[yellow]Existing chapter found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = CHAPTER_PROMPT_REFINE.format(
            prompt=prompt, language=load_book_config(book_name).primary_language
        )
        chapter_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing chapter found. Generating new content...[/yellow]"
        )  # Progress message
        content = CHAPTER_PROMPT_NEW.format(
            prompt=prompt, language=load_book_config(book_name).primary_language
        )
        chapter_content = create_message(
            thread_id=thread.id, content=content, assistant=assistant
        )

    # Save the updated chapter content to markdown
    save_to_markdown(
        book_name,
        "chapters/" + chapter_file,
        f"Chapter {chapter_number}",
        chapter_content,
    )
    console.print(
        f"[bold green]✔ Chapter {chapter_number} generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_name, assistant)
    return chapter_content


def generate_cover(book_name, prompt):
    """
    Generate a professional book cover in markdown format using the book's metadata
    and a prompt for additional guidance.
    """
    console.print("[bold blue]Generating book cover...[/bold blue]")  # Progress message
    config = load_book_config(book_name)
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    # Generate the cover content
    prompt_content = COVER_PROMPT.format(
        title=config.book_name,
        author=config.default_author,
        genre=config.genre,
        alternate_languages=", ".join(config.alternate_languages),
        prompt=prompt,
        language=config.primary_language,
    )

    cover_content = create_message(
        thread_id=thread.id, content=prompt_content, assistant=assistant
    )

    # Save the cover content to markdown
    save_to_markdown(book_name, "chapters/cover.md", "Cover", cover_content)
    console.print(
        "[bold green]✔ Cover generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_name, assistant)
    return cover_content


# Function to generate the back cover page
def generate_back_cover(book_name, prompt):
    """Generate the back cover page for the book."""
    console.print("[bold blue]Generating back cover...[/bold blue]")  # Progress message
    config = load_book_config(book_name)
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    # Generate the back cover content
    back_cover_content = create_message(
        thread_id=thread.id,
        content=BACK_COVER_PROMPT.format(
            title=config.book_name,
            author=config.default_author,
            genre=config.genre,
            alternate_languages=", ".join(config.alternate_languages),
            prompt=prompt,
            language=config.primary_language,
            license=config.license,
        ),
        assistant=assistant,
    )

    # Save to markdown
    save_to_markdown(
        book_name, "chapters/back-cover.md", "Back Cover", back_cover_content
    )
    console.print(
        "[bold green]✔ Back cover generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_name, assistant)
    return back_cover_content


# Function to generate the epilogue of the book
def generate_epilogue(book_name, prompt):
    """Generate the epilogue for the book."""
    console.print("[bold blue]Generating epilogue...[/bold blue]")  # Progress message
    assistant = create_or_get_assistant(book_name)
    thread = get_thread()

    # Prepare the epilogue file path
    file_path = os.path.join(book_name, "chapters", "epilogue.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path):
        console.print(
            f"[yellow]Existing epilogue found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = EPILOGUE_PROMPT_REFINE.format(
            prompt=prompt, language=load_book_config(book_name).primary_language
        )
        epilogue_content = create_message(
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing epilogue found. Generating new content...[/yellow]"
        )  # Progress message
        content = EPILOGUE_PROMPT_NEW.format(
            prompt=prompt, language=load_book_config(book_name).primary_language
        )
        epilogue_content = create_message(
            thread_id=thread.id, content=content, assistant=assistant
        )

    # Save the updated epilogue content to markdown
    save_to_markdown(book_name, "chapters/epilogue.md", "Epilogue", epilogue_content)
    console.print(
        "[bold green]✔ Epilogue generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_name, assistant)
    return epilogue_content
