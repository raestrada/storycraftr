import click
import os
import sys
from rich.console import Console
from pathlib import Path

console = Console()


# Function to load the OpenAI API key from the user's home folder
def load_openai_api_key():
    """
    Loads the OpenAI API key from `.storycraftr` or `.papercraftr` folders
    in the user's home directory, using the first file it finds.
    """
    home_dir = Path.home()
    possible_paths = [
        os.path.join(home_dir, ".storycraftr", "openai_api_key.txt"),
        os.path.join(home_dir, ".papercraftr", "openai_api_key.txt"),
    ]

    print(possible_paths)

    for api_key_file in possible_paths:
        if os.path.exists(api_key_file):
            with open(api_key_file, "r") as file:
                api_key = file.read().strip()
            os.environ["OPENAI_API_KEY"] = api_key
            console.print(
                f"[green]OPENAI_API_KEY loaded successfully from {api_key_file}[/green]"
            )
            return  # Exit after first successful load

    # Error if none of the files are found
    console.print(
        f"[red]The file 'openai_api_key.txt' was not found in either .storycraftr or .papercraftr folders.[/red]"
    )


load_openai_api_key()

# Import statements grouped together for clarity
from storycraftr.state import debug_state
from storycraftr.cmd.publish import publish
from storycraftr.cmd.chat import chat
from storycraftr.agent.agents import create_or_get_assistant, update_agent_files
from storycraftr.utils.core import load_book_config

# Imports StoryCraftr in storycraftr.cmd.story
from storycraftr.cmd.story.worldbuilding import worldbuilding as story_worldbuilding
from storycraftr.cmd.story.outline import outline as story_outline
from storycraftr.cmd.story.chapters import chapters as story_chapters
from storycraftr.cmd.story.iterate import iterate as story_iterate

# Imports PaperCraftr in storycraftr.cmd.paper
from storycraftr.cmd.paper.define import define as paper_define
from storycraftr.cmd.paper.organize_lit import organize_lit as paper_organize_lit
from storycraftr.cmd.paper.outline_sections import outline as paper_outline
from storycraftr.cmd.paper.analyze import analyze as paper_analyze
from storycraftr.cmd.paper.finalize import finalize as paper_finalize

from storycraftr.init import init_structure_story, init_structure_paper


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
    "--openai-url", default="https://api.openai.com/v1", help="URL of the OpenAI API."
)
@click.option("--openai-model", default="gpt-4o", help="OpenAI model to use.")
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
    openai_url,
    openai_model,
):
    """
    Initialize the project structure with configuration and behavior content.
    """
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

    # Load behavior file content
    behavior_path = Path(behavior)
    if not behavior_path.is_file():
        console.print("[red]Behavior must be a file.[/red]")
        sys.exit(1)

    behavior_content = behavior_path.read_text(encoding="utf-8")

    # Project initialization based on the CLI
    if cli_name == "storycraftr":
        alternate_languages_list = (
            [lang.strip() for lang in alternate_languages.split(",")]
            if alternate_languages
            else []
        )
        init_structure_story(
            book_path=project_path,
            license=license,
            primary_language=primary_language,
            alternate_languages=alternate_languages_list,
            default_author=author,
            genre=genre,
            behavior_content=behavior_content,
            reference_author=reference_author,
            cli_name=cli_name,
            openai_url=openai_url,
            openai_model=openai_model,
        )
    elif cli_name == "papercraftr":
        init_structure_paper(
            paper_path=project_path,
            primary_language=primary_language,
            author=author,
            keywords=keywords,
            behavior_content=behavior_content,
            cli_name=cli_name,
            openai_url=openai_url,
            openai_model=openai_model,
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


# Add common commands to CLI
cli.add_command(init, name="init")
cli.add_command(reload_files)
cli.add_command(chat)
cli.add_command(publish)

# CLI-specific group configuration
if cli_name == "storycraftr":
    cli.add_command(story_outline)
    cli.add_command(story_worldbuilding)
    cli.add_command(story_chapters)
    cli.add_command(story_iterate)
elif cli_name == "papercraftr":
    cli.add_command(paper_define)
    cli.add_command(paper_organize_lit)
    cli.add_command(paper_outline)
    cli.add_command(paper_analyze)
    cli.add_command(paper_finalize)
else:
    console.print(
        "[red]Unknown CLI tool name. Use 'storycraftr' or 'papercraftr'.[/red]"
    )
    sys.exit(1)

if __name__ == "__main__":
    cli()
