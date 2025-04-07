import os
import click
import subprocess
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.utils.markdown import consolidate_paper_md
from storycraftr.agent.agents import create_or_get_assistant, get_thread, create_message

console = Console()


@click.group()
def publish():
    """
    Publish the paper in various formats.

    This command group provides options to publish the paper,
    including generating a PDF version using pandoc and LaTeX.
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
    type=click.Path(),
    help="Path to a custom LaTeX template",
    required=False
)
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
def pdf(primary_language: str, translate: str = None, template: str = None, book_path: str = None):
    """
    Publish the paper as a PDF using pandoc and LaTeX.

    Args:
        primary_language (str): The primary language of the paper.
        translate (str, optional): The language to translate the paper into before publishing.
        template (str, optional): Path to a custom LaTeX template.
        book_path (str, optional): Path to the paper directory.
    """
    book_path = book_path or os.getcwd()

    # Load book configuration
    config = load_book_config(book_path)
    if not config:
        console.print(
            f"[red bold]Error:[/red bold] Paper configuration not found in {book_path}."
        )
        return

    # Check if pandoc is installed
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print(
            "[red bold]Error:[/red bold] Pandoc is not installed. Please install it first."
        )
        return

    # Check if xelatex is installed
    try:
        subprocess.run(["xelatex", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print(
            "[red bold]Error:[/red bold] xelatex is not installed. Please install texlive-xetex first:"
        )
        console.print("\nFor Ubuntu/Debian:")
        console.print("sudo apt-get install texlive-xetex")
        console.print("\nFor macOS:")
        console.print("brew install --cask mactex")
        console.print("\nFor Windows:")
        console.print("Please install MiKTeX from https://miktex.org/download")
        return

    # Log the start of the process
    if translate:
        console.print(f"[bold blue]Generating PDF for the paper in [bold]{primary_language}[/bold] and translating to [bold]{translate}[/bold]...[/bold blue]")
    else:
        console.print(f"[bold blue]Generating PDF for the paper in [bold]{primary_language}[/bold]...[/bold blue]")

    try:
        # Verificar dependencias de LaTeX
        latex_packages = {
            "IEEEtran.cls": "texlive-publishers",
            "algorithm.sty": "texlive-science",
            "algorithmic.sty": "texlive-science",
            "booktabs.sty": "texlive-latex-extra",
            "multirow.sty": "texlive-latex-extra"
        }
        
        missing_packages = []
        for latex_file, package in latex_packages.items():
            result = subprocess.run(["kpsewhich", latex_file], capture_output=True, text=True)
            if not result.stdout.strip():
                missing_packages.append((latex_file, package))
        
        if missing_packages:
            console.print("[red]Error: Missing LaTeX packages[/red]")
            console.print("\nThe following LaTeX packages are required but not installed:")
            for latex_file, package in missing_packages:
                console.print(f"- {latex_file} (from package {package})")
            console.print("\nPlease install them using your package manager:")
            console.print("\nFor Ubuntu/Debian:")
            console.print("sudo apt-get install " + " ".join(set(p[1] for p in missing_packages)))
            console.print("\nFor macOS:")
            console.print("brew install --cask mactex")
            console.print("\nFor Windows:")
            console.print("Please install MiKTeX from https://miktex.org/download")
            return

        # Consolidate all markdown files into one
        consolidated_md = consolidate_paper_md(book_path, primary_language, translate)
        if not consolidated_md:
            console.print("[red bold]Error:[/red bold] Failed to consolidate markdown files.")
            return

        # Get metadata from config
        config = load_book_config(book_path)
        title = getattr(config, 'book_name', 'Untitled Paper')
        authors = getattr(config, 'authors', [])
        keywords = getattr(config, 'keywords', [])
        
        # Format authors as a string
        author_str = " and ".join(authors) if isinstance(authors, list) else authors
        
        # Format keywords as a string
        keywords_str = ", ".join(keywords) if isinstance(keywords, list) else keywords

        # Create output directory if it doesn't exist
        output_dir = Path(book_path) / "output"
        output_dir.mkdir(exist_ok=True)

        # Create templates directory if it doesn't exist
        templates_dir = Path(book_path) / "templates"
        templates_dir.mkdir(exist_ok=True)

        # Use default IEEE template if none provided
        if not template:
            # Copy default template to project's templates directory
            default_template = Path(__file__).parent.parent.parent / "templates" / "ieee.tex"
            project_template = templates_dir / "ieee.tex"
            
            if not project_template.exists():
                if not default_template.exists():
                    console.print("[red bold]Error:[/red bold] Default IEEE template not found in package.")
                    return
                # Copy template to project directory
                import shutil
                shutil.copy2(default_template, project_template)
            
            template = str(project_template)

        # Generate PDF using pandoc
        output_pdf = output_dir / f"paper-{primary_language}.pdf"
        if translate:
            output_pdf = output_dir / f"paper-{translate}.pdf"
            
        cmd = [
            "pandoc",
            consolidated_md,
            "-o", str(output_pdf),
            "--pdf-engine=xelatex",
            "--template=" + template,
            "--toc",
            "--number-sections",
            "--highlight-style=tango",
            "-V", "mainfont=DejaVu Serif",
            "-V", "sansfont=DejaVu Sans",
            "-V", "monofont=DejaVu Sans Mono",
            "-V", "CJKmainfont=Noto Sans CJK JP",
            "-V", f"title={title}",
            "-V", f"author={author_str}",
            "-V", f"keywords={keywords_str}"
        ]

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Success log
        console.print(
            f"[green bold]Success![/green bold] PDF generated at: [bold]{output_pdf}[/bold]"
        )
    except subprocess.CalledProcessError as e:
        console.print(f"[red bold]Error:[/red bold] Failed to generate PDF: {e.stderr}")
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] Failed to generate PDF: {str(e)}") 