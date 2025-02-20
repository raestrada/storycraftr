import os
import re
import subprocess  # nosec
from pathlib import Path
from storycraftr.utils.markdown import consolidate_book_md
from rich.console import Console

console = Console()


def check_tool_installed(tool_name: str) -> bool:
    """
    Check if a tool is installed on the system by attempting to run it with '--version'.

    Args:
        tool_name (str): The name of the tool to check.

    Returns:
        bool: True if the tool is installed, False otherwise.
    """
    try:
        subprocess.run(
            [tool_name, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )  # nosec
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def to_pdf(book_path: str, primary_language: str, translate: str = None) -> str:
    """
    Convert a book from markdown to PDF using Pandoc and a LaTeX template.

    Args:
        book_path (str): The path to the book's directory.
        primary_language (str): The primary language of the book.
        translate (str, optional): Optional translation option.

    Returns:
        str: The path to the generated PDF file.

    Raises:
        SystemExit: If pandoc or xelatex are not installed.
        FileNotFoundError: If the LaTeX template is not found.
    """
    # Check if required tools are installed
    if not check_tool_installed("pandoc"):
        console.print(
            "[red bold]Error:[/red bold] 'pandoc' is not installed. Please install it to proceed."
        )
        raise SystemExit(1)

    if not check_tool_installed("xelatex"):
        console.print(
            "[red bold]Error:[/red bold] 'xelatex' is not installed. Please install it to proceed."
        )
        raise SystemExit(1)

    # Log the start of the PDF conversion process
    console.print(f"Starting PDF conversion for book: [bold]{book_path}[/bold]")

    # Consolidate markdown content
    console.print("Consolidating chapters into a single markdown file...")
    consolidated_md_path = consolidate_book_md(book_path, primary_language, translate)

    # Read and clean markdown content
    with open(consolidated_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(consolidated_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)  # Rewrites cleaned content

    # Define the output PDF file path
    output_pdf_path = consolidated_md_path.replace(".md", ".pdf")
    console.print(f"Markdown consolidated at [bold]{consolidated_md_path}[/bold]")

    # Check if LaTeX template exists
    template_path = Path(book_path) / "templates" / "template.tex"
    if not template_path.exists():
        console.print(
            f"[red bold]Error:[/red bold] LaTeX template not found at {template_path}"
        )
        raise FileNotFoundError(f"Template file {template_path} not found.")

    console.print(f"Using LaTeX template: [bold]{template_path}[/bold]")

    # Convert markdown to PDF using pandoc
    try:
        subprocess.run(
            [
                "pandoc",
                consolidated_md_path,
                "-o",
                output_pdf_path,
                "--pdf-engine=xelatex",
                f"--template={template_path}",
                "--no-highlight",  # Disable syntax highlighting
            ],
            check=True,
        )  # nosec
    except subprocess.CalledProcessError as e:
        console.print(
            f"[red bold]Error:[/red bold] Failed to convert markdown to PDF: {e}"
        )
        raise

    console.print(f"PDF generated at [bold]{output_pdf_path}[/bold]")
    return output_pdf_path
