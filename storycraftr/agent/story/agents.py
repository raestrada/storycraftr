import os
import glob
import time
import openai
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.progress import Progress
from storycraftr.prompts.story.core import FORMAT_OUTPUT
from storycraftr.utils.core import load_book_config, generate_prompt_with_hash

load_dotenv()

client = OpenAI()
console = Console()


def get_vector_store_id_by_name(assistant_name: str) -> str:
    """
    Retrieve the vector store ID by the assistant's name.

    Args:
        assistant_name (str): The name of the assistant.

    Returns:
        str: The ID of the vector store associated with the assistant's name, or None if not found.
    """
    vector_stores = client.beta.vector_stores.list()

    expected_name = f"{assistant_name} Docs"
    for vector_store in vector_stores.data:
        if vector_store.name == expected_name:
            return vector_store.id

    console.print(
        f"[bold red]No vector store found with name '{expected_name}'.[/bold red]"
    )
    return None


def upload_markdown_files_to_vector_store(
    vector_store_id: str, book_path: str, progress: Progress = None, task=None
):
    """
    Upload all Markdown files from the book directory to the specified vector store.

    Args:
        vector_store_id (str): ID of the vector store to upload files to.
        book_path (str): Path to the book's directory containing markdown files.
        progress (Progress, optional): Progress bar object for tracking progress.
        task (Task, optional): Task ID for progress tracking.

    Returns:
        None
    """
    console.print(
        f"[bold blue]Uploading all knowledge files from '{book_path}'...[/bold blue]"
    )
    md_files = load_markdown_files(book_path)

    if not md_files:
        console.print("[bold yellow]No Markdown files found to upload.[/bold yellow]")
        return

    file_streams = [open(file_path, "rb") for file_path in md_files]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )

    # Monitor progress
    while file_batch.status in ["queued", "in_progress"]:
        status_message = f"{file_batch.status}..."
        if progress and task:
            progress.update(task, description=status_message)
        else:
            console.print(f"[bold yellow]{status_message}[/bold yellow]")
        time.sleep(1)

    console.print(
        f"[bold green]Files uploaded successfully to vector store '{vector_store_id}'.[/bold green]"
    )


def load_markdown_files(book_path: str) -> list:
    """
    Load all Markdown files from the book's directory.

    Args:
        book_path (str): Path to the book directory.

    Returns:
        list: A list of valid Markdown file paths.
    """
    console.print(
        f"[bold blue]Loading all Markdown files from '{book_path}'...[/bold blue]"
    )
    md_files = glob.glob(f"{book_path}/**/*.md", recursive=True)

    # Filter files with more than 3 lines
    valid_md_files = [
        file_path for file_path in md_files if sum(1 for _ in open(file_path)) > 3
    ]

    console.print(
        f"[bold green]Loaded {len(valid_md_files)} Markdown files with more than 3 lines.[/bold green]"
    )
    return valid_md_files


def delete_assistant(book_path: str):
    """
    Delete an assistant if it exists.

    Args:
        book_path (str): Path to the book directory.

    Returns:
        None
    """
    name = os.path.basename(book_path)
    console.print(
        f"[bold blue]Checking if assistant '{name}' exists for deletion...[/bold blue]"
    )

    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"Deleting assistant {name}...")
            client.beta.assistants.delete(assistant_id=assistant.id)
            console.print(
                f"[bold green]Assistant {name} deleted successfully.[/bold green]"
            )
            break


def create_or_get_assistant(book_path: str, progress: Progress = None, task=None):
    """
    Create or retrieve an assistant for the given book.

    Args:
        book_path (str): Path to the book directory.
        progress (Progress, optional): Progress object for tracking.
        task (Task, optional): Task ID for progress tracking.

    Returns:
        Assistant: The created or retrieved assistant object.
    """
    name = os.path.basename(book_path)
    if progress and task:
        progress.update(
            task, description=f"Searching for existing assistant '{name}'..."
        )
    else:
        console.print(
            f"[bold blue]Searching for existing assistant '{name}'...[/bold blue]"
        )

    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(
                f"[bold yellow]Assistant {name} already exists.[/bold yellow]"
            )
            return assistant

    vector_store = client.beta.vector_stores.create(name=f"{name} Docs")
    upload_markdown_files_to_vector_store(vector_store.id, book_path, progress, task)

    # Read instructions from behaviors
    with open(os.path.join(book_path, "behaviors", "default.txt"), "r") as file:
        instructions = file.read()

    assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "file_search"}],
        model="gpt-4o",
        temperature=0.7,  # Nivel de creatividad balanceado
        top_p=1.0,  # Considerar todas las opciones
    )

    client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    console.print(f"[bold green]Assistant '{name}' created successfully.[/bold green]")
    return assistant


