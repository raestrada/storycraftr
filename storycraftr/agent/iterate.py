import os
from rich.progress import Progress
from rich.console import Console
from storycraftr.prompts.iterate import CHECK_NAMES_PROMPT, FIX_NAME_PROMPT
from storycraftr.agent.agents import create_message, get_thread, create_or_get_assistant
from storycraftr.utils.markdown import save_to_markdown

console = Console()


def check_character_names_consistency(book_name, chapter_path, progress, task_id):
    """
    Checks for character name consistency in a chapter file.
    Uses an OpenAI assistant to perform the review.
    """
    with open(chapter_path, "r") as file:
        chapter_text = file.read()

    # Create the prompt with the chapter content
    prompt = CHECK_NAMES_PROMPT.format(chapter_text=chapter_text)

    # Get or create the assistant and the thread
    assistant = create_or_get_assistant(book_name, progress, task_id)
    thread = get_thread()

    # Create the message with the thread_id and assistant
    response = create_message(
        thread_id=thread.id,
        content=prompt,
        assistant=assistant,
        progress=progress,
        task_id=task_id,
    )

    # Advance the task in the OpenAI progress
    progress.update(task_id, advance=1)

    return response


def iterate_check_names(book_name):
    """
    Iterates over all chapters in the directory and checks for name consistency.
    """
    corrections = {}

    # Verificar si el directorio del libro existe
    if not os.path.exists(book_name):
        console.print(
            f"[bold red]El directorio del libro '{book_name}' no existe.[/bold red]"
        )
        return

    chapters_dir = os.path.join(book_name, "chapters")

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
                book_name, chapter_path, progress, task_openai
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

    return corrections


import os
from rich.progress import Progress
from storycraftr.prompts.iterate import FIX_NAME_PROMPT
from storycraftr.agent.agents import create_message, get_thread, create_or_get_assistant
from storycraftr.utils.markdown import save_to_markdown


def fix_name_in_chapters(book_name, original_name, new_name):
    """
    Function to update character names across all chapters in a book.
    """
    chapters_dir = os.path.join(book_name, "chapters")

    if not os.path.exists(chapters_dir):
        raise FileNotFoundError(
            f"El directorio de capítulos '{chapters_dir}' no existe."
        )

    files_to_process = [f for f in os.listdir(chapters_dir) if f.endswith(".md")]

    if not files_to_process:
        raise FileNotFoundError(
            "No se encontraron archivos Markdown (.md) en el directorio de capítulos."
        )

    # Crear la barra de progreso
    with Progress() as progress:
        task_chapters = progress.add_task(
            "[cyan]Procesando capítulos...", total=len(files_to_process)
        )
        # Task for calling OpenAI for each chapter
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        # Iterar sobre cada archivo de capítulo
        for chapter_file in files_to_process:
            chapter_path = os.path.join(chapters_dir, chapter_file)

            # Leer el contenido del capítulo
            with open(chapter_path, "r") as file:
                chapter_text = file.read()

            # Crear el prompt usando el formato definido
            prompt = FIX_NAME_PROMPT.format(
                original_name=original_name, new_name=new_name, content=chapter_text
            )

            # Obtener el asistente y el thread
            assistant = create_or_get_assistant(book_name)
            thread = get_thread()

            progress.reset(task_openai)
            # Enviar el mensaje para realizar el cambio de nombre
            corrected_text = create_message(
                thread_id=thread.id,
                content=prompt,
                assistant=assistant,
                progress=progress,
                task_id=task_openai,
            )

            # Guardar el capítulo corregido
            save_to_markdown(
                book_name,
                os.path.join("chapters", chapter_file),
                "Character Name Update",
                corrected_text,
                progress=progress,
                task=task_openai,
            )

            # Avanzar en la barra de progreso
            progress.update(task_chapters, advance=1)
