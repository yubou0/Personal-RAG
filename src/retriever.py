from src.embedder import Embedder
from src.vectordb import VectorDB


class Retriever:
    def __init__(self, top_k: int = 5):
        self.embedder = Embedder()
        self.db = VectorDB()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        query_embedding = self.embedder.embed_query(query)
        results = self.db.query(query_embedding, top_k=self.top_k)
        return results