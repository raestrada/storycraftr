import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.analyze import run_data_analysis, summarize_analysis_results

console = Console()


@click.group()
def analyze():
    """
    Group of commands for running data analysis and summarizing results.
    """
    pass


@analyze.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def run_analysis(prompt: str, book_path: str = None):
    """
    Generate or refine a data analysis plan.
    Uses OpenAI to create a comprehensive analysis strategy.

    Args:
        prompt (str): Instructions detailing the analysis to perform.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    run_data_analysis(book_path, prompt)


@analyze.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def summarize_results(prompt: str, book_path: str = None):
    """
    Generate or refine a summary of analysis results.
    Uses OpenAI to create a comprehensive results section.

    Args:
        prompt (str): Instructions for customizing the results summary.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    summarize_analysis_results(book_path, prompt)
