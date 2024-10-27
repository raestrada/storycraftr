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
def define(book_path):
    """
    Group of commands for defining core elements of an academic paper (e.g., research question, contribution).
    """
    # Store book_path in context for file operations if needed
    define.book_path = Path(book_path)


@define.command()
@click.argument("question", type=str)
def core_question(question):
    """
    Define the main research question or hypothesis of the paper.

    Args:
        question (str): The main research question or hypothesis.
    """
    console.print(f"[green]Core Research Question defined:[/green] {question}")
    # This command currently acts as a placeholder; no actual storage is implemented yet.


@define.command()
@click.argument("contribution", type=str)
def contribution(contribution):
    """
    Define the main contribution or novelty of the paper.

    Args:
        contribution (str): The unique contribution or impact that the paper aims to bring to the field.
    """
    console.print(f"[green]Main Contribution defined:[/green] {contribution}")
    # This command currently acts as a placeholder; no actual storage is implemented yet.
