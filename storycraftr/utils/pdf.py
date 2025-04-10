import os
import re
import subprocess  # nosec
from pathlib import Path
from storycraftr.utils.markdown import consolidate_book_md
from rich.console import Console
import shutil

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


def check_font_available(font_name: str) -> bool:
    """
    Check if a font is available on the system using fc-list.

    Args:
        font_name (str): The name of the font to check.

    Returns:
        bool: True if the font is available, False otherwise.
    """
    try:
        result = subprocess.run(
            ["fc-list", font_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )  # nosec
        return result.returncode == 0 and len(result.stdout) > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_available_font() -> str:
    """
    Get an available font from a list of preferred fonts.

    Returns:
        str: The name of an available font.
    """
    preferred_fonts = [
        "Palatino",
        "Times New Roman",
        "Times",
        "DejaVu Serif",
        "Liberation Serif",
        "FreeSerif",
        "Nimbus Roman",
        "Bitstream Vera Serif",
    ]

    for font in preferred_fonts:
        if check_font_available(font):
            return font

    return "DejaVu Serif"  # Default to a common font that should be available


def find_executable(executable_name):
    """Find the full path of an executable."""
    return shutil.which(executable_name)


def compile_latex_to_pdf(tex_path, output_dir, output_name="output.pdf"):
    """
    Compile a LaTeX file to PDF using pdflatex.

    Args:
        tex_path (str): Path to the LaTeX file
        output_dir (str): Directory to store output files
        output_name (str): Name of the output PDF file

    Returns:
        str: Path to the generated PDF file
    """
    # Find executables
    pdflatex_path = find_executable("pdflatex")
    bibtex_path = find_executable("bibtex")
    makeindex_path = find_executable("makeindex")
    makeglossaries_path = find_executable("makeglossaries")

    if not all([pdflatex_path, bibtex_path, makeindex_path, makeglossaries_path]):
        raise RuntimeError(
            "Required LaTeX tools not found. Please install pdflatex, bibtex, makeindex, and makeglossaries."
        )

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get absolute paths
    tex_path = os.path.abspath(tex_path)
    output_dir = os.path.abspath(output_dir)

    # Get base name without extension
    tex_base = os.path.splitext(os.path.basename(tex_path))[0]

    # Define paths for auxiliary files
    aux_path = os.path.join(output_dir, f"{tex_base}.aux")
    idx_path = os.path.join(output_dir, f"{tex_base}.idx")

    try:
        # First pdflatex run - generates aux file
        console.print("First pdflatex run (generating aux file)...")
        subprocess.run(  # nosec
            [
                pdflatex_path,
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                tex_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Run bibtex if aux file exists
        if os.path.exists(aux_path):
            console.print("Running bibtex for bibliography...")
            subprocess.run(  # nosec
                [bibtex_path, aux_path],
                check=True,
                capture_output=True,
                text=True,
            )

        # Run makeindex if idx file exists
        if os.path.exists(idx_path):
            console.print("Running makeindex for index generation...")
            subprocess.run(  # nosec
                [makeindex_path, idx_path],
                check=True,
                capture_output=True,
                text=True,
            )

            # Run makeglossaries if needed
            console.print("Running makeglossaries for glossary...")
            subprocess.run(  # nosec
                [
                    makeglossaries_path,
                    "-d",
                    output_dir,
                    tex_base,
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        # Second pdflatex run - processes bibliography and other references
        console.print("Second pdflatex run (processing references)...")
        subprocess.run(  # nosec
            [
                pdflatex_path,
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                tex_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Third pdflatex run - final pass for all references
        console.print("Third pdflatex run (final pass)...")
        subprocess.run(  # nosec
            [
                pdflatex_path,
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                tex_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Return the path to the generated PDF
        output_pdf_path = os.path.join(output_dir, output_name)
        if not os.path.exists(output_pdf_path):
            raise RuntimeError(
                f"PDF generation failed. Expected output file not found: {output_pdf_path}"
            )

        return output_pdf_path

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error during LaTeX compilation:[/bold red]")
        console.print(e.stderr)
        raise


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

    # Check if Palatino font is available
    if not check_font_available("Palatino"):
        console.print("[yellow]Warning:[/yellow] Palatino font not found.")
        console.print(
            "[yellow]Recommendation:[/yellow] Install Palatino for the best experience."
        )
        console.print("[yellow]Installation instructions:[/yellow]")
        console.print(
            "  - Ubuntu/Debian: sudo apt-get install texlive-fonts-recommended"
        )
        console.print("  - Fedora: sudo dnf install texlive-palatino")
        console.print("  - macOS: Palatino is included by default")
        console.print("  - Windows: Install TeX Live with Palatino package")

        # Get an available font
        available_font = get_available_font()
        console.print(f"[yellow]Using {available_font} as fallback font.[/yellow]")

        # Create a temporary template with the available font
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Replace Palatino with the available font
        modified_template = template_content.replace(
            "\\setmainfont{Palatino}", f"\\setmainfont{{{available_font}}}"
        )

        # Create a temporary template file
        temp_template_path = Path(book_path) / "templates" / "template_temp.tex"
        with open(temp_template_path, "w", encoding="utf-8") as f:
            f.write(modified_template)

        template_path = temp_template_path
        console.print(
            f"Using modified template with {available_font} font: [bold]{template_path}[/bold]"
        )

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

    # Clean up temporary template if it was created
    if "template_temp.tex" in str(template_path):
        try:
            os.remove(template_path)
            console.print("Temporary template removed.")
        except Exception as e:
            console.print(
                f"[yellow]Warning:[/yellow] Failed to remove temporary template: {e}"
            )

    console.print(f"PDF generated at [bold]{output_pdf_path}[/bold]")
    return output_pdf_path
