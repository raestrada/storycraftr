import os
import click
import json
from storycraftr.agent.chapters import (
    generate_chapter,
    generate_cover,
    generate_back_cover,
    generate_epilogue
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
def chapters():
    """Manage chapters of the book."""
    pass

@chapters.command()
@click.argument('chapter_number', type=int)
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def chapter(chapter_number, prompt, book_name=None):
    """Generate a new chapter for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter(book_name, chapter_number, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def cover(prompt, book_name=None):
    """Generate the cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_cover(book_name, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def back_cover(prompt, book_name=None):
    """Generate the back cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_back_cover(book_name, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def epilogue(prompt, book_name=None):
    """Generate the epilogue of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_epilogue(book_name, prompt)
