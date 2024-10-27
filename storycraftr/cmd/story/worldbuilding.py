import os
import click
from storycraftr.utils.core import load_book_config
from storycraftr.agent.story.worldbuilding import (
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
    """
    Manage worldbuilding aspects of the book.

    This command group provides options to generate various aspects of worldbuilding
    such as geography, history, culture, magic systems, and technology.
    """
    pass


@worldbuilding.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def geography(prompt: str, book_path: str = None):
    """
    Generate geography details for the book.

    Args:
        prompt (str): The prompt to guide the generation of geography.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Could not load book configuration from {book_path}."
        )
        return

    console.print(
        f"[bold blue]Generating geography details for the book at: {book_path}[/bold blue]"
    )
    generate_geography(book_path, prompt)


@worldbuilding.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def history(prompt: str, book_path: str = None):
    """
    Generate history details for the book.

    Args:
        prompt (str): The prompt to guide the generation of history.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Could not load book configuration from {book_path}."
        )
        return

    console.print(
        f"[bold blue]Generating history details for the book at: {book_path}[/bold blue]"
    )
    generate_history(book_path, prompt)


@worldbuilding.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def culture(prompt: str, book_path: str = None):
    """
    Generate culture details for the book.

    Args:
        prompt (str): The prompt to guide the generation of culture.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Could not load book configuration from {book_path}."
        )
        return

    console.print(
        f"[bold blue]Generating culture details for the book at: {book_path}[/bold blue]"
    )
    generate_culture(book_path, prompt)


@worldbuilding.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def magic_system(prompt: str, book_path: str = None):
    """
    Generate magic or science system details for the book.

    Args:
        prompt (str): The prompt to guide the generation of the magic/science system.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Could not load book configuration from {book_path}."
        )
        return

    console.print(
        f"[bold blue]Generating magic system details for the book at: {book_path}[/bold blue]"
    )
    generate_magic_system(book_path, prompt)


@worldbuilding.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def technology(prompt: str, book_path: str = None):
    """
    Generate technology details for the book.

    Args:
        prompt (str): The prompt to guide the generation of technology.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Could not load book configuration from {book_path}."
        )
        return

    console.print(
        f"[bold blue]Generating technology details for the book at: {book_path}[/bold blue]"
    )
    generate_technology(book_path, prompt)
