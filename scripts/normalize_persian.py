#!/usr/bin/env python3
"""
Persian text normalization for Nova-Edu dataset pipeline.

Handles:
- Character normalization (Arabic → Persian ye/kaf, etc.)
- Basic ZWNJ (نیم‌فاصله) insertion
- Whitespace and punctuation cleanup
- Optional digit conversion
"""

import re
from typing import Optional


def normalize_persian(
    text: str,
    fix_zwnj: bool = True,
    normalize_digits: Optional[str] = None,  # "persian" | "arabic" | None
) -> str:
    if not text:
        return text

    # 1. Character normalization
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = text.replace("أ", "ا").replace("إ", "ا")
    # Keep آ as is

    # 2. Remove zero-width non-joiners that are already wrong, then re-apply later
    text = text.replace("\u200c", "")  # remove existing ZWNJ first for consistency

    # 3. Whitespace cleanup
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    # 4. ZWNJ heuristics (expandable)
    if fix_zwnj:
        # می / نمی + verb
        text = re.sub(r"\b(ن?می)([\u0600-\u06FF])", r"\1‌\2", text)

        # Common plural / suffix patterns
        text = re.sub(r"(ها)([\u0600-\u06FF])", r"\1‌\2", text)
        text = re.sub(r"(تر)([\u0600-\u06FF])", r"\1‌\2", text)
        text = re.sub(r"(ترین)([\u0600-\u06FF])", r"\1‌\2", text)

        # Some common prefixes
        text = re.sub(r"\b(بی)([\u0600-\u06FF])", r"\1‌\2", text)

    # 5. Digit normalization
    if normalize_digits == "persian":
        trans = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
        text = text.translate(trans)
    elif normalize_digits == "arabic":
        trans = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        text = text.translate(trans)

    return text


if __name__ == "__main__":
    samples = [
        "میخواهم کتابهای ریاضی پایه نهم را بررسی کنم.",
        "این یک متن آزمایشی است با اعداد 123 و ی و ك.",
        "نمیخواهم بروم ولی میروم.",
    ]

    for s in samples:
        print("Original :", s)
        print("Normalized:", normalize_persian(s, normalize_digits="persian"))
        print("-" * 50)
