import sys
import json
import requests
from rich.console import Console
from pathlib import Path
import storycraftr.templates.folder_story
from storycraftr.agent.agents import create_or_get_assistant
from storycraftr.templates.tex import TEMPLATE_TEX
from storycraftr.templates.paper_tex import TEMPLATE_PAPER_TEX
from storycraftr.templates.ieee_tex import TEMPLATE_IEEE_TEX

console = Console()


# Download files from a URL to a specified directory
def download_file(url, save_dir, filename):
    """
    Downloads a file from a URL and saves it in the specified directory.

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


# Function to initialize StoryCraftr
def init_structure_story(
    book_path,
    license,
    primary_language,
    alternate_languages,
    default_author,
    genre,
    behavior_content,
    reference_author,
    cli_name,
    openai_url,
    openai_model,
):
    """
    Initializes the StoryCraftr project structure by creating necessary files and folders.
    """
    book_name = Path(book_path).name
    console.print(
        f"[blue]Initializing StoryCraftr project structure: {book_name}[/blue]"
    )

    # Create project structure based on StoryCraftr templates
    for file in storycraftr.templates.folder_story.files_to_create:
        file_path = Path(book_path) / file["folder"] / file["filename"]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file["content"], encoding="utf-8")
        console.print(f"[green]File created: {file_path}[/green]")

    # Create configuration file
    config_data = {
        "book_path": book_path,
        "book_name": book_name,
        "primary_language": primary_language,
        "alternate_languages": alternate_languages,
        "default_author": default_author,
        "genre": genre,
        "license": license,
        "reference_author": reference_author,
        "cli_name": cli_name,
        "openai_url": openai_url,
        "openai_model": openai_model,
        "multiple_answer": True,
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

    # Create LaTeX template
    template_dir = Path(book_path) / "templates"
    template_dir.mkdir(exist_ok=True)
    template_file = template_dir / "template.tex"
    template_file.write_text(TEMPLATE_TEX, encoding="utf-8")
    console.print(f"[green]LaTeX template created: {template_file}[/green]")

    # Download additional files
    urls = [
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/getting_started.md",
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/iterate.md",
        "https://raw.githubusercontent.com/raestrada/storycraftr/refs/heads/main/docs/chat.md",
    ]
    filenames = ["getting_started.md", "iterate.md", "chat.md"]
    for url, filename in zip(urls, filenames):
        download_file(url, Path(book_path) / "storycraftr", filename)

    create_or_get_assistant(book_path)


# Function to initialize PaperCraftr
def init_structure_paper(
    paper_path,
    primary_language,
    author,
    keywords,
    behavior_content,
    cli_name,
    openai_url="https://api.openai.com/v1",
    openai_model="gpt-4",
):
    """
    Initializes the PaperCraftr project structure by creating necessary files and folders.
    """
    paper_name = Path(paper_path).name
    console.print(
        f"[blue]Initializing PaperCraftr project structure: {paper_name}[/blue]"
    )

    # Create project structure based on PaperCraftr templates
    for file in storycraftr.templates.folder_paper.files_to_create:
        file_path = Path(paper_path) / file["folder"] / file["filename"]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file["content"], encoding="utf-8")
        console.print(f"[green]File created: {file_path}[/green]")

    # Create configuration file with default values if not provided
    config_data = {
        "book_path": paper_path,
        "book_name": paper_name,
        "primary_language": primary_language,
        "default_author": author,
        "keywords": keywords,
        "cli_name": cli_name,
        "openai_url": openai_url,
        "openai_model": openai_model,
        "multiple_answer": True,
        "reference_author": "Leading experts in the field",  # Valor por defecto para papers
    }

    # Guardar configuración solo en el directorio del proyecto
    project_config_file = Path(paper_path) / "papercraftr.json"
    project_config_file.write_text(json.dumps(config_data, indent=4), encoding="utf-8")
    console.print(f"[green]Configuration file created: {project_config_file}[/green]")

    # Create behavior file in the project directory
    behaviors_dir = Path(paper_path) / "behaviors"
    behaviors_dir.mkdir(exist_ok=True)
    behavior_file = behaviors_dir / "default.txt"
    behavior_file.write_text(behavior_content, encoding="utf-8")
    console.print(f"[green]Behavior file created: {behavior_file}[/green]")

    # Create IEEE template
    template_dir = Path(paper_path) / "templates"
    template_dir.mkdir(exist_ok=True)
    ieee_template_file = template_dir / "ieee.tex"
    ieee_template_file.write_text(TEMPLATE_IEEE_TEX, encoding="utf-8")
    console.print(f"[green]IEEE template created: {ieee_template_file}[/green]")

    # Initialize the assistant
    create_or_get_assistant(paper_path)
