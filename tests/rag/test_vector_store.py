import pytest
from unittest.mock import MagicMock, patch
from storycraftr.rag.vector_store import VectorStore
from storycraftr.rag.models import DocumentChunk
from typing import List


class MockEmbeddingFunction:
    def __call__(self, texts: List[str]) -> List[List[float]]:
        # Return a list of dummy embeddings, one for each text
        return [[0.1 * (i + 1)] * 5 for i, _ in enumerate(texts)]


@pytest.fixture
def mock_embedding_function():
    """Fixture for a mock embedding function."""
    return MockEmbeddingFunction()


@patch("chromadb.PersistentClient")
def test_vector_store_init(mock_chromadb_client, mock_embedding_function):
    """
    Test that VectorStore initializes correctly and creates a collection.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    collection_name = "test_collection"

    store = VectorStore(
        collection_name=collection_name, embedding_generator=mock_embedding_function
    )

    mock_client_instance.get_or_create_collection.assert_called_once_with(
        name=collection_name, embedding_function=mock_embedding_function
    )
    assert store.collection is not None


@patch("chromadb.PersistentClient")
def test_store_documents(mock_chromadb_client, mock_embedding_function):
    """
    Test adding documents to the vector store.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        collection_name="test", embedding_generator=mock_embedding_function
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
def test_query(mock_chromadb_client, mock_embedding_function):
    """
    Test querying the vector store.
    """
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
        collection_name="test", embedding_generator=mock_embedding_function
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
    mock_chromadb_client, mock_embedding_function
):
    """
    Test that store_documents handles an empty list without error.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(
        collection_name="test", embedding_generator=mock_embedding_function
    )
    store.store_documents([])

    mock_collection.upsert.assert_not_called()


@patch("chromadb.PersistentClient")
def test_query_with_distance_threshold(mock_chromadb_client, mock_embedding_function):
    """
    Test querying with a distance threshold.
    """
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
        collection_name="test", embedding_generator=mock_embedding_function
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
