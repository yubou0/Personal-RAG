from typing import List
import chromadb


class VectorDB:
    def __init__(self, db_path: str = "./db/chroma", collection_name: str = "rag_collection"):
        """
        Initialize Chroma persistent client and collection.
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def reset(self) -> None:
        """
        Delete all documents in the collection.
        """
        existing = self.collection.get()
        ids = existing.get("ids", [])
        if ids:
            self.collection.delete(ids=ids)
        print("[INFO] Collection reset complete")

    def add_documents(self, chunks: List[dict], embeddings: List[List[float]]) -> None:
        """
        Add chunk records and embeddings to vector DB.

        Each chunk should be:
        {
            "text": "...",
            "source": "file.md",
            "chunk_id": 0
        }
        """
        if not chunks:
            print("[INFO] No chunks to add")
            return

        ids = [f"{chunk['source']}_{chunk['chunk_id']}" for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"[INFO] Added {len(chunks)} chunks to vector DB")

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[dict]:
        """
        Query similar chunks from vector DB.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        retrieved = []
        for doc, meta in zip(documents, metadatas):
            retrieved.append({
                "text": doc,
                "source": meta["source"],
                "chunk_id": meta["chunk_id"]
            })

        return retrieved