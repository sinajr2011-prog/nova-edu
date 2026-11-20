#!/usr/bin/env python3
"""
Nova full training pipeline orchestrator.

Stages:
  1. build dataset
  2. (optional) CPT
  3. SFT
  4. mine DPO pairs (if candidates exist)
  5. DPO
  6. merge
  7. eval reminder

This script prints / launches the standard path so training is reproducible.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


def run(cmd: str):
    print("\n$ " + cmd)
    subprocess.check_call(shlex.split(cmd))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", nargs="+", default=["data/examples/*.jsonl"])
    p.add_argument("--build-dir", default="data/sft/build")
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--out-prefix", default="outputs/nova-edu-7b")
    p.add_argument("--skip-train", action="store_true", help="only build data")
    p.add_argument("--with-cpt", action="store_true")
    p.add_argument("--cpt-data", default="")
    args = p.parse_args()

    build_dir = Path(args.build_dir)
    train_file = build_dir / "train.jsonl"

    # 1) Dataset build
    inputs = " ".join(args.inputs)
    run(
        f"python data/pipeline/build_dataset.py --inputs {inputs} "
        f"--out-dir {args.build_dir} --min-pedagogy 0.3"
    )

    if args.skip_train:
        print("Dataset ready. Skipping training by request.")
        return

    if not train_file.exists():
        raise SystemExit(f"Missing {train_file}")

    # 2) Optional CPT
    if args.with_cpt:
        if not args.cpt_data:
            raise SystemExit("--with-cpt requires --cpt-data")
        run(
            f"python training/train_cpt.py --model {args.model} "
            f"--data {args.cpt_data} --out {args.out_prefix}-cpt"
        )

    # 3) SFT
    sft_out = f"{args.out_prefix}-sft"
    run(
        f"python training/train_sft.py --model {args.model} "
        f"--data {train_file} --out {sft_out}"
    )

    # 4/5 DPO if pairs file exists
    dpo_pairs = build_dir / "dpo_pairs.jsonl"
    if dpo_pairs.exists():
        run(
            f"python training/train_dpo.py --model {sft_out} "
            f"--data {dpo_pairs} --out {args.out_prefix}-dpo"
        )
        adapter_for_merge = f"{args.out_prefix}-dpo"
    else:
        print(f"No {dpo_pairs}; skipping DPO")
        adapter_for_merge = sft_out

    # 6) Merge
    merged = f"{args.out_prefix}-merged"
    run(
        f"python training/merge_lora.py --base {args.model} "
        f"--adapter {adapter_for_merge} --out {merged}"
    )

    print("\nPipeline finished.")
    print(f"Merged model: {merged}")
    print("Next: python evaluation/run_eval.py ...")
    print(f"Serve locally: export NOVA_LOCAL_MODEL={merged}")


if __name__ == "__main__":
    main()
