import os
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
    update_agent_files,
)
from storycraftr.utils.core import load_book_config, file_has_more_than_three_lines
from storycraftr.utils.markdown import save_to_markdown
from storycraftr.prompts.worldbuilding import (
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


# Function to generate the geography of the world
def generate_geography(book_path, prompt):
    """Generate the geography details for the book."""
    console.print("[bold blue]Generating geography...[/bold blue]")  # Progress message
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # File path for the geography details
    file_path = os.path.join(book_path, "worldbuilding", "geography.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing geography found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = GEOGRAPHY_PROMPT_REFINE.format(prompt=prompt, language=language)
        geography_content = create_message(
            book_path,
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing geography found. Generating new content...[/yellow]"
        )  # Progress message
        content = GEOGRAPHY_PROMPT_NEW.format(prompt=prompt, language=language)
        geography_content = create_message(
            book_path, thread_id=thread.id, content=content, assistant=assistant
        )

    # Save to markdown
    save_to_markdown(
        book_path, "worldbuilding/geography.md", "Geography", geography_content
    )
    console.print(
        "[bold green]✔ Geography generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_path, assistant)
    return geography_content


# Function to generate the history of the world
def generate_history(book_path, prompt):
    """Generate the history details for the book."""
    console.print("[bold blue]Generating history...[/bold blue]")  # Progress message
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # File path for the history details
    file_path = os.path.join(book_path, "worldbuilding", "history.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing history found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = HISTORY_PROMPT_REFINE.format(prompt=prompt, language=language)
        history_content = create_message(
            book_path,
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing history found. Generating new content...[/yellow]"
        )  # Progress message
        content = HISTORY_PROMPT_NEW.format(prompt=prompt, language=language)
        history_content = create_message(
            book_path, thread_id=thread.id, content=content, assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_path, "worldbuilding/history.md", "History", history_content)
    console.print(
        "[bold green]✔ History generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_path, assistant)
    return history_content


# Function to generate the culture of the world
def generate_culture(book_path, prompt):
    """Generate the culture details for the book."""
    console.print("[bold blue]Generating culture...[/bold blue]")  # Progress message
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # File path for the culture details
    file_path = os.path.join(book_path, "worldbuilding", "culture.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing culture found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = CULTURE_PROMPT_REFINE.format(prompt=prompt, language=language)
        culture_content = create_message(
            book_path,
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing culture found. Generating new content...[/yellow]"
        )  # Progress message
        content = CULTURE_PROMPT_NEW.format(prompt=prompt, language=language)
        culture_content = create_message(
            book_path, thread_id=thread.id, content=content, assistant=assistant
        )

    # Save to markdown
    save_to_markdown(book_path, "worldbuilding/culture.md", "Culture", culture_content)
    console.print(
        "[bold green]✔ Culture generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_path, assistant)
    return culture_content


# Function to generate the magic or science system of the world
def generate_magic_system(book_path, prompt):
    """Generate the magic/science system for the book."""
    console.print(
        "[bold blue]Generating magic/science system...[/bold blue]"
    )  # Progress message
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # File path for the magic system
    file_path = os.path.join(book_path, "worldbuilding", "magic_system.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing magic/science system found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = MAGIC_SYSTEM_PROMPT_REFINE.format(prompt=prompt, language=language)
        magic_system_content = create_message(
            book_path,
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing magic/science system found. Generating new content...[/yellow]"
        )  # Progress message
        content = MAGIC_SYSTEM_PROMPT_NEW.format(prompt=prompt, language=language)
        magic_system_content = create_message(
            book_path, thread_id=thread.id, content=content, assistant=assistant
        )

    # Save to markdown
    save_to_markdown(
        book_path,
        "worldbuilding/magic_system.md",
        "Magic/Science System",
        magic_system_content,
    )
    console.print(
        "[bold green]✔ Magic/Science system generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_path, assistant)
    return magic_system_content


# Function to generate the technology of the world (if applicable)
def generate_technology(book_path, prompt):
    """Generate the technology details for the book."""
    console.print("[bold blue]Generating technology...[/bold blue]")  # Progress message
    language = load_book_config(book_path).primary_language
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    # File path for the technology details
    file_path = os.path.join(book_path, "worldbuilding", "technology.md")

    # Check if the file exists and pass it as an attachment
    if os.path.exists(file_path) and file_has_more_than_three_lines(file_path):
        console.print(
            f"[yellow]Existing technology file found at {file_path}. Attaching for further refinement...[/yellow]"
        )  # Progress message
        content = TECHNOLOGY_PROMPT_REFINE.format(prompt=prompt, language=language)
        technology_content = create_message(
            book_path,
            thread_id=thread.id,
            content=content,
            assistant=assistant,
            file_path=file_path,
        )
    else:
        console.print(
            "[yellow]No existing technology found. Generating new content...[/yellow]"
        )  # Progress message
        content = TECHNOLOGY_PROMPT_NEW.format(prompt=prompt, language=language)
        technology_content = create_message(
            book_path, thread_id=thread.id, content=content, assistant=assistant
        )

    # Save to markdown
    save_to_markdown(
        book_path, "worldbuilding/technology.md", "Technology", technology_content
    )
    console.print(
        "[bold green]✔ Technology generated successfully[/bold green]"
    )  # Success message
    update_agent_files(book_path, assistant)
    return technology_content
