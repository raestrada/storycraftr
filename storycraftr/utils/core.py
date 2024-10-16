import os
import hashlib
import json
from typing import NamedTuple
from rich.console import Console

console = Console()


def generate_prompt_with_hash(original_prompt):
    # Genera un hash basado en el contenido del prompt
    hash_object = hashlib.sha256(original_prompt.encode())
    hash_hex = hash_object.hexdigest()

    # Combina el hash con el prompt original (puedes limitar el hash a los primeros caracteres si prefieres)
    modified_prompt = (
        f"{hash_hex}: {original_prompt}"  # Usa los primeros 10 caracteres del hash
    )
    return modified_prompt


# Define the structure for the book using NamedTuple
class BookConfig(NamedTuple):
    book_path: str
    book_name: str
    primary_language: str
    alternate_languages: list
    default_author: str
    genre: str
    license: str
    reference_author: str


# Function to load the JSON file and convert it into a BookConfig object
def load_book_config(book_path):
    try:
        with open(
            os.path.join(book_path, "storycraftr.json"), "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
            # Create an instance of BookConfig with the values from the JSON
            book_config = BookConfig(
                book_path=data["book_path"],
                book_name=data["book_name"],
                primary_language=data["primary_language"],
                alternate_languages=data["alternate_languages"],
                default_author=data["default_author"],
                genre=data["genre"],
                license=data["license"],
                reference_author=data["reference_author"],
            )
    except FileNotFoundError or NotADirectoryError:
        console.print(
            f"[bold red]⚠[/bold red] Folder '[bold]{book_path}[/bold]' is not a storycraftr project.",
            style="red",
        )
        return None

    return book_config


def file_has_more_than_three_lines(file_path):
    """Check if a file has more than three lines."""
    with open(file_path, "r") as file:
        # Iterate through the first 4 lines and stop if we reach 4 lines
        for i, _ in enumerate(file, 1):
            if i > 3:
                return True
    return False
