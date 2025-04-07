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
    generate_conclusion,
    generate_custom_section
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
    Uses OpenAI to create a clear presentation of research findings.

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
    Uses OpenAI to create a comprehensive discussion of the results.

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
    Uses OpenAI to create a strong conclusion that summarizes key findings.

    Args:
        prompt (str): Instructions for the conclusion content.
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_conclusion(book_path, prompt)

@generate.command()
@click.option(
    "--book-path",
    type=click.Path(),
    help="Path to the paper directory",
    required=False
)
@click.option(
    "--order",
    type=int,
    help="Order number for the section (between methodology and results)",
    required=True
)
@click.argument("section_title", type=str)
@click.argument("prompt", type=str)
def custom(section_title: str, prompt: str, order: int, book_path: str = None):
    """
    Generate or refine a custom section with a specified title and order.
    Uses OpenAI to create a custom section that fits between methodology and results.

    Args:
        section_title (str): Title of the custom section.
        prompt (str): Instructions for the section content.
        order (int): Order number for the section (between methodology and results).
        book_path (str, optional): The path to the paper's directory. Defaults to current directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return None

    generate_custom_section(book_path, prompt, section_title, order)
