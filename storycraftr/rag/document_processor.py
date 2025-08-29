"""
Functions to load and chunk Markdown files.
"""

def load_and_chunk_markdown(book_path: str, chunk_size: int, chunk_overlap: int) -> list:
    """
    Loads Markdown files from the given path, chunks them, and returns a list of document chunks.

    :param book_path: The path to the book directory.
    :type book_path: str
    :param chunk_size: The size of each chunk in characters.
    :type chunk_size: int
    :param chunk_overlap: The overlap between chunks in characters.
    :type chunk_overlap: int
    :return: A list of document chunks.
    :rtype: list
    """
    raise NotImplementedError
