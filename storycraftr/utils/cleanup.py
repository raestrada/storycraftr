from __future__ import annotations

import shutil
from pathlib import Path

from rich.console import Console

console = Console()


def cleanup_vector_stores(book_path: str) -> None:
    """
    Remove the embedded Chroma vector store for the given project path.
    """

    vector_dir = Path(book_path) / "vector_store"
    if vector_dir.exists():
        shutil.rmtree(vector_dir, ignore_errors=True)
        console.print(f"[green]Local vector store removed from {vector_dir}[/green]")
    else:
        console.print(f"[yellow]No vector store found at {vector_dir}[/yellow]")
