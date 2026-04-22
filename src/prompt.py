def build_prompt(query: str, contexts: list[dict]) -> str:
    context_text = "\n\n".join(
        [
            f"[Source: {c['source']} | Chunk: {c['chunk_id']}]\n{c['text']}"
            for c in contexts
        ]
    )

    prompt = f"""
You are a precise AI assistant.

STRICT RULES:
1. Answer ONLY based on the provided context.
2. If the answer is not in the context, say "I cannot find this in the provided context."
3. ALWAYS cite sources in this format: (Source: filename, Chunk: id)
4. Do NOT use external knowledge.

Context:
{context_text}

Question:
{query}

Answer:
"""
    return prompt.strip()