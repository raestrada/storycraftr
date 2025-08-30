import os
from pathlib import Path
from rich.progress import Progress
from rich.console import Console
from storycraftr.prompts.story.iterate import (
    CHECK_NAMES_PROMPT,
    FIX_NAME_PROMPT,
    REFINE_MOTIVATION_PROMPT,
    STRENGTHEN_ARGUMENT_PROMPT,
    INSERT_CHAPTER_PROMPT,
    REWRITE_SURROUNDING_CHAPTERS_PROMPT,
    INSERT_FLASHBACK_CHAPTER_PROMPT,
    REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT,
    CHECK_CHAPTER_CONSISTENCY_PROMPT,
    INSERT_SPLIT_CHAPTER_PROMPT,
    REWRITE_SURROUNDING_CHAPTERS_FOR_SPLIT_PROMPT,
)
from storycraftr.agent.agents import (
    create_message,
    process_chapters,
)
from storycraftr.utils.markdown import save_to_markdown

console = Console()


def iterate_check_names(book_path: str):
    """
    Check for name consistency across all chapters in the book.

    Args:
        book_path (str): The path to the book's directory.

    Returns:
        Corrections made to ensure name consistency.
    """
    corrections = process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=CHECK_NAMES_PROMPT,
        task_description="Checking name consistency...",
        file_suffix="Name Consistency Check",
    )
    return corrections


def fix_name_in_chapters(book_path: str, original_name: str, new_name: str):
    """
    Update character names across all chapters.

    Args:
        book_path (str): The path to the book's directory.
        original_name (str): The original name to be replaced.
        new_name (str): The new name to replace the original.
    """
    process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=FIX_NAME_PROMPT,
        task_description="Updating character names...",
        file_suffix="Character Name Update",
        original_name=original_name,
        new_name=new_name,
    )


def refine_character_motivation(
    book_path: str, character_name: str, story_context: str
):
    """
    Refine the motivations of a character across all chapters.

    Args:
        book_path (str): The path to the book's directory.
        character_name (str): The name of the character to refine.
        story_context (str): The story context to guide the refinement.
    """
    process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=REFINE_MOTIVATION_PROMPT,
        task_description="Refining character motivations...",
        file_suffix="Character Motivation Refinement",
        character_name=character_name,
        story_context=story_context,
    )


def strengthen_core_argument(book_path: str, argument: str):
    """
    Strengthen the core argument across all chapters.

    Args:
        book_path (str): The path to the book's directory.
        argument (str): The core argument to strengthen across the story.
    """
    process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=STRENGTHEN_ARGUMENT_PROMPT,
        task_description="Strengthening core argument across chapters...",
        file_suffix="Core Argument Strengthening",
        argument=argument,
    )


def check_consistency_across(book_path: str, consistency_type: str):
    """
    Check for overall consistency across chapters.

    Args:
        book_path (str): The path to the book's directory.
        consistency_type (str): The type of consistency to check (e.g., plot, character).
    """
    process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=CHECK_CHAPTER_CONSISTENCY_PROMPT,
        task_description=f"Checking {consistency_type} consistency across chapters...",
        file_suffix=f"{consistency_type} Consistency Check",
        consistency_type=consistency_type,
    )


def insert_new_chapter(
    book_path: str,
    position: int,
    prompt: str,
    flashback: bool = False,
    split: bool = False,
):
    # TODO: Refactor this function to use the new RAG-based agent.
    console.print(
        "[bold yellow]Warning: Chapter insertion is disabled during refactoring.[/bold yellow]"
    )
    pass


def rewrite_surrounding_chapter(
    book_path: str,
    chapter_path: Path,
    chapter_num: int,
    position: int,
    flashback: bool,
    split: bool,
    progress: Progress,
    task_chapters,
):
    # TODO: Refactor this function to use the new RAG-based agent.
    console.print(
        "[bold yellow]Warning: Rewriting surrounding chapters is disabled during refactoring.[/bold yellow]"
    )
    pass
