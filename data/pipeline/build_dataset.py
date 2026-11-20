#!/usr/bin/env python3
"""
Nova dataset builder.

Merges multiple JSONL sources, normalizes metadata, filters weak samples,
and writes train/val splits for SFT.

Example:
  python data/pipeline/build_dataset.py \
    --inputs data/examples/*.jsonl data/sft/*.jsonl \
    --out-dir data/sft/build \
    --min-pedagogy 0.35
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from neural.reward.pedagogy_reward import score_pedagogy


REQUIRED_META = ["subject", "grade", "topic", "source", "difficulty", "type"]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"skip {path}:{line_no} ({e})")
    return rows


def assistant_text(row: dict[str, Any]) -> str:
    for m in row.get("messages", []):
        if m.get("role") == "assistant":
            return str(m.get("content", ""))
    return ""


def normalize_row(row: dict[str, Any]) -> dict[str, Any] | None:
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) < 2:
        return None

    roles = [m.get("role") for m in messages]
    if "user" not in roles or "assistant" not in roles:
        return None

    for m in messages:
        if not str(m.get("content", "")).strip():
            return None

    meta = dict(row.get("metadata") or {})
    meta.setdefault("subject", "math")
    meta.setdefault("grade", 9)
    meta.setdefault("topic", "general")
    meta.setdefault("source", "unknown")
    meta.setdefault("difficulty", "medium")
    meta.setdefault("type", "concept_explanation")

    # ensure system message exists
    if messages[0].get("role") != "system":
        messages = [{
            "role": "system",
            "content": (
                "You are Nova, an expert Iranian educational tutor specialized in "
                "secondary school curriculum, Konkur, Tizhooshan and Olympiad preparation."
            ),
        }] + messages

    return {"messages": messages, "metadata": meta}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out-dir", default="data/sft/build")
    parser.add_argument("--val-ratio", type=float, default=0.05)
    parser.add_argument("--min-pedagogy", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    paths: list[Path] = []
    for pattern in args.inputs:
        matches = list(Path().glob(pattern)) if any(c in pattern for c in "*[?") else [Path(pattern)]
        paths.extend(matches)

    rows: list[dict[str, Any]] = []
    for p in paths:
        if p.is_file():
            rows.extend(load_jsonl(p))

    cleaned = []
    rejected = 0
    for row in rows:
        norm = normalize_row(row)
        if not norm:
            rejected += 1
            continue
        ped = score_pedagogy(assistant_text(norm))
        if ped.total < args.min_pedagogy:
            rejected += 1
            continue
        norm["metadata"]["pedagogy_score"] = ped.total
        cleaned.append(norm)

    rng = random.Random(args.seed)
    rng.shuffle(cleaned)

    n_val = max(1, int(len(cleaned) * args.val_ratio)) if cleaned else 0
    val = cleaned[:n_val]
    train = cleaned[n_val:]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def dump(name: str, data: list[dict[str, Any]]):
        path = out_dir / name
        with path.open("w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return path

    train_path = dump("train.jsonl", train)
    val_path = dump("val.jsonl", val)

    stats = {
        "inputs": [str(p) for p in paths],
        "raw": len(rows),
        "accepted": len(cleaned),
        "rejected": rejected,
        "train": len(train),
        "val": len(val),
        "min_pedagogy": args.min_pedagogy,
    }
    (out_dir / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"train → {train_path}")
    print(f"val   → {val_path}")


if __name__ == "__main__":
    main()
