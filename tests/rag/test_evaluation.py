import os
import shutil
import tempfile
from pathlib import Path

import pytest
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision, context_recall

# The following imports are based on the project structure outlined in TODO-API-Change.md.
# They assume a certain API for the RAG components.
from storycraftr.rag.document_processor import load_and_chunk_markdown
from storycraftr.rag.embeddings import EmbeddingGenerator

# Assuming the existence of a VectorStore class that abstracts ChromaDB.
from storycraftr.rag.vector_store import VectorStore

# Sample markdown content to be used for creating a test vector store.
# This content is specific enough to test retrieval quality.
SAMPLE_MARKDOWN_CONTENT = """
# Chapter 1: The Dragon's Rest

In the misty valleys of Eldoria, the village of Oakhaven was known for its masterful weavers.
Their tapestries depicted ancient legends, the most prominent being the tale of Ignis, the Ember-Eyed Dragon.
The legend says Ignis sleeps in the heart of the nearby Mount Cinder, kept in slumber by a forgotten lullaby.
Only the lullaby can soothe the beast; any other noise risks waking it and bringing fiery ruin.
"""


@pytest.fixture(scope="module")
def rag_retriever():
    """
    Sets up an in-memory RAG vector store populated with sample markdown content.

    This fixture simulates the document ingestion part of the RAG pipeline, providing
    a retriever (the vector store's query interface) for evaluation tests.
    """
    temp_dir = tempfile.mkdtemp()
    book_path = Path(temp_dir)
    (book_path / "chapters").mkdir()
    (book_path / "chapters" / "chapter-1.md").write_text(SAMPLE_MARKDOWN_CONTENT)

    # 1. Load and chunk documents from the temporary book path.
    # Assuming load_and_chunk_markdown returns a list of objects with a 'page_content' attribute.
    chunks = load_and_chunk_markdown(str(book_path), chunk_size=150, chunk_overlap=30)

    # 2. Initialize the embedding generator.
    embedding_generator = EmbeddingGenerator()

    # 3. Create and populate an in-memory vector store.
    # This assumes VectorStore can be initialized for in-memory use and has an interface
    # compatible with sentence-transformers and methods like `add_documents` and `query`.
    vector_store = VectorStore(embedding_function=embedding_generator, in_memory=True)
    vector_store.add_documents(chunks)

    yield vector_store

    shutil.rmtree(temp_dir)


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set (required for RAGAS evaluation)",
)
def test_rag_retrieval_quality(rag_retriever):
    """
    Tests the RAG retrieval quality using RAGAS context precision and recall.

    This test validates the core of the retrieval system: its ability to find the
    most relevant document chunks for a given query, which is a prerequisite for
    generating high-quality, faithful answers. This aligns with Phase 1.5 of the
    RAG migration plan.
    """
    # 1. Define the evaluation dataset with a question and a ground truth statement.
    data_samples = {
        "question": ["What is the legend of the Ember-Eyed Dragon?"],
        "ground_truth": [
            "The legend of Ignis, the Ember-Eyed Dragon, is that it sleeps in Mount Cinder, "
            "kept asleep by a forgotten lullaby."
        ],
    }
    dataset = Dataset.from_dict(data_samples)

    # 2. Use the rag_retriever fixture to get relevant context for the question.
    question = data_samples["question"][0]
    # Assuming the retriever has a `query` method that returns a list of document chunks.
    retrieved_chunks = rag_retriever.query(question, n_results=2)

    # 3. Format the retrieved contexts for RAGAS.
    # RAGAS expects a list of lists of strings.
    contexts = [[chunk.page_content for chunk in retrieved_chunks]]

    # 4. Create a new dataset containing the question, retrieved contexts, and ground truth.
    eval_dataset = Dataset.from_dict(
        {
            "question": data_samples["question"],
            "contexts": contexts,
            "ground_truth": data_samples["ground_truth"],
        }
    )

    # 5. Evaluate the retrieval quality using RAGAS.
    result = evaluate(
        dataset=eval_dataset,
        metrics=[context_precision, context_recall],
    )

    # 6. Assert that the retrieval scores are above a high threshold.
    assert result is not None
    assert result["context_precision"] > 0.9
    assert result["context_recall"] > 0.9
