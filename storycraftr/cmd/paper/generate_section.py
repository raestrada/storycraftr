import os
import click
from rich.console import Console
from pathlib import Path
from storycraftr.utils.core import load_book_config
from storycraftr.agent.paper.generate_section import (
    generate_introduction,
    generate_methodology,
    generate_results,
    generate_discussion,
    generate_conclusion
)

console = Console()

@click.group()
def generate():
    """
    Group of commands for generating different sections of the paper.
    """
    pass

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def introduction(prompt: str, book_path: str = None):
    """
    Generate or refine the introduction section.
    Uses OpenAI to create a compelling introduction.

    Args:
        prompt (str): Instructions for the introduction content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_introduction(book_path, prompt)

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def methodology(prompt: str, book_path: str = None):
    """
    Generate or refine the methodology section.
    Uses OpenAI to create a detailed methodology description.

    Args:
        prompt (str): Instructions for the methodology content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_methodology(book_path, prompt)

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def results(prompt: str, book_path: str = None):
    """
    Generate or refine the results section.
    Uses OpenAI to create a clear presentation of findings.

    Args:
        prompt (str): Instructions for the results content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_results(book_path, prompt)

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def discussion(prompt: str, book_path: str = None):
    """
    Generate or refine the discussion section.
    Uses OpenAI to create an insightful discussion of results.

    Args:
        prompt (str): Instructions for the discussion content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_discussion(book_path, prompt)

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.argument("prompt", type=str)
def conclusion(prompt: str, book_path: str = None):
    """
    Generate or refine the conclusion section.
    Uses OpenAI to create a strong conclusion.

    Args:
        prompt (str): Instructions for the conclusion content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_conclusion(book_path, prompt)
