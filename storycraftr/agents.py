import os
import glob
import time
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

load_dotenv()

client = OpenAI()
console = Console()

# Function to load all Markdown files from the book's directory and subdirectories
def load_markdown_files(book_name):
    """Load all Markdown files from the book's directory and subdirectories."""
    md_files = glob.glob(f'{book_name}/**/*.md', recursive=True)
    return md_files

# Function to delete an existing assistant
def delete_assistant(name):
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"Deleting assistant {name}...")
            client.beta.assistants.delete(assistant_id=assistant.id)
            console.print(f"Assistant {name} deleted.")
            break

# Function to create or get an assistant
def create_or_get_assistant(name, book_name):
    assistant = None
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"Assistant {name} already exists.")
            return assistant

    # Step 1. Create a vector store for the book
    console.print(f"Creating vector store for '{book_name}'...")
    vector_store = client.beta.vector_stores.create(name=f"{book_name} Docs")

    # Step 2. Upload Knowledge (Markdown files)
    console.print(f"Uploading knowledge from '{book_name}'...")
    md_files = load_markdown_files(book_name)

    file_streams = [open(file_path, "rb") for file_path in md_files]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    while file_batch.status == "queued" or file_batch.status == "in_progress":
        console.print(f"[bold yellow]{file_batch.status}...[/bold yellow]")
        time.sleep(1)

    # Step 3. Create the Assistant
    with open('behaviors/default.txt', 'r') as file:
        instructions = file.read()

    console.print(f"Creating assistant {name}...")
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        model="gpt-4-turbo",
    )

    # Associate the assistant with the vector store
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    console.print(f"[bold green]Assistant '{name}' created successfully.[/bold green]")

    return assistant

# Function to create a message in a thread and handle async processing
def create_message(thread_id, content, assistant):
    """Create a message in the thread and process it asynchronously."""
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.id
    )

    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    return messages.data[-1].content[0].text.value

# Function to get a new thread
def get_thread():
    return client.beta.threads.create()

# Function to update the assistant's knowledge with new files
def update_agent_files(book_name, assistant):
    """Update the assistant with new Markdown files from the book."""
    console.print(f"Updating assistant '{assistant.name}' with new files from '{book_name}'...")
    md_files = load_markdown_files(book_name)

    file_streams = [open(file_path, "rb") for file_path in md_files]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=assistant.vector_store_ids[0],  # Assuming the first vector store is associated
        files=file_streams
    )

    while file_batch.status == "queued" or file_batch.status == "in_progress":
        console.print(f"[bold yellow]{file_batch.status}...[/bold yellow]")
        time.sleep(1)

    console.print(f"[bold green]Files updated successfully in assistant '{assistant.name}'.[/bold green]")