def create_message(
    book_path: str,
    thread_id: str,
    content: str,
    assistant,
    file_path: str = None,
    progress: Progress = None,
    task_id=None,
) -> str:
    """
    Create a message in the thread and process it asynchronously.

    Args:
        book_path (str): Path to the book directory.
        thread_id (str): ID of the thread where the message will be created.
        content (str): The content of the message.
        assistant (object): The assistant object with an ID.
        file_path (str, optional): The path to a file to attach as an attachment. Defaults to None.
        progress (Progress, optional): Progress object for tracking. Defaults to None.
        task_id (int, optional): Task ID for the progress bar.

    Returns:
        str: The generated response text from the assistant.
    """
    config = load_book_config(book_path)
    should_print = progress is None

    internal_progress = False
    if progress is None:
        progress = Progress()
        task_id = progress.add_task("[cyan]Waiting for assistant response...", total=50)
        internal_progress = True

    if should_print:
        console.print(
            f"[bold blue]Creating message in thread {thread_id}...[/bold blue]"
        )

    if file_path and os.path.exists(file_path):
        if should_print:
            console.print(
                f"[bold blue]Reading content from {file_path} for improvement...[/bold blue]"
            )
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            content = (
                f"{content}\n\nHere is the existing content to improve:\n{file_content}"
            )
    else:
        if should_print:
            console.print(
                f"[bold blue]Using provided prompt to generate new content...[/bold blue]"
            )

    try:
        prompt_with_hash = generate_prompt_with_hash(
            f"{FORMAT_OUTPUT.format(reference_author=config.reference_author, language=config.primary_language)}\n\n{content}",
            datetime.now().strftime("%B %d, %Y"),
            book_path=book_path,
        )
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=prompt_with_hash
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant.id
        )
        if internal_progress:
            progress.start()

        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            progress.update(task_id, advance=1)
            time.sleep(0.5)

        if internal_progress:
            progress.stop()

        console.print(f"[bold green]Generated content received.[/bold green]")

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        response_text = messages.data[0].content[0].text.value

        if response_text.strip() == content.strip():
            console.print(
                "[bold yellow]Warning: The response matches the original prompt. You might be out of credit.[/bold yellow]"
            )
            raise Exception(
                "The response matches the original prompt. Check your account for credit availability."
            )

        return response_text

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise


def get_thread() -> object:
    """Retrieve or create a new thread."""
    return client.beta.threads.create()


def update_agent_files(book_path: str, assistant):
    """Update the assistant's knowledge with new files from the book path."""
    assistant_name = assistant.name
    vector_store_id = get_vector_store_id_by_name(assistant_name)

    if not vector_store_id:
        console.print(
            f"[bold red]Error: Could not find vector store for assistant '{assistant_name}'.[/bold red]"
        )
        return

    upload_markdown_files_to_vector_store(vector_store_id, book_path)
    console.print(
        f"[bold green]Files updated successfully in assistant '{assistant.name}'.[/bold green]"
    )


def process_chapters(
    save_to_markdown,
    book_path: str,
    prompt_template: str,
    task_description: str,
    file_suffix: str,
    **prompt_kwargs,
):
    """
    Process each chapter of the book with the given prompt template and generate output.

    Args:
        book_path (str): Path to the book directory.
        prompt_template (str): The template for the prompt.
        task_description (str): Description of the task for progress display.
        file_suffix (str): Suffix for the output file.
        **prompt_kwargs: Additional arguments for the prompt template.
    """
    # Directories to process
    chapters_dir = os.path.join(book_path, "chapters")
    outline_dir = os.path.join(book_path, "outline")
    worldbuilding_dir = os.path.join(book_path, "worldbuilding")

    # Check if directories exist
    for dir_path in [chapters_dir, outline_dir, worldbuilding_dir]:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"The directory '{dir_path}' does not exist.")

    # Files to exclude
    excluded_files = ["cover.md", "back-cover.md"]

    # Get Markdown files from each directory, excluding the unwanted files
    files_to_process = []
    for dir_path in [chapters_dir, outline_dir, worldbuilding_dir]:
        files = [
            f
            for f in os.listdir(dir_path)
            if f.endswith(".md") and f not in excluded_files
        ]
        files_to_process.extend([os.path.join(dir_path, f) for f in files])

    if not files_to_process:
        raise FileNotFoundError(
            "No Markdown (.md) files were found in the chapter directory."
        )

    with Progress() as progress:
        task_chapters = progress.add_task(
            f"[cyan]{task_description}", total=len(files_to_process)
        )
        task_openai = progress.add_task("[green]Calling OpenAI...", total=1)

        for chapter_file in files_to_process:
            chapter_path = os.path.join(chapters_dir, chapter_file)
            prompt = prompt_template.format(**prompt_kwargs)

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
