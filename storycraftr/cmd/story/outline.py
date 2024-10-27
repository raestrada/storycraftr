import os
import click
from storycraftr.utils.core import load_book_config
from storycraftr.agent.story.outline import (
    generate_general_outline,
    generate_character_summary,
    generate_plot_points,
    generate_chapter_synopsis,
)
from rich.console import Console

console = Console()


@click.group()
def outline():
    """
    Manage outline aspects of the book.

    This command group provides functionality for generating general outlines,
    character summaries, plot points, and chapter-by-chapter synopses.
    """
    pass


@outline.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def general_outline(prompt: str, book_path: str = None):
    """
    Generate the general outline of the book.

    Args:
        prompt (str): The prompt to guide the generation of the outline.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Generating general outline for the book: {book_path}[/bold blue]"
    )
    generate_general_outline(book_path, prompt)


@outline.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def character_summary(prompt: str, book_path: str = None):
    """
    Generate the character summary of the book.

    Args:
        prompt (str): The prompt to guide the generation of the character summary.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Generating character summary for the book: {book_path}[/bold blue]"
    )
    generate_character_summary(book_path, prompt)


@outline.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def plot_points(prompt: str, book_path: str = None):
    """
    Generate the main plot points of the book.

    Args:
        prompt (str): The prompt to guide the generation of plot points.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Generating plot points for the book: {book_path}[/bold blue]"
    )
    generate_plot_points(book_path, prompt)


@outline.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def chapter_synopsis(prompt: str, book_path: str = None):
    """
    Generate the chapter-by-chapter synopsis of the book.

    Args:
        prompt (str): The prompt to guide the generation of the chapter synopsis.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Generating chapter synopsis for the book: {book_path}[/bold blue]"
    )
    generate_chapter_synopsis(book_path, prompt)
