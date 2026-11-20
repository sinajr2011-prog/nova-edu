# Cloud / GPU Training Guide for Nova

## Recommended path

1. Build dataset locally
2. Smoke-test 7B for 50-200 steps
3. Launch 14B full run on cloud GPU
4. Merge + evaluate + ship

## 7B smoke test

```bash
python data/pipeline/build_dataset.py \
  --inputs data/examples/*.jsonl data/sft/*.jsonl \
  --out-dir data/sft/build

python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-7b-sft \
  --epochs 1 \
  --batch-size 2 \
  --grad-accum 8
```

## 14B production run

Config: `training/configs/nova_14b_qlora.yaml`

```bash
python training/train_sft.py \
  --model Qwen/Qwen2.5-14B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-14b-sft \
  --max-seq-length 4096 \
  --epochs 2 \
  --batch-size 1 \
  --grad-accum 16 \
  --lr 1.5e-4 \
  --lora-r 32
```

## VRAM strategy

| GPU VRAM | Suggestion |
|---------|------------|
| 16GB | 7B QLoRA only |
| 24GB | 14B QLoRA with seq 2048-4096, batch 1 |
| 40GB+ | 14B comfortable, longer context, faster accum |

## After training

```bash
python training/merge_lora.py \
  --base Qwen/Qwen2.5-14B-Instruct \
  --adapter outputs/nova-edu-14b-sft \
  --out outputs/nova-edu-14b-merged

export NOVA_LOCAL_MODEL=outputs/nova-edu-14b-merged
python evaluation/run_eval.py --benchmark evaluation/benchmarks/grade9_math_holdout.jsonl
```

## Quality gates before calling it "Nova-14B"

- holdout accuracy not collapsed
- pedagogy score on sampled answers is high
- mistake-repair examples still coherent
- no severe Persian formatting regression
