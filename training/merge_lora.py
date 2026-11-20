#!/usr/bin/env python3
"""
Merge LoRA adapters into base weights for independent deployment.

Example:
  python training/merge_lora.py \
    --base Qwen/Qwen2.5-7B-Instruct \
    --adapter outputs/nova-edu-7b-sft \
    --out outputs/nova-edu-7b-merged
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-seq-length", type=int, default=4096)
    args = parser.parse_args()

    from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.adapter,
        max_seq_length=args.max_seq_length,
        dtype=None,
        load_in_4bit=False,
    )

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Save merged 16-bit weights for serving
    model.save_pretrained_merged(str(out), tokenizer, save_method="merged_16bit")
    print(f"Merged model saved to {out}")


if __name__ == "__main__":
    main()
