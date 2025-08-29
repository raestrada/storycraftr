"""
An abstraction layer for a vector store.
"""

class VectorStore:
    """
    An abstraction layer for ChromaDB to handle storing and retrieving document chunks.
    """
    def __init__(self, collection_name: str, embedding_generator):
        """
        Initializes the VectorStore.

        :param collection_name: The name of the collection in ChromaDB.
        :type collection_name: str
        :param embedding_generator: An instance of a callable embedding generator.
        :type embedding_generator: object
        """
        raise NotImplementedError

    def store_documents(self, documents: list):
        """
        Stores document chunks in the vector store.

        :param documents: A list of document chunks to store.
        :type documents: list
        """
        raise NotImplementedError

    def query(self, query_text: str, n_results: int = 5) -> list:
        """
        Queries the vector store for relevant document chunks.

        :param query_text: The query text.
        :type query_text: str
        :param n_results: The number of results to return.
        :type n_results: int
        :return: A list of relevant document chunks.
        :rtype: list
        """
        raise NotImplementedError
