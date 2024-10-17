import os
import click
from storycraftr.utils.core import load_book_config
from storycraftr.agent.worldbuilding import (
    generate_geography,
    generate_history,
    generate_culture,
    generate_magic_system,
    generate_technology,
)
from rich.console import Console

console = Console()


@click.group()
def worldbuilding():
    """Manage worldbuilding aspects of the book."""
    pass


@worldbuilding.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def geography(prompt, book_path=None):
    """Generate geography details for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_geography(book_path, prompt)


@worldbuilding.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def history(prompt, book_path=None):
    """Generate history details for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_history(book_path, prompt)


@worldbuilding.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def culture(prompt, book_path=None):
    """Generate culture details for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_culture(book_path, prompt)


@worldbuilding.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def magic_system(prompt, book_path=None):
    """Generate magic or science system details for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_magic_system(book_path, prompt)


@worldbuilding.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def technology(prompt, book_path=None):
    """Generate technology details for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_technology(book_path, prompt)
