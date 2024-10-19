import os
import click
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.agent.iterate import (
    iterate_check_names,
    fix_name_in_chapters,
    refine_character_motivation,
    strengthen_core_argument,
    insert_new_chapter,
)

console = Console()


@click.group()
def iterate():
    """Iterative refinement commands for StoryCraftr."""
    pass


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", default="Check character names for consistency.")
def check_names(prompt, book_path=None):
    """
    Comando para revisar la consistencia de los nombres de personajes en los capítulos de un libro.
    Los capítulos se encuentran en 'book_path/chapters'.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Iniciando la revisión de consistencia de nombres en los capítulos del libro: {book_path}[/bold blue]"
    )

    # Llamar a la función que revisa los nombres en los capítulos
    iterate_check_names(book_path)

    # Success log
    console.print(f"[green bold]Success![/green bold] Check Names!")


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("original_name")
@click.argument("new_name")
def fix_name(original_name, new_name, book_path=None):
    """
    Comando para cambiar el nombre de un personaje en todos los capítulos del libro.
    Recibe como parámetros el nombre original y el nuevo nombre.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Iniciando el cambio de nombre: '{original_name}' a '{new_name}' en el libro: {book_path}[/bold blue]"
    )

    # Llamar a la función que realiza el cambio de nombres
    fix_name_in_chapters(book_path, original_name, new_name)

    # Success log
    console.print(
        f"[green bold]Cambio de nombre completado de '{original_name}' a '{new_name}' en todos los capítulos![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("character_name")
@click.argument("story_context")
def refine_motivation(character_name, story_context, book_path=None):
    """
    Command to refine the motivations of a character across all chapters of the book.
    It takes the character's name and the story context as parameters.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Starting motivation refinement for '{character_name}' in the book: {book_path}[/bold blue]"
    )

    # Call the function to refine the character's motivations
    refine_character_motivation(book_path, character_name, story_context)

    # Success log
    console.print(
        f"[green bold]Refinement completed for the character '{character_name}' across all chapters![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("argument")
def strengthen_argument(argument, book_path=None):
    """
    Command to ensure the core argument of the story is strong and clear across all chapters.
    Takes the argument as a parameter.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Starting to strengthen the core argument: '{argument}' in the book: {book_path}[/bold blue]"
    )

    # Call the function to strengthen the core argument in the chapters
    strengthen_core_argument(book_path, argument)

    # Success log
    console.print(
        f"[green bold]Strengthening the argument '{argument}' completed across all chapters![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("position", type=int)
@click.argument("prompt")
def insert_chapter(position, prompt, book_path=None):
    """
    Command to insert a new chapter at the specified position, shifting existing chapters and renaming them accordingly.
    Adjusts the content of the chapters before and after the insertion, ensuring the new chapter fits contextually.
    """
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Inserting a new chapter at position {position} in the book: {book_path}[/bold blue]"
    )

    # Call the function to insert the new chapter and adjust the surrounding chapters
    insert_new_chapter(book_path, position, prompt)

    # Success log
    console.print(
        f"[green bold]Chapter insertion completed at position {position}, and chapters renumbered accordingly![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("position", type=int)
@click.argument("prompt")
def add_flashback(position, prompt, book_path=None):
    """Add a flashback scene between two chapters."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[bold blue]Inserting a new flashback chapter at position {position} in the book: {book_path}[/bold blue]"
    )

    # Call the function to insert the new chapter and adjust the surrounding chapters
    insert_new_chapter(book_path, position, prompt, flashback=True)

    # Success log
    console.print(
        f"[green bold] Flashback Chapter insertion completed at position {position}, and chapters renumbered accordingly![/green bold]"
    )


@iterate.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
@click.argument("chapter_number", type=int)
def split_chapter(prompt, chapter_number, book_path):
    """Split a chapter and adjust the numbering of subsequent chapters."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[yellow]The command 'split-chapter' is not yet implemented.[/yellow]"
    )
    console.print(f"Prompt: {prompt}, Split chapter: {chapter_number}")


@iterate.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def update_plot_points(prompt, book_path):
    """Refine key plot points across the story."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    console.print(
        f"[yellow]The command 'update-plot-points' is not yet implemented.[/yellow]"
    )
    console.print(f"Prompt: {prompt}")


@iterate.command()
@click.option("--book-path", type=click.Path(), help="Path to the book directory")
@click.argument("prompt")
def check_consistency(prompt, book_path):
    """Check for consistency across all chapters and elements of the book."""
    if not book_path:
        book_path = os.getcwd()

    if not load_book_config(book_path):
        return None

    # Placeholder for future retrieval-based consistency check
    console.print(
        f"[yellow]The command 'check-consistency' is not yet implemented.[/yellow]"
    )
    console.print(f"Prompt: {prompt}")
    # Future implementation would involve checking character arcs, plot points, worldbuilding, etc., using retrieval.


if __name__ == "__main__":
    iterate()
