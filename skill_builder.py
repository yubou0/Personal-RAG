import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from litellm import completion
from src.retriever import Retriever


GLOBAL_QUESTIONS = [
    "What are the main concepts in this AI agent knowledge base?",
    "What frameworks and tools are important?",
    "What are typical agent workflows?",
    "How do agents use memory and tools?",
    "What are current trends in agent systems?",
    "What are best practices?",
    "What are limitations and failure modes?"
]


def normalize_model(model: str) -> str:
    if model == "gemini-2.5-flash":
        return "gemini/gemini-2.5-flash"
    return model


def get_source_files():
    root = Path("data/raw")
    return [f for f in root.iterdir() if f.is_file()]


def extract_source(file_path):
    """
    從文件中抓出 Source 行
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.lower().startswith("source"):
                    return line.strip()
    except:
        pass
    return "Source: Unknown"


def run_query(query, retriever, model):
    results = retriever.retrieve(query)

    context = "\n\n".join([
        f"[Source: {r['source']} | Chunk: {r['chunk_id']}]\n{r['text']}"
        for r in results
    ])

    prompt = f"""
Answer using ONLY the context.

Context:
{context}

Question:
{query}
"""

    response = completion(
        model=model,
        api_key=os.getenv("LITELLM_API_KEY"),
        base_url=os.getenv("LITELLM_BASE_URL"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def generate_body(text, model):
    prompt = f"""
You are an expert technical writer.

Generate a structured Markdown document.

STRICT FORMAT:

## Overview
(<=200 words)

## Core Concepts
(5–15 bullet points)

## Key Trends
(3–10 bullet points)

## Key Entities

## Methodology & Best Practices

## Knowledge Gaps & Limitations

## Example Q&A
(3–5 Q&A pairs)

Rules:
- Do NOT include title
- Do NOT include metadata
- Do NOT include source references

Content:
{text}
"""

    response = completion(
        model=model,
        api_key=os.getenv("LITELLM_API_KEY"),
        base_url=os.getenv("LITELLM_BASE_URL"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Build skill.md")
    parser.add_argument("--output", default="skill.md")
    parser.add_argument("--model", default="gemini-2.5-flash")
    parser.add_argument("--skill-name", default="AI agent")
    args = parser.parse_args()

    model = normalize_model(args.model)
    retriever = Retriever()

    print("[INFO] Running scan...")

    answers = []
    for q in GLOBAL_QUESTIONS:
        print(f"[INFO] {q}")
        ans = run_query(q, retriever, model)
        answers.append(ans)

    combined = "\n\n".join(answers)

    print("[INFO] Generating content...")
    body = generate_body(combined, model)

    files = get_source_files()

    print("[INFO] Assembling document...")

    header = f"# Skill: {args.skill_name}"

    metadata = f"""
## Metadata
- **知識領域**：AI Agent Systems
- **資料來源數量**：{len(files)} 份文件
- **最後更新時間**：{date.today()}
- **適用 Agent 類型**：研究助手 / 技術顧問 / 領域問答機器人
"""

    # 🔥 新版：帶來源的 Source References
    sources = []
    for f in files:
        src = extract_source(f)
        sources.append(f"- {f.name} — {src}")

    sources_text = "\n".join(sources)

    final_doc = f"""{header}

{metadata}

{body}

## Source References
{sources_text}
"""

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_doc.strip())

    print(f"[INFO] Saved to {args.output}")


if __name__ == "__main__":
    main()