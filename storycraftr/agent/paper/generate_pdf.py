import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.utils.pdf import compile_latex
from storycraftr.prompts.paper.generate_pdf import (
    GENERATE_LATEX_PROMPT,
    VALIDATE_LATEX_PROMPT
)
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
)

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
    thread = get_thread(book_path)
    
    # Generate LaTeX content
    response = create_message(
        book_path=book_path,
        thread_id=thread.id,
        content=GENERATE_LATEX_PROMPT.format(
            language=language,
            template=template,
            paper_path=book_path
        ),
        assistant=assistant
    )
    
    # Validate LaTeX
    validation = create_message(
        book_path=book_path,
        thread_id=thread.id,
        content=VALIDATE_LATEX_PROMPT.format(
            latex_content=response
        ),
        assistant=assistant
    )
    
    if "VALID" not in validation:
        console.print("[red]Generated LaTeX failed validation.[/red]")
        return None
    
    # Save LaTeX file
    tex_file = output.replace(".pdf", ".tex")
    tex_path = os.path.join(book_path, tex_file)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(response)
    
    # Compile PDF using the common function
    try:
        compile_latex(tex_path, book_path, output)
    except Exception as e:
        console.print(f"[red]Error generating PDF: {e}[/red]")
        return None
