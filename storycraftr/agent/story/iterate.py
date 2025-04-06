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
    update_agent_files,
    create_message,
    get_thread,
    create_or_get_assistant,
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
    """
    Insert a new chapter at the specified position and adjust subsequent chapters.

    Args:
        book_path (str): The path to the book's directory.
        position (int): The position to insert the new chapter.
        prompt (str): The prompt to guide chapter generation.
        flashback (bool, optional): If True, the new chapter will be a flashback. Defaults to False.
        split (bool, optional): If True, the new chapter will be a split. Defaults to False.
    """
    chapters_dir = Path(book_path) / "chapters"
    if not chapters_dir.exists():
        raise FileNotFoundError(
            f"The chapter directory '{chapters_dir}' does not exist."
        )

    # Función para extraer el número del capítulo
    def extract_chapter_number(filename):
        # Esto supone que los archivos tienen el formato "chapter-<numero>.md"
        return int(filename.stem.split("-")[1])

    # Ordenar los archivos por el número del capítulo
    files_to_process = sorted(
        [
            f
            for f in chapters_dir.iterdir()
            if f.is_file() and f.suffix == ".md" and f.stem.startswith("chapter-")
        ],
        key=extract_chapter_number,
    )

    if len(files_to_process) < position or position < 1:
        raise ValueError(
            f"Invalid position: {position}. Position must be between 1 and {len(files_to_process)}."
        )

    # Create progress bar for chapter renaming and content insertion
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Inserting new chapter and renaming chapters...",
            total=len(files_to_process) + 2,
        )

        # Renaming chapters from the insert point onward
        for i in range(len(files_to_process) - 1, position - 1, -1):
            old_chapter_path = chapters_dir / files_to_process[i]
            new_chapter_path = chapters_dir / f"chapter-{i + 2}.md"
            old_chapter_path.rename(new_chapter_path)
            progress.update(task_chapters, advance=1)

        # Get or create the assistant and thread
        assistant = create_or_get_assistant(book_path)
        thread = get_thread(book_path)

        # Determine prompt type (flashback or regular chapter)
        prompt_text = (
            INSERT_FLASHBACK_CHAPTER_PROMPT
            if flashback
            else INSERT_SPLIT_CHAPTER_PROMPT if split else INSERT_CHAPTER_PROMPT
        ).format(prompt=prompt, position=position)

        # Generate new chapter content
        new_chapter_text = create_message(
            book_path,
            thread_id=thread.id,
            content=prompt_text,
            assistant=assistant,
            progress=progress,
            task_id=task_chapters,
        )

        # Save the new chapter
        new_chapter_path = chapters_dir / f"chapter-{position}.md"
        save_to_markdown(
            book_path,
            new_chapter_path,
            f"Chapter {position}",
            new_chapter_text,
            progress,
            task_chapters,
        )

        progress.update(task_chapters, advance=1)

        # Upload updated files to the agent's retrieval system
        update_agent_files(book_path, assistant)

        # Rewrite adjacent chapters for consistency
        if position > 1:
            prev_chapter_path = chapters_dir / f"chapter-{position - 1}.md"
            rewrite_surrounding_chapter(
                book_path,
                prev_chapter_path,
                position - 1,
                position,
                flashback,
                split,
                progress,
                task_chapters,
            )

        if position < len(files_to_process):
            next_chapter_path = chapters_dir / f"chapter-{position + 1}.md"
            rewrite_surrounding_chapter(
                book_path,
                next_chapter_path,
                position + 1,
                position,
                flashback,
                split,
                progress,
                task_chapters,
            )


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
    """
    Rewrite chapters adjacent to the inserted chapter for consistency.

    Args:
        book_path (str): The path to the book's directory.
        chapter_path (Path): The path to the chapter file.
        chapter_num (int): The chapter number to rewrite.
        position (int): The position of the inserted chapter.
        flashback (bool): Whether the inserted chapter is a flashback.
        progress (Progress): Progress object for tracking progress.
        task_chapters (Task): Task ID for tracking chapter rewrites.
    """
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    prompt = (
        REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT
        if flashback
        else (
            REWRITE_SURROUNDING_CHAPTERS_FOR_SPLIT_PROMPT
            if split
            else REWRITE_SURROUNDING_CHAPTERS_PROMPT
        )
    ).format(prompt=chapter_num, position=position)

    # Generate the rewritten chapter content
    updated_chapter_text = create_message(
        book_path,
        thread_id=thread.id,
        content=prompt,
        assistant=assistant,
        progress=progress,
        task_id=task_chapters,
        file_path=str(chapter_path),
    )

    # Save the rewritten chapter content
    save_to_markdown(
        book_path,
        chapter_path,
        f"Chapter {chapter_num} (Updated)",
        updated_chapter_text,
        progress,
        task_chapters,
    )

    progress.update(task_chapters, advance=1)
