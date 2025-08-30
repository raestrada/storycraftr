import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import chromadb
from dotenv import load_dotenv
from openai import APIError, OpenAI
from rich.console import Console
from rich.progress import Progress

from storycraftr.prompts.story.core import FORMAT_OUTPUT
from storycraftr.rag.document_processor import load_and_chunk_markdown
from storycraftr.rag.embeddings import EmbeddingGenerator
from storycraftr.rag.vector_store import VectorStore
from storycraftr.utils.core import generate_prompt_with_hash, load_book_config

load_dotenv()

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def initialize_openai_client(book_path: str):
    """
    Initialize the OpenAI client with the configuration from the book.

    Args:
        book_path (str): Path to the book directory.
    """
    config = load_book_config(book_path)
    # Si no hay configuración o no hay URL específica, usar la URL por defecto
    api_base = getattr(config, "api_base_url", "https://api.openai.com/v1")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=api_base)
    return client


def ingest_book_data(book_path: str):
    """
    Loads all Markdown files from the book directory, chunks them, generates embeddings,
    and stores them in a vector store if not already ingested.

    :param book_path: The path to the book directory.
    """
    logging.info(f"Starting data ingestion check for '{book_path}'.")
    console.print(
        f"[bold blue]Starting data ingestion check for '{book_path}'...[/bold blue]"
    )

    collection_name = Path(book_path).name.replace(" ", "_").lower()

    # Check for existing data without loading the embedding model
    try:
        client = chromadb.PersistentClient()
        collection = client.get_collection(name=collection_name)
        if collection.count() > 0:
            logging.info(f"Data for '{book_path}' has already been ingested. Skipping.")
            console.print(
                f"[bold yellow]Data for '{book_path}' has already been ingested. Skipping.[/bold yellow]"
            )
            return
    except ValueError:
        # Collection does not exist, so we proceed with ingestion.
        logging.info(
            f"Collection for '{collection_name}' not found. Proceeding with ingestion."
        )
        pass
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while checking ChromaDB collection: {e}"
        )
        console.print(
            f"[bold red]An unexpected error occurred with ChromaDB: {e}. Ingestion aborted.[/bold red]"
        )
        return

    logging.info(f"No existing data found. Starting ingestion for '{book_path}'.")
    console.print(
        f"[bold blue]No existing data found. Starting ingestion for '{book_path}'...[/bold blue]"
    )

    config = load_book_config(book_path)

    # 1. Load and chunk documents
    # Use OpenAI's recommended defaults for file search chunking
    chunk_size = getattr(config, "chunk_size", 800)
    chunk_overlap = getattr(config, "chunk_overlap", 400)
    console.print(
        f"Loading and chunking documents with chunk size {chunk_size} and "
        f"overlap {chunk_overlap}..."
    )
    document_chunks = load_and_chunk_markdown(book_path, chunk_size, chunk_overlap)

    if not document_chunks:
        console.print("[bold yellow]No documents found to ingest.[/bold yellow]")
        return

    console.print(f"Found {len(document_chunks)} chunks to process.")

    # 2. Generate embeddings and store in vector store
    console.print("Initializing embedding generator...")
    embedding_generator = EmbeddingGenerator()
    vector_store = VectorStore(
        collection_name=collection_name, embedding_generator=embedding_generator
    )

    console.print("Storing document chunks in the vector store...")
    vector_store.store_documents(document_chunks)

    logging.info(f"Data ingestion complete for '{book_path}'.")
    console.print("[bold green]Data ingestion complete.[/bold green]")


def create_message(
    book_path: str,
    content: str,
    history: List[Dict[str, str]],
    file_path: str = None,
    progress: Progress = None,
    task_id=None,
) -> str:
    """
    Create a message using the Chat Completions API with RAG.

    Args:
        book_path (str): Path to the book directory.
        content (str): The content of the user's message.
        history (List[Dict[str, str]]): A list of previous messages in the conversation.
        file_path (str, optional): The path to a file to include as context. Defaults to None.
        progress (Progress, optional): Progress object for tracking. Defaults to None.
        task_id (int, optional): Task ID for the progress bar.

    Returns:
        str: The generated response text from the model.
    """
    client = initialize_openai_client(book_path)
    config = load_book_config(book_path)

    # 1. Handle file content
    if file_path and os.path.exists(file_path):
        console.print(
            f"[bold blue]Reading content from {file_path} for context...[/bold blue]"
        )
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            content = (
                f"{content}\n\nHere is the existing content to improve:\n{file_content}"
            )

    # 2. Query vector store for relevant context (RAG)
    console.print("Querying vector store for relevant context...")
    embedding_generator = EmbeddingGenerator()
    collection_name = Path(book_path).name.replace(" ", "_").lower()
    vector_store = VectorStore(
        collection_name=collection_name, embedding_generator=embedding_generator
    )

    # The distance_threshold is a configurable value that determines how similar
    # the retrieved documents must be to the query. A lower value means stricter
    # similarity. This value is based on L2 distance.
    distance_threshold = getattr(config, "distance_threshold", 1.2)
    retrieved_chunks = vector_store.query(
        content, n_results=5, distance_threshold=distance_threshold
    )

    if not retrieved_chunks:
        console.print(
            "[bold yellow]Warning: No relevant context found in the book for this query.[/bold yellow]"
        )
        context = "No context was found in the book for this query."
    else:
        context = "\n".join([chunk.content for chunk in retrieved_chunks])
        console.print(f"Retrieved {len(retrieved_chunks)} context chunks.")

    # 3. Construct the prompt
    system_prompt = (
        "You are a helpful assistant. Use the following context from the book to answer "
        "the user's question. If the answer is not in the context, say that you "
        "don't know.\n\n"
        "--- CONTEXT ---\n"
        f"{context}\n"
        "--- END CONTEXT ---\n\n"
        f"{FORMAT_OUTPUT}"
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": content})

    # 4. Call Chat Completions API
    console.print("Calling Chat Completions API...")
    try:
        if progress and task_id:
            progress.update(task_id, description="Generating response...", total=100)

        completion = client.chat.completions.create(
            model=config.model_name,
            messages=messages,
            temperature=0.7,
            top_p=1.0,
        )

        if progress and task_id:
            progress.update(task_id, completed=100)

        response_text = completion.choices[0].message.content
        return response_text

    except APIError as e:
        console.print(f"[bold red]Error calling Chat Completions API: {e}[/bold red]")
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

        for chapter_full_path in files_to_process:
            prompt = prompt_template.format(**prompt_kwargs)

            progress.reset(task_openai)
            # For each chapter, we start with an empty history.
            refined_text = create_message(
                book_path,
                content=prompt,
                history=[],
                progress=progress,
                task_id=task_openai,
                file_path=chapter_full_path,
            )

            relative_path = os.path.relpath(chapter_full_path, book_path)
            save_to_markdown(
                book_path,
                relative_path,
                file_suffix,
                refined_text,
                progress=progress,
                task=task_chapters,
            )
            progress.update(task_chapters, advance=1)

    # Data ingestion should be handled by a separate command.
