#!/usr/bin/env python3
"""
Continued PreTraining (CPT) skeleton for Nova.

This is BIGGER than SFT:
First adapt the base model to Iranian textbook / exam language distribution,
THEN run supervised fine-tuning and preference optimization.

Expected data: plain text JSONL
{"text": "...clean textbook chunk..."}
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Nova continued pretraining skeleton")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B")
    parser.add_argument("--data", required=True, help="JSONL with text field")
    parser.add_argument("--out", default="outputs/nova-edu-cpt")
    parser.add_argument("--max-seq-length", type=int, default=4096)
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--lr", type=float, default=1e-5)
    args = parser.parse_args()

    if not Path(args.data).exists():
        raise FileNotFoundError(args.data)

    print("=" * 60)
    print("NOVA CONTINUED PRETRAINING")
    print("=" * 60)
    print(f"base model : {args.model}")
    print(f"corpus     : {args.data}")
    print(f"output     : {args.out}")
    print(f"seq length : {args.max_seq_length}")
    print(f"epochs     : {args.epochs}")
    print(f"lr         : {args.lr}")
    print()
    print("Pipeline position:")
    print("  1) CPT on clean curriculum corpus")
    print("  2) SFT on instruction/teaching pairs")
    print("  3) DPO/ORPO on pedagogy-ranked pairs")
    print("  4) Merge + eval + local serve")
    print()
    print("Implement next: Unsloth/HF causal LM training over text chunks with packing.")


if __name__ == "__main__":
    main()
