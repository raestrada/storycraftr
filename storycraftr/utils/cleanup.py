import os
from pathlib import Path
from rich.console import Console
from storycraftr.agent.agents import initialize_openai_client

console = Console()


def cleanup_vector_stores(book_path: str):
    """
    Delete all vector stores and their files.

    Args:
        book_path (str): Path to the book directory.
    """
    client = initialize_openai_client(book_path)

    try:
        # Intentar con la API beta primero
        vector_stores_api = client.beta.vector_stores
    except AttributeError:
        # Si falla, intentar con la API más reciente
        try:
            vector_stores_api = client.vector_stores
        except AttributeError:
            console.print(
                f"[bold red]Error: The OpenAI API version being used does not support vector stores.[/bold red]"
            )
            return

    # Obtener todos los vector stores
    vector_stores = vector_stores_api.list()

    if not vector_stores.data:
        console.print("[bold yellow]No vector stores found.[/bold yellow]")
        return

    # Eliminar cada vector store y sus archivos
    for vector_store in vector_stores.data:
        try:
            # Obtener los archivos del vector store
            files = vector_stores_api.files.list(vector_store_id=vector_store.id)

            # Eliminar cada archivo
            for file in files.data:
                console.print(f"[bold blue]Deleting file {file.id}...[/bold blue]")
                vector_stores_api.files.delete(
                    vector_store_id=vector_store.id, file_id=file.id
                )

            # Eliminar el vector store
            console.print(
                f"[bold blue]Deleting vector store {vector_store.id}...[/bold blue]"
            )
            vector_stores_api.delete(vector_store_id=vector_store.id)

        except Exception as e:
            console.print(
                f"[bold red]Error deleting vector store {vector_store.id}: {str(e)}[/bold red]"
            )
            continue

    console.print(
        "[bold green]All vector stores and files have been deleted.[/bold green]"
    )
