import os
import json
import click
import storycraftr.templates.folder
from storycraftr.worldbuilding import (
    generate_geography,
    generate_history,
    generate_culture,
    generate_magic_system,
    generate_technology
)
from storycraftr.outline import (
    generate_general_outline,
    generate_character_summary,
    generate_plot_points,
    generate_chapter_synopsis
)
from storycraftr.chapters import (
    generate_chapter,
    generate_cover,
    generate_back_cover,
    generate_epilogue
)
from rich.console import Console

console = Console()

def verify_book_path(book_name=None):
    """Verify if the book path is valid and contains storycraftr.json."""
    if not book_name:
        book_name = os.getcwd()  # Use the current directory if --book-name is not provided
    storycraftr_file = os.path.join(book_name, 'storycraftr.json')

    if not os.path.exists(storycraftr_file):
        raise click.ClickException(f"The file storycraftr.json was not found in the path: {book_name}")

    return book_name

def is_initialized(book_name):
    """Check if the book structure is already initialized."""
    storycraftr_file = os.path.join(book_name, 'storycraftr.json')
    return os.path.exists(storycraftr_file)

# Function to show error if project is not initialized
def project_not_initialized_error(book_name):
    console.print(f"[bold red]✖[/bold red] Project '[bold]{book_name}[/bold]' is not initialized. "
                  f"Run '[bold]storycraftr init {book_name}[/bold]' first.", style="bold red")

# Function to create the folder structure and config file
def init_structure(book_name, primary_language, alternate_languages, default_author, genre):
    # Show initialization start
    console.print(f"[bold blue]Initializing book structure: {book_name}[/bold blue]")
    
    # Iterate over the list and create each file, showing progress
    for file in storycraftr.templates.folder.files_to_create:
        # Build the full file path
        file_path = os.path.join(book_name, file['folder'], file['filename'])

        # Ensure the directory exists
        os.makedirs(os.path.join(book_name, file['folder']), exist_ok=True)

        # Write the content to the file
        with open(file_path, 'w') as f:
            f.write(file['content'])
        
        # Log the created file
        console.log(f"[green]File created:[/green] {file_path}")

    # Create the storycraftr.json file
    config_data = {
        "book_name": book_name,
        "primary_language": primary_language,
        "alternate_languages": alternate_languages,
        "default_author": default_author,
        "genre": genre
    }
    
    config_file = os.path.join(book_name, 'storycraftr.json')
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

    # Log configuration file creation
    console.print(f"[green]Configuration file created:[/green] {config_file}", style="green")
    
    # Confirm completion
    console.print(f"[bold green]✔[/bold green] Project '[bold]{book_name}[/bold]' initialized successfully.", style="bold green")


# Function to load the configuration file
def load_config(book_name):
    config_file = os.path.join(book_name, 'storycraftr.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        project_not_initialized_error(book_name)
        return None


@click.group()
def cli():
    """StoryCraftr CLI - A tool to help you write books using OpenAI."""
    pass


@click.command()
@click.argument("book_name")
@click.option("--primary-language", default="en", help="The primary language for the book (default: 'en').")
@click.option("--alternate-languages", default="", help="Comma-separated list of alternate languages (e.g., 'es,fr').")
@click.option("--author", default="Author Name", help="The default author of the book.")
@click.option("--genre", default="fantasy", help="The genre of the book (default: 'fantasy').")
def init(book_name, primary_language, alternate_languages, author, genre):
    """Initialize the book structure with relevant configuration."""
    if not is_initialized(book_name):
        alternate_languages_list = [lang.strip() for lang in alternate_languages.split(',')] if alternate_languages else []
        init_structure(book_name, primary_language, alternate_languages_list, author, genre)
    else:
        console.print(f"[bold yellow]⚠[/bold yellow] Project '[bold]{book_name}[/bold]' is already initialized.", style="yellow")

cli.add_command(init)

# CLI for worldbuilding
@cli.group()
@click.pass_context
def worldbuilding():
    """Manage worldbuilding aspects of the book."""
    pass

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def geography(prompt):
    """Generate geography details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_geography(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def history(prompt):
    """Generate history details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_history(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def culture(prompt):
    """Generate culture details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_culture(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def magic_system(prompt):
    """Generate magic or science system details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_magic_system(book_name, prompt)

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def technology(prompt):
    """Generate technology details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_technology(book_name, prompt)

# CLI for outline
@cli.group()
@click.pass_context
def outline():
    """Manage outline aspects of the book."""
    pass

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def general_outline(prompt):
    """Generate the general outline of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_general_outline(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def character_summary(prompt):
    """Generate the character summary of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_character_summary(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def plot_points(prompt):
    """Generate the main plot points of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_plot_points(book_name, prompt)

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def chapter_synopsis(prompt):
    """Generate the chapter-by-chapter synopsis of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter_synopsis(book_name, prompt)

# CLI for chapters
@cli.group()
@click.pass_context
def chapters():
    """Manage chapters of the book."""
    pass

@chapters.command()
@click.argument('chapter_number', type=int)
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def chapter(chapter_number, prompt):
    """Generate a new chapter for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter(book_name, chapter_number, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def cover(prompt):
    """Generate the cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_cover(book_name, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def back_cover(prompt):
    """Generate the back cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_back_cover(book_name, prompt)

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
@click.pass_context
def epilogue(prompt):
    """Generate the epilogue of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_epilogue(book_name, prompt)

# Add your specific generation functions here
def generate_geography(book_name, prompt):
    print(f"Generating geography for book: {book_name} with prompt: {prompt}")


if __name__ == "__main__":
    cli()
