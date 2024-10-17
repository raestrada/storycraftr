import os
import re
import subprocess  # nosec
from storycraftr.utils.markdown import consolidate_book_md
from rich.console import Console
from rich.progress import track

console = Console()


def check_tool_installed(tool_name: str) -> bool:
    """Check if a tool is installed on the system."""
    try:
        subprocess.run(
            [tool_name, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )  # nosec
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def to_pdf(book_path: str, primary_language: str, translate: str = None) -> str:
    # Check if pandoc is installed
    if not check_tool_installed("pandoc"):
        console.print(
            "[red bold]Error:[/red bold] 'pandoc' is not installed. Please install it to proceed."
        )
        raise SystemExit(1)

    # Check if xelatex is installed
    if not check_tool_installed("xelatex"):
        console.print(
            "[red bold]Error:[/red bold] 'xelatex' is not installed. Please install it to proceed."
        )
        raise SystemExit(1)

    # Log the start of the process
    console.print(f"Starting PDF conversion for book: [bold]{book_path}[/bold]")

    # Get the path of the consolidated markdown
    console.print("Consolidating chapters into a single markdown file...")
    consolidated_md_path = consolidate_book_md(book_path, primary_language, translate)

    # Read the consolidated markdown content
    with open(consolidated_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Write the cleaned markdown content back to the file
    with open(consolidated_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Determine the output PDF file name
    output_pdf_path = consolidated_md_path.replace(".md", ".pdf")
    console.print(f"Markdown consolidated at [bold]{consolidated_md_path}[/bold]")

    # Path to the LaTeX template
    template_path = os.path.join(book_path, "templates", "template.tex")

    if not os.path.exists(template_path):
        console.print(
            f"[red bold]Error:[/red bold] LaTeX template not found at {template_path}"
        )
        raise FileNotFoundError(f"Template file {template_path} not found.")

    console.print(f"Using LaTeX template: [bold]{template_path}[/bold]")

    # Use subprocess to call pandoc via the system shell
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
