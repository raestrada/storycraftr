import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.paper.outline_sections import (
    OUTLINE_SECTIONS_PROMPT_NEW,
    OUTLINE_SECTIONS_PROMPT_REFINE,
)

console = Console()

def generate_outline(book_path: str, prompt: str) -> str:
    """
    Generate or refine the paper outline.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the outline generation.

    Returns:
        str: The generated or refined outline.
    """
    console.print("[bold blue]Generating paper outline...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "outline.md")
    paper_title = config.book_name

    # Check if outline exists and choose appropriate prompt
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print("[yellow]Refining existing outline...[/yellow]")
        content = OUTLINE_SECTIONS_PROMPT_REFINE.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print("[yellow]Generating new outline...[/yellow]")
        content = OUTLINE_SECTIONS_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate outline using the assistant
    outline_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "sections/outline.md",
        "Paper Outline",
        outline_content
    )
    console.print("[bold green]✔ Paper outline generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return outline_content 