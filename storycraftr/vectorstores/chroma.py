from __future__ import annotations

from pathlib import Path
from typing import Optional
import shutil

from langchain_chroma import Chroma
from chromadb import PersistentClient
from chromadb.config import Settings


def build_chroma_store(
    project_path: str,
    embedding_function,
    collection_name: str = "storycraftr",
    persist_subdir: str = "vector_store",
    metadata: Optional[dict] = None,
) -> Chroma:
    """
    Create (or load) a persistent Chroma collection rooted inside the project directory.
    """

    store_path = Path(project_path) / persist_subdir
    store_path.mkdir(parents=True, exist_ok=True)

    settings = Settings(anonymized_telemetry=False)

    try:
        client = PersistentClient(path=str(store_path), settings=settings)
        store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embedding_function,
            collection_metadata=metadata,
        )
        setattr(store, "_persist_directory", str(store_path))
        return store
    except Exception as exc:
        shutil.rmtree(store_path, ignore_errors=True)
        raise RuntimeError(
            f"Failed to initialise Chroma vector store at {store_path}: {exc}"
        ) from exc
