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
from storycraftr.prompts.paper.references import (
    ADD_REFERENCE_PROMPT,
    FORMAT_REFERENCES_PROMPT,
    CHECK_CITATIONS_PROMPT,
    GENERATE_CITATION_PROMPT,
    GENERATE_BIBTEX_PROMPT,
)

console = Console()


def add_reference(book_path: str, prompt: str) -> str:
    """
    Format and add a new reference.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The reference information to format and add.

    Returns:
        str: The formatted reference.
    """
    console.print("[bold blue]Formatting and adding reference...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "references", "references.md")
    paper_title = config.book_name

    # Generate formatted reference using the assistant
    content = ADD_REFERENCE_PROMPT.format(prompt=prompt, paper_title=paper_title)

    reference_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Append to references file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n{reference_content}\n")

    console.print("[bold green]✔ Reference added successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return reference_content


def format_references(book_path: str, prompt: str) -> str:
    """
    Format all references according to specified style.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The style guide to follow.

    Returns:
        str: The formatted reference list.
    """
    console.print("[bold blue]Formatting references...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "references", "references.md")
    paper_title = config.book_name

    # Generate formatted references using the assistant
    content = FORMAT_REFERENCES_PROMPT.format(prompt=prompt, paper_title=paper_title)

    formatted_references = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the formatted references
    save_to_markdown(
        book_path, "references/references.md", "References", formatted_references
    )
    console.print("[bold green]✔ References formatted successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return formatted_references


def check_citations(book_path: str, prompt: str) -> str:
    """
    Check citations throughout the paper.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): Additional instructions for citation checking.

    Returns:
        str: The citation check report.
    """
    console.print("[bold blue]Checking citations...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "reviews", "citation_check.md")
    paper_title = config.book_name

    # Generate citation check report using the assistant
    content = CHECK_CITATIONS_PROMPT.format(prompt=prompt, paper_title=paper_title)

    citation_report = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the citation check report
    save_to_markdown(
        book_path, "reviews/citation_check.md", "Citation Check Report", citation_report
    )
    console.print("[bold green]✔ Citations checked successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return citation_report


def generate_citation(book_path: str, prompt: str, citation_format: str) -> str:
    """
    Generate a citation in the specified format.

    Args:
        book_path (str): Path to the paper's directory.
        prompt (str): The reference information to cite.
        citation_format (str): The format in which to generate the citation.

    Returns:
        str: The generated citation.
    """
    console.print("[bold blue]Generating citation...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "references", "references.md")
    paper_title = config.book_name

    # Generate citation using the assistant
    content = GENERATE_CITATION_PROMPT.format(
        prompt=prompt, paper_title=paper_title, citation_format=citation_format
    )

    citation_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Append to references file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n{citation_content}\n")

    console.print("[bold green]✔ Citation generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return citation_content


def generate_bibtex(book_path: str, bibtex_style: str) -> str:
    """
    Generate BibTeX references file for the paper.

    Args:
        book_path (str): Path to the paper's directory.
        bibtex_style (str): The BibTeX style to use.

    Returns:
        str: The generated BibTeX content.
    """
    console.print("[bold blue]Generating BibTeX references...[/bold blue]")

    # Load configuration and setup
    config = load_book_config(book_path)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)
    file_path = os.path.join(book_path, "references", "references.bib")
    paper_title = config.book_name

    # Generate BibTeX references using the assistant
    content = GENERATE_BIBTEX_PROMPT.format(
        paper_title=paper_title, bibtex_style=bibtex_style
    )

    bibtex_content = create_message(
        book_path,
        thread_id=thread.id,
        content=content,
        assistant=assistant,
        file_path=file_path,
    )

    # Save the BibTeX content
    save_to_markdown(
        book_path, "references/references.bib", "BibTeX References", bibtex_content
    )
    console.print("[bold green]✔ BibTeX references generated successfully[/bold green]")

    update_agent_files(book_path, assistant)
    return bibtex_content
