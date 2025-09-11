import logging
import os
import shutil
import tempfile
from pathlib import Path

import pytest
from datasets import Dataset
from langchain_community.cache import InMemoryCache
from langchain_core.globals import set_llm_cache
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import context_precision, context_recall
from ragas.run_config import RunConfig
from langchain_openai import ChatOpenAI

# The following imports are based on the project structure outlined in TODO-API-Change.md.
# They assume a certain API for the RAG components.
from storycraftr.rag.document_processor import load_and_chunk_markdown
from storycraftr.rag.embeddings import EmbeddingGenerator

# Assuming the existence of a VectorStore class that abstracts ChromaDB.
from storycraftr.rag.vector_store import VectorStore


logger = logging.getLogger(__name__)

# Sample markdown content to be used for creating a test vector store.
# This content is specific enough to test retrieval quality.
SAMPLE_MARKDOWN_CONTENT = """
# Chapter 1: The Dragon's Rest

In the misty valleys of Eldoria, the village of Oakhaven was known for its masterful weavers.
Their tapestries depicted ancient legends, the most prominent being the tale of Ignis, the Ember-Eyed Dragon.
The legend says Ignis sleeps in the heart of the nearby Mount Cinder, kept in slumber by a forgotten lullaby.
Only the lullaby can soothe the beast; any other noise risks waking it and bringing fiery ruin.

The weavers of Oakhaven use moonpetal silk, a material that shimmers with faint light, harvested only
during the twin moons' alignment. This gives their work a unique, ethereal quality. Another tale often
woven is that of the Sunken City of Aeridor, a metropolis of glass spires that was plunged into the sea
by a sorcerer's curse. It is said that on clear nights, the city's light can still be seen from the cliffs.
"""


@pytest.fixture(scope="module")
def rag_retriever():
    """
    Sets up an in-memory RAG vector store populated with sample markdown content.

    This fixture simulates the document ingestion part of the RAG pipeline, providing
    a retriever (the vector store's query interface) for evaluation tests.
    """
    logger.info("Setting up RAG retriever fixture...")
    temp_dir = tempfile.mkdtemp()
    book_path = Path(temp_dir)
    (book_path / "chapters").mkdir()
    (book_path / "chapters" / "chapter-1.md").write_text(SAMPLE_MARKDOWN_CONTENT)

    # 1. Load and chunk documents from the temporary book path.
    # load_and_chunk_markdown returns a list of DocumentChunk objects.
    logger.info("Loading and chunking documents...")
    chunks = load_and_chunk_markdown(str(book_path), chunk_size=300, chunk_overlap=50)

    # 2. Initialize the embedding generator.
    logger.info("Initializing embedding generator...")
    embedding_generator = EmbeddingGenerator()

    # 3. Create and populate the vector store.
    vector_store = VectorStore(
        book_path=str(book_path), embedding_generator=embedding_generator
    )
    logger.info("Storing documents and generating embeddings...")
    vector_store.store_documents(chunks)
    logger.info("RAG retriever setup complete.")

    yield vector_store

    shutil.rmtree(temp_dir)


@pytest.mark.slow
@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY is required for RAGAS evaluation",
)
async def test_rag_retrieval_quality(rag_retriever):
    """
    Tests the RAG retrieval quality using RAGAS context precision and recall.

    This test validates the core of the retrieval system: its ability to find the
    most relevant document chunks for a given query, which is a prerequisite for
    generating high-quality, faithful answers. This aligns with Phase 1.5 of the
    RAG migration plan.
    """
    # Set up caching for LLM calls to speed up subsequent test runs.
    set_llm_cache(InMemoryCache())
    logger.info("Starting RAG retrieval quality test (with LLM caching)...")

    # Allow overriding the OpenAI API base URL and model via environment variables.
    openai_api_base = os.environ.get("OPENAI_API_BASE")
    openai_eval_model = os.environ.get("OPENAI_EVALUATION_MODEL")

    llm_params = {}
    if openai_api_base:
        logger.info(f"Using custom OpenAI API base URL: {openai_api_base}")
        llm_params["base_url"] = openai_api_base
    if openai_eval_model:
        logger.info(f"Using custom OpenAI evaluation model: {openai_eval_model}")
        llm_params["model_name"] = openai_eval_model

    if llm_params:
        chat_open_ai = ChatOpenAI(**llm_params)
        llm = LangchainLLMWrapper(langchain_llm=chat_open_ai)
        context_precision.llm = llm
        context_recall.llm = llm
    # 1. Define a more comprehensive evaluation dataset.
    data_samples = {
        "question": [
            "What is the legend of the Ember-Eyed Dragon?",
            "What material do Oakhaven weavers use?",
            "What happened to the city of Aeridor?",
        ],
        "ground_truth": [
            "The legend of Ignis, the Ember-Eyed Dragon, is that it sleeps in Mount Cinder, kept asleep by a forgotten lullaby.",
            "The weavers use moonpetal silk, which is harvested during the twin moons' alignment and shimmers with faint light.",
            "Aeridor was a city of glass spires that was plunged into the sea by a sorcerer's curse.",
        ],
    }
    dataset = Dataset.from_dict(data_samples)

    # 2. Retrieve contexts for each question in the dataset.
    contexts = []
    for question in data_samples["question"]:
        logger.info(f"Querying vector store for: '{question}'")
        retrieved_chunks = rag_retriever.query(question, n_results=3)
        contexts.append([chunk.content for chunk in retrieved_chunks])

    # 3. Create a new dataset with questions, retrieved contexts, and ground truth.
    eval_dataset = Dataset.from_dict(
        {
            "question": data_samples["question"],
            "contexts": contexts,
            "ground_truth": data_samples["ground_truth"],
        }
    )

    # 5. Evaluate the retrieval quality using RAGAS.
    logger.info("Evaluating retrieval quality with RAGAS (this may take a while)...")
    # Note: Using max_workers=1 to prevent potential asyncio-related deadlocks
    # during evaluation in a synchronous pytest environment.
    run_config = RunConfig(max_workers=1)
    result = evaluate(
        dataset=eval_dataset,
        metrics=[context_precision, context_recall],
        run_config=run_config,
    )
    logger.info("RAGAS evaluation complete.")

    # 6. Assert that the retrieval scores are above a reasonable threshold.
    assert result is not None
    assert result["context_precision"] > 0.7
    assert result["context_recall"] > 0.7
