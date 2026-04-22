from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize embedding model.
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Convert a list of texts into embeddings.

        Args:
            texts: list of strings

        Returns:
            list of embeddings
        """
        if not texts:
            return []

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """
        Convert a single query string into one embedding vector.
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()