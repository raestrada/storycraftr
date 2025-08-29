"""
Functions to load and chunk Markdown files.
"""
from typing import List
from .models import DocumentChunk

import os

def load_and_chunk_markdown(
    book_path: str, chunk_size: int, chunk_overlap: int
) -> List[DocumentChunk]:
    """
    Loads Markdown files from a directory, chunks them, and returns document chunks.

    This function walks through the given directory, finds all Markdown files,
    reads their content, and splits it into chunks of a specified size with overlap.

    :param book_path: The path to the book directory.
    :param chunk_size: The target size for each chunk in characters.
    :param chunk_overlap: The amount of overlap between chunks in characters.
    :return: A list of DocumentChunk objects.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    markdown_files = []
    for root, _, files in os.walk(book_path):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))

    document_chunks = []
    for file_path in markdown_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            # Skip files that can't be read.
            continue

        if not text:
            continue

        start_index = 0
        while start_index < len(text):
            end_index = start_index + chunk_size
            chunk_content = text[start_index:end_index]

            document_chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    metadata={"source": file_path},
                )
            )

            start_index += chunk_size - chunk_overlap
            if start_index >= len(text):
                break

    return document_chunks
