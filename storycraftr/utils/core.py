import os
import secrets  # Para generar números aleatorios seguros
import json
from typing import NamedTuple
from rich.console import Console
from rich.markdown import Markdown  # Importar soporte de Markdown de Rich
from storycraftr.prompts.permute import longer_date_formats
from storycraftr.state import debug_state  # Importar el estado de debug

console = Console()


def generate_prompt_with_hash(original_prompt, date):
    # Selecciona una frase aleatoria de la lista usando secrets.choice para mayor seguridad
    random_phrase = secrets.choice(longer_date_formats).format(date=date)

    # Combina la frase seleccionada, un salto de línea, el hash y el prompt original
    modified_prompt = f"{random_phrase}\n\n{original_prompt}"  # Usa los primeros 10 caracteres del hash

    # Si el modo debug está activado, imprime el prompt modificado en formato Markdown
    if debug_state.is_debug():
        console.print(
            Markdown(modified_prompt)
        )  # Usa Rich para imprimir en formato Markdown

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
