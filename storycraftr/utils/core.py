import json
import os
import secrets  # Para generar números aleatorios seguros
from pathlib import Path
from types import SimpleNamespace
from typing import NamedTuple

import yaml
from rich.console import Console
from rich.markdown import Markdown  # Importar soporte de Markdown de Rich

from storycraftr.prompts.permute import longer_date_formats
from storycraftr.state import debug_state  # Importar el estado de debug

console = Console()


def generate_prompt_with_hash(original_prompt: str, date: str, book_path: str) -> str:
    """
    Generates a modified prompt by combining a random phrase from a list,
    a date, and the original prompt. Logs the prompt details in a YAML file.

    Args:
        original_prompt (str): The original prompt to be modified.
        date (str): The current date to be used in the prompt.
        book_path (str): Path to the book's directory where prompts.yaml will be saved.

    Returns:
        str: The modified prompt with the date and random phrase.
    """
    # Selecciona una frase aleatoria segura de la lista
    random_phrase = secrets.choice(longer_date_formats).format(date=date)
    modified_prompt = f"{random_phrase}\n\n{original_prompt}"

    # Define la ruta del archivo YAML
    yaml_path = Path(book_path) / "prompts.yaml"

    # Nueva entrada de log con fecha y prompt original
    log_entry = {"date": str(date), "original_prompt": original_prompt}

    # Verifica si el archivo YAML existe y carga los datos
    if yaml_path.exists():
        with yaml_path.open("r", encoding="utf-8") as file:
            existing_data = (
                yaml.safe_load(file) or []
            )  # Carga una lista vacía si está vacío
    else:
        existing_data = []

    # Añade la nueva entrada al log
    existing_data.append(log_entry)

    # Guarda los datos actualizados en el archivo YAML
    with yaml_path.open("w", encoding="utf-8") as file:
        yaml.dump(existing_data, file, default_flow_style=False)

    # Imprime el prompt modificado en Markdown si el modo debug está activado
    if debug_state.is_debug():
        console.print(Markdown(modified_prompt))

    return modified_prompt


class BookConfig(NamedTuple):
    """
    A NamedTuple representing the configuration of a book.

    Attributes:
        book_path (str): The path to the book's directory.
        book_name (str): The name of the book.
        primary_language (str): The primary language of the book.
        alternate_languages (list): A list of alternate languages.
        default_author (str): The default author of the book.
        genre (str): The genre of the book.
        license (str): The license type for the book.
        reference_author (str): A reference author for style guidance.
        keywords (str): Keywords for the paper (optional).
        cli_name (str): The name of the CLI tool used.
        api_base_url (str): The URL of the OpenAI-compatible API.
        model_name (str): The model to use for completions.
        multiple_answer (bool): Whether multiple answers are allowed.
    """

    book_path: str
    book_name: str
    primary_language: str
    alternate_languages: list
    default_author: str
    genre: str
    license: str
    reference_author: str
    keywords: str
    cli_name: str
    api_base_url: str
    model_name: str
    multiple_answer: bool


def load_book_config(book_path: str):
    """
    Load configuration from the book path.
    """
    if not book_path:
        console.print(
            "[red]Error: Please either:\n"
            "1. Run the command inside a StoryCraftr/PaperCraftr project directory, or\n"
            "2. Specify the project path using --book-path[/red]"
        )
        return None

    try:
        # Intentar cargar papercraftr.json primero
        config_path = Path(book_path) / "papercraftr.json"
        if not config_path.exists():
            # Si no existe, intentar storycraftr.json
            config_path = Path(book_path) / "storycraftr.json"
            if not config_path.exists():
                console.print(
                    "[red]Error: No configuration file found. Please either:\n"
                    "1. Run the command inside a StoryCraftr/PaperCraftr project directory, or\n"
                    "2. Specify the project path using --book-path[/red]"
                )
                return None

        config_data = json.loads(config_path.read_text(encoding="utf-8"))

        # Ensure required fields exist with default values
        default_config = {
            "book_name": "Untitled Paper",
            "authors": [],
            "primary_language": "en",
            "alternate_languages": [],
            "default_author": "Unknown Author",
            "genre": "research",
            "license": "CC BY",
            "reference_author": "",
            "keywords": "",
            "cli_name": "papercraftr",
            "api_base_url": "https://api.openai.com/v1",
            "model_name": "gpt-4o",
            "multiple_answer": True,
        }

        # Update default config with actual config data
        for key, value in config_data.items():
            default_config[key] = value

        return SimpleNamespace(**default_config)

    except Exception as e:
        console.print(f"[red]Error loading configuration: {str(e)}[/red]")
        return None


def file_has_more_than_three_lines(file_path: str) -> bool:
    """
    Check if a file has more than three lines.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file has more than three lines, False otherwise.
    """
    try:
        with Path(file_path).open("r", encoding="utf-8") as file:
            # Itera sobre las primeras 4 líneas y devuelve True si hay más de 3 líneas
            for i, _ in enumerate(file, start=1):
                if i > 3:
                    return True
    except FileNotFoundError:
        console.print(f"[red bold]Error:[/red bold] File not found: {file_path}")
        return False
    return False
