import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.outline_sections import generate_outline

console = Console()


@click.group()
def outline():
    """
    Group of commands for outlining the paper.
    """
    pass


@outline.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def outline_sections(prompt: str, book_path: str = None):
    """
    Generate or refine the paper's outline.
    Uses OpenAI to create a structured outline with all necessary sections.

    Args:
        prompt (str): Instructions to guide the outline generation.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_outline(book_path, prompt)
