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

def init_structure(book_name, primary_language, alternate_languages, default_author, genre, behavior_content):
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

    # Create 'behaviors' folder inside the root book_name directory
    behaviors_dir = os.path.join(book_name, 'behaviors')
    os.makedirs(behaviors_dir, exist_ok=True)
    
    # Create the default.txt file inside the 'behaviors' folder with the behavior content
    behavior_file = os.path.join(behaviors_dir, 'default.txt')
    with open(behavior_file, 'w') as f:
        f.write(behavior_content)

    # Log behavior file creation
    console.print(f"[green]Behavior file created:[/green] {behavior_file}", style="green")
    
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
@click.option("--behavior", help="Behavior content, either as a string or a path to a file.")
def init(book_name, primary_language, alternate_languages, author, genre, behavior):
    """Initialize the book structure with relevant configuration and behavior content."""
    if not is_initialized(book_name):
        alternate_languages_list = [lang.strip() for lang in alternate_languages.split(',')] if alternate_languages else []
        
        # Verificamos si el contenido de behavior es un archivo o un string directo
        if os.path.isfile(behavior):
            with open(behavior, 'r') as f:
                behavior_content = f.read()
        else:
            behavior_content = behavior  # Si no es un archivo, asumimos que es un string
        
        init_structure(book_name, primary_language, alternate_languages_list, author, genre, behavior_content)
    else:
        console.print(f"[bold yellow]⚠[/bold yellow] Project '[bold]{book_name}[/bold]' is already initialized.", style="yellow")

cli.add_command(init)

# CLI for worldbuilding
@cli.group()
def worldbuilding():
    """Manage worldbuilding aspects of the book."""
    pass

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def geography(prompt, book_name=None):
    """Generate geography details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_geography(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Geography generated successfully.", style="bold green")

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def history(prompt, book_name=None):
    """Generate history details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_history(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] History generated successfully.", style="bold green")

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def culture(prompt, book_name=None):
    """Generate culture details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_culture(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Culture generated successfully.", style="bold green")

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def magic_system(prompt, book_name=None):
    """Generate magic or science system details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_magic_system(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Magic system generated successfully.", style="bold green")

@worldbuilding.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def technology(prompt, book_name=None):
    """Generate technology details for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_technology(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Technology generated successfully.", style="bold green")

# CLI for outline
@cli.group()
def outline():
    """Manage outline aspects of the book."""
    pass

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def general_outline(prompt, book_name=None):
    """Generate the general outline of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_general_outline(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] General outline generated successfully.", style="bold green")

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def character_summary(prompt, book_name=None):
    """Generate the character summary of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_character_summary(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Character summary generated successfully.", style="bold green")

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def plot_points(prompt, book_name=None):
    """Generate the main plot points of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_plot_points(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Plot points generated successfully.", style="bold green")

@outline.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def chapter_synopsis(prompt, book_name=None):
    """Generate the chapter-by-chapter synopsis of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter_synopsis(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Chapter synopsis generated successfully.", style="bold green")

# CLI for chapters
@cli.group()
def chapters():
    """Manage chapters of the book."""
    pass

@chapters.command()
@click.argument('chapter_number', type=int)
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def chapter(chapter_number, prompt):
    """Generate a new chapter for the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_chapter(book_name, chapter_number, prompt)
    console.print(f"[bold green]✔[/bold green] Chapter {chapter_number} generated successfully.", style="bold green")

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def cover(prompt, book_name=None):
    """Generate the cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_cover(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Cover generated successfully.", style="bold green")

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def back_cover(prompt, book_name=None):
    """Generate the back cover of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_back_cover(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Back cover generated successfully.", style="bold green")

@chapters.command()
@click.option('--book-name', type=click.Path(), help='Path to the book directory')
@click.argument('prompt')
def epilogue(prompt, book_name=None):
    """Generate the epilogue of the book."""
    if not book_name:
        book_name = os.getcwd()
    load_config(book_name)
    generate_epilogue(book_name, prompt)
    console.print(f"[bold green]✔[/bold green] Epilogue generated successfully.", style="bold green")


if __name__ == "__main__":
    cli()
