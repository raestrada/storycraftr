import click
from rich.console import Console
from pathlib import Path

console = Console()


@click.group()
@click.option(
    "--book_path",
    type=click.Path(),
    required=True,
    help="Path to the paper project directory.",
)
def organize_lit(book_path):
    """
    Group of commands for organizing literature and building the conceptual framework for the paper.
    """
    # Store the book_path as an attribute for future file operations
    organize_lit.book_path = Path(book_path)


@organize_lit.command()
@click.argument("prompt", type=str, required=False)
def lit_summary(prompt):
    """
    Placeholder for generating a summary of key literature.
    In the future, this command will use OpenAI to summarize major sources and identify research gaps.

    Args:
        prompt (str): Additional instructions to customize the summary generation.
    """
    console.print(
        "[yellow]The 'lit_summary' command is a placeholder and currently does nothing.[/yellow]"
    )
    console.print(f"Prompt: {prompt if prompt else 'No additional prompt provided.'}")


@organize_lit.command()
@click.argument("prompt", type=str, required=False)
def concept_map(prompt):
    """
    Placeholder for creating a concept map of the research framework.
    In the future, this command will use OpenAI to map key concepts and theories related to the research question.

    Args:
        prompt (str): Additional instructions to customize the concept map creation.
    """
    console.print(
        "[yellow]The 'concept_map' command is a placeholder and currently does nothing.[/yellow]"
    )
    console.print(f"Prompt: {prompt if prompt else 'No additional prompt provided.'}")
