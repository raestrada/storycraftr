import click
import os
import sys
from rich.console import Console
from pathlib import Path
from storycraftr.utils.cleanup import cleanup_vector_stores
from storycraftr.llm.credentials import load_local_credentials

console = Console()


load_local_credentials()

# Import statements grouped together for clarity
from storycraftr.state import debug_state
from storycraftr.cmd.story.publish import publish
from storycraftr.cmd.chat import chat
from storycraftr.agent.agents import create_or_get_assistant, update_agent_files
from storycraftr.utils.core import load_book_config

# Imports StoryCraftr in storycraftr.cmd.story
from storycraftr.cmd.story.worldbuilding import worldbuilding as story_worldbuilding
from storycraftr.cmd.story.outline import outline as story_outline
from storycraftr.cmd.story.chapters import chapters as story_chapters
from storycraftr.cmd.story.iterate import iterate as story_iterate

# Imports PaperCraftr in storycraftr.cmd.paper
from storycraftr.cmd.paper.organize_lit import organize_lit as paper_organize_lit
from storycraftr.cmd.paper.outline_sections import outline as paper_outline
from storycraftr.cmd.paper.generate_section import generate as paper_generate
from storycraftr.cmd.paper.references import references as paper_references
from storycraftr.cmd.paper.iterate import iterate as paper_iterate
from storycraftr.cmd.paper.publish import publish as paper_publish
from storycraftr.cmd.paper.abstract import abstract as paper_abstract

from storycraftr.init import init_structure_story, init_structure_paper
from storycraftr.subagents import seed_default_roles


# Detect CLI (storycraftr or papercraftr)
def detect_invocation():
    """
    Detects how the CLI is being invoked (StoryCraftr or PaperCraftr).
    """
    script_name = Path(sys.argv[0]).stem
    return "papercraftr" if script_name == "papercraftr" else "storycraftr"


cli_name = detect_invocation()


# Verify if the directory contains storycraftr.json
def verify_book_path(book_path=None):
    """
    Verifies if the specified directory contains `storycraftr.json`.

    Args:
        book_path (str): The path to the book directory.

    Returns:
        str: The verified book path.

    Raises:
        ClickException: If `storycraftr.json` file is not found.
    """
    book_path = book_path or os.getcwd()
    storycraftr_file = os.path.join(book_path, "storycraftr.json")

    if not os.path.exists(storycraftr_file):
        raise click.ClickException(
            f"The file storycraftr.json was not found in: {book_path}"
        )

    return book_path


# Check if the project is already initialized
def is_initialized(book_path):
    """
    Checks if the book project is already initialized.

    Args:
        book_path (str): The path to the book project.

    Returns:
        bool: True if the project is initialized, False if not.
    """
    return os.path.exists(os.path.join(book_path, "storycraftr.json"))


