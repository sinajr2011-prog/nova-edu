#!/usr/bin/env python3
"""
Preference optimization skeleton for Nova-Edu (DPO-style).

Use this after SFT to push teaching quality:
- preferred = pedagogically strong answer
- rejected = bland / incomplete / weakly explained answer

Expected JSONL fields:
{
  "prompt": "...",
  "chosen": "...",
  "rejected": "..."
}
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Nova-Edu DPO trainer skeleton")
    p.add_argument("--model", default="outputs/nova-edu-sft")
    p.add_argument("--data", required=True)
    p.add_argument("--out", default="outputs/nova-edu-dpo")
    p.add_argument("--max-seq-length", type=int, default=4096)
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--lr", type=float, default=5e-6)
    return p.parse_args()


def main():
    args = parse_args()
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(data_path)

    print("DPO training skeleton ready.")
    print("Model:", args.model)
    print("Data:", args.data)
    print("Output:", args.out)
    print("\nNext implementation step: wire TRL DPOTrainer with the same Qwen tokenizer/chat template.")
    print("Keep chosen answers pedagogically richer than rejected ones.")


if __name__ == "__main__":
    main()
