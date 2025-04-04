import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.iterate import reinforce_ideas, improve_clarity

console = Console()


@click.group()
def iterate():
    """
    Group of commands for iterative improvements to the paper.
    """
    pass


@iterate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def reinforce_ideas(prompt: str, book_path: str = None):
    """Strengthen core ideas and arguments throughout the paper."""
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    reinforce_ideas(book_path, prompt)


@iterate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def improve_clarity(prompt: str, book_path: str = None):
    """Enhance clarity and readability throughout the paper."""
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return None
    improve_clarity(book_path, prompt)


@iterate.command()
@click.argument("prompt", type=str, required=False)
def check_references_needed(prompt):
    """
    Placeholder for checking where additional references might be needed.

    Args:
        prompt (str): Instructions on areas or sections to focus for references.
    """
    console.print(
        f"[yellow]Checking for missing references with prompt:[/yellow] {prompt if prompt else 'No specific prompt provided.'}"
    )
    console.print(
        "[yellow]The 'check_references_needed' command is a placeholder and currently does nothing.[/yellow]"
    )


@iterate.command()
@click.argument("prompt", type=str, required=False)
def adjust_tone(prompt):
    """
    Placeholder for adjusting the tone across all sections.

    Args:
        prompt (str): Instructions specifying the desired tone (e.g., formal, persuasive).
    """
    console.print(
        f"[yellow]Adjusting tone with prompt:[/yellow] {prompt if prompt else 'No specific prompt provided.'}"
    )
    console.print(
        "[yellow]The 'adjust_tone' command is a placeholder and currently does nothing.[/yellow]"
    )


@iterate.command()
@click.argument("prompt", type=str, required=False)
def validate_data(prompt):
    """
    Placeholder for validating data consistency and accuracy across the paper.

    Args:
        prompt (str): Instructions on specific data or sections to validate.
    """
    console.print(
        f"[yellow]Validating data with prompt:[/yellow] {prompt if prompt else 'No specific prompt provided.'}"
    )
    console.print(
        "[yellow]The 'validate_data' command is a placeholder and currently does nothing.[/yellow]"
    )
