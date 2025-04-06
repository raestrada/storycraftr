import os
import re
import shutil
from pathlib import Path
from storycraftr.agent.agents import (
    create_or_get_assistant,
    get_thread,
    create_message,
)
from rich.console import Console
from rich.progress import Progress

console = Console()


def save_to_markdown(
    book_path, file_name, header, content, progress: Progress = None, task=None
) -> str:
    """
    Save the generated content to a specified markdown file, creating a backup if the file exists.

    Args:
        book_path (str): The path to the book's directory.
        file_name (str): The name of the markdown file to save.
        header (str): The header to add at the beginning of the content.
        content (str): The content to save in the file.
        progress (Progress, optional): Rich Progress object for updating progress.
        task (optional): Task associated with progress for updates.

    Returns:
        str: The path to the saved markdown file.
    """
    file_path = Path(book_path) / file_name
    backup_path = file_path.with_suffix(file_path.suffix + ".back")

    # Create a backup if the file exists
    if file_path.exists():
        if progress and task:
            progress.update(task, description=f"Backing up {file_name}")
        else:
            console.print(
                f"[bold yellow]Backing up {file_path} to {backup_path}...[/bold yellow]"
            )
        shutil.copyfile(file_path, backup_path)

    # Save the new content to the markdown file
    if progress and task:
        progress.update(task, description=f"Saving content to {file_name}")
    else:
        console.print(f"[bold blue]Saving content to {file_path}...[/bold blue]")

    with file_path.open("w", encoding="utf-8") as f:
        f.write(f"# {header}\n\n{content}")

    if progress and task:
        progress.update(task, description=f"Content saved successfully to {file_name}")
    else:
        console.print(
            f"[bold green]Content saved successfully to {file_path}[/bold green]"
        )

    return str(file_path)


def append_to_markdown(book_path, folder_name, file_name, content):
    """
    Append content to an existing markdown file.

    Args:
        book_path (str): The path to the book's directory.
        folder_name (str): The folder where the file is located.
        file_name (str): The name of the markdown file to append to.
        content (str): The content to append.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(book_path) / folder_name / file_name

    if file_path.exists():
        with file_path.open("a", encoding="utf-8") as f:
            f.write(f"\n\n{content}")
        console.print(f"Appended content to {file_path}")
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")


def read_from_markdown(book_path, folder_name, file_name) -> str:
    """
    Read content from the specified markdown file.

    Args:
        book_path (str): The path to the book's directory.
        folder_name (str): The folder where the file is located.
        file_name (str): The name of the markdown file to read from.

    Returns:
        str: The content of the markdown file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(book_path) / folder_name / file_name

    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        console.print(f"Read content from {file_path}")
        return content
    else:
        raise FileNotFoundError(f"File {file_path} does not exist.")


def consolidate_book_md(
    book_path: str, primary_language: str, translate: str = None
) -> str:
    """
    Consolidate all chapters of a book into a single markdown file.

    Args:
        book_path (str): The path to the book's directory.
        primary_language (str): The primary language of the book.
        translate (str, optional): If provided, translates the content to the specified language.

    Returns:
        str: The path to the consolidated markdown file.
    """
    chapters_dir = Path(book_path) / "chapters"
    output_file_name = (
        f"book-{primary_language}.md" if not translate else f"book-{translate}.md"
    )
    output_file_path = Path(book_path) / "book" / output_file_name

    # Ensure the "book" folder exists
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create or get the assistant and thread for translation (if needed)
    assistant = create_or_get_assistant(book_path)
    thread = get_thread(book_path)

    # Collect chapters to process
    files_to_process = []

    # Add cover and back-cover if they exist
    for section in ["cover.md", "back-cover.md"]:
        section_path = chapters_dir / section
        if section_path.exists():
            files_to_process.append(section_path)

    # Add chapters in order
    chapter_files = sorted(
        [f for f in chapters_dir.iterdir() if re.match(r"chapter-\d+\.md", f.name)],
        key=lambda x: int(re.findall(r"\d+", x.name)[0]),
    )
    files_to_process.extend(chapter_files)

    # Add epilogue if it exists
    epilogue_path = chapters_dir / "epilogue.md"
    if epilogue_path.exists():
        files_to_process.append(epilogue_path)

    # Log start of consolidation
    if translate:
        console.print(
            f"Consolidating and translating to [bold]{translate}[/bold] for [bold]{book_path}[/bold]..."
        )
    else:
        console.print(
            f"Consolidating chapters for [bold]{book_path}[/bold] without translation..."
        )

    # Process files and consolidate into one markdown file
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Processing chapters...", total=len(files_to_process)
        )
        task_translation = (
            progress.add_task("[cyan]Translating content...", total=50)
            if translate
            else None
        )
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        with output_file_path.open("w", encoding="utf-8") as consolidated_md:
            for chapter_file in files_to_process:
                progress.update(
                    task_chapters, description=f"Processing {chapter_file.name}..."
                )
                with chapter_file.open("r", encoding="utf-8") as chapter_md:
                    content = chapter_md.read()

                    # Translate content if translation is requested
                    if translate:
                        progress.update(
                            task_translation,
                            description=f"Translating {chapter_file.name}...",
                        )
                        content = create_message(
                            book_path,
                            thread_id=thread.id,
                            content=content,
                            assistant=assistant,
                            progress=progress,
                            task_id=task_openai,
                        )

                    # Write (translated or original) content to consolidated file
                    consolidated_md.write(content)
                    consolidated_md.write("\n\\newpage\n")

                # Update progress for chapters
                progress.update(task_chapters, advance=1)

    # Log completion of consolidation
    progress.update(
        task_chapters,
        description=f"[green bold]Book consolidated[/green bold] at {output_file_path}",
    )

    return str(output_file_path)
