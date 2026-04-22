from pathlib import Path


def load_documents(data_dir: str) -> list[dict]:
    """
    Load .md and .txt files from a directory.

    Returns:
        [
            {
                "text": "...",
                "source": "filename"
            },
            ...
        ]
    """
    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        raise ValueError(f"[ERROR] Directory not found: {data_dir}")

    for file_path in data_path.glob("*"):
        if file_path.suffix.lower() not in [".md", ".txt"]:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            if not text.strip():
                continue  # skip empty file

            documents.append({
                "text": text,
                "source": file_path.name
            })

        except Exception as e:
            print(f"[ERROR] Failed to read {file_path}: {e}")

    print(f"[INFO] Loaded {len(documents)} documents")

    return documents