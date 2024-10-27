import os
import click
from rich.console import Console
from storycraftr.utils.core import load_book_config
from storycraftr.agent.story.iterate import (
    iterate_check_names,
    fix_name_in_chapters,
    refine_character_motivation,
    strengthen_core_argument,
    insert_new_chapter,
    check_consistency_across,
)

console = Console()


@click.group()
def iterate():
    """
    Iterative refinement commands for StoryCraftr.
    This command group provides various options to iteratively refine your story.
    """
    pass


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt", default="Check character names for consistency.")
def check_names(prompt: str, book_path: str = None):
    """
    Check the consistency of character names across all chapters of the book.

    Args:
        prompt (str): The prompt to guide the checking of names.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(f"[bold blue]Checking name consistency in: {book_path}[/bold blue]")
    iterate_check_names(book_path)
    console.print(
        f"[green bold]Name consistency check completed successfully![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("original_name")
@click.argument("new_name")
def fix_name(original_name: str, new_name: str, book_path: str = None):
    """
    Change a character's name across all chapters of the book.

    Args:
        original_name (str): The character's original name.
        new_name (str): The new name to replace the original one.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Changing name from '{original_name}' to '{new_name}' in: {book_path}[/bold blue]"
    )
    fix_name_in_chapters(book_path, original_name, new_name)
    console.print(f"[green bold]Name change completed successfully![/green bold]")


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("character_name")
@click.argument("story_context")
def refine_motivation(character_name: str, story_context: str, book_path: str = None):
    """
    Refine a character's motivation across all chapters of the book.

    Args:
        character_name (str): The character's name.
        story_context (str): The story context to refine the motivation within.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Refining motivation for '{character_name}' in: {book_path}[/bold blue]"
    )
    refine_character_motivation(book_path, character_name, story_context)
    console.print(
        f"[green bold]Motivation refinement completed successfully![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("argument")
def strengthen_argument(argument: str, book_path: str = None):
    """
    Strengthen the core argument of the story across all chapters.

    Args:
        argument (str): The core argument of the story to strengthen.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Strengthening the core argument: '{argument}' in: {book_path}[/bold blue]"
    )
    strengthen_core_argument(book_path, argument)
    console.print(f"[green bold]Core argument strengthened successfully![/green bold]")


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("position", type=int)
@click.argument("prompt", type=str)
def insert_chapter(position: int, prompt: str, book_path: str = None):
    """
    Insert a new chapter at the specified position, renaming and shifting existing chapters as needed.

    Args:
        position (int): The position to insert the new chapter.
        prompt (str): The content prompt for the new chapter.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Inserting new chapter at position {position} in: {book_path}[/bold blue]"
    )
    insert_new_chapter(book_path, position, prompt)
    console.print(
        f"[green bold]New chapter inserted successfully at position {position}![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("position", type=int)
@click.argument("prompt")
def add_flashback(position: int, prompt: str, book_path: str = None):
    """
    Add a flashback scene between two chapters.

    Args:
        position (int): The position to insert the flashback scene.
        prompt (str): The content prompt for the flashback.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Inserting flashback at position {position} in: {book_path}[/bold blue]"
    )
    insert_new_chapter(book_path, position, prompt, flashback=True)
    console.print(
        f"[green bold]Flashback inserted successfully at position {position}![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("position", type=int)
@click.argument("prompt")
def split_chapter(position: int, prompt: str, book_path: str = None):
    """
    Split a chapter and adjust the numbering of subsequent chapters.

    Args:
        prompt (str): The content prompt for splitting the chapter.
        chapter_number (int): The chapter to split.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()
    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Inserting flashback at position {position} in: {book_path}[/bold blue]"
    )
    insert_new_chapter(book_path, position, prompt, split=True)
    console.print(
        f"[green bold]Split inserted successfully at position {position}![/green bold]"
    )


@iterate.command()
@click.option(
    "--book-path", type=click.Path(), help="Path to the book directory", required=False
)
@click.argument("prompt")
def check_consistency(prompt: str, book_path: str = None):
    """
    Check the overall consistency of chapters in the book.

    Args:
        prompt (str): The custom prompt for consistency check.
        book_path (str, optional): The path to the book's directory. Defaults to the current working directory.
    """
    book_path = book_path or os.getcwd()

    if not load_book_config(book_path):
        return

    console.print(
        f"[bold blue]Checking overall consistency in: {book_path}[/bold blue]"
    )
    check_consistency_across(book_path, prompt)
    console.print(f"[green bold]Consistency check completed successfully![/green bold]")


if __name__ == "__main__":
    iterate()
