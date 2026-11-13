#!/usr/bin/env python3
"""
Simple text chunking helper for Nova-Edu.

Splits long textbook extracts into smaller pedagogical units
while trying to respect paragraph boundaries.
"""

from pathlib import Path
import argparse
import re


def split_into_paragraphs(text: str) -> list[str]:
    # Normalize newlines
    text = re.sub(r"\r\n|\r", "\n", text)
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_paragraphs(paragraphs: list[str], max_chars: int = 1200) -> list[str]:
    chunks = []
    current = []
    current_len = 0

    for p in paragraphs:
        p_len = len(p)
        if current and current_len + p_len + 2 > max_chars:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = p_len
        else:
            current.append(p)
            current_len += p_len + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Chunk text into pedagogical units")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("-o", "--output-dir", default="data/chunks", help="Output directory")
    parser.add_argument("--max-chars", type=int, default=1200, help="Max characters per chunk")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    paragraphs = split_into_paragraphs(text)
    chunks = chunk_paragraphs(paragraphs, max_chars=args.max_chars)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks, 1):
        out_path = out_dir / f"chunk_{i:03d}.txt"
        out_path.write_text(chunk, encoding="utf-8")

    print(f"Created {len(chunks)} chunks in {out_dir}")


if __name__ == "__main__":
    main()
