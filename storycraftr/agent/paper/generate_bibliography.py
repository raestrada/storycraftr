import os
from pathlib import Path
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.prompts.paper.generate_bibliography import (
    GENERATE_BIBLIOGRAPHY_PROMPT,
    VALIDATE_BIBLIOGRAPHY_PROMPT
)
from storycraftr.agent.agents import create_or_get_assistant

console = Console()

def generate_bibliography_file(book_path: str, format: str, output: str):
    """
    Generate a bibliography file in the specified format.
    
    Args:
        book_path (str): Path to the paper directory
        format (str): Bibliography format (bibtex, biblatex, etc.)
        output (str): Output file name
    """
    config = load_book_config(book_path)
    if not config:
        return None

    assistant = create_or_get_assistant(book_path)
    
    # Generate bibliography content
    response = assistant.chat(
        GENERATE_BIBLIOGRAPHY_PROMPT.format(
            format=format,
            references_path=os.path.join(book_path, "references")
        )
    )
    
    # Validate bibliography
    validation = assistant.chat(
        VALIDATE_BIBLIOGRAPHY_PROMPT.format(
            format=format,
            bibliography_content=response
        )
    )
    
    if "VALID" not in validation:
        console.print("[red]Generated bibliography failed validation.[/red]")
        return None
    
    # Save bibliography file
    output_path = os.path.join(book_path, output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response)
    
    console.print(f"[green]Bibliography generated successfully: {output_path}[/green]")
