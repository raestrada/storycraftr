import pytest
import requests
from unittest.mock import patch, MagicMock
from storycraftr.rag.embeddings import EmbeddingGenerator

@patch('storycraftr.rag.embeddings.SentenceTransformer')
def test_embedding_generator_init(MockSentenceTransformer):
    """
    Test the initialization of EmbeddingGenerator.
    """
    mock_model = MagicMock()
    MockSentenceTransformer.return_value = mock_model
    
    generator = EmbeddingGenerator(model_name='test-model')
    
    MockSentenceTransformer.assert_called_once_with('test-model')
    assert generator.model is mock_model

import numpy as np

@patch('storycraftr.rag.embeddings.SentenceTransformer')
def test_generate_embeddings(MockSentenceTransformer):
    """
    Test that generate_embeddings calls the model's encode method and returns a list of lists.
    """
    mock_model = MagicMock()
    # sentence-transformers encode returns a numpy array
    mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
    MockSentenceTransformer.return_value = mock_model

    generator = EmbeddingGenerator(model_name='test-model')
    
    documents = ["doc1", "doc2"]
    embeddings = generator.generate_embeddings(documents)
    
    mock_model.encode.assert_called_once_with(documents, convert_to_tensor=False)
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

@patch('storycraftr.rag.embeddings.SentenceTransformer')
def test_embedding_generator_is_callable(MockSentenceTransformer):
    """
    Test that the EmbeddingGenerator is callable and uses generate_embeddings.
    """
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1, 0.2]]
    MockSentenceTransformer.return_value = mock_model

    generator = EmbeddingGenerator(model_name='test-model')
    
    documents = ["doc1"]

    # model.encode is mocked to return a numpy array
    mock_model.encode.return_value = np.array([[0.1, 0.2]])
    
    embeddings = generator(documents) # call it
    
    mock_model.encode.assert_called_once_with(documents, convert_to_tensor=False)
    assert embeddings == [[0.1, 0.2]]


def has_internet_connection():
    """
    Check for an active internet connection by making a request to Hugging Face.

    :return: True if the request is successful, False otherwise.
    :rtype: bool
    """
    try:
        # Use a reliable host that is likely to be up.
        requests.get("https://huggingface.co", timeout=5)
        return True
    except requests.RequestException:
        return False


@pytest.mark.skipif(not has_internet_connection(), reason="No internet connection available")
def test_embedding_generator_with_real_model():
    """
    Test that EmbeddingGenerator can download and use a real model.

    This is an integration test that verifies the end-to-end functionality of
    the EmbeddingGenerator with a live model from sentence-transformers. It will
    be skipped if there is no internet connection.
    """
    generator = EmbeddingGenerator()  # Uses default 'all-MiniLM-L6-v2'
    documents = ["This is a test document.", "This is another test document."]
    embeddings = generator.generate_embeddings(documents)

    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert all(isinstance(e, list) for e in embeddings)
    # The 'all-MiniLM-L6-v2' model generates embeddings of 384 dimensions.
    assert all(len(e) == 384 for e in embeddings)
    assert all(isinstance(val, float) for e in embeddings for val in e)
