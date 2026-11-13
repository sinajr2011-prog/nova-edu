#!/usr/bin/env python3
"""
Turn a text chunk into a candidate SFT example (heuristic helper).

This is not magic — it creates a reasonable starting point that a human
(or a stronger model) should still review and improve.
"""

import argparse
import json
from pathlib import Path

from build_sft_example import make_example, save_jsonl
from normalize_persian import normalize_persian


def chunk_to_example(
    chunk: str,
    subject: str = "math",
    grade: int = 9,
    topic: str = "general",
    difficulty: str = "medium",
) -> dict:
    chunk = normalize_persian(chunk.strip())

    # Very simple heuristic prompt
    user = (
        "متن زیر بخشی از کتاب درسی است. آن را به صورت واضح و مرحله‌به‌مرحله "
        "برای یک دانش‌آموز پایه نهم توضیح بده و اگر لازم است مثال اضافه کن:\n\n"
        + chunk
    )

    # Placeholder assistant — in real use this should be rewritten by a strong model or human
    assistant = (
        "در این بخش از درس با مفهوم زیر روبه‌رو هستیم:\n\n"
        + chunk
        + "\n\n"
        "توضیح ساده‌تر و مثال‌های بیشتر باید در نسخه نهایی اضافه شود."
    )

    return make_example(
        user=user,
        assistant=assistant,
        subject=subject,  # type: ignore
        grade=grade,
        topic=topic,
        difficulty=difficulty,  # type: ignore
        example_type="concept_explanation",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunk_file", help="Path to a single chunk .txt file")
    parser.add_argument("-o", "--output", default="data/sft/from_chunk.jsonl")
    parser.add_argument("--subject", default="math")
    parser.add_argument("--grade", type=int, default=9)
    parser.add_argument("--topic", default="general")
    args = parser.parse_args()

    text = Path(args.chunk_file).read_text(encoding="utf-8")
    example = chunk_to_example(
        text,
        subject=args.subject,
        grade=args.grade,
        topic=args.topic,
    )

    save_jsonl([example], args.output)
    print(json.dumps(example, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