# Show an error if the project is not initialized
def project_not_initialized_error(book_path):
    """
    Shows an error message if the project is not initialized.

    Args:
        book_path (str): The path to the book project.
    """
    console.print(
        f"[red]✖ Project '{book_path}' is not initialized. "
        "Run 'storycraftr init {book_path}' first.[/red]"
    )


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
@click.argument("project_path")
@click.option(
    "--license",
    default="CC BY-NC-SA",
    help="Define the license type (StoryCraftr only).",
)
@click.option(
    "--primary-language", default="en", help="Primary language of the project."
)
@click.option(
    "--alternate-languages",
    default="",
    help="Comma-separated list of alternate languages (StoryCraftr only).",
)
@click.option("--author", default="Author Name", help="Default author name.")
@click.option(
    "--genre", default="fantasy", help="Genre of the book (StoryCraftr only)."
)
@click.option("--behavior", required=True, help="Path to behavior content file.")
@click.option(
    "--reference-author",
    default="None",
    help="Reference author for style (StoryCraftr only).",
)
@click.option("--keywords", help="Keywords for the paper (PaperCraftr only).")
@click.option(
    "--llm-provider",
    default="openai",
    type=click.Choice(["openai", "openrouter", "ollama", "fake"]),
    show_default=True,
    help="LLM provider to use for generations.",
)
@click.option("--llm-model", default="gpt-4o", show_default=True, help="Model name.")
@click.option(
    "--llm-endpoint",
    default="",
    show_default=False,
    help="Optional custom endpoint/base URL for the selected provider.",
)
@click.option(
    "--llm-api-key-env",
    default="",
    show_default=False,
    help="Environment variable to read the provider API key from.",
)
@click.option(
    "--temperature",
    default=0.7,
    show_default=True,
    type=float,
    help="Sampling temperature.",
)
@click.option(
    "--request-timeout",
    default=120,
    show_default=True,
    type=int,
    help="Timeout in seconds for LLM calls.",
)
@click.option(
    "--embed-model",
    default="BAAI/bge-large-en-v1.5",
    show_default=True,
    help="Embedding model used for local vector search.",
)
@click.option(
    "--embed-device",
    default="auto",
    show_default=True,
    help="Device hint for embedding inference (auto, cpu, cuda, mps, ...).",
)
@click.option(
    "--embed-cache-dir",
    default="",
    show_default=False,
    help="Optional cache directory for embedding artifacts.",
)
def init(
    project_path,
    license,
    primary_language,
    alternate_languages,
    author,
    genre,
    behavior,
    reference_author,
    keywords,
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
    Initialize the project structure with configuration and behavior content.
    """
    # Asegurarse de que el directorio del proyecto existe o crearlo
    project_path = Path(project_path).resolve()
    try:
        project_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Error creating project directory: {e}[/red]")
        sys.exit(1)

    # Manejar la ruta del archivo behavior
    behavior_path = Path(behavior).resolve()
    if not behavior_path.is_file():
        # Intentar buscar el archivo en el directorio actual
        current_dir_behavior = Path.cwd() / behavior
        if current_dir_behavior.is_file():
            behavior_path = current_dir_behavior
        else:
            console.print(
                f"[red]Behavior file not found at {behavior_path} or {current_dir_behavior}[/red]"
            )
            sys.exit(1)

    try:
        behavior_content = behavior_path.read_text(encoding="utf-8")
    except Exception as e:
        console.print(f"[red]Error reading behavior file: {e}[/red]")
        sys.exit(1)

    # Cambiar al directorio del proyecto
    try:
        os.chdir(project_path)
    except Exception as e:
        console.print(f"[red]Error accessing project directory: {e}[/red]")
        sys.exit(1)

    cli_name = detect_invocation()

    # Parameter validation based on the CLI
    if cli_name == "storycraftr" and keywords:
        console.print(
            "[red]Error: The --keywords option is only valid for PaperCraftr.[/red]"
        )
        sys.exit(1)
    elif cli_name == "papercraftr" and (
        license != "CC BY-NC-SA"
        or alternate_languages
        or genre != "fantasy"
        or reference_author != "None"
    ):
        console.print(
            "[red]Error: The options --license, --alternate-languages, --genre, and --reference-author "
            "are only valid for StoryCraftr.[/red]"
        )
        sys.exit(1)

    # Project initialization based on the CLI
    if cli_name == "storycraftr":
        alternate_languages_list = (
            [lang.strip() for lang in alternate_languages.split(",")]
            if alternate_languages
            else []
        )
        init_structure_story(
            book_path=str(project_path),
            license=license,
            primary_language=primary_language,
            alternate_languages=alternate_languages_list,
            default_author=author,
            genre=genre,
            behavior_content=behavior_content,
            reference_author=reference_author,
            cli_name=cli_name,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_endpoint=llm_endpoint,
            llm_api_key_env=llm_api_key_env,
            temperature=temperature,
            request_timeout=request_timeout,
            embed_model=embed_model,
            embed_device=embed_device,
            embed_cache_dir=embed_cache_dir,
        )
    elif cli_name == "papercraftr":
        init_structure_paper(
            paper_path=str(project_path),
            primary_language=primary_language,
            author=author,
            keywords=keywords,
            behavior_content=behavior_content,
            cli_name=cli_name,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_endpoint=llm_endpoint,
            llm_api_key_env=llm_api_key_env,
            temperature=temperature,
            request_timeout=request_timeout,
            embed_model=embed_model,
            embed_device=embed_device,
            embed_cache_dir=embed_cache_dir,
        )


@click.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
def reload_files(book_path):
    """
    Reloads the agent files for the given book path.

    Args:
        book_path (str): Path to the book project.
    """
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return
    if is_initialized(book_path):
        assistant = create_or_get_assistant(book_path)
        update_agent_files(book_path, assistant)
        console.print(
            f"[green]Agent files reloaded successfully for project: {book_path}[/green]"
        )
    else:
        project_not_initialized_error(book_path)


@click.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.option("--force", is_flag=True, help="Skip confirmation prompt", default=False)
def cleanup(book_path, force):
    """Delete all vector stores and their files."""
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return
    if is_initialized(book_path):
        console.print(
            "[bold red]WARNING: This will delete the local vector store and cached embeddings for this project.[/bold red]"
        )
        console.print("[bold red]This action cannot be undone![/bold red]")

        if not force:
            if not click.confirm("Are you sure you want to continue?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

        cleanup_vector_stores(book_path)
    else:
        project_not_initialized_error(book_path)


@cli.group(name="sub-agents")
def sub_agents():
    """Manage sub-agent role definitions."""
    pass


@sub_agents.command("seed")
@click.option("--book-path", type=click.Path(), required=False, help="Book path.")
@click.option(
    "--language",
    default="en",
    show_default=True,
    help="Language used to seed default prompts.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing role files.",
)
def sub_agents_seed(book_path, language, force):
    """Seed or overwrite the default sub-agent roles."""
    book_path = verify_book_path(book_path)
    written = seed_default_roles(book_path, language=language, force=force)
    if written:
        console.print(
            f"[green]Seeded {len(written)} role definition(s) in {book_path}.[/green]"
        )
    else:
        console.print(
            f"[yellow]Roles already exist in {book_path}. Use --force to overwrite.[/yellow]"
        )


# Add common commands to CLI
cli.add_command(init, name="init")
cli.add_command(reload_files)
cli.add_command(chat)
cli.add_command(publish)
cli.add_command(cleanup)
cli.add_command(sub_agents)

# CLI-specific group configuration
if cli_name == "storycraftr":
    cli.add_command(story_worldbuilding)
    cli.add_command(story_outline)
    cli.add_command(story_chapters)
    cli.add_command(story_iterate)
    cli.add_command(publish)
    cli.add_command(chat)
    cli.add_command(reload_files)
elif cli_name == "papercraftr":
    cli.add_command(paper_organize_lit)
    cli.add_command(paper_outline)
    cli.add_command(paper_generate)
    cli.add_command(paper_references)
    cli.add_command(paper_iterate)
    cli.add_command(paper_publish)
    cli.add_command(paper_abstract)
    cli.add_command(chat)
    cli.add_command(reload_files)
else:
    console.print(
        "[red]Unknown CLI tool name. Use 'storycraftr' or 'papercraftr'.[/red]"
    )
    sys.exit(1)

if __name__ == "__main__":
    cli()
