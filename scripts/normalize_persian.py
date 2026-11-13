#!/usr/bin/env python3
"""
Basic Persian text normalization for Nova-Edu dataset pipeline.

Handles:
- ZWNJ (نیم‌فاصله) insertion in common cases
- Character normalization (Arabic vs Persian ye/kaf, etc.)
- Whitespace and punctuation cleanup
- Digit consistency (optional)
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

    # 1. Basic character normalization
    # Arabic ye/kaf → Persian
    text = text.replace("ي", "ی").replace("ك", "ک")

    # 2. Normalize different forms of hamza / alef
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "آ")

    # 3. Whitespace cleanup
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    # 4. Common ZWNJ fixes (very basic heuristics — will be expanded)
    if fix_zwnj:
        # mi + verb
        text = re.sub(r"\bمی([\u0600-\u06FF])", r"می‌\1", text)
        # nemi +
        text = re.sub(r"\bنمی([\u0600-\u06FF])", r"نمی‌\1", text)
        # common suffixes
        text = re.sub(r"(ها)([\u0600-\u06FF])", r"\1‌\2", text)

    # 5. Digit normalization (optional)
    if normalize_digits == "persian":
        trans = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
        text = text.translate(trans)
    elif normalize_digits == "arabic":
        trans = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        text = text.translate(trans)

    return text


if __name__ == "__main__":
    sample = """میخواهم کتابهای ریاضی پایه نهم را بررسی کنم.
این یک متن آزمایشی است با اعداد 123 و ی و ك."""

    print("Original:")
    print(sample)
    print("\nNormalized:")
    print(normalize_persian(sample, normalize_digits="persian"))
