import os
from rich.progress import Progress
from rich.console import Console
from storycraftr.prompts.iterate import (
    CHECK_NAMES_PROMPT,
    FIX_NAME_PROMPT,
    REFINE_MOTIVATION_PROMPT,
    STRENGTHEN_ARGUMENT_PROMPT,
    INSERT_CHAPTER_PROMPT,
    REWRITE_SURROUNDING_CHAPTERS_PROMPT,
    INSERT_FLASHBACK_CHAPTER_PROMPT,
    REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT,
    CHECK_CHAPTER_CONSISTENCY_PROMPT,
)
from storycraftr.agent.agents import (
    update_agent_files,
    create_message,
    get_thread,
    create_or_get_assistant,
)
from storycraftr.utils.markdown import save_to_markdown

console = Console()


def check_character_names_consistency(
    book_path, chapter_path, progress, task_id, assistant
):
    """
    Checks for character name consistency in a chapter file.
    Uses an OpenAI assistant to perform the review.
    """

    # Create the prompt with the chapter content
    prompt = CHECK_NAMES_PROMPT

    # Get or create the assistant and the thread
    thread = get_thread()

    # Create the message with the thread_id and assistant
    response = create_message(
        book_path,
        thread_id=thread.id,
        content=prompt,
        assistant=assistant,
        progress=progress,
        task_id=task_id,
        file_path=chapter_path,
    )

    # Advance the task in the OpenAI progress
    progress.update(task_id, advance=1)

    return response


def iterate_check_names(book_path):
    """
    Iterates over all chapters in the directory and checks for name consistency.
    """
    corrections = {}

    # Verificar si el directorio del libro existe
    if not os.path.exists(book_path):
        console.print(
            f"[bold red]El directorio del libro '{book_path}' no existe.[/bold red]"
        )
        return

    chapters_dir = os.path.join(book_path, "chapters")

    # Verificar si el directorio de capítulos existe
    if not os.path.exists(chapters_dir):
        console.print(
            f"[bold red]El directorio de capítulos '{chapters_dir}' no existe.[/bold red]"
        )
        return

    # Get all .md files in the chapters directory
    files_to_process = [f for f in os.listdir(chapters_dir) if f.endswith(".md")]

    if not files_to_process:
        console.print(
            "[bold red]No Markdown (.md) files found in the directory.[/bold red]"
        )
        return corrections

    # Create a rich progress bar
    assistant = create_or_get_assistant(book_path)
    with Progress() as progress:
        # Task to process chapters
        task_chapters = progress.add_task(
            "[cyan]Processing chapters...", total=len(files_to_process)
        )

        for chapter_file in files_to_process:
            chapter_path = os.path.join(chapters_dir, chapter_file)

            # Task for calling OpenAI for each chapter
            task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

            progress.reset(task_openai)

            # Call the function to check name consistency in the chapter
            corrections[chapter_file] = check_character_names_consistency(
                book_path, chapter_path, progress, task_openai, assistant=assistant
            )

            # Save to markdown
            save_to_markdown(
                chapters_dir,
                chapter_file,
                "Character Summary",
                corrections[chapter_file],
                progress,
                task_openai,
            )

            # Advance the chapter processing task
            progress.update(task_chapters, advance=1)

    update_agent_files(book_path, assistant)

    return corrections


