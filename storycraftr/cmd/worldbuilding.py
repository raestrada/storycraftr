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
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def geography(prompt, book_name=None):
    """Generate geography details for the book."""
    if not book_name:
        book_name = os.getcwd()

    if not load_book_config(book_name):
        return None

    generate_geography(book_name, prompt)


@worldbuilding.command()
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def history(prompt, book_name=None):
    """Generate history details for the book."""
    if not book_name:
        book_name = os.getcwd()

    if not load_book_config(book_name):
        return None

    generate_history(book_name, prompt)


@worldbuilding.command()
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def culture(prompt, book_name=None):
    """Generate culture details for the book."""
    if not book_name:
        book_name = os.getcwd()

    if not load_book_config(book_name):
        return None

    generate_culture(book_name, prompt)


@worldbuilding.command()
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def magic_system(prompt, book_name=None):
    """Generate magic or science system details for the book."""
    if not book_name:
        book_name = os.getcwd()

    if not load_book_config(book_name):
        return None

    generate_magic_system(book_name, prompt)


@worldbuilding.command()
@click.option("--book-name", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def technology(prompt, book_name=None):
    """Generate technology details for the book."""
    if not book_name:
        book_name = os.getcwd()

    if not load_book_config(book_name):
        return None

    generate_technology(book_name, prompt)
