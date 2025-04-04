import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.generate_bibliography import generate_bibliography_file

console = Console()

@click.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.option(
    "--format",
    default="bibtex",
    help="Bibliography format (bibtex, biblatex, etc.)"
)
@click.option(
    "--output",
    default="references.bib",
    help="Output file name"
)
def generate_bibliography(book_path: str = None, format: str = "bibtex", output: str = "references.bib"):
    """
    Generate bibliography file in the specified format.
    """
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    
    generate_bibliography_file(book_path, format, output)
