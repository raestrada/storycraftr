import os
import click
from storycraftr.utils.pdf import to_pdf
from storycraftr.utils.core import load_book_config
from rich.console import Console
from rich.progress import track

console = Console()


@click.group()
def publish():
    """Publish the book in various formats."""
    pass


@publish.command()
@click.argument("primary_language")
@click.option(
    "--translate",
    type=str,
    default=None,
    help="Translate the book to this language before publishing",
)
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
def pdf(primary_language, translate=None, book_path=None):
    """Publish the book as a PDF."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        console.print(
            f"[red bold]Error:[/red bold] Book configuration not found in {book_path}."
        )
        return None

    # Log the start of the process
    console.print(
        f"Generating PDF for the book in [bold]{primary_language}[/bold] language..."
    )

    output_pdf_path = to_pdf(book_path, primary_language, translate)

    # Success log
    console.print(
        f"[green bold]Success![/green bold] PDF generated at: [bold]{output_pdf_path}[/bold]"
    )
