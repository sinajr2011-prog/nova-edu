#!/usr/bin/env python3
"""
Helper to create properly formatted SFT examples for Nova-Edu.

Usage example:
    python scripts/build_sft_example.py
"""

import json
from pathlib import Path
from typing import Literal, Optional

Subject = Literal["math", "physics", "chemistry", "biology", "literature", "other"]
Difficulty = Literal["easy", "medium", "hard", "olympiad"]
ExampleType = Literal["concept_explanation", "worked_example", "exercise", "full_solution"]

SYSTEM_PROMPT = (
    "You are Nova, an expert and patient Iranian educational tutor specialized in "
    "secondary school curriculum, Konkur, Tizhooshan and Olympiad preparation. "
    "Explain concepts clearly, use step-by-step reasoning, and adapt to the student's level."
)


def make_example(
    user: str,
    assistant: str,
    subject: Subject,
    grade: int,
    topic: str,
    source: str = "textbook",
    difficulty: Difficulty = "medium",
    example_type: ExampleType = "concept_explanation",
    year: Optional[int] = None,
) -> dict:
    metadata = {
        "subject": subject,
        "grade": grade,
        "topic": topic,
        "source": source,
        "difficulty": difficulty,
        "type": example_type,
    }
    if year is not None:
        metadata["year"] = year

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": metadata,
    }


def save_jsonl(examples: list[dict], path: str | Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Saved {len(examples)} examples → {path}")


if __name__ == "__main__":
    # Quick demo / template
    examples = [
        make_example(
            user="تفاضل دو مجموعه یعنی چه؟ با مثال توضیح بده.",
            assistant=(
                "تفاضل دو مجموعه A منهای B (A − B) یعنی عضوهایی که در A هستند "
                "ولی در B نیستند.\n\n"
                "مثال:\n"
                "A = {۱، ۲، ۳، ۴}\n"
                "B = {۳، ۴، ۵}\n\n"
                "A − B = {۱، ۲}"
            ),
            subject="math",
            grade=9,
            topic="sets",
            difficulty="easy",
            example_type="concept_explanation",
        )
    ]

    save_jsonl(examples, "data/examples/generated_demo.jsonl")
