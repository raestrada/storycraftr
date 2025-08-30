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


def iterate_check_names(book_path: str) -> None:
    """
    Check for name consistency across all chapters in the book.
    The results are saved to markdown files.

    Args:
        book_path (str): The path to the book's directory.
    """
    process_chapters(
        save_to_markdown,
        book_path,
        prompt_template=CHECK_NAMES_PROMPT,
        task_description="Checking name consistency...",
        file_suffix="Name Consistency Check",
    )


def fix_name_in_chapters(book_path: str, original_name: str, new_name: str) -> None:
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
) -> None:
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


def strengthen_core_argument(book_path: str, argument: str) -> None:
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


def check_consistency_across(book_path: str, consistency_type: str) -> None:
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
) -> None:
    """
    Insert a new chapter at a specific position, renumbering subsequent chapters.
    Optionally handles flashbacks and chapter splits.

    Args:
        book_path (str): Path to the book directory.
        position (int): The position to insert the new chapter (1-based index).
        prompt (str): The prompt for generating the new chapter's content.
        flashback (bool): Whether the new chapter is a flashback.
        split (bool): Whether the new chapter is a result of a split.
    """
    chapters_dir = Path(book_path) / "chapters"
    if not chapters_dir.is_dir():
        console.print(
            f"[bold red]Error: Chapters directory not found at '{chapters_dir}'[/bold red]"
        )
        return

    chapter_files = sorted(
        [f for f in chapters_dir.glob("chapter-*.md")],
        key=lambda p: int(p.stem.split("-")[1]),
    )

    # Validate position
    if not (1 <= position <= len(chapter_files) + 1):
        console.print(
            f"[bold red]Error: Invalid position. Must be between 1 and {len(chapter_files) + 1}.[/bold red]"
        )
        return

    # Rename subsequent chapters to make space for the new one
    for i in range(len(chapter_files) - 1, position - 2, -1):
        old_path = chapter_files[i]
        old_num = int(old_path.stem.split("-")[1])
        new_path = old_path.with_name(f"chapter-{old_num + 1}.md")
        old_path.rename(new_path)
        console.print(f"Renamed '{old_path.name}' to '{new_path.name}'")

    # Select the appropriate prompt template
    if flashback:
        prompt_template = INSERT_FLASHBACK_CHAPTER_PROMPT
    elif split:
        prompt_template = INSERT_SPLIT_CHAPTER_PROMPT
    else:
        prompt_template = INSERT_CHAPTER_PROMPT

    full_prompt = prompt_template.format(position=position, prompt=prompt)

    console.print(f"Generating content for new chapter at position {position}...")
    new_chapter_content = create_message(book_path, content=full_prompt, history=[])

    new_chapter_path = chapters_dir / f"chapter-{position}.md"
    with open(new_chapter_path, "w", encoding="utf-8") as f:
        f.write(new_chapter_content)

    console.print(
        f"[bold green]Successfully inserted new chapter: '{new_chapter_path.name}'[/bold green]"
    )

    # Rewrite surrounding chapters for consistency
    console.print("Rewriting surrounding chapters for consistency...")

    # Previous chapter
    if position > 1:
        prev_chapter_path = chapters_dir / f"chapter-{position - 1}.md"
        rewrite_surrounding_chapter(
            book_path,
            prev_chapter_path,
            chapter_num=position - 1,
            position=position,
            flashback=flashback,
            split=split,
        )

    # Next chapter
    next_chapter_path = chapters_dir / f"chapter-{position + 1}.md"
    rewrite_surrounding_chapter(
        book_path,
        next_chapter_path,
        chapter_num=position + 1,
        position=position,
        flashback=flashback,
        split=split,
    )


def rewrite_surrounding_chapter(
    book_path: str,
    chapter_path: Path,
    chapter_num: int,
    position: int,
    flashback: bool,
    split: bool,
) -> None:
    """
    Rewrite a chapter to ensure it fits seamlessly with surrounding chapters,
    especially after an insertion.

    Args:
        book_path (str): The path to the book's directory.
        chapter_path (Path): The path to the chapter file to rewrite.
        chapter_num (int): The number of the chapter being rewritten.
        position (int): The position where a new chapter was inserted.
        flashback (bool): Whether the inserted chapter was a flashback.
        split (bool): Whether the inserted chapter was from a split.
    """
    if not chapter_path.exists():
        console.print(
            f"[bold yellow]Warning: Chapter to rewrite not found: {chapter_path}[/bold yellow]"
        )
        return

    if flashback:
        rewrite_prompt = REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT
    elif split:
        rewrite_prompt = REWRITE_SURROUNDING_CHAPTERS_FOR_SPLIT_PROMPT
    else:
        rewrite_prompt = REWRITE_SURROUNDING_CHAPTERS_PROMPT

    console.print(f"Rewriting '{chapter_path.name}' for consistency...")

    rewritten_content = create_message(
        book_path,
        content=rewrite_prompt,
        history=[],
        file_path=str(chapter_path),
    )

    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(rewritten_content)

    console.print(f"Successfully rewrote '{chapter_path.name}'.")
