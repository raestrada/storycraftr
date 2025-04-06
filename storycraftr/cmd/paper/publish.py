import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.generate_pdf import generate_pdf_file

console = Console()


@click.group()
def publish():
    """
    Publish the paper in various formats.

    This command group provides options to publish the paper,
    including generating a PDF version and other formats in the future.
    """
    pass


@publish.command()
@click.argument("primary_language", type=str)
@click.option(
    "--translate",
    type=str,
    default=None,
    help="Translate the paper to this language before publishing.",
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
@click.option("--book-path", type=click.Path(), help="Path to the paper directory")
def pdf(primary_language: str, translate: str = None, template: str = "ieee", output: str = None, book_path: str = None):
    """
    Publish the paper as a PDF using AI-generated LaTeX.

    Args:
        primary_language (str): The primary language of the paper.
        translate (str, optional): The language to translate the paper into before publishing.
        template (str, optional): The LaTeX template to use. Defaults to "ieee".
        output (str, optional): The name of the output PDF file.
        book_path (str, optional): The path to the paper's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Paper configuration not found in {book_path}."
        )
        return

    # Set default output name if not provided
    if output is None:
        output = f"{Path(book_path).name}.pdf"
    
    # Log the start of the process
    console.print(f"Generating PDF for the paper in [bold]{primary_language}[/bold] using template [bold]{template}[/bold]...")
    
    try:
        # If translation is requested, we'll handle it in the future
        # For now, we just use the primary language
        generate_pdf_file(book_path, primary_language, template, output)
        # Success log is handled inside generate_pdf_file
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] Failed to generate PDF: {str(e)}")
        return 