import os
import click
from storycraftr.utils.core import load_book_config
from storycraftr.agent.chapters import (
    generate_chapter,
    generate_cover,
    generate_back_cover,
    generate_epilogue,
)
from rich.console import Console

console = Console()


@click.group()
def chapters():
    """Manage chapters of the book."""
    pass


@chapters.command()
@click.argument("chapter_number", type=int)
@click.argument("prompt")
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
def chapter(chapter_number, prompt, book_path=None):
    """Generate a new chapter for the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_chapter(book_path, chapter_number, prompt)


@chapters.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def cover(prompt, book_path=None):
    """Generate the cover of the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_cover(book_path, prompt)


@chapters.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def back_cover(prompt, book_path=None):
    """Generate the back cover of the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_back_cover(book_path, prompt)


@chapters.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def epilogue(prompt, book_path=None):
    """Generate the epilogue of the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_epilogue(book_path, prompt)
