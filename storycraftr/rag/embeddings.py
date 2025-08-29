"""
Handles embedding generation.
"""

class EmbeddingGenerator:
    """
    A class to handle embedding generation using a sentence-transformer model.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingGenerator.

        :param model_name: The name of the sentence-transformer model to use.
        :type model_name: str
        """
        raise NotImplementedError

    def generate_embeddings(self, documents: list) -> list:
        """
        Generates embeddings for a list of documents.

        :param documents: A list of document chunks (strings).
        :type documents: list
        :return: A list of embeddings.
        :rtype: list
        """
        raise NotImplementedError

    def __call__(self, input: list) -> list:
        """
        Makes the class callable for ChromaDB's embedding function.

        :param input: A list of document chunks (strings).
        :type input: list
        :return: A list of embeddings.
        :rtype: list
        """
        return self.generate_embeddings(input)
