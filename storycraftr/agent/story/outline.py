import os
from storycraftr.utils.core import load_book_config, file_has_more_than_three_lines
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.story.outline import (
    GENERAL_OUTLINE_PROMPT_NEW,
    GENERAL_OUTLINE_PROMPT_REFINE,
    CHARACTER_SUMMARY_PROMPT_NEW,
    CHARACTER_SUMMARY_PROMPT_REFINE,
    PLOT_POINTS_PROMPT_NEW,
    PLOT_POINTS_PROMPT_REFINE,
    CHAPTER_SYNOPSIS_PROMPT_NEW,
    CHAPTER_SYNOPSIS_PROMPT_REFINE,
)
from rich.console import Console

console = Console()


def generate_general_outline(book_path: str, prompt: str) -> str:
    """
    Generate or refine the general outline of the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): The prompt to guide the outline generation.

    Returns:
        str: The generated or refined general outline.
    """
    console.print("[bold blue]Generating general outline...[/bold blue]")

    # Load the book configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()
    file_path = os.path.join(book_path, "outline", "general_outline.md")
    book_name = config.book_name

    # Check if the outline already exists and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing general outline...[/yellow]")
        content = GENERAL_OUTLINE_PROMPT_REFINE.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )
    else:
        console.print(f"[yellow]Generating new general outline...[/yellow]")
        content = GENERAL_OUTLINE_PROMPT_NEW.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )

    # Generate the outline using the assistant
    general_outline_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path,
        "outline/general_outline.md",
        "General Outline",
        general_outline_content,
    )
    console.print("[bold green]✔ General outline generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return general_outline_content


def generate_character_summary(book_path: str, prompt: str) -> str:
    """
    Generate or refine the character summary of the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): The prompt to guide the character summary generation.

    Returns:
        str: The generated or refined character summary.
    """
    console.print("[bold blue]Generating character summary...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()
    file_path = os.path.join(book_path, "outline", "character_summary.md")
    book_name = os.path.basename(book_path)

    # Check if the character summary already exists and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing character summary...[/yellow]")
        content = CHARACTER_SUMMARY_PROMPT_REFINE.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )
    else:
        console.print(f"[yellow]Generating new character summary...[/yellow]")
        content = CHARACTER_SUMMARY_PROMPT_NEW.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )

    # Generate the character summary using the assistant
    character_summary_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path,
        "outline/character_summary.md",
        "Character Summary",
        character_summary_content,
    )
    console.print("[bold green]✔ Character summary generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return character_summary_content


def generate_plot_points(book_path: str, prompt: str) -> str:
    """
    Generate or refine the main plot points of the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): The prompt to guide the plot points generation.

    Returns:
        str: The generated or refined plot points.
    """
    console.print("[bold blue]Generating main plot points...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()
    file_path = os.path.join(book_path, "outline", "plot_points.md")
    book_name = os.path.basename(book_path)

    # Check if the plot points already exist and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing plot points...[/yellow]")
        content = PLOT_POINTS_PROMPT_REFINE.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )
    else:
        console.print(f"[yellow]Generating new plot points...[/yellow]")
        content = PLOT_POINTS_PROMPT_NEW.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )

    # Generate the plot points using the assistant
    plot_points_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path, "outline/plot_points.md", "Main Plot Points", plot_points_content
    )
    console.print("[bold green]✔ Main plot points generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return plot_points_content


def generate_chapter_synopsis(book_path: str, prompt: str) -> str:
    """
    Generate or refine the chapter-by-chapter synopsis of the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): The prompt to guide the chapter synopsis generation.

    Returns:
        str: The generated or refined chapter synopsis.
    """
    console.print("[bold blue]Generating chapter-by-chapter synopsis...[/bold blue]")

    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()
    file_path = os.path.join(book_path, "outline", "chapter_synopsis.md")
    book_name = os.path.basename(book_path)

    # Check if the synopsis already exists and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing chapter synopsis...[/yellow]")
        content = CHAPTER_SYNOPSIS_PROMPT_REFINE.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )
    else:
        console.print(f"[yellow]Generating new chapter synopsis...[/yellow]")
        content = CHAPTER_SYNOPSIS_PROMPT_NEW.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )

    # Generate the chapter synopsis using the assistant
    chapter_synopsis_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path,
        "outline/chapter_synopsis.md",
        "Chapter Synopsis",
        chapter_synopsis_content,
    )
    console.print(
        "[bold green]✔ Chapter-by-chapter synopsis generated successfully[/bold green]"
    )

    update_agent_files(book_path, assistant)
    return chapter_synopsis_content
