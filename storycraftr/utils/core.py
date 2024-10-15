import os
import json
from typing import NamedTuple
from rich.console import Console

console = Console()

# Define the structure for the book using NamedTuple
class BookConfig(NamedTuple):
    book_name: str
    primary_language: str
    alternate_languages: list
    default_author: str
    genre: str

# Function to load the JSON file and convert it into a BookConfig object
def load_book_config(book_name):
    try:
        with open(os.path.join(book_name, "storycraftr.json"), 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Create an instance of BookConfig with the values from the JSON
            book_config = BookConfig(
                book_name=data['book_name'],
                primary_language=data['primary_language'],
                alternate_languages=data['alternate_languages'],
                default_author=data['default_author'],
                genre=data['genre']
            )
    except FileNotFoundError or NotADirectoryError:
        console.print(f"[bold red]⚠[/bold red] Folder '[bold]{book_name}[/bold]' is not a storycraftr project.", style="red")
        return None
    
    return book_config

def file_has_more_than_three_lines(file_path):
    """Check if a file has more than three lines."""
    with open(file_path, 'r') as file:
        # Iterate through the first 4 lines and stop if we reach 4 lines
        for i, _ in enumerate(file, 1):
            if i > 3:
                return True
    return False
