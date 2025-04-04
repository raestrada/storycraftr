import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.generate_pdf import generate_pdf_file

console = Console()

@click.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.option(
    "--language",
    default="en",
    help="Output language (en, es)"
)
@click.option(
    "--template",
    default="ieee",
    help="LaTeX template to use"
)
@click.option(
    "--output",
    help="Output PDF file name"
)
def generate_pdf(book_path: str = None, language: str = "en", template: str = "ieee", output: str = None):
    """
    Generate PDF file in the specified language using LaTeX.
    """
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    
    generate_pdf_file(book_path, language, template, output)
