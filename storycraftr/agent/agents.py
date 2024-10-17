import os
import glob
import time
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.progress import Progress
from storycraftr.prompts.core import FORMAT_OUTPUT
from storycraftr.utils.core import load_book_config, generate_prompt_with_hash

load_dotenv()

client = OpenAI()
console = Console()


def load_markdown_files(book_path):
    """Load all Markdown files from the book's directory and subdirectories."""
    console.print(
        f"[bold blue]Loading all Markdown files from '{book_path}'...[/bold blue]"
    )  # Progress message

    # Find all Markdown files in the directory
    md_files = glob.glob(f"{book_path}/**/*.md", recursive=True)

    # Filter out files with less than 3 lines
    valid_md_files = []
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) > 3:
                valid_md_files.append(file_path)

    console.print(
        f"[bold green]Loaded {len(valid_md_files)} Markdown files with more than 3 lines.[/bold green]"
    )  # Success message

    return valid_md_files


# Function to delete an existing assistant
def delete_assistant(book_path):
    name = book_path.split("/")[-1]
    console.print(
        f"[bold blue]Checking if assistant '{name}' exists for deletion...[/bold blue]"
    )  # Progress message
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"Deleting assistant {name}...")
            client.beta.assistants.delete(assistant_id=assistant.id)
            console.print(
                f"[bold green]Assistant {name} deleted successfully.[/bold green]"
            )  # Success message
            break


# Function to create or get an assistant with optional progress task
def create_or_get_assistant(book_path, progress: Progress = None, task=None):
    name = book_path.split("/")[-1]

    # Progress message for searching an existing assistant
    if progress and task:
        progress.update(
            task, description=f"Searching for existing assistant '{name}'..."
        )
    else:
        console.print(
            f"[bold blue]Searching for existing assistant '{name}'...[/bold blue]"
        )

    assistant = None
    assistants = client.beta.assistants.list()

    for assistant in assistants.data:
        if assistant.name == name:
            # Progress message for found assistant
            if progress and task:
                progress.update(task, description=f"Assistant {name} already exists.")
            else:
                console.print(
                    f"[bold yellow]Assistant {name} already exists.[/bold yellow]"
                )
            return assistant

    # Step 1: Create a vector store for the book
    if progress and task:
        progress.update(task, description=f"Creating vector store for '{book_path}'...")
    else:
        console.print(
            f"[bold blue]Creating vector store for '{book_path}'...[/bold blue]"
        )

    vector_store = client.beta.vector_stores.create(name=f"{name} Docs")

    # Step 2: Upload Knowledge (Markdown files)
    if progress and task:
        progress.update(task, description=f"Uploading knowledge from '{book_path}'...")
    else:
        console.print(
            f"[bold blue]Uploading knowledge from '{book_path}'...[/bold blue]"
        )

    md_files = load_markdown_files(book_path)

    if len(md_files):
        file_streams = [open(file_path, "rb") for file_path in md_files]

        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        while file_batch.status == "queued" or file_batch.status == "in_progress":
            if progress and task:
                progress.update(task, description=f"{file_batch.status}...")
            else:
                console.print(f"[bold yellow]{file_batch.status}...[/bold yellow]")
            time.sleep(1)

    # Step 3: Create the Assistant
    if progress and task:
        progress.update(task, description=f"Reading behavior instructions...")
    else:
        console.print(f"[bold blue]Reading behavior instructions...[/bold blue]")

    with open("behaviors/default.txt", "r") as file:
        instructions = file.read()

    if progress and task:
        progress.update(task, description=f"Creating assistant '{name}'...")
    else:
        console.print(f"[bold blue]Creating assistant '{name}'...[/bold blue]")

    assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        model="gpt-4o",
    )

    # Step 4: Associate the assistant with the vector store
    if progress and task:
        progress.update(
            task, description=f"Associating assistant '{name}' with vector store..."
        )
    else:
        console.print(
            f"[bold blue]Associating assistant '{name}' with vector store...[/bold blue]"
        )

    if len(md_files):
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

    # Success message
    if progress and task:
        progress.update(task, description=f"Assistant '{name}' created successfully.")
    else:
        console.print(
            f"[bold green]Assistant '{name}' created successfully.[/bold green]"
        )

    return assistant


