import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.references import (
    add_reference,
    format_references,
    check_citations,
    generate_citation,
    generate_bibtex,
)

console = Console()


@click.group()
def references():
    """
    Group of commands for managing references and citations in the paper.
    """
    pass


@references.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.argument("reference_info", type=str)
def add(reference_info: str, book_path: str = None):
    """
    Add a new reference to the paper.
    Uses OpenAI to format and add the reference in the proper style.

    Args:
        reference_info (str): The reference information to add.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    add_reference(book_path, reference_info)


@references.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.argument("style_guide", type=str)
def format(style_guide: str, book_path: str = None):
    """
    Format all references according to the specified style guide.
    Uses OpenAI to ensure consistent formatting across all references.

    Args:
        style_guide (str): The style guide to follow (e.g., APA, IEEE).
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    format_references(book_path, style_guide)


@references.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.argument("prompt", type=str)
def check(prompt: str, book_path: str = None):
    """
    Check citations throughout the paper.
    Uses OpenAI to verify citation accuracy and consistency.

    Args:
        prompt (str): Additional instructions for citation checking.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    check_citations(book_path, prompt)


@references.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.option(
    "--format",
    "citation_format",
    default="APA",
    help="Citation format to use (e.g., APA, IEEE)",
)
@click.argument("reference_info", type=str)
def cite(reference_info: str, citation_format: str, book_path: str = None):
    """
    Generate a citation for a reference.
    Uses OpenAI to create properly formatted citations.

    Args:
        reference_info (str): The reference information to cite.
        citation_format (str): The desired citation format.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_citation(book_path, reference_info, citation_format)


@references.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.option(
    "--style",
    "bibtex_style",
    default="IEEEtran",
    help="BibTeX style to use (e.g., IEEEtran, plain, unsrt)",
)
def bibtex(bibtex_style: str, book_path: str = None):
    """
    Generate BibTeX references file for the paper.
    Uses OpenAI to format references in proper BibTeX format.

    Args:
        bibtex_style (str): The BibTeX style to use.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_bibtex(book_path, bibtex_style)
