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

@patch('chromadb.PersistentClient')
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

@patch('chromadb.PersistentClient')
def test_store_documents(mock_chromadb_client, mock_embedding_function):
    """
    Test adding documents to the vector store.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(collection_name="test", embedding_generator=mock_embedding_function)
    
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

@patch('chromadb.PersistentClient')
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
    }
    mock_collection.query.return_value = mock_query_response
    
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(collection_name="test", embedding_generator=mock_embedding_function)
    
    query_text = "find this"
    results = store.query(query_text, n_results=1)
    
    mock_collection.query.assert_called_once_with(
        query_texts=[query_text], n_results=1
    )
    
    assert len(results) == 1
    assert isinstance(results[0], DocumentChunk)
    assert results[0].content == "queried doc content"
    assert results[0].metadata == {"source": "queried_file.md"}

@patch('chromadb.PersistentClient')
def test_store_documents_with_no_documents(mock_chromadb_client, mock_embedding_function):
    """
    Test that store_documents handles an empty list without error.
    """
    mock_client_instance = MagicMock()
    mock_collection = MagicMock()
    mock_client_instance.get_or_create_collection.return_value = mock_collection
    mock_chromadb_client.return_value = mock_client_instance

    store = VectorStore(collection_name="test", embedding_generator=mock_embedding_function)
    store.store_documents([])
    
    mock_collection.upsert.assert_not_called()
