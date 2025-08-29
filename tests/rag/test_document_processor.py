import pytest
import os
import tempfile
from storycraftr.rag.document_processor import load_and_chunk_markdown

@pytest.fixture
def book_path():
    """
    Creates a temporary directory with some markdown files for testing.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy markdown files
        with open(os.path.join(tmpdir, "chapter1.md"), "w") as f:
            f.write("# Chapter 1\n\nThis is the first chapter.")
        with open(os.path.join(tmpdir, "chapter2.md"), "w") as f:
            f.write("# Chapter 2\n\nThis is the second chapter, it is a bit longer to test chunking.")
        # Create a non-markdown file that should be ignored
        with open(os.path.join(tmpdir, "notes.txt"), "w") as f:
            f.write("Some notes.")
        yield tmpdir

def test_load_and_chunk_markdown_loads_files(book_path):
    """
    Test that load_and_chunk_markdown loads and chunks markdown files.
    """
    chunks = load_and_chunk_markdown(book_path, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 0
    assert any("Chapter 1" in chunk.content for chunk in chunks)
    assert any("Chapter 2" in chunk.content for chunk in chunks)
    assert not any("Some notes" in chunk.content for chunk in chunks)

def test_load_and_chunk_markdown_chunking(book_path):
    """
    Test that the chunking mechanism works as expected.
    """
    # Using content from chapter2.md: "# Chapter 2\n\nThis is the second chapter, it is a bit longer to test chunking."
    chunks = load_and_chunk_markdown(book_path, chunk_size=30, chunk_overlap=5)

    # We expect multiple chunks from the files.
    assert len(chunks) > 2

    # This test is somewhat implementation-specific and might need adjustment.
    # We check if one of the chunks has a smaller size than chunk_size.
    assert any(len(chunk.content) <= 30 for chunk in chunks)
