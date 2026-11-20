#!/usr/bin/env python3
"""
Synthesize seed SFT data from topic specs.

This is for bootstrapping volume BEFORE human/textbook-scale data arrives.
Uses an LLM function if provided; otherwise writes prompt templates for offline generation.

Topic spec JSONL:
{"subject":"math","grade":9,"topic":"sets","difficulty":"easy","type":"concept_explanation"}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, Optional


SYSTEM = (
    "You are Nova, an expert Iranian educational tutor specialized in "
    "secondary school curriculum, Konkur, Tizhooshan and Olympiad preparation. "
    "Explain clearly in Persian with correct نیم‌فاصله and step-by-step reasoning."
)


def make_user_prompt(spec: dict[str, Any]) -> str:
    t = spec.get("type", "concept_explanation")
    topic = spec.get("topic", "general")
    grade = spec.get("grade", 9)
    difficulty = spec.get("difficulty", "medium")

    if t == "worked_example":
        return (
            f"یک مثال حل‌شده {difficulty} برای موضوع «{topic}» پایه {grade} بنویس. "
            f"صورت سؤال + راه‌حل کامل مرحله‌به‌مرحله."
        )
    if t == "mistake_repair":
        return (
            f"یک اشتباه رایج دانش‌آموز در موضوع «{topic}» پایه {grade} طراحی کن، "
            f"بعد اشتباه را دقیق توضیح بده و راه‌حل درست را بنویس."
        )
    if t == "exam_item":
        return (
            f"یک سؤال امتحانی/کنکوری {difficulty} در موضوع «{topic}» پایه {grade} بساز "
            f"و پاسخ + راه‌حل کامل بده."
        )
    return (
        f"مفهوم «{topic}» را برای دانش‌آموز پایه {grade} در سطح {difficulty} "
        f"با توضیح شفاف و یک مثال کوتاه آموزش بده."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", required=True, help="topic spec JSONL")
    parser.add_argument("--out", default="data/sft/build/synthetic_seed.jsonl")
    parser.add_argument("--templates-only", action="store_true",
                        help="do not call LLM; write generation requests only")
    args = parser.parse_args()

    topics_path = Path(args.topics)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    with topics_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            spec = json.loads(line)
            user = make_user_prompt(spec)
            if args.templates_only:
                row = {
                    "messages": [
                        {"role": "system", "content": SYSTEM},
                        {"role": "user", "content": user},
                        {"role": "assistant", "content": "[[GENERATE_ME]]"},
                    ],
                    "metadata": {
                        **spec,
                        "source": "synthetic_template",
                    },
                }
            else:
                # Placeholder assistant content; replace via LLM offline batch later
                row = {
                    "messages": [
                        {"role": "system", "content": SYSTEM},
                        {"role": "user", "content": user},
                        {"role": "assistant", "content": "[[GENERATE_ME]]"},
                    ],
                    "metadata": {
                        "subject": spec.get("subject", "math"),
                        "grade": spec.get("grade", 9),
                        "topic": spec.get("topic", "general"),
                        "source": "synthetic_seed",
                        "difficulty": spec.get("difficulty", "medium"),
                        "type": spec.get("type", "concept_explanation"),
                    },
                }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1

    print(f"wrote {n} synthetic seeds → {out_path}")


if __name__ == "__main__":
    main()
