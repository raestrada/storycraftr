import os
import click
from storycraftr.utils.pdf import to_pdf
from storycraftr.utils.core import load_book_config
from rich.console import Console

console = Console()


@click.group()
def publish():
    """
    Publish the book in various formats.

    This command group provides options to publish the book,
    including generating a PDF version and other formats in the future.
    """
    pass


@publish.command()
@click.argument("primary_language", type=str)
@click.option(
    "--translate",
    type=str,
    default=None,
    help="Translate the book to this language before publishing.",
)
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
def pdf(primary_language: str, translate: str = None, book_path: str = None):
    """
    Publish the book as a PDF.

    Args:
        primary_language (str): The primary language of the book.
        translate (str, optional): The language to translate the book into before publishing.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Book configuration not found in {book_path}."
        )
        return

    # Log the start of the process
    console.print(f"Generating PDF for the book in [bold]{primary_language}[/bold]...")

    try:
        output_pdf_path = to_pdf(book_path, primary_language, translate)
        # Success log
        console.print(
            f"[green bold]Success![/green bold] PDF generated at: [bold]{output_pdf_path}[/bold]"
        )
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] Failed to generate PDF: {str(e)}") 