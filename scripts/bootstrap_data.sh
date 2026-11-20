#!/usr/bin/env bash
set -euo pipefail

# Build a larger training set in one go:
# 1) synthesize many samples from topic seeds
# 2) merge with handcrafted seeds
# 3) filter + split

python data/pipeline/batch_synthesize.py \
  --topics data/curriculum/topic_seeds.jsonl \
  --out data/sft/synthetic_batch.jsonl \
  --per-topic 25 \
  --mode template

python data/pipeline/build_dataset.py \
  --inputs data/examples/*.jsonl data/sft/*.jsonl \
  --out-dir data/sft/build \
  --min-pedagogy 0.25

python data/pipeline/report_dataset.py data/sft/build/train.jsonl data/sft/build/val.jsonl

echo "Bootstrap complete → data/sft/build"
