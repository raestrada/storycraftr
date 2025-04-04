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
from storycraftr.prompts.paper.organize_lit import (
    LIT_SUMMARY_PROMPT_NEW,
    LIT_SUMMARY_PROMPT_REFINE,
    CONCEPT_MAP_PROMPT_NEW,
    CONCEPT_MAP_PROMPT_REFINE,
)

console = Console()

def generate_lit_summary(book_path: str, prompt: str) -> str:
    """
    Generate or refine a literature summary for the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the literature summary generation.

    Returns:
        str: The generated or refined literature summary.
    """
    console.print("[bold blue]Generating literature summary...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "literature_summary.md")
    paper_title = config.book_name

    # Check if literature summary exists and choose appropriate prompt
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print("[yellow]Refining existing literature summary...[/yellow]")
        content = LIT_SUMMARY_PROMPT_REFINE.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print("[yellow]Generating new literature summary...[/yellow]")
        content = LIT_SUMMARY_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate literature summary using the assistant
    lit_summary_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "sections/literature_summary.md",
        "Literature Summary",
        lit_summary_content
    )
    console.print("[bold green]✔ Literature summary generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return lit_summary_content

def generate_concept_map(book_path: str, prompt: str) -> str:
    """
    Generate or refine a concept map for the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the concept map generation.

    Returns:
        str: The generated or refined concept map.
    """
    console.print("[bold blue]Generating concept map...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "concept_map.md")
    paper_title = config.book_name

    # Check if concept map exists and choose appropriate prompt
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        console.print("[yellow]Refining existing concept map...[/yellow]")
        content = CONCEPT_MAP_PROMPT_REFINE.format(
            prompt=prompt,
            paper_title=paper_title
        )
    else:
        console.print("[yellow]Generating new concept map...[/yellow]")
        content = CONCEPT_MAP_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate concept map using the assistant
    concept_map_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "sections/concept_map.md",
        "Concept Map",
        concept_map_content
    )
    console.print("[bold green]✔ Concept map generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return concept_map_content 