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

# Function to check if the structure is initialized
def is_initialized(book_name):
    return os.path.exists(book_name) and os.path.exists(os.path.join(book_name, 'chapters'))

# Function to show error if project is not initialized
def project_not_initialized_error(book_name):
    console.print(f"[bold red]✖[/bold red] Project '[bold]{book_name}[/bold]' is not initialized. "
                  f"Run '[bold]storycraftr init {book_name}[/bold]' first.", style="bold red")

# Function to create the folder structure and config file
def init_structure(book_name, primary_language, alternate_languages, default_author, genre):
    

    # Iterate over the list and create each file
    for file in storycraftr.templates.folder.files_to_create:
        # Build the full file path
        file_path = os.path.join(book_name, file['folder'], file['filename'])

        # Ensure the directory exists
        os.makedirs(os.path.join(book_name, file['folder']), exist_ok=True)

        # Write the content to the file
        with open(file_path, 'w') as f:
            f.write(file['content'])



    
    # Create the config.json file
    config_data = {
        "book_name": book_name,
        "primary_language": primary_language,
        "alternate_languages": alternate_languages,
        "default_author": default_author,
        "genre": genre
    }
    
    config_file = os.path.join(book_name, 'config.json')
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)
    
    console.print(f"[bold green]✔[/bold green] Project '[bold]{book_name}[/bold]' initialized successfully with configuration.", style="bold green")


# Function to load the configuration file
def load_config(book_name):
    config_file = os.path.join(book_name, 'config.json')
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
@click.argument('book_name')
def worldbuilding(book_name):
    """Manage worldbuilding aspects of the book."""
    pass

@worldbuilding.command()
@click.argument('prompt')
@click.argument('book_name')
def geography(book_name, prompt):
    """Generate geography details for the book."""
    generate_geography(book_name, prompt)

@worldbuilding.command()
@click.argument('prompt')
@click.argument('book_name')
def history(book_name, prompt):
    """Generate history details for the book."""
    generate_history(book_name, prompt)

@worldbuilding.command()
@click.argument('prompt')
@click.argument('book_name')
def culture(book_name, prompt):
    """Generate culture details for the book."""
    generate_culture(book_name, prompt)

@worldbuilding.command()
@click.argument('prompt')
@click.argument('book_name')
def magic_system(book_name, prompt):
    """Generate magic or science system details for the book."""
    generate_magic_system(book_name, prompt)

@worldbuilding.command()
@click.argument('prompt')
@click.argument('book_name')
def technology(book_name, prompt):
    """Generate technology details for the book."""
    generate_technology(book_name, prompt)


# CLI for outline
@cli.group()
@click.argument('book_name')
def outline(book_name):
    """Manage outline aspects of the book."""
    pass

@outline.command()
@click.argument('prompt')
@click.argument('book_name')
def general_outline(book_name, prompt):
    """Generate the general outline of the book."""
    generate_general_outline(book_name, prompt)

@outline.command()
@click.argument('prompt')
@click.argument('book_name')
def character_summary(book_name, prompt):
    """Generate the character summary of the book."""
    generate_character_summary(book_name, prompt)

@outline.command()
@click.argument('prompt')
@click.argument('book_name')
def plot_points(book_name, prompt):
    """Generate the main plot points of the book."""
    generate_plot_points(book_name, prompt)

@outline.command()
@click.argument('prompt')
@click.argument('book_name')
def chapter_synopsis(book_name, prompt):
    """Generate the chapter-by-chapter synopsis of the book."""
    generate_chapter_synopsis(book_name, prompt)


# CLI for chapters
@cli.group()
@click.argument('book_name')
def chapters(book_name):
    """Manage chapters of the book."""
    pass

@chapters.command()
@click.argument('prompt')
@click.argument('chapter_number', type=int)
@click.argument('book_name')
def chapter(book_name, prompt, chapter_number):
    """Generate a new chapter for the book."""
    generate_chapter(book_name, prompt, chapter_number)

@chapters.command()
@click.argument('prompt')
@click.argument('book_name')
def cover(book_name, prompt):
    """Generate the cover of the book."""
    generate_cover(book_name, prompt)

@chapters.command()
@click.argument('prompt')
@click.argument('book_name')
def back_cover(book_name, prompt):
    """Generate the back cover of the book."""
    generate_back_cover(book_name, prompt)

@chapters.command()
@click.argument('prompt')
@click.argument('book_name')
def epilogue(book_name, prompt):
    """Generate the epilogue of the book."""
    generate_epilogue(book_name, prompt)

if __name__ == "__main__":
    cli()
