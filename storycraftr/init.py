import sys
import json
from rich.console import Console
from pathlib import Path
import storycraftr.templates.folder_story
from storycraftr.agent.agents import create_or_get_assistant
from storycraftr.templates.tex import TEMPLATE_TEX
from storycraftr.templates.paper_tex import TEMPLATE_PAPER_TEX
from storycraftr.templates.ieee_tex import TEMPLATE_IEEE_TEX

console = Console()


def ensure_local_docs(book_path: str, filenames):
    """
    Ensure StoryCraftr documentation files exist by copying from the local docs directory when downloads fail.
    """

    target_dir = Path(book_path) / "storycraftr"
    target_dir.mkdir(parents=True, exist_ok=True)

    local_docs_root = Path(__file__).resolve().parent.parent / "docs"

    for filename in filenames:
        destination = target_dir / filename
        if destination.exists():
            continue
        source = local_docs_root / filename
        if source.exists():
            destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            console.print(f"[green]Local documentation copied to {destination}[/green]")
        else:
            console.print(
                f"[yellow]Warning: Local documentation source not found for {filename}[/yellow]"
            )


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
    llm_provider,
    llm_model,
    llm_endpoint,
    llm_api_key_env,
    temperature,
    request_timeout,
    embed_model,
    embed_device,
    embed_cache_dir,
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
        "multiple_answer": True,
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "llm_endpoint": llm_endpoint,
        "llm_api_key_env": llm_api_key_env,
        "temperature": temperature,
        "request_timeout": request_timeout,
        "embed_model": embed_model,
        "embed_device": embed_device,
        "embed_cache_dir": embed_cache_dir,
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

    # Ship core documentation alongside the project so the RAG can ingest it without network access
    filenames = ["getting_started.md", "iterate.md", "chat.md"]
    ensure_local_docs(book_path, filenames)

    create_or_get_assistant(book_path)


# Function to initialize PaperCraftr
def init_structure_paper(
    paper_path,
    primary_language,
    author,
    keywords,
    behavior_content,
    cli_name,
    llm_provider="openai",
    llm_model="gpt-4",
    llm_endpoint="",
    llm_api_key_env="",
    temperature=0.7,
    request_timeout=120,
    embed_model="BAAI/bge-large-en-v1.5",
    embed_device="auto",
    embed_cache_dir="",
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
        "multiple_answer": True,
        "reference_author": "Leading experts in the field",  # Valor por defecto para papers
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "llm_endpoint": llm_endpoint,
        "llm_api_key_env": llm_api_key_env,
        "temperature": temperature,
        "request_timeout": request_timeout,
        "embed_model": embed_model,
        "embed_device": embed_device,
        "embed_cache_dir": embed_cache_dir,
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
