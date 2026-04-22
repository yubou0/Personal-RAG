import argparse
import os
from dotenv import load_dotenv
from litellm import completion

from src.embedder import Embedder
from src.vectordb import VectorDB
from src.prompt import build_prompt
from src.retriever import Retriever


def format_sources(results: list[dict]) -> str:
    lines = []
    for r in results:
        lines.append(f"- {r['source']} (chunk {r['chunk_id']})")
    return "\n".join(lines)


def run_query(query: str, top_k: int, model: str):

    retriever = Retriever(top_k=top_k)
    results = retriever.retrieve(query)

    if not results:
        print("No relevant information found.")
        return

    prompt = build_prompt(query, results)

    print("[INFO] Calling LLM...")
    try:
        response = completion(
            model= "gemini/gemini-2.5-flash",
            api_key=os.getenv("LITELLM_API_KEY"),
            base_url=os.getenv("LITELLM_BASE_URL"),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        print("\n=== Answer ===")
        print(answer)

    except Exception as e:
        print(f"[WARNING] LLM call failed: {e}")
        print("\n=== Retrieved Context Preview ===")
        for r in results:
            print(f"\n[Source: {r['source']} | Chunk: {r['chunk_id']}]")
            print(r["text"][:200])

    print("\n=== Sources ===")
    print(format_sources(results))


def interactive_mode(top_k: int, model: str):
    print("Entering interactive mode (type 'exit' to quit)\n")

    while True:
        query = input(">>> ")
        if query.lower() in ["exit", "quit"]:
            break

        run_query(query, top_k, model)
        print("\n" + "-" * 50 + "\n")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="RAG query interface")
    parser.add_argument("--query", type=str, help="Single query mode")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--model", type=str, default="gpt-4o-mini")

    args = parser.parse_args()

    if args.query:
        run_query(args.query, args.top_k, args.model)
    else:
        interactive_mode(args.top_k, args.model)


if __name__ == "__main__":
    main()