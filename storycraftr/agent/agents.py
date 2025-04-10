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
from pathlib import Path
import asyncio

load_dotenv()

console = Console()


def initialize_openai_client(book_path: str):
    """
    Initialize the OpenAI client with the configuration from the book.

    Args:
        book_path (str): Path to the book directory.
    """
    config = load_book_config(book_path)
    # Si no hay configuración o no hay URL específica, usar la URL por defecto
    api_base = getattr(config, 'openai_url', "https://api.openai.com/v1")
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), 
        base_url=api_base
    )
    
    # Verificar si la API es compatible con Assistants
    try:
        # Intentar listar los assistants para verificar la compatibilidad
        client.beta.assistants.list()
        return client
    except Exception as e:
        console.print(
            f"[bold red]Error: The OpenAI API version being used does not support Assistants API. Please ensure you are using a compatible version.[/bold red]"
        )
        console.print(f"[bold red]Error details: {str(e)}[/bold red]")
        raise


def get_vector_store_id_by_name(assistant_name: str, client) -> str:
    """
    Retrieve the vector store ID by the assistant's name.

    Args:
        assistant_name (str): The name of the assistant.
        client (OpenAI): The OpenAI client.

    Returns:
        str: The ID of the vector store associated with the assistant's name, or None if not found.
    """
    try:
        vector_stores = client.vector_stores.list()
    except Exception as e:
        console.print(
            f"[bold red]Error: The OpenAI API version being used does not support vector stores. Please ensure you are using a compatible version.[/bold red]"
        )
        console.print(f"[bold red]Error details: {str(e)}[/bold red]")
        return None

    expected_name = f"{assistant_name} Docs"
    for vector_store in vector_stores.data:
        if vector_store.name == expected_name:
            return vector_store.id

    console.print(
        f"[bold red]No vector store found with name '{expected_name}'.[/bold red]"
    )
    return None


