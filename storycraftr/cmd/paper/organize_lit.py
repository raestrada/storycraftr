import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.organize_lit import generate_lit_summary

console = Console()


@click.group()
def organize_lit():
    """
    Group of commands for organizing literature for the paper.
    """
    pass


@organize_lit.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.argument("prompt", type=str)
def lit_summary(prompt: str, book_path: str = None):
    """
    Generate or refine a summary of key literature.
    Uses OpenAI to analyze and summarize major sources and identify research gaps.

    Args:
        prompt (str): Instructions to guide the literature summary generation.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_lit_summary(book_path, prompt)
