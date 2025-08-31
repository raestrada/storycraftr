import logging
from unittest.mock import MagicMock, patch

import pytest
import chromadb

from storycraftr.agent.agents import ingest_book_data


@pytest.fixture
def mock_chromadb():
    """Fixture to mock chromadb client and collection."""
    with patch(
        "storycraftr.agent.agents.chromadb.PersistentClient"
    ) as mock_client_constructor:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_collection.return_value = mock_collection
        mock_client.list_collections.return_value = []
        mock_client_constructor.return_value = mock_client
        yield mock_client, mock_collection


@patch("storycraftr.agent.agents.load_book_config")
@patch(
    "storycraftr.agent.agents.load_and_chunk_markdown",
    return_value=["chunk1", "chunk2"],
)
@patch("storycraftr.agent.agents.EmbeddingGenerator")
@patch("storycraftr.agent.agents.VectorStore")
def test_ingest_book_data_new_collection(
    mock_vector_store,
    mock_embedding_generator,
    mock_load_and_chunk,
    mock_load_config,
    mock_chromadb,
    caplog,
    tmp_path,
):
    """Test ingestion when no collection exists."""
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client, mock_collection = mock_chromadb
    mock_client.list_collections.return_value = []
    mock_load_config.return_value = MagicMock(chunk_size=800, chunk_overlap=400)

    with caplog.at_level(logging.INFO):
        ingest_book_data(str(book_path))

    assert (
        f"No existing data found. Starting ingestion for '{book_path}'." in caplog.text
    )
    mock_load_config.assert_called_once_with(str(book_path))
    mock_load_and_chunk.assert_called_once_with(str(book_path), 800, 400)
    mock_vector_store.assert_called_once_with(
        str(book_path), embedding_generator=mock_embedding_generator.return_value
    )
    mock_vector_store.return_value.store_documents.assert_called_once_with(
        ["chunk1", "chunk2"]
    )
    assert f"Data ingestion complete for '{book_path}'" in caplog.text


@patch("storycraftr.agent.agents.load_and_chunk_markdown")
def test_ingest_book_data_already_ingested(
    mock_load_and_chunk, mock_chromadb, caplog, tmp_path
):
    """Test ingestion is skipped when data is already present."""
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client, mock_collection = mock_chromadb
    mock_collection.count.return_value = 10

    mock_collection_meta = MagicMock()
    mock_collection_meta.name = "book"
    mock_client.list_collections.return_value = [mock_collection_meta]

    with caplog.at_level(logging.INFO):
        ingest_book_data(str(book_path))

    assert f"Data for '{book_path}' has already been ingested. Skipping." in caplog.text
    mock_load_and_chunk.assert_not_called()


@patch("storycraftr.agent.agents.load_and_chunk_markdown")
def test_ingest_book_data_chromadb_error(
    mock_load_and_chunk, mock_chromadb, caplog, tmp_path
):
    """Test that ingestion is aborted on unexpected ChromaDB error."""
    book_path = tmp_path / "book"
    book_path.mkdir()

    mock_client, mock_collection = mock_chromadb
    mock_client.list_collections.side_effect = chromadb.errors.ChromaError(
        "Some ChromaDB error"
    )

    with caplog.at_level(logging.ERROR):
        ingest_book_data(str(book_path))

    assert (
        "A ChromaDB error occurred while checking collection: Some ChromaDB error"
        in caplog.text
    )
    mock_load_and_chunk.assert_not_called()
