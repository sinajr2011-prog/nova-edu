# Training Nova as an Independent Model

## Objective

Produce a specialized educational model that can eventually run independently of cloud APIs.

## Pipeline

1. **Collect & clean data** (`data/`)
2. **SFT** (`training/train_sft.py`)
3. **Preference optimization** (`training/train_dpo.py`)
4. **Evaluate** (`evaluation/run_eval.py`)
5. **Serve locally** (`core/local_engine.py`)

## Recommended first training run

```bash
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/nova_grade9.jsonl \
  --out outputs/nova-edu-7b-sft \
  --epochs 1 \
  --batch-size 2 \
  --grad-accum 8
```

Then point the app to local weights:

```bash
export NOVA_LOCAL_MODEL="outputs/nova-edu-7b-sft"
python app/ui.py
```

## Data philosophy

High-value educational pairs only:
- concept explanation
- worked example
- mistake repair
- exam-style question + full solution

## Model targets

- Fast iteration: Qwen2.5-7B
- Strong production target: Qwen2.5-14B
- Later: preference-optimized Nova specialist
