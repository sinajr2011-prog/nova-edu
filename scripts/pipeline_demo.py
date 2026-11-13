#!/usr/bin/env python3
"""
Simple end-to-end demo of the current Nova-Edu data pipeline.

1. Normalize Persian text
2. Build an SFT example
3. Validate it
"""

import json
from pathlib import Path

from normalize_persian import normalize_persian
from build_sft_example import make_example, save_jsonl


def main():
    raw_user = "میخواهم مفهوم اشتراک دو مجموعه را یاد بگیرم. لطفا با مثال توضیح بده."
    raw_assistant = (
        "اشتراک دو مجموعه یعنی عضوهایی که همزمان در هر دو مجموعه وجود دارند.\n\n"
        "مثال:\n"
        "A = {۱، ۲، ۳، ۴}\n"
        "B = {۳، ۴، ۵، ۶}\n\n"
        "A ∩ B = {۳، ۴}"
    )

    user = normalize_persian(raw_user, normalize_digits="persian")
    assistant = normalize_persian(raw_assistant, normalize_digits="persian")

    example = make_example(
        user=user,
        assistant=assistant,
        subject="math",
        grade=9,
        topic="sets",
        difficulty="easy",
        example_type="concept_explanation",
    )

    out_path = Path("data/examples/pipeline_demo.jsonl")
    save_jsonl([example], out_path)

    print("\nGenerated example:")
    print(json.dumps(example, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