def upload_markdown_files_to_vector_store(
    vector_store_id: str, book_path: str, client, progress: Progress = None, task=None
):
    """
    Upload all Markdown files from the book directory to the specified vector store.

    Args:
        vector_store_id (str): ID of the vector store to upload files to.
        book_path (str): Path to the book's directory containing markdown files.
        client (OpenAI): The OpenAI client.
        progress (Progress, optional): Progress bar object for tracking progress.
        task (Task, optional): Task ID for progress tracking.

    Returns:
        None
    """
    try:
        vector_stores_api = client.vector_stores
    except Exception as e:
        console.print(
            f"[bold red]Error: The OpenAI API version being used does not support vector stores. Please ensure you are using a compatible version.[/bold red]"
        )
        console.print(f"[bold red]Error details: {str(e)}[/bold red]")
        return

    console.print(
        f"[bold blue]Uploading all knowledge files from '{book_path}'...[/bold blue]"
    )
    md_files = load_markdown_files(book_path)

    if not md_files:
        console.print("[bold yellow]No Markdown files found to upload.[/bold yellow]")
        return

    file_streams = [open(file_path, "rb") for file_path in md_files]
    file_batch = vector_stores_api.file_batches.upload_and_poll(
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
    md_files = glob.glob(os.path.join(book_path, "**", "*.md"), recursive=True)

    # Filter files with more than 3 lines
    valid_md_files = []
    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                if sum(1 for _ in file) > 3:
                    valid_md_files.append(file_path)
        except UnicodeDecodeError:
            console.print(f"[bold red]Error reading file: {file_path}[/bold red]")

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
    client = initialize_openai_client(book_path)
    name = os.path.basename(book_path)
    console.print(
        f"[bold blue]Checking if assistant '{name}' exists for deletion...[/bold blue]"
    )

    try:
        assistants = client.assistants.list()
        for assistant in assistants.data:
            if assistant.name == name:
                console.print(f"Deleting assistant {name}...")
                client.assistants.delete(assistant_id=assistant.id)
                console.print(
                    f"[bold green]Assistant {name} deleted successfully.[/bold green]"
                )
                break
    except AttributeError:
        console.print(
            f"[bold red]Error: The OpenAI API version being used does not support assistants. Please ensure you are using a compatible version.[/bold red]"
        )


def create_or_get_assistant(book_path: str):
    """
    Create or get an existing assistant for the book.

    Args:
        book_path (str): Path to the book directory.
    """
    config = load_book_config(book_path)
    client = initialize_openai_client(book_path)
    
    # Usar valores por defecto si config es None o no tiene los atributos
    openai_model = "gpt-4" if config is None else getattr(config, 'openai_model', "gpt-4")
    
    # Obtener el contenido del behavior file
    behavior_file = Path(book_path) / "behaviors" / "default.txt"
    if behavior_file.exists():
        behavior_content = behavior_file.read_text(encoding="utf-8")
    else:
        console.print("[red]Behavior file not found.[/red]")
        return None

    # Usar la API de Assistants
    assistants = client.beta.assistants.list(
        order="desc",
        limit=100,
    )
    assistants_api = client.beta.assistants
    vector_stores_api = client.vector_stores

    name = Path(book_path).name
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(
                f"[bold yellow]Assistant {name} already exists.[/bold yellow]"
            )
            return assistant

    try:
        # Crear vector store para file_search
        console.print(f"[bold blue]Creating vector store for {name}...[/bold blue]")
        vector_store = vector_stores_api.create(name=f"{name} Docs")
        
        # Cargar archivos de documentación desde la carpeta storycraftr dentro del book_path
        docs_path = Path(book_path) / "storycraftr"
        if docs_path.exists():
            console.print(f"[bold blue]Loading documentation from {docs_path}...[/bold blue]")
            upload_markdown_files_to_vector_store(vector_store.id, str(docs_path), client)
        else:
            console.print(f"[bold yellow]Documentation folder not found at {docs_path}[/bold yellow]")
        
        # Cargar archivos del libro
        console.print(f"[bold blue]Loading book files from {book_path}...[/bold blue]")
        upload_markdown_files_to_vector_store(vector_store.id, book_path, client)

        # Esperar a que los archivos se carguen completamente
        console.print("[bold blue]Waiting for files to be processed...[/bold blue]")
        time.sleep(5)  # Dar tiempo para que los archivos se procesen

        # Si no existe, crear uno nuevo con las herramientas soportadas
        console.print(f"[bold blue]Creating assistant {name}...[/bold blue]")
        assistant = assistants_api.create(
            name=name,
            instructions=behavior_content,
            model=openai_model,
            tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
            temperature=0.7,  # Nivel de creatividad balanceado
            top_p=1.0,  # Considerar todas las opciones
        )

        # Asociar el vector store con el asistente
        console.print(f"[bold blue]Associating vector store with assistant {name}...[/bold blue]")
        assistants_api.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )

        return assistant
    except Exception as e:
        console.print(f"[bold red]Error creating assistant: {str(e)}[/bold red]")
        raise


def create_message(
    book_path: str,
    thread_id: str,
    content: str,
    assistant,
    file_path: str = None,
    progress: Progress = None,
    task_id=None,
    force_single_answer: bool = False,
) -> str:
    """
    Create a message in the thread and process it asynchronously. If config.multiple_answer is true,
    the assistant response will be requested in parts, iterating until the response is complete.

    Args:
        book_path (str): Path to the book directory.
        thread_id (str): ID of the thread where the message will be created.
        content (str): The content of the message.
        assistant (object): The assistant object with an ID.
        file_path (str, optional): The path to a file to attach as an attachment. Defaults to None.
        progress (Progress, optional): Progress object for tracking. Defaults to None.
        task_id (int, optional): Task ID for the progress bar.
        force_single_answer (bool, optional): If true, forces a single response regardless of config.multiple_answer. Defaults to False.

    Returns:
        str: The generated response text from the assistant, post-processed if multiple_answer is true.
    """
    client = initialize_openai_client(book_path)
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

    # Generar el prompt con hash
    prompt_with_hash = generate_prompt_with_hash(
        content,
        datetime.now().strftime("%B %d, %Y"),
        book_path
    )

    try:
        # Usar la API de Assistants
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=prompt_with_hash
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant.id
        )

        if internal_progress:
            progress.start()

        response_text = ""
        done_flag = "END_OF_RESPONSE"

        # Initial run to get the first part of the response
        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            progress.update(task_id, advance=1)
            time.sleep(0.5)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        response_text = messages.data[0].content[0].text.value

        # Continue iterating if the response is incomplete or if multiple_answer is true
        iter = 0
        while not force_single_answer and (done_flag not in response_text) and iter < 3:
            iter += 1
            if should_print:
                console.print(
                    f"[bold blue]Iteration {iter} of response generation...[/bold blue]"
                )

            # Create a new run to continue the response
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant.id,
                instructions=f"Continue the response from where you left off. If you have finished, end with {done_flag}.",
            )

            # Wait for the run to complete
            while run.status in ["queued", "in_progress"]:
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
                progress.update(task_id, advance=1)
                time.sleep(0.5)

            # Get the updated messages
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            new_response = messages.data[0].content[0].text.value

            # Append the new response to the existing one
            response_text += "\n" + new_response

        if internal_progress:
            progress.stop()

        # Remove the done flag if it exists
        if done_flag in response_text:
            response_text = response_text.replace(done_flag, "")

        return response_text

    except Exception as e:
        console.print(f"[bold red]Error creating message: {str(e)}[/bold red]")
        raise


def get_thread(book_path: str):
    """
    Retrieve or create a new thread.
    
    Args:
        book_path (str): Path to the book directory.
        
    Returns:
        object: The thread object.
    """
    client = initialize_openai_client(book_path)
    try:
        # Intentar con la API beta primero
        thread = client.beta.threads.create()
        return thread
    except AttributeError:
        # Si falla, intentar con la API más reciente
        try:
            thread = client.threads.create()
            return thread
        except Exception as e:
            console.print(
                f"[bold red]Error creating thread: {str(e)}. Please ensure you are using a compatible version of the OpenAI API.[/bold red]"
            )
            # Crear un thread dummy para evitar errores
            class DummyThread:
                def __init__(self):
                    self.id = "dummy_thread_id"
            return DummyThread()


async def delete_file(vector_stores_api, vector_store_id, file_id):
    """Delete a single file from the vector store."""
    try:
        await vector_stores_api.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
    except Exception as e:
        console.print(f"[bold red]Error deleting file {file_id}: {str(e)}[/bold red]")

async def delete_files_in_parallel(vector_stores_api, vector_store_id, files):
    """Delete multiple files from the vector store in parallel."""
    tasks = [
        delete_file(vector_stores_api, vector_store_id, file.id)
        for file in files.data
    ]
    await asyncio.gather(*tasks)

def update_agent_files(book_path: str, assistant):
    """
    Update the assistant's knowledge with new files from the book path.
    
    Args:
        book_path (str): Path to the book directory.
        assistant (object): The assistant object.
    """
    client = initialize_openai_client(book_path)
    assistant_name = assistant.name
    vector_store_id = get_vector_store_id_by_name(assistant_name, client)

    if not vector_store_id:
        console.print(
            f"[bold red]Error: Could not find vector store for assistant '{assistant_name}'.[/bold red]"
        )
        return

    try:
        # Obtener los archivos actuales del vector store
        vector_stores_api = client.vector_stores
        files = vector_stores_api.files.list(vector_store_id=vector_store_id)
        
        # Eliminar archivos en paralelo
        if files.data:
            console.print(f"[bold blue]Deleting {len(files.data)} old files...[/bold blue]")
            asyncio.run(delete_files_in_parallel(vector_stores_api, vector_store_id, files))
        
        # Cargar archivos de documentación
        docs_path = Path(book_path) / "storycraftr"
        if docs_path.exists():
            console.print(f"[bold blue]Loading documentation from {docs_path}...[/bold blue]")
            upload_markdown_files_to_vector_store(vector_store_id, str(docs_path), client)
        else:
            console.print(f"[bold yellow]Documentation folder not found at {docs_path}[/bold yellow]")
        
        # Cargar archivos del libro
        console.print(f"[bold blue]Loading book files from {book_path}...[/bold blue]")
        upload_markdown_files_to_vector_store(vector_store_id, book_path, client)

        console.print(
            f"[bold green]Files updated successfully in assistant '{assistant.name}'.[/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error updating files: {str(e)}[/bold red]")
        raise


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
        save_to_markdown (function): Function to save the output to a markdown file.
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
            thread = get_thread(book_path)

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
