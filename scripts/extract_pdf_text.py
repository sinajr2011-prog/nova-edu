#!/usr/bin/env python3
"""
Basic PDF text extraction for Nova-Edu.

This is a starting point. For production quality on Iranian textbooks
we will later move to better layout-aware tools (e.g. marker, nougat, or
custom pipelines), but this gives us a working baseline.
"""

from pathlib import Path
from typing import Optional
import argparse

try:
    from pypdf import PdfReader
except ImportError:
    raise ImportError("Please install pypdf: pip install pypdf")


def extract_text_from_pdf(pdf_path: str | Path, max_pages: Optional[int] = None) -> str:
    """Extract raw text from a PDF file."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    texts = []

    pages = reader.pages
    if max_pages is not None:
        pages = pages[:max_pages]

    for i, page in enumerate(pages):
        try:
            text = page.extract_text() or ""
            texts.append(text)
        except Exception as e:
            texts.append(f"\n[Error extracting page {i+1}: {e}]\n")

    return "\n\n".join(texts)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF for Nova-Edu")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output text file (optional)")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit number of pages")
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf, max_pages=args.max_pages)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