def fix_name_in_chapters(book_path, original_name, new_name):
    """
    Function to update character names across all chapters in a book.
    """
    chapters_dir = os.path.join(book_path, "chapters")

    if not os.path.exists(chapters_dir):
        raise FileNotFoundError(
            f"The chapter directory '{chapters_dir}' does not exist."
        )

    files_to_process = [f for f in os.listdir(chapters_dir) if f.endswith(".md")]

    if not files_to_process:
        raise FileNotFoundError(
            "No Markdown (.md) files were found in the chapter directory."
        )

    # Create progress bar
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Processing chapters...", total=len(files_to_process)
        )
        # Task for calling OpenAI for each chapter
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        # Iterate over each chapter file
        for chapter_file in files_to_process:
            chapter_path = os.path.join(chapters_dir, chapter_file)

            # Create the prompt using the defined format
            prompt = FIX_NAME_PROMPT.format(
                original_name=original_name, new_name=new_name
            )

            # Get the assistant and thread
            assistant = create_or_get_assistant(book_path)
            thread = get_thread()

            progress.reset(task_openai)
            # Send the message to perform the name change
            corrected_text = create_message(
                book_path,
                thread_id=thread.id,
                content=prompt,
                assistant=assistant,
                progress=progress,
                task_id=task_openai,
                file_path=chapter_path,
            )

            # Save the corrected chapter
            save_to_markdown(
                book_path,
                os.path.join("chapters", chapter_file),
                "Character Name Update",
                corrected_text,
                progress=progress,
                task=task_openai,
            )

            # Advance the progress bar
            progress.update(task_chapters, advance=1)
    update_agent_files(book_path, assistant)
    return


def process_chapters(
    book_path, prompt_template, task_description, file_suffix, **prompt_kwargs
):
    """
    Generic function to process chapters in a book with a given prompt template.
    """
    chapters_dir = os.path.join(book_path, "chapters")

    if not os.path.exists(chapters_dir):
        raise FileNotFoundError(
            f"The chapter directory '{chapters_dir}' does not exist."
        )

    files_to_process = [f for f in os.listdir(chapters_dir) if f.endswith(".md")]

    if not files_to_process:
        raise FileNotFoundError(
            "No Markdown (.md) files were found in the chapter directory."
        )

    # Create progress bar
    with Progress() as progress:
        task_chapters = progress.add_task(
            f"[cyan]{task_description}", total=len(files_to_process)
        )
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        for chapter_file in files_to_process:
            chapter_path = os.path.join(chapters_dir, chapter_file)

            # Create the prompt using the provided template and kwargs
            prompt = prompt_template.format(**prompt_kwargs)

            # Get the assistant and thread
            assistant = create_or_get_assistant(book_path)
            thread = get_thread()

            progress.reset(task_openai)
            refined_text = create_message(
                book_path,
                thread_id=thread.id,
                content=prompt,
                assistant=assistant,
                progress=progress,
                task_id=task_openai,
                file_path=chapter_path,
            )

            # Save the refined chapter
            save_to_markdown(
                book_path,
                os.path.join("chapters", chapter_file),
                file_suffix,
                refined_text,
                progress=progress,
                task=task_chapters,
            )

            progress.update(task_chapters, advance=1)

    update_agent_files(book_path, assistant)
    return


def refine_character_motivation(book_path, character_name, story_context):
    """
    Function to refine character motivations across all chapters in a book.
    """
    process_chapters(
        book_path,
        prompt_template=REFINE_MOTIVATION_PROMPT,
        task_description="Refining character motivations...",
        file_suffix="Character Motivation Refinement",
        character_name=character_name,
        story_context=story_context,
    )


def strengthen_core_argument(book_path, argument):
    """
    Function to strengthen the core argument across all chapters in a book.
    """
    process_chapters(
        book_path,
        prompt_template=STRENGTHEN_ARGUMENT_PROMPT,
        task_description="Strengthening core argument across chapters...",
        file_suffix="Core Argument Strengthening",
        argument=argument,
    )


def check_consistency_across(book_path, consistency_type):
    """
    Function to check the consistency of chapters in a book.
    """
    process_chapters(
        book_path,
        prompt_template=CHECK_CHAPTER_CONSISTENCY_PROMPT,
        task_description=f"Checking {consistency_type} consistency across chapters...",
        file_suffix=f"{consistency_type} Consistency Check",
        consistency_type=consistency_type,
    )


