import pytest
from unittest.mock import patch, MagicMock
from storycraftr.rag.embeddings import EmbeddingGenerator

@patch('sentence_transformers.SentenceTransformer')
def test_embedding_generator_init(MockSentenceTransformer):
    """
    Test the initialization of EmbeddingGenerator.
    """
    mock_model = MagicMock()
    MockSentenceTransformer.return_value = mock_model
    
    generator = EmbeddingGenerator(model_name='test-model')
    
    MockSentenceTransformer.assert_called_once_with('test-model')
    assert generator.model is mock_model

@patch('sentence_transformers.SentenceTransformer')
def test_generate_embeddings(MockSentenceTransformer):
    """
    Test that generate_embeddings calls the model's encode method.
    """
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
    MockSentenceTransformer.return_value = mock_model

    generator = EmbeddingGenerator(model_name='test-model')
    
    documents = ["doc1", "doc2"]
    embeddings = generator.generate_embeddings(documents)
    
    mock_model.encode.assert_called_once_with(documents)
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

@patch('sentence_transformers.SentenceTransformer')
def test_embedding_generator_is_callable(MockSentenceTransformer):
    """
    Test that the EmbeddingGenerator is callable and uses generate_embeddings.
    """
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1, 0.2]]
    MockSentenceTransformer.return_value = mock_model

    generator = EmbeddingGenerator(model_name='test-model')
    
    documents = ["doc1"]
    
    # Temporarily mock the method that is not yet implemented
    # to test the __call__ logic itself.
    generator.generate_embeddings = MagicMock(return_value=[[0.1, 0.2]])

    embeddings = generator(documents) # call it
    
    generator.generate_embeddings.assert_called_once_with(documents)
    assert embeddings == [[0.1, 0.2]]
