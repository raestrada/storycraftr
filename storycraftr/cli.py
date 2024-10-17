import click
import os
import json
from rich.console import Console
import storycraftr.templates.folder
from storycraftr.cmd.worldbuilding import worldbuilding
from storycraftr.cmd.outline import outline
from storycraftr.cmd.chapters import chapters
from storycraftr.cmd.iterate import iterate
from storycraftr.cmd.publish import publish
from storycraftr.cmd.chat import chat
from storycraftr.templates.tex import TEMPLATE_TEX


console = Console()


def load_openai_api_key():
    # Path to the API key file
    api_key_file = os.path.expanduser("~/.storycraftr/openai_api_key.txt")

    # Check if the file exists
    if os.path.exists(api_key_file):
        # Read the content of the file
        with open(api_key_file, "r") as file:
            api_key = file.read().strip()  # Strip any whitespace or newlines

        # Set the API key as an environment variable
        os.environ["OPENAI_API_KEY"] = api_key
        console.print("[green]OPENAI_API_KEY has been successfully loaded.[/green]")
    else:
        console.print(f"[red]The file {api_key_file} does not exist.[/red]")


# Run the function
load_openai_api_key()


def verify_book_path(book_path=None):
    """Verify if the book path is valid and contains storycraftr.json."""
    if not book_path:
        book_path = (
            os.getcwd()
        )  # Use the current directory if --book-path is not provided
    storycraftr_file = os.path.join(book_path, "storycraftr.json")

    if not os.path.exists(storycraftr_file):
        raise click.ClickException(
            f"The file storycraftr.json was not found in the path: {book_path}"
        )

    return book_path


def is_initialized(book_path):
    """Check if the book structure is already initialized."""
    storycraftr_file = os.path.join(book_path, "storycraftr.json")
    return os.path.exists(storycraftr_file)


# Function to show error if project is not initialized
def project_not_initialized_error(book_path):
    console.print(
        f"[bold red]✖[/bold red] Project '[bold]{book_path}[/bold]' is not initialized. "
        f"Run '[bold]storycraftr init {book_path}[/bold]' first.",
        style="bold red",
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
    # Show initialization start
    console.print(f"[bold blue]Initializing book structure: {book_path}[/bold blue]")

    book_name = book_path.split("/")[-1]

    # Iterate over the list and create each file, showing progress
    for file in storycraftr.templates.folder.files_to_create:
        # Build the full file path
        file_path = os.path.join(book_path, file["folder"], file["filename"])

        # Ensure the directory exists
        os.makedirs(os.path.join(book_path, file["folder"]), exist_ok=True)

        # Write the content to the file
        with open(file_path, "w") as f:
            f.write(file["content"])

        # Log the created file
        console.log(f"[green]File created:[/green] {file_path}")

    # Create the storycraftr.json file
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

    config_file = os.path.join(book_path, "storycraftr.json")
    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=4)

    # Log configuration file creation
    console.print(
        f"[green]Configuration file created:[/green] {config_file}", style="green"
    )

    # Create 'behaviors' folder inside the root book_path directory
    behaviors_dir = os.path.join(book_path, "behaviors")
    os.makedirs(behaviors_dir, exist_ok=True)

    # Create the default.txt file inside the 'behaviors' folder with the behavior content
    behavior_file = os.path.join(behaviors_dir, "default.txt")
    with open(behavior_file, "w") as f:
        f.write(behavior_content)

    # Log behavior file creation
    console.print(
        f"[green]Behavior file created:[/green] {behavior_file}", style="green"
    )

    # Confirm completion
    console.print(
        f"[bold green]✔[/bold green] Project '[bold]{book_path}[/bold]' initialized successfully.",
        style="bold green",
    )

    # Ruta donde se creará la nueva carpeta de book_path/templates/
    new_template_dir = os.path.join(book_path, "templates")

    # Log: Creación de la carpeta
    console.log(f"Creando el directorio: {new_template_dir}", style="bold blue")

    # Crear la carpeta si no existe
    os.makedirs(new_template_dir, exist_ok=True)

    # Ruta completa del archivo template.tex
    new_template_path = os.path.join(new_template_dir, "template.tex")

    # Log: Escribiendo el archivo
    console.log(f"Writing LaTex file: {new_template_path}", style="bold green")

    # Escribir el contenido del template en el archivo
    with open(new_template_path, "w") as f:
        f.write(TEMPLATE_TEX)

    # Log: Proceso completado
    console.log(f"LaTex template copied: {new_template_path}", style="bold magenta")


@click.group()
def cli():
    """StoryCraftr CLI - A tool to help you write books using OpenAI."""
    pass


@click.command()
@click.argument("book_path")
@click.option(
    "--license",
    default="CC BY-NC-SA",
    help="Define the type of Creative Commons license to use. Options include 'CC BY', 'CC BY-SA', 'CC BY-ND', 'CC BY-NC', 'CC BY-NC-SA', 'CC BY-NC-ND'. The default is 'CC BY-NC-SA'.",
)
@click.option(
    "--primary-language",
    default="en",
    help="The primary language for the book (default: 'en').",
)
@click.option(
    "--alternate-languages",
    default="",
    help="Comma-separated list of alternate languages (e.g., 'es,fr').",
)
@click.option("--author", default="Author Name", help="The default author of the book.")
@click.option(
    "--genre", default="fantasy", help="The genre of the book (default: 'fantasy')."
)
@click.option(
    "--behavior", help="Behavior content, either as a string or a path to a file."
)
@click.option(
    "--reference-author",
    help="Behavior content, either as a string or a path to a file.",
)
def init(
    book_path,
    license,
    primary_language,
    alternate_languages,
    author,
    genre,
    behavior,
    reference_author="(None: use all your knwoledge to assume writing style )",
):
    """Initialize the book structure with relevant configuration and behavior content."""
    if not is_initialized(book_path):
        alternate_languages_list = (
            [lang.strip() for lang in alternate_languages.split(",")]
            if alternate_languages
            else []
        )

        # Verificamos si el contenido de behavior es un archivo o un string directo
        if os.path.isfile(behavior):
            with open(behavior, "r") as f:
                behavior_content = f.read()
        else:
            behavior_content = (
                behavior  # Si no es un archivo, asumimos que es un string
            )

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
        console.print(
            f"[bold yellow]⚠[/bold yellow] Project '[bold]{book_path}[/bold]' is already initialized.",
            style="yellow",
        )


cli.add_command(init)

# Add the worldbuilding, outline, chapters, and iterate commands from their respective modules
cli.add_command(worldbuilding)
cli.add_command(outline)
cli.add_command(chapters)
cli.add_command(iterate)
cli.add_command(publish)
cli.add_command(chat)

if __name__ == "__main__":
    cli()
