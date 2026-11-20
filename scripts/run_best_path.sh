#!/usr/bin/env bash
set -euo pipefail

# Nova "best specialist" execution path
# 1) bootstrap data
# 2) SFT
# 3) optional DPO if pairs exist
# 4) merge
# 5) remind eval/serve

MODEL="${MODEL:-Qwen/Qwen2.5-7B-Instruct}"
PREFIX="${PREFIX:-outputs/nova-edu-7b}"

echo "[1/5] Bootstrap dataset"
bash scripts/bootstrap_data.sh

echo "[2/5] SFT"
python training/train_sft.py \
  --model "$MODEL" \
  --data data/sft/build/train.jsonl \
  --out "${PREFIX}-sft"

if [[ -f data/sft/build/dpo_pairs.jsonl ]]; then
  echo "[3/5] DPO"
  python training/train_dpo.py \
    --model "${PREFIX}-sft" \
    --data data/sft/build/dpo_pairs.jsonl \
    --out "${PREFIX}-dpo"
  ADAPTER="${PREFIX}-dpo"
else
  echo "[3/5] DPO skipped (no dpo_pairs.jsonl)"
  ADAPTER="${PREFIX}-sft"
fi

echo "[4/5] Merge"
python training/merge_lora.py \
  --base "$MODEL" \
  --adapter "$ADAPTER" \
  --out "${PREFIX}-merged"

echo "[5/5] Next commands:"
echo "  export NOVA_LOCAL_MODEL=${PREFIX}-merged"
echo "  python evaluation/run_eval.py --benchmark evaluation/benchmarks/grade9_math_holdout.jsonl"
echo "  python deployment/serve_local.py --ui"
