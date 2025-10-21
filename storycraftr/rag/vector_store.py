"""
An abstraction layer for a vector store.
"""
import hashlib
import os
from typing import List

import chromadb

from .models import DocumentChunk, EmbeddingFunction


class VectorStore:
    """
    An abstraction layer for ChromaDB to handle storing and retrieving document chunks.
    """

    def __init__(self, book_path: str, embedding_generator: EmbeddingFunction):
        """
        Initializes the VectorStore.

        :param book_path: The path to the book's root directory.
        :type book_path: str
        :param embedding_generator: An instance of a callable embedding generator.
        :type embedding_generator: EmbeddingFunction
        """
        if not os.path.isdir(book_path):
            raise ValueError(
                f"The provided book path is not a valid directory: {book_path}"
            )

        # Store the ChromaDB database inside the book's directory to make it portable.
        db_path = os.path.join(book_path, ".chroma")
        client = chromadb.PersistentClient(path=db_path)
        # Use a constant collection name as the DB is scoped to the book.
        collection_name = "book"
        self.collection = client.get_or_create_collection(
            name=collection_name, embedding_function=embedding_generator
        )

    def store_documents(self, documents: List[DocumentChunk]):
        """
        Stores document chunks in the vector store.

        :param documents: A list of document chunks to store.
        :type documents: List[DocumentChunk]
        """
        if not documents:
            return

        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [
            hashlib.sha256(
                f"{doc.metadata.get('source', '')}:{doc.content}".encode()
            ).hexdigest()
            for doc in documents
        ]

        self.collection.upsert(documents=contents, metadatas=metadatas, ids=ids)

    def query(
        self, query_text: str, n_results: int = 5, distance_threshold: float = None
    ) -> List[DocumentChunk]:
        """
        Queries the vector store for relevant document chunks.

        :param query_text: The query text.
        :type query_text: str
        :param n_results: The number of results to return.
        :type n_results: int
        :param distance_threshold: Optional distance threshold for filtering results.
                                   ChromaDB uses L2 distance by default, so lower is better.
        :type distance_threshold: float
        :return: A list of relevant document chunks.
        :rtype: List[DocumentChunk]
        """
        results = self.collection.query(query_texts=[query_text], n_results=n_results)

        retrieved_chunks = []
        if results and results.get("documents"):
            # ChromaDB query returns a list of lists, one for each query text.
            # We are only querying with one text.
            docs = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]

            for content, metadata, distance in zip(docs, metadatas, distances):
                if distance_threshold is None or distance <= distance_threshold:
                    retrieved_chunks.append(
                        DocumentChunk(content=content, metadata=metadata)
                    )

        return retrieved_chunks

    def count(self) -> int:
        """
        Returns the number of documents in the collection.

        :return: The number of documents.
        :rtype: int
        """
        return self.collection.count()