def create_message(
    book_path,
    thread_id,
    content,
    assistant,
    file_path=None,
    progress=None,
    task_id=None,
):
    """
    Create a message in the thread and process it asynchronously.

    Parameters:
        thread_id (str): The ID of the thread where the message will be created.
        content (str): The content of the message.
        assistant (object): The assistant object with an ID.
        file_path (str, optional): The path to a file to attach as an attachment. Defaults to None.
        progress (rich.progress.Progress, optional): Progress object for tracking. Defaults to None.
        task_id (int, optional): Task ID for the progress bar. Required if progress is passed.

    Raises:
        OpenAIError: Custom exception if a problem occurs during the OpenAI request.
    """

    config = load_book_config(book_path)

    # Flag to determine if we should print to the console
    should_print = progress is None

    # Use the provided progress or create a new one if not passed
    internal_progress = False
    if progress is None:
        progress = Progress()
        task_id = progress.add_task(
            "[cyan]Waiting for assistant response...", total=500
        )
        internal_progress = True

    if should_print:
        console.print(
            f"[bold blue]Creating message in thread {thread_id}...[/bold blue]"
        )

    # Prepare the base prompt
    if file_path and os.path.exists(file_path):
        if should_print:
            console.print(
                f"[bold blue]Reading content from {file_path} for improvement...[/bold blue]"
            )
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            # Append the file content to the prompt asking for improvement
            content = (
                f"{content}\n\nHere is the existing content to improve:\n{file_content}"
            )
    else:
        if should_print:
            console.print(
                f"[bold blue]Using provided prompt to generate new content...[/bold blue]"
            )

    try:
        # Send prompt to OpenAI API
        avoid_cache_content = generate_prompt_with_hash(
            f"content\n\n{FORMAT_OUTPUT.format(reference_author=config.reference_author)}"
        )
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=avoid_cache_content
        )

        # Start the assistant run
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant.id
        )
        if should_print:
            console.print("[bold blue]Sending prompt to OpenAI API...[/bold blue]")

        if internal_progress:
            progress.start()

        # Wait for the assistant response while updating the progress bar
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            progress.update(task_id, advance=1)
            time.sleep(0.5)

        if internal_progress:
            progress.stop()

        if should_print:
            console.print(f"[bold green]Generated content received.[/bold green]")

        # Retrieve the list of messages in the thread
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        response_text = messages.data[0].content[0].text.value

        # Check if the response is the same as the original prompt (potential issue with credits)
        if response_text.strip() == content.strip():
            console.print(
                "[bold yellow]Warning: The response matches the original prompt. You might be out of credit.[/bold yellow]"
            )
            raise OpenAIError(
                "The response matches the original prompt. Check your account for credit availability."
            )

        return response_text

    except openai.error.Timeout as e:
        console.print(f"[bold red]OpenAI API request timed out: {e}[/bold red]")
        raise OpenAIError("OpenAI API request timed out. Please try again.")
    except openai.error.APIError as e:
        console.print(f"[bold red]OpenAI API returned an API Error: {e}[/bold red]")
        raise OpenAIError(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        console.print(f"[bold red]OpenAI API request failed to connect: {e}[/bold red]")
        raise OpenAIError(
            f"OpenAI API request failed to connect. Please check your network connection: {e}"
        )
    except openai.error.InvalidRequestError as e:
        console.print(f"[bold red]OpenAI API request was invalid: {e}[/bold red]")
        raise OpenAIError(
            f"OpenAI API request was invalid. Please check your request parameters: {e}"
        )
    except openai.error.AuthenticationError as e:
        console.print(
            f"[bold red]OpenAI API request was not authorized: {e}[/bold red]"
        )
        raise OpenAIError(
            "OpenAI API request was not authorized. Please check your API key or credentials."
        )
    except openai.error.PermissionError as e:
        console.print(f"[bold red]OpenAI API request was not permitted: {e}[/bold red]")
        raise OpenAIError(
            "OpenAI API request was not permitted. Please check your permissions or access level."
        )
    except openai.error.RateLimitError as e:
        console.print(
            f"[bold red]OpenAI API request exceeded rate limit: {e}[/bold red]"
        )
        raise OpenAIError(
            "OpenAI API request exceeded rate limit. Please wait and try again."
        )
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        raise OpenAIError(f"Unexpected error: {e}")


# Function to get a new thread
def get_thread():
    return client.beta.threads.create()


# Function to update the assistant's knowledge with new files
def update_agent_files(book_path, assistant):
    delete_assistant(book_path)
    create_or_get_assistant(book_path)

    console.print(
        f"[bold green]Files updated successfully in assistant '{assistant.name}'.[/bold green]"
    )  # Success message
