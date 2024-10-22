import click
import os
import sys
import json
import requests
from rich.console import Console
from pathlib import Path

console = Console()


def load_openai_api_key():
    """
    Loads the OpenAI API key from the expected file path and sets it
    as an environment variable. Provides feedback on success or failure.
    """
    api_key_file = Path.home() / ".storycraftr" / "openai_api_key.txt"

    if api_key_file.exists():
        with api_key_file.open("r") as file:
            api_key = file.read().strip()
        os.environ["OPENAI_API_KEY"] = api_key
        console.print("[green]OPENAI_API_KEY loaded successfully.[/green]")
    else:
        console.print(f"[red]The file {api_key_file} does not exist.[/red]")


load_openai_api_key()

# Import statements grouped together for clarity
import storycraftr.templates.folder
from storycraftr.state import debug_state
from storycraftr.cmd.worldbuilding import worldbuilding
from storycraftr.cmd.outline import outline
from storycraftr.cmd.chapters import chapters
from storycraftr.cmd.iterate import iterate
from storycraftr.cmd.publish import publish
from storycraftr.cmd.chat import chat
from storycraftr.templates.tex import TEMPLATE_TEX
from storycraftr.agent.agents import create_or_get_assistant


def download_file(url, save_dir, filename):
    """
    Downloads a file from a URL and saves it to the specified directory.

    Args:
        url (str): The URL to download the file from.
        save_dir (str): The directory where the file will be saved.
        filename (str): The name of the file.

    Raises:
        SystemExit: If the file download fails.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / filename

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        save_path.write_text(response.text, encoding="utf-8")
        console.print(f"[green]File downloaded successfully from {url}[/green]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error downloading the file from {url}: {e}[/red]")
        sys.exit(1)


def verify_book_path(book_path=None):
    """
    Verifies if the given book path is valid and contains storycraftr.json.

    Args:
        book_path (str): The path to the book directory.

    Returns:
        str: The verified book path.

    Raises:
        ClickException: If the storycraftr.json file is not found in the directory.
    """
    book_path = book_path or os.getcwd()
    storycraftr_file = Path(book_path) / "storycraftr.json"

    if not storycraftr_file.exists():
        raise click.ClickException(
            f"The file storycraftr.json was not found in: {book_path}"
        )

    return book_path


def is_initialized(book_path):
    """
    Checks if the book project is already initialized.

    Args:
        book_path (str): The path to the book project.

    Returns:
        bool: True if the project is initialized, False otherwise.
    """
    return (Path(book_path) / "storycraftr.json").exists()


def project_not_initialized_error(book_path):
    """
    Displays an error message if the project is not initialized.

    Args:
        book_path (str): The path to the book project.
    """
    console.print(
        f"[red]✖ Project '{book_path}' is not initialized. "
        "Run 'storycraftr init {book_path}' first.[/red]"
    )


def init_structure(
    book_path,
    license,
    primary_language,
    alternate_languages,
    default_author,
    genre,
    behavior_content,
    reference_author,
):
    """
    Initializes the book project structure by creating necessary files and directories.

    Args:
        book_path (str): Path to the book project.
        license (str): License type for the project.
        primary_language (str): Primary language of the book.
        alternate_languages (list): List of alternate languages.
        default_author (str): Default author name.
        genre (str): Genre of the book.
        behavior_content (str): Behavior configuration content.
        reference_author (str): Reference author for writing style.
    """
    book_name = Path(book_path).name
    console.print(f"[blue]Initializing book structure: {book_name}[/blue]")

    # Create project structure based on templates
    for file in storycraftr.templates.folder.files_to_create:
        file_path = Path(book_path) / file["folder"] / file["filename"]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file["content"], encoding="utf-8")
        console.print(f"[green]File created: {file_path}[/green]")

    # Generate the storycraftr.json configuration file
    config_data = {
        "book_path": book_path,
        "book_name": book_name,
        "primary_language": primary_language,
        "alternate_languages": alternate_languages,
        "default_author": default_author,
        "genre": genre,
        "license": license,
        "reference_author": reference_author,
    }
    config_file = Path(book_path) / "storycraftr.json"
    config_file.write_text(json.dumps(config_data, indent=4), encoding="utf-8")
    console.print(f"[green]Configuration file created: {config_file}[/green]")

    # Create behavior file
    behaviors_dir = Path(book_path) / "behaviors"
    behaviors_dir.mkdir(exist_ok=True)
    behavior_file = behaviors_dir / "default.txt"
    behavior_file.write_text(behavior_content, encoding="utf-8")
    console.print(f"[green]Behavior file created: {behavior_file}[/green]")

    # Initialize LaTeX template
    template_dir = Path(book_path) / "templates"
    template_dir.mkdir(exist_ok=True)
    template_file = template_dir / "template.tex"
    template_file.write_text(TEMPLATE_TEX, encoding="utf-8")
    console.print(f"[green]LaTeX template created: {template_file}[/green]")

    # Download additional documentation files
    urls = [
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/getting_started.md",
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/iterate.md",
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/chat.md",
    ]
    filenames = ["getting_started.md", "iterate.md", "chat.md"]
    for url, filename in zip(urls, filenames):
        download_file(url, Path(book_path) / "storycraftr", filename)

    create_or_get_assistant(book_path)


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def cli(debug):
    """
    StoryCraftr CLI - A tool to assist in writing books using AI tools.
    """
    debug_state.set_debug(debug)
    if debug:
        console.print("[yellow]Debug mode is ON[/yellow]")


@click.command()
@click.argument("book_path")
@click.option("--license", default="CC BY-NC-SA", help="Define the license type.")
@click.option("--primary-language", default="en", help="Primary language of the book.")
@click.option(
    "--alternate-languages",
    default="",
    help="Comma-separated list of alternate languages.",
)
@click.option("--author", default="Author Name", help="Default author name.")
@click.option("--genre", default="fantasy", help="Genre of the book.")
@click.option("--behavior", required=True, help="Path to behavior content file.")
@click.option("--reference-author", default="None", help="Reference author for style.")
def init(
    book_path,
    license,
    primary_language,
    alternate_languages,
    author,
    genre,
    behavior,
    reference_author,
):
    """
    Initialize the book structure with configuration and behavior content.
    """
    if not is_initialized(book_path):
        alternate_languages_list = (
            [lang.strip() for lang in alternate_languages.split(",")]
            if alternate_languages
            else []
        )

        # Load behavior content from file
        behavior_path = Path(behavior)
        if behavior_path.is_file():
            behavior_content = behavior_path.read_text(encoding="utf-8")
        else:
            console.print("[red]Behavior must be a file.[/red]")
            sys.exit(1)

        init_structure(
            book_path,
            license,
            primary_language,
            alternate_languages_list,
            author,
            genre,
            behavior_content,
            reference_author,
        )
    else:
        console.print(f"[yellow]Project '{book_path}' is already initialized.[/yellow]")


cli.add_command(init)
cli.add_command(outline)
cli.add_command(worldbuilding)
cli.add_command(chapters)
cli.add_command(iterate)
cli.add_command(publish)
cli.add_command(chat)

if __name__ == "__main__":
    cli()
