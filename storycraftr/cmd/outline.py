import os
import click
import json
from storycraftr.agent.outline import (
    generate_general_outline,
    generate_character_summary,
    generate_plot_points,
    generate_chapter_synopsis
)
from rich.console import Console

console = Console()

def load_config(book_name):
    """Load the configuration file."""
    config_file = os.path.join(book_name, 'storycraftr.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        console.print(f"[bold red]The file storycraftr.json was not found in the path: {book_name}[/bold red]")
        return None

@click.group()
def outline():
    """Manage outline aspects of the book."""
    pass

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def general_outline(prompt, book_name=None):
    """Generate the general outline of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_general_outline(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def character_summary(prompt, book_name=None):
    """Generate the character summary of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_character_summary(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def plot_points(prompt, book_name=None):
    """Generate the main plot points of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_plot_points(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def chapter_synopsis(prompt, book_name=None):
    """Generate the chapter-by-chapter synopsis of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter_synopsis(book_name, prompt)
