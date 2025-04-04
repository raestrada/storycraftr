import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.prompts.paper.generate_pdf import (
    GENERATE_LATEX_PROMPT,
    VALIDATE_LATEX_PROMPT
)
from storycraftr.agent.agents import create_or_get_assistant

console = Console()

def generate_pdf_file(book_path: str, language: str, template: str, output: str):
    """
    Generate a PDF file in the specified language using LaTeX.
    
    Args:
        book_path (str): Path to the paper directory
        language (str): Output language (en, es)
        template (str): LaTeX template to use
        output (str): Output PDF file name
    """
    config = load_book_config(book_path)
    if not config:
        return None

    assistant = create_or_get_assistant(book_path)
    
    # Generate LaTeX content
    response = assistant.chat(
        GENERATE_LATEX_PROMPT.format(
            language=language,
            template=template,
            paper_path=book_path
        )
    )
    
    # Validate LaTeX
    validation = assistant.chat(
        VALIDATE_LATEX_PROMPT.format(
            latex_content=response
        )
    )
    
    if "VALID" not in validation:
        console.print("[red]Generated LaTeX failed validation.[/red]")
        return None
    
    # Save LaTeX file
    tex_file = output.replace(".pdf", ".tex")
    tex_path = os.path.join(book_path, tex_file)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(response)
    
    # Compile PDF
    try:
        os.system(f"pdflatex -output-directory={book_path} {tex_path}")
        os.system(f"bibtex {os.path.join(book_path, tex_file.replace('.tex', '.aux'))}")
        os.system(f"pdflatex -output-directory={book_path} {tex_path}")
        os.system(f"pdflatex -output-directory={book_path} {tex_path}")
        
        console.print(f"[green]PDF generated successfully: {os.path.join(book_path, output)}[/green]")
    except Exception as e:
        console.print(f"[red]Error generating PDF: {e}[/red]")
