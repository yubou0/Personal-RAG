def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: cleaned text
        chunk_size: max characters per chunk
        overlap: overlapping characters between consecutive chunks

    Returns:
        list of chunk strings
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start += chunk_size - overlap

    return chunks


def chunk_document(document: dict, chunk_size: int = 500, overlap: int = 100) -> list[dict]:
    """
    Convert one document into chunk records with metadata.

    Input:
        {
            "text": "...",
            "source": "file.md"
        }

    Output:
        [
            {
                "text": "...",
                "source": "file.md",
                "chunk_id": 0
            },
            ...
        ]
    """
    text = document["text"]
    source = document["source"]

    raw_chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    return [
        {
            "text": chunk,
            "source": source,
            "chunk_id": idx
        }
        for idx, chunk in enumerate(raw_chunks)
    ]