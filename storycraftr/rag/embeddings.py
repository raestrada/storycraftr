"""
Handles embedding generation.
"""
from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    A class to handle embedding generation using a sentence-transformer model.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the EmbeddingGenerator.

        :param model_name: The name of the sentence-transformer model to use.
        :type model_name: str
        """
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def generate_embeddings(self, documents: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of documents.

        :param documents: A list of document chunks (strings).
        :type documents: List[str]
        :return: A list of embeddings.
        :rtype: List[List[float]]
        """
        embeddings = self.model.encode(documents, convert_to_tensor=False)
        return embeddings.tolist()

    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Makes the class callable for ChromaDB's embedding function.

        :param input: A list of document chunks (strings).
        :type input: List[str]
        :return: A list of embeddings.
        :rtype: List[List[float]]
        """
        return self.generate_embeddings(input)

    def name(self) -> str:
        """
        Returns the name of the embedding model.
        Required by ChromaDB for embedding function validation.

        :return: The model name.
        :rtype: str
        """
        return self.model_name
