import re


def clean_text(text: str) -> str:
    """
    Clean raw text while preserving readable structure.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove complete fenced code blocks: ``` ... ```
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # Remove unclosed fenced code blocks: ``` ... (to end of text)
    text = re.sub(r"```.*$", "", text, flags=re.DOTALL)

    # Remove inline code: `...`
    text = re.sub(r"`[^`\n]*`", "", text)

    # Remove markdown markers at line start
    text = re.sub(r"^[ \t]*[#>*\-]+[ \t]?", "", text, flags=re.MULTILINE)

    # Remove trailing spaces
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Collapse repeated spaces/tabs but keep newlines
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()