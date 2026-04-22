import argparse
from pathlib import Path

from src.loaders import load_documents
from src.cleaner import clean_text
from src.chunker import chunk_document
from src.embedder import Embedder
from src.vectordb import VectorDB


RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def save_processed_text(source: str, text: str) -> None:
    """
    Save cleaned text into data/processed as .txt
    Example:
        notes.md -> notes.txt
    """
    processed_path = Path(PROCESSED_DIR)
    processed_path.mkdir(parents=True, exist_ok=True)

    output_name = Path(source).stem + ".txt"
    output_file = processed_path / output_name

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description="Update RAG data index")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the whole vector database"
    )
    args = parser.parse_args()

    print("[INFO] Loading raw documents...")
    documents = load_documents(RAW_DIR)

    if not documents:
        print("[INFO] No documents found in data/raw")
        return

    print("[INFO] Cleaning documents and saving processed text...")
    cleaned_documents = []
    for doc in documents:
        cleaned = clean_text(doc["text"])
        save_processed_text(doc["source"], cleaned)

        cleaned_documents.append({
            "text": cleaned,
            "source": doc["source"]
        })

    print("[INFO] Chunking documents...")
    all_chunks = []
    for doc in cleaned_documents:
        chunks = chunk_document(doc, chunk_size=500, overlap=100)
        all_chunks.extend(chunks)

    print(f"[INFO] Total chunks: {len(all_chunks)}")

    if not all_chunks:
        print("[INFO] No chunks generated")
        return

    print("[INFO] Generating embeddings...")
    embedder = Embedder()
    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = embedder.embed_texts(texts)

    print("[INFO] Writing to vector DB...")
    db = VectorDB()

    if args.rebuild:
        db.reset()

    db.add_documents(all_chunks, embeddings)

    print("[INFO] data_update completed successfully")


if __name__ == "__main__":
    main()