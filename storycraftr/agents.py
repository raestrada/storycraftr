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
    console.print(f"[bold blue]Loading all Markdown files from '{book_name}'...[/bold blue]")  # Progress message
    md_files = glob.glob(f'{book_name}/**/*.md', recursive=True)
    console.print(f"[bold green]Loaded {len(md_files)} Markdown files.[/bold green]")  # Success message
    return md_files

# Function to delete an existing assistant
def delete_assistant(name):
    console.print(f"[bold blue]Checking if assistant '{name}' exists for deletion...[/bold blue]")  # Progress message
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"Deleting assistant {name}...")
            client.beta.assistants.delete(assistant_id=assistant.id)
            console.print(f"[bold green]Assistant {name} deleted successfully.[/bold green]")  # Success message
            break

# Function to create or get an assistant
def create_or_get_assistant(name, book_name):
    console.print(f"[bold blue]Searching for existing assistant '{name}'...[/bold blue]")  # Progress message
    assistant = None
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            console.print(f"[bold yellow]Assistant {name} already exists.[/bold yellow]")  # Success message
            return assistant

    # Step 1. Create a vector store for the book
    console.print(f"[bold blue]Creating vector store for '{book_name}'...[/bold blue]")  # Progress message
    vector_store = client.beta.vector_stores.create(name=f"{book_name} Docs")

    # Step 2. Upload Knowledge (Markdown files)
    console.print(f"[bold blue]Uploading knowledge from '{book_name}'...[/bold blue]")  # Progress message
    md_files = load_markdown_files(book_name)

    file_streams = [open(file_path, "rb") for file_path in md_files]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    while file_batch.status == "queued" or file_batch.status == "in_progress":
        console.print(f"[bold yellow]{file_batch.status}...[/bold yellow]")  # Progress message
        time.sleep(1)

    # Step 3. Create the Assistant
    console.print(f"[bold blue]Reading behavior instructions...[/bold blue]")  # Progress message
    with open('behaviors/default.txt', 'r') as file:
        instructions = file.read()

    console.print(f"[bold blue]Creating assistant '{name}'...[/bold blue]")  # Progress message
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        model="gpt-4o",
    )

    # Associate the assistant with the vector store
    console.print(f"[bold blue]Associating assistant '{name}' with vector store...[/bold blue]")  # Progress message
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    console.print(f"[bold green]Assistant '{name}' created successfully.[/bold green]")  # Success message

    return assistant

# Function to create a message in a thread and handle async processing
def create_message(thread_id, content, assistant, file_path=None):
    """
    Create a message in the thread and process it asynchronously using OpenAI completions.
    
    Parameters:
        thread_id (str): The ID of the thread where the message will be created.
        content (str): The content of the prompt for improving or generating text.
        assistant (object): The assistant object with an ID.
        file_path (str, optional): The path to a file to improve or generate content. Defaults to None.
    
    Returns:
        str: The text content generated or improved by the assistant.
    """
    console.print(f"[bold blue]Creating message in thread {thread_id}...[/bold blue]")  # Progress message

    # Prepare the base prompt
    if file_path and os.path.exists(file_path):
        console.print(f"[bold blue]Reading content from {file_path} for improvement...[/bold blue]")  # Progress message
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            # Append the file content to the prompt asking for improvement
            prompt = f"{content}\n\nHere is the existing content to improve:\n{file_content}"
    else:
        console.print(f"[bold blue]Using provided prompt to generate new content...[/bold blue]")  # Progress message
        # If no file, use the original prompt for generating new content
        prompt = content

    # Send the prompt to OpenAI completions API
    console.print("[bold blue]Sending prompt to OpenAI API...[/bold blue]")  # Progress message
    response = client.chat.completions.create(
        model="gpt-4o",  # Adjust model as needed
        messages=[{"role": "user", "content": prompt}]
    )

    # Retrieve the completion result (generated or improved content)
    generated_content = response.choices[0].message.content
    console.print(f"[bold green]Generated content received.[/bold green]")  # Success message

    # If a file path is provided, save the result to the file
    if file_path:
        console.print(f"[bold blue]Saving generated content to {file_path}...[/bold blue]")  # Progress message
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(generated_content)
        console.print(f"[bold green]Content saved successfully to {file_path}.[/bold green]")  # Success message
    
    # Return the generated content
    return generated_content

# Function to get a new thread
def get_thread():
    console.print(f"[bold blue]Creating new thread...[/bold blue]")  # Progress message
    return client.beta.threads.create()

# Function to update the assistant's knowledge with new files
def update_agent_files(book_name, assistant):
    """Update the assistant with new Markdown files from the book."""
    console.print(f"[bold blue]Updating assistant '{assistant.name}' with new files from '{book_name}'...[/bold blue]")  # Progress message
    md_files = load_markdown_files(book_name)

    file_streams = [open(file_path, "rb") for file_path in md_files]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=assistant.vector_store_ids[0],  # Assuming the first vector store is associated
        files=file_streams
    )

    while file_batch.status == "queued" or file_batch.status == "in_progress":
        console.print(f"[bold yellow]{file_batch.status}...[/bold yellow]")  # Progress message
        time.sleep(1)

    console.print(f"[bold green]Files updated successfully in assistant '{assistant.name}'.[/bold green]")  # Success message
