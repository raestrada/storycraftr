import pytest
from unittest.mock import patch, MagicMock
from storycraftr.rag.vector_store import VectorStore
from storycraftr.rag.models import DocumentChunk

@pytest.fixture
def mock_embedding_generator():
    """
    Fixture for a mock embedding generator.
    """
    generator = MagicMock()
    # Make it callable
    generator.return_value = [[0.1, 0.2, 0.3]]
    return generator

@patch('chromadb.PersistentClient')
def test_vector_store_init(MockChromaClient, mock_embedding_generator):
    """
    Test initialization of the VectorStore.
    """
    mock_collection = MagicMock()
    MockChromaClient.return_value.get_or_create_collection.return_value = mock_collection

    store = VectorStore(collection_name="test_collection", embedding_generator=mock_embedding_generator)
    
    MockChromaClient.assert_called_once()
    MockChromaClient.return_value.get_or_create_collection.assert_called_once_with(
        name="test_collection",
        embedding_function=mock_embedding_generator
    )
    assert store.collection is mock_collection

@patch('chromadb.PersistentClient')
def test_vector_store_store_documents(MockChromaClient, mock_embedding_generator):
    """
    Test storing documents in the vector store.
    """
    mock_collection = MagicMock()
    MockChromaClient.return_value.get_or_create_collection.return_value = mock_collection
    
    store = VectorStore(collection_name="test_collection", embedding_generator=mock_embedding_generator)
    
    documents = [
        DocumentChunk(page_content="doc1", metadata={"source": "test"}),
        DocumentChunk(page_content="doc2", metadata={"source": "test"}),
    ]
    store.store_documents(documents)
    
    mock_collection.add.assert_called_once()
    args, kwargs = mock_collection.add.call_args
    assert "documents" in kwargs
    assert kwargs["documents"] == ["doc1", "doc2"]
    assert isinstance(kwargs["ids"], list)
    assert len(kwargs["ids"]) == len(documents)

@patch('chromadb.PersistentClient')
def test_vector_store_query(MockChromaClient, mock_embedding_generator):
    """
    Test querying the vector store.
    """
    mock_collection = MagicMock()
    mock_collection.query.return_value = {'documents': [["result1", "result2"]]}
    MockChromaClient.return_value.get_or_create_collection.return_value = mock_collection

    store = VectorStore(collection_name="test_collection", embedding_generator=mock_embedding_generator)
    
    results = store.query("my query", n_results=2)
    
    mock_collection.query.assert_called_once_with(
        query_texts=["my query"],
        n_results=2
    )
    assert results == ["result1", "result2"]
