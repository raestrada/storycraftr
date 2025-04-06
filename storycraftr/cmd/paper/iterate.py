import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.iterate import reinforce_ideas, improve_clarity

console = Console()


@click.group()
def iterate():
    """
    Group of commands for iterative improvements to the paper.
    """
    pass


@iterate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def reinforce_ideas(prompt: str, book_path: str = None):
    """Strengthen core ideas and arguments throughout the paper."""
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    reinforce_ideas(book_path, prompt)


@iterate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def improve_clarity(prompt: str, book_path: str = None):
    """Enhance clarity and readability throughout the paper."""
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    improve_clarity(book_path, prompt)
