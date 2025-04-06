import os
from pathlib import Path
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.core import load_book_config, file_has_more_than_three_lines
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.story.worldbuilding import (
    GEOGRAPHY_PROMPT_NEW,
    GEOGRAPHY_PROMPT_REFINE,
    HISTORY_PROMPT_NEW,
    HISTORY_PROMPT_REFINE,
    CULTURE_PROMPT_NEW,
    CULTURE_PROMPT_REFINE,
    MAGIC_SYSTEM_PROMPT_NEW,
    MAGIC_SYSTEM_PROMPT_REFINE,
    TECHNOLOGY_PROMPT_NEW,
    TECHNOLOGY_PROMPT_REFINE,
)
from rich.console import Console

console = Console()


def generate_geography(book_path: str, prompt: str) -> str:
    """
    Generate the geography details for the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): Prompt to guide geography generation.

    Returns:
        str: Generated or refined geography content.
    """
    console.print("[bold blue]Generating geography...[/bold blue]")
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "worldbuilding" / "geography.md"

    # Refining or generating new geography content
    if file_path.exists() and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing geography found at {file_path}. Refining...[/yellow]"
        )
        content = GEOGRAPHY_PROMPT_REFINE.format(prompt=prompt, language=language)
    else:
        console.print(
            "[yellow]No existing geography found. Generating new content...[/yellow]"
        )
        content = GEOGRAPHY_PROMPT_NEW.format(prompt=prompt, language=language)

    geography_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save content and update agent files
    save_to_markdown(
        book_path, "worldbuilding/geography.md", "Geography", geography_content
    )
    console.print("[bold green]✔ Geography generated successfully[/bold green]")
    update_agent_files(book_path, assistant)

    return geography_content


def generate_history(book_path: str, prompt: str) -> str:
    """
    Generate the history details for the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): Prompt to guide history generation.

    Returns:
        str: Generated or refined history content.
    """
    console.print("[bold blue]Generating history...[/bold blue]")
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "worldbuilding" / "history.md"

    # Refining or generating new history content
    if file_path.exists() and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing history found at {file_path}. Refining...[/yellow]"
        )
        content = HISTORY_PROMPT_REFINE.format(prompt=prompt, language=language)
    else:
        console.print(
            "[yellow]No existing history found. Generating new content...[/yellow]"
        )
        content = HISTORY_PROMPT_NEW.format(prompt=prompt, language=language)

    history_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save content and update agent files
    save_to_markdown(book_path, "worldbuilding/history.md", "History", history_content)
    console.print("[bold green]✔ History generated successfully[/bold green]")
    update_agent_files(book_path, assistant)

    return history_content


def generate_culture(book_path: str, prompt: str) -> str:
    """
    Generate the culture details for the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): Prompt to guide culture generation.

    Returns:
        str: Generated or refined culture content.
    """
    console.print("[bold blue]Generating culture...[/bold blue]")
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "worldbuilding" / "culture.md"

    # Refining or generating new culture content
    if file_path.exists() and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing culture found at {file_path}. Refining...[/yellow]"
        )
        content = CULTURE_PROMPT_REFINE.format(prompt=prompt, language=language)
    else:
        console.print(
            "[yellow]No existing culture found. Generating new content...[/yellow]"
        )
        content = CULTURE_PROMPT_NEW.format(prompt=prompt, language=language)

    culture_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save content and update agent files
    save_to_markdown(book_path, "worldbuilding/culture.md", "Culture", culture_content)
    console.print("[bold green]✔ Culture generated successfully[/bold green]")
    update_agent_files(book_path, assistant)

    return culture_content


def generate_magic_system(book_path: str, prompt: str) -> str:
    """
    Generate the magic/science system for the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): Prompt to guide magic/science system generation.

    Returns:
        str: Generated or refined magic/science system content.
    """
    console.print("[bold blue]Generating magic/science system...[/bold blue]")
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "worldbuilding" / "magic_system.md"

    # Refining or generating new magic/science system content
    if file_path.exists() and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing magic/science system found at {file_path}. Refining...[/yellow]"
        )
        content = MAGIC_SYSTEM_PROMPT_REFINE.format(prompt=prompt, language=language)
    else:
        console.print(
            "[yellow]No existing magic/science system found. Generating new content...[/yellow]"
        )
        content = MAGIC_SYSTEM_PROMPT_NEW.format(prompt=prompt, language=language)

    magic_system_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save content and update agent files
    save_to_markdown(
        book_path,
        "worldbuilding/magic_system.md",
        "Magic/Science System",
        magic_system_content,
    )
    console.print(
        "[bold green]✔ Magic/Science system generated successfully[/bold green]"
    )
    update_agent_files(book_path, assistant)

    return magic_system_content


def generate_technology(book_path: str, prompt: str) -> str:
    """
    Generate the technology details for the book.

    Args:
        book_path (str): Path to the book's directory.
        prompt (str): Prompt to guide technology generation.

    Returns:
        str: Generated or refined technology content.
    """
    console.print("[bold blue]Generating technology...[/bold blue]")
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    file_path = Path(book_path) / "worldbuilding" / "technology.md"

    # Refining or generating new technology content
    if file_path.exists() and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing technology found at {file_path}. Refining...[/yellow]"
        )
        content = TECHNOLOGY_PROMPT_REFINE.format(prompt=prompt, language=language)
    else:
        console.print(
            "[yellow]No existing technology found. Generating new content...[/yellow]"
        )
        content = TECHNOLOGY_PROMPT_NEW.format(prompt=prompt, language=language)

    technology_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=str(file_path),
    )

    # Save content and update agent files
    save_to_markdown(
        book_path, "worldbuilding/technology.md", "Technology", technology_content
    )
    console.print("[bold green]✔ Technology generated successfully[/bold green]")
    update_agent_files(book_path, assistant)

    return technology_content
