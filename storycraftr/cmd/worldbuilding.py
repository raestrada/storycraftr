import os
import click
import json
from storycraftr.agent.worldbuilding import (
    generate_geography,
    generate_history,
    generate_culture,
    generate_magic_system,
    generate_technology
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
def worldbuilding():
    """Manage worldbuilding aspects of the book."""
    pass

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def geography(prompt, book_name=None):
    """Generate geography details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_geography(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def history(prompt, book_name=None):
    """Generate history details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_history(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def culture(prompt, book_name=None):
    """Generate culture details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_culture(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def magic_system(prompt, book_name=None):
    """Generate magic or science system details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_magic_system(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def technology(prompt, book_name=None):
    """Generate technology details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_technology(book_name, prompt)
