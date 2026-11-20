#!/usr/bin/env python3
"""
Mine DPO pairs from candidate answers using pedagogy reward.

Input JSONL rows:
{
  "prompt": "...",
  "candidates": ["ans1", "ans2", ...]
}

or SFT-like rows with messages + optional candidates.

Output:
{
  "prompt": "...",
  "chosen": "...",
  "rejected": "...",
  "score_chosen": 0.8,
  "score_rejected": 0.2
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from neural.reward.pedagogy_reward import score_pedagogy


def extract_prompt(row: dict[str, Any]) -> str:
    if "prompt" in row:
        return str(row["prompt"])
    messages = row.get("messages", [])
    for m in messages:
        if m.get("role") == "user":
            return str(m.get("content", ""))
    return ""


def extract_candidates(row: dict[str, Any]) -> list[str]:
    if "candidates" in row and isinstance(row["candidates"], list):
        return [str(c) for c in row["candidates"] if str(c).strip()]
    # fallback: single assistant as chosen-only (skip)
    for m in row.get("messages", []):
        if m.get("role") == "assistant":
            return [str(m.get("content", ""))]
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="data/sft/build/dpo_pairs.jsonl")
    parser.add_argument("--min-margin", type=float, default=0.12)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_in = n_out = 0
    with in_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            n_in += 1
            row = json.loads(line)
            prompt = extract_prompt(row)
            cands = extract_candidates(row)
            if not prompt or len(cands) < 2:
                continue

            scored = [(c, score_pedagogy(c).total) for c in cands]
            scored.sort(key=lambda x: x[1], reverse=True)
            chosen, s_c = scored[0]
            rejected, s_r = scored[-1]
            if s_c - s_r < args.min_margin:
                continue

            fout.write(json.dumps({
                "prompt": prompt,
                "chosen": chosen,
                "rejected": rejected,
                "score_chosen": s_c,
                "score_rejected": s_r,
            }, ensure_ascii=False) + "\n")
            n_out += 1

    print(f"read={n_in} wrote={n_out} → {out_path}")


if __name__ == "__main__":
    main()
