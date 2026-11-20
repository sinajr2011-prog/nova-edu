#!/usr/bin/env python3
"""Report topic/type/difficulty coverage for a JSONL SFT dataset."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    total = 0
    by_topic = Counter()
    by_type = Counter()
    by_diff = Counter()
    by_subject = Counter()
    pedagogy = []

    for pattern in args.files:
        for path in Path().glob(pattern) if any(c in pattern for c in "*[?") else [Path(pattern)]:
            if not path.is_file():
                continue
            with path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    total += 1
                    meta = row.get("metadata", {})
                    by_topic[meta.get("topic", "?")] += 1
                    by_type[meta.get("type", "?")] += 1
                    by_diff[meta.get("difficulty", "?")] += 1
                    by_subject[meta.get("subject", "?")] += 1
                    if "pedagogy_score" in meta:
                        pedagogy.append(float(meta["pedagogy_score"]))

    print(f"total={total}")
    print("subjects=", dict(by_subject))
    print("topics=", dict(by_topic))
    print("types=", dict(by_type))
    print("difficulty=", dict(by_diff))
    if pedagogy:
        print(f"pedagogy_avg={sum(pedagogy)/len(pedagogy):.3f}")


if __name__ == "__main__":
    main()