def insert_new_chapter(book_path, position, prompt, flashback=False):
    """
    Function to insert a new chapter at the specified position, renaming chapters and adjusting content accordingly.
    """
    chapters_dir = os.path.join(book_path, "chapters")

    if not os.path.exists(chapters_dir):
        raise FileNotFoundError(
            f"The chapter directory '{chapters_dir}' does not exist."
        )

    files_to_process = sorted(
        [
            f
            for f in os.listdir(chapters_dir)
            if f.endswith(".md") and f.startswith("chapter-")
        ]
    )

    if len(files_to_process) < position or position < 1:
        raise ValueError(
            f"Invalid position: {position}. Position must be between 1 and {len(files_to_process)}."
        )

    # Create progress bar
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Inserting new chapter and renaming chapters...",
            total=len(files_to_process) + 2,
        )

        # Task for calling OpenAI for each chapter
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        # Adjust the names of the chapters from the insert point onwards
        i = len(files_to_process) - 1
        while i >= position:
            old_chapter_path = os.path.join(chapters_dir, files_to_process[i])
            new_chapter_path = os.path.join(chapters_dir, f"chapter-{i + 2}.md")
            os.rename(old_chapter_path, new_chapter_path)
            progress.update(task_chapters, advance=1)
            i -= 1

        # Get or create the assistant and thread
        assistant = create_or_get_assistant(book_path)
        thread = get_thread()

        prompt = INSERT_FLASHBACK_CHAPTER_PROMPT if flashback else INSERT_CHAPTER_PROMPT

        # Generate new chapter content using context
        prompt_text = prompt.format(prompt=prompt, position=position)
        new_chapter_text = create_message(
            book_path,
            thread_id=thread.id,
            content=prompt_text,
            assistant=assistant,
            progress=progress,
            task_id=task_openai,
            file_path=None,
        )

        # Save the new chapter as the new chapter-{position}.md
        new_chapter_path = os.path.join(chapters_dir, f"chapter-{position}.md")
        save_to_markdown(
            book_path,
            os.path.join("chapters", f"chapter-{position}.md"),
            f"Chapter {position}",
            new_chapter_text,
            progress=progress,
            task=task_chapters,
        )

        progress.update(task_chapters, advance=1)

        # Upload files to retrieval system
        update_agent_files(book_path, assistant)

        # Handle the chapters before and after the insertion point, if they exist
        prev_chapter = None if position == 1 else position - 1
        next_chapter = None if position == len(files_to_process) else position + 1

        # Handle the chapters before and after the insertion point, if they exist
        prev_chapter_path = (
            None
            if position == 1
            else os.path.join(chapters_dir, f"chapter-{position-1}.md")
        )
        next_chapter_path = (
            None
            if position == len(files_to_process)
            else os.path.join(chapters_dir, f"chapter-{position + 1}.md")
        )

        # Rewriting previous and next chapters using retrieval system
        if prev_chapter:
            progress.reset(task_openai)
            rewrite_chapters(
                book_path,
                prev_chapter_path,
                prev_chapter,
                position,
                prompt,
                progress,
                task_openai,
                flashback,
            )

        if next_chapter:
            progress.reset(task_openai)
            rewrite_chapters(
                book_path,
                next_chapter_path,
                next_chapter,
                position,
                prompt,
                progress,
                task_openai,
                flashback,
            )


def rewrite_chapters(
    book_path, path, num, position, prompt, progress, task_chapters, flashback=False
):
    """
    Function to rewrite the chapters before and after the inserted chapter to ensure consistency with the new chapter.
    Utilizes the retrieval system to access the full context of the book without loading chapter contents directly.
    """
    # Get the assistant and thread
    assistant = create_or_get_assistant(book_path)
    thread = get_thread()

    prompt = (
        REWRITE_SURROUNDING_CHAPTERS_FOR_FLASHBACK_PROMPT
        if flashback
        else REWRITE_SURROUNDING_CHAPTERS_PROMPT
    )

    # Rewrite chapters using retrieval context
    rewrite_prompt = prompt.format(prompt=prompt, position=position, chapter=num)

    updated_chapters = create_message(
        book_path,
        thread_id=thread.id,
        content=rewrite_prompt,
        assistant=assistant,
        progress=progress,
        task_id=task_chapters,
        file_path=path,
    )

    # Save the updated chapters back to the markdown files
    save_to_markdown(
        book_path,
        os.path.join("chapters", f"chapter-{num}.md"),
        "Updated chapters with retrieval context",
        updated_chapters,
        progress=progress,
        task=task_chapters,
    )
    progress.update(task_chapters, advance=1)
