import os
import pytest
from unittest.mock import MagicMock, patch
from storycraftr.rag.vector_store import VectorStore
from storycraftr.rag.models import DocumentChunk
from typing import List


class MockEmbeddingFunction:
    def name(self) -> str:
        """Returns the name of the mock embedding function."""
        return "mock_embedding_function"

    def __call__(self, input: List[str]) -> List[List[float]]:
        # Return a list of dummy embeddings, one for each text
        return [[0.1 * (i + 1)] * 5 for i, _ in enumerate(input)]


@pytest.fixture
def mock_embedding_function():
    """Fixture for a mock embedding function."""
    return MockEmbeddingFunction()


@patch("chromadb.PersistentClient")
def test_vector_store_init(mock_chromadb_client, mock_embedding_function, tmp_path):
    """
    Test that VectorStore initializes correctly and creates a collection.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    book_path = tmp_path / "book"
    book_path.mkdir()
    expected_db_path = os.path.join(book_path, ".chroma")

    store = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )

    mock_chromadb_client.assert_called_once_with(path=expected_db_path)
    mock_client_instance.get_or_create_collection.assert_called_once_with(
        name="book", embedding_function=mock_embedding_function
    )
    assert store.collection is not None


def test_vector_store_init_invalid_path(mock_embedding_function):
    """
    Test that VectorStore raises ValueError for a non-existent directory.
    """
    with pytest.raises(ValueError):
        VectorStore(
            book_path="non_existent_dir", embedding_generator=mock_embedding_function
        )


@patch("chromadb.PersistentClient")
def test_store_documents(mock_chromadb_client, mock_embedding_function, tmp_path):
    """
    Test adding documents to the vector store.
    """
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )

    documents = [
        DocumentChunk(content="doc1 content", metadata={"source": "file1.md"}),
        DocumentChunk(content="doc2 content", metadata={"source": "file2.md"}),
    ]

    store.store_documents(documents)

    assert mock_collection.upsert.call_count == 1
    call_args, call_kwargs = mock_collection.upsert.call_args

    assert "documents" in call_kwargs
    assert "metadatas" in call_kwargs
    assert "ids" in call_kwargs

    assert call_kwargs["documents"] == ["doc1 content", "doc2 content"]
    assert call_kwargs["metadatas"] == [{"source": "file1.md"}, {"source": "file2.md"}]
    assert len(call_kwargs["ids"]) == 2


@patch("chromadb.PersistentClient")
def test_query(mock_chromadb_client, mock_embedding_function, tmp_path):
    """
    Test querying the vector store.
    """
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client_instance = MagicMock()
    mock_collection = MagicMock()

    # Mock query response from ChromaDB
    mock_query_response = {
        "documents": [["queried doc content"]],
        "metadatas": [[{"source": "queried_file.md"}]],
        "distances": [[0.1]],
    }
    mock_collection.query.return_value = mock_query_response

    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )

    query_text = "find this"
    results = store.query(query_text, n_results=1)

    mock_collection.query.assert_called_once_with(query_texts=[query_text], n_results=1)

    assert len(results) == 1
    assert isinstance(results[0], DocumentChunk)
    assert results[0].content == "queried doc content"
    assert results[0].metadata == {"source": "queried_file.md"}


@patch("chromadb.PersistentClient")
def test_store_documents_with_no_documents(
    mock_chromadb_client, mock_embedding_function, tmp_path
):
    """
    Test that store_documents handles an empty list without error.
    """
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )
    store.store_documents([])

    mock_collection.upsert.assert_not_called()


@patch("chromadb.PersistentClient")
def test_query_with_distance_threshold(
    mock_chromadb_client, mock_embedding_function, tmp_path
):
    """
    Test querying with a distance threshold.
    """
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client_instance = MagicMock()
    mock_collection = MagicMock()

    # Mock query response from ChromaDB with varying distances
    mock_query_response = {
        "documents": [["doc1", "doc2", "doc3"]],
        "metadatas": [[{"source": "f1.md"}, {"source": "f2.md"}, {"source": "f3.md"}]],
        "distances": [[0.1, 0.5, 1.2]],
    }
    mock_collection.query.return_value = mock_query_response

    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )

    # Test case 1: Threshold includes 2 results
    results = store.query("find this", n_results=3, distance_threshold=1.0)

    assert len(results) == 2
    assert results[0].content == "doc1"
    assert results[1].content == "doc2"

    # Test case 2: Threshold includes 1 result
    results = store.query("find this", n_results=3, distance_threshold=0.2)
    assert len(results) == 1
    assert results[0].content == "doc1"

    # Test case 3: Threshold includes no results
    results = store.query("find this", n_results=3, distance_threshold=0.05)
    assert len(results) == 0

    assert mock_collection.query.call_count == 3


def test_vector_store_reinitialization(tmp_path, mock_embedding_function):
    """
    Tests that re-initializing a VectorStore with an existing database works.
    This simulates the scenario of running a command multiple times.
    """
    book_path = tmp_path / "book"
    book_path.mkdir()

    # First initialization (creates the DB)
    store1 = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )
    store1.store_documents(
        [DocumentChunk(content="doc1", metadata={"source": "f1.md"})]
    )
    assert store1.count() == 1

    # Second initialization (should load the existing DB without error)
    store2 = VectorStore(
        book_path=str(book_path), embedding_generator=mock_embedding_function
    )
    assert store2.count() == 1
