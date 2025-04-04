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
from storycraftr.prompts.paper.finalize import (
    CHECK_CONSISTENCY_PROMPT,
    FINALIZE_FORMAT_PROMPT,
    GENERATE_ABSTRACT_PROMPT_NEW,
    GENERATE_ABSTRACT_PROMPT_REFINE,
)

console = Console()

def check_paper_consistency(book_path: str, prompt: str) -> str:
    """
    Check the consistency across all sections of the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the consistency check.

    Returns:
        str: The consistency check report.
    """
    console.print("[bold blue]Checking paper consistency...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "reviews", "consistency_check.md")
    paper_title = config.book_name

    # Generate consistency check using the assistant
    content = CHECK_CONSISTENCY_PROMPT.format(
        prompt=prompt,
        paper_title=paper_title
    )

    consistency_report = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "reviews/consistency_check.md",
        "Consistency Check Report",
        consistency_report
    )
    console.print("[bold green]✔ Consistency check completed successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return consistency_report

def finalize_paper_format(book_path: str, prompt: str) -> str:
    """
    Finalize the formatting of the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the formatting.

    Returns:
        str: The formatting report.
    """
    console.print("[bold blue]Finalizing paper format...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "reviews", "formatting_report.md")
    paper_title = config.book_name

    # Generate formatting report using the assistant
    content = FINALIZE_FORMAT_PROMPT.format(
        prompt=prompt,
        paper_title=paper_title
    )

    formatting_report = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path
    )

    # Save the result
    save_to_markdown(
        book_path,
        "reviews/formatting_report.md",
        "Formatting Report",
        formatting_report
    )
    console.print("[bold green]✔ Formatting report completed successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return formatting_report

def generate_abstract(book_path: str, prompt: str) -> str:
    """
    Generate or refine the abstract of the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the abstract generation.

    Returns:
        str: The generated abstract.
    """
    console.print("[bold blue]Generating abstract...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "abstracts", "abstract.md")
    paper_title = config.book_name

    # Check if abstract already exists
    abstract_exists = os.path.exists(file_path)
    
    # Choose appropriate prompt based on whether abstract exists
    if abstract_exists:
        content = GENERATE_ABSTRACT_PROMPT_REFINE.format(
            prompt=prompt
        )
    else:
        content = GENERATE_ABSTRACT_PROMPT_NEW.format(
            prompt=prompt,
            paper_title=paper_title
        )

    # Generate abstract using the assistant
    abstract_text = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path if abstract_exists else None
    )

    # Save the result
    save_to_markdown(
        book_path,
        "abstracts/abstract.md",
        "Abstract",
        abstract_text
    )
    console.print("[bold green]✔ Abstract generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return abstract_text 