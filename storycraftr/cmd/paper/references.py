import click
from rich.console import Console
from pathlib import Path

console = Console()


@click.group()
@click.option(
    "--book_path",
    type=click.Path(),
    required=True,
    help="Path to the paper project directory.",
)
def references(book_path):
    """
    Group of commands for managing references in the academic paper.
    """
    # Store the book_path as an attribute for future file operations
    references.book_path = Path(book_path)


@references.command()
@click.argument("reference_text", type=str)
@click.option(
    "--format",
    default="mixed",
    help="Format of the reference (default is mixed/unordered).",
)
def add_references(reference_text, format):
    """
    Placeholder for adding references to the project's bibliography file.
    In the future, this command will format and order references using OpenAI.

    Args:
        reference_text (str): The reference text in any format.
        format (str): The format of the reference; currently unused but defaults to 'mixed'.
    """
    console.print(
        "[yellow]The 'add_references' command is a placeholder and currently does nothing.[/yellow]"
    )
