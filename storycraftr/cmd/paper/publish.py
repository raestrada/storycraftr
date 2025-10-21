import os
import click
import subprocess  # nosec
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.utils.markdown import consolidate_paper_md
from storycraftr.agent.paper.references import generate_bibtex
import shutil
from rich.progress import Progress

console = Console()


@click.group()
def publish():
    """
    Publish the paper in various formats.

    This command group provides options to publish the paper,
    including generating a PDF version using pandoc and LaTeX.
    """
    pass


def find_executable(executable_name):
    """Find the full path of an executable."""
    return shutil.which(executable_name)


def check_dependencies():
    """Check if required dependencies are installed."""
    pandoc_path = find_executable("pandoc")
    if not pandoc_path:
        raise click.ClickException("pandoc is not installed. Please install it first.")

    xelatex_path = find_executable("xelatex")
    if not xelatex_path:
        raise click.ClickException("xelatex is not installed. Please install it first.")

    return pandoc_path, xelatex_path


def check_latex_packages():
    """Check if required LaTeX packages are installed."""
    kpsewhich_path = find_executable("kpsewhich")
    if not kpsewhich_path:
        raise click.ClickException(
            "kpsewhich is not installed. Please install it first."
        )

    latex_packages = {
        "book.cls": "book",
        "geometry.sty": "geometry",
        "fancyhdr.sty": "fancyhdr",
        "graphicx.sty": "graphicx",
        "hyperref.sty": "hyperref",
        "xcolor.sty": "xcolor",
        "titlesec.sty": "titlesec",
        "fontspec.sty": "fontspec",
        "polyglossia.sty": "polyglossia",
    }

    missing_packages = []
    for latex_file, package in latex_packages.items():
        try:
            result = subprocess.run(  # nosec
                [kpsewhich_path, latex_file], capture_output=True, text=True, check=True
            )
            if not result.stdout.strip():
                missing_packages.append(package)
        except subprocess.CalledProcessError:
            missing_packages.append(package)

    if missing_packages:
        raise click.ClickException(
            f"The following LaTeX packages are missing: {', '.join(missing_packages)}. "
            "Please install them using your LaTeX distribution's package manager."
        )


def generate_pdf(book_path, pandoc_path, xelatex_path):
    """Generate PDF from markdown files."""
    config = load_book_config(book_path)
    output_dir = Path(book_path) / "output"
    output_dir.mkdir(exist_ok=True)

    # Generate PDF using pandoc
    cmd = [
        pandoc_path,
        "--from=markdown",
        "--to=pdf",
        f"--output={output_dir / 'book.pdf'}",
        "--pdf-engine=xelatex",
        "--template=template.tex",
        "--variable=mainfont:DejaVu Serif",
        "--variable=monofont:DejaVu Sans Mono",
        "--variable=fontsize:12pt",
        "--variable=geometry:margin=1in",
        "--variable=colorlinks:true",
        "--variable=linkcolor:blue",
        "--variable=toccolor:blue",
        "--toc",
        "--toc-depth=3",
        "--number-sections",
        "--standalone",
    ]

    # Add input files
    cmd.extend(str(f) for f in Path(book_path).glob("**/*.md"))

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )  # nosec
        console.print("[bold green]PDF generated successfully![/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error generating PDF: {e.stderr}[/bold red]")
        raise click.ClickException("Failed to generate PDF")


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
    type=click.Path(),
    help="Path to a custom LaTeX template",
    required=False,
)
@click.option(
    "--book-path", type=click.Path(), help="Path to the paper directory", required=False
)
@click.option(
    "--bibtex-style",
    type=str,
    default="IEEEtran",
    help="BibTeX style to use (e.g., IEEEtran, plain, unsrt)",
)
def pdf(
    primary_language: str,
    translate: str = None,
    template: str = None,
    book_path: str = None,
    bibtex_style: str = "IEEEtran",
):
    """
    Publish the paper as a PDF using pandoc and LaTeX.

    Args:
        primary_language (str): The primary language of the paper.
        translate (str, optional): The language to translate the paper into before publishing.
        template (str, optional): Path to a custom LaTeX template.
        book_path (str, optional): Path to the paper directory.
        bibtex_style (str, optional): BibTeX style to use. Defaults to IEEEtran.
    """
    book_path = book_path or os.getcwd()

    # Load book configuration
    config = load_book_config(book_path)
    if not config:
        console.print(
            f"[red bold]Error:[/red bold] Paper configuration not found in {book_path}."
        )
        return

    try:
        # Check dependencies
        pandoc_path, xelatex_path = check_dependencies()

        # Check LaTeX packages
        check_latex_packages()

        # Generate PDF
        generate_pdf(book_path, pandoc_path, xelatex_path)

    except click.ClickException as e:
        console.print(f"[bold red]Error: {e.message}[/bold red]")
        raise
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")
        raise click.ClickException("Failed to publish book")
