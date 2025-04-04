import os
from storycraftr.utils.core import load_book_config, file_has_more_than_three_lines
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.paper.define import (
    CORE_QUESTION_PROMPT_NEW,
    CORE_QUESTION_PROMPT_REFINE,
    CONTRIBUTION_PROMPT_NEW,
    CONTRIBUTION_PROMPT_REFINE,
)
from rich.console import Console

console = Console()


def define_core_question(book_path: str, question: str) -> str:
    """
    Define or refine the core research question or hypothesis of the paper.

    Args:
        book_path (str): Path to the book's directory.
        question (str): The research question or hypothesis.

    Returns:
        str: The defined or refined research question.
    """
    console.print("[bold blue]Defining core research question...[/bold blue]")

    # Load the book configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "core_question.md")
    paper_title = config.book_name

    # Check if the core question already exists and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing core research question...[/yellow]")
        content = CORE_QUESTION_PROMPT_REFINE.format(
            question=question, language=config.primary_language, paper_title=paper_title
        )
    else:
        console.print(f"[yellow]Generating new core research question...[/yellow]")
        content = CORE_QUESTION_PROMPT_NEW.format(
            question=question, language=config.primary_language, paper_title=paper_title
        )

    # Generate the core research question using the assistant
    core_question_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path,
        "sections/core_question.md",
        "Core Research Question",
        core_question_content,
    )
    console.print(
        "[bold green]✔ Core research question defined successfully[/bold green]"
    )

    update_agent_files(book_path, assistant)
    return core_question_content


def define_contribution(book_path: str, prompt: str) -> str:
    """
    Define or refine the main contribution of the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The prompt to guide the contribution definition.

    Returns:
        str: The generated or refined contribution statement.
    """
    console.print("[bold blue]Defining contribution of the paper...[/bold blue]")

    # Load the book configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "sections", "contribution.md")
    book_name = config.book_name

    # Check if the contribution statement already exists and choose the appropriate prompt
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(f"[yellow]Refining existing contribution...[/yellow]")
        content = CONTRIBUTION_PROMPT_REFINE.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )
    else:
        console.print(f"[yellow]Generating new contribution...[/yellow]")
        content = CONTRIBUTION_PROMPT_NEW.format(
            prompt=prompt, language=config.primary_language, book_name=book_name
        )

    # Generate the contribution using the assistant
    contribution_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the result to a markdown file
    save_to_markdown(
        book_path,
        "sections/contribution.md",
        "Contribution",
        contribution_content,
    )
    console.print("[bold green]✔ Contribution defined successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return contribution_content
