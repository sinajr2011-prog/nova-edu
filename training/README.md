# Training Nova at Scale

## The full path (bigger than plain fine-tune)

```text
Raw educational sources
        ↓
Dataset build + pedagogy filter
        ↓
Optional Continued PreTraining (CPT)
        ↓
SFT (teaching instructions)
        ↓
DPO (pedagogy-ranked preferences)
        ↓
Merge LoRA → independent weights
        ↓
Eval + local serve
```

## Commands

### 1) Build dataset
```bash
python data/pipeline/build_dataset.py \
  --inputs data/examples/*.jsonl \
  --out-dir data/sft/build \
  --min-pedagogy 0.3
```

### 2) Synthetic seed expansion
```bash
python data/pipeline/synthesize_from_topics.py \
  --topics data/curriculum/topic_seeds.jsonl \
  --out data/sft/build/synthetic_seed.jsonl \
  --templates-only
```

### 3) SFT
```bash
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-7b-sft
```

### 4) DPO pair mining
```bash
python data/pipeline/mine_dpo_pairs.py \
  --input data/sft/build/candidates.jsonl \
  --out data/sft/build/dpo_pairs.jsonl
```

### 5) Full orchestrated pipeline
```bash
python training/run_full_pipeline.py \
  --inputs data/examples/*.jsonl \
  --model Qwen/Qwen2.5-7B-Instruct \
  --out-prefix outputs/nova-edu-7b
```

### 6) Local independent mode
```bash
export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged
python app/ui.py
```

## Model sizes

- **7B**: fast iteration / consumer GPU
- **14B**: stronger production specialist

## Quality rule

Do not scale garbage.
Every accepted assistant response should teach.
