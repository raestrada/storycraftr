import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.define import define_core_question, define_contribution

console = Console()


@click.group()
def define():
    """
    Group of commands for defining core elements of an academic paper (e.g., research question, contribution).
    """
    # Store book_path in context for file operations if needed
    pass


@define.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("question", type=str)
def core_question(question: str, book_path: str = None):
    """
    Define the main research question or hypothesis of the paper.

    Args:
        question (str): The main research question or hypothesis.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Defining core research question for the paper: {book_path}[/bold blue]"
    )
    define_core_question(book_path, question)


@define.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", type=str)
def contribution(prompt: str, book_path: str = None):
    """
    Define the main contribution of the paper.

    Args:
        prompt (str): The prompt to guide the contribution definition.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Defining contribution for the paper: {book_path}[/bold blue]"
    )
    define_contribution(book_path, prompt)
