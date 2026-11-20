# Nova-Edu

> Specialized Iranian educational neural system — dataset factory, 7B/14B training configs, agents, memory, API.

**Status:** Dataset expansion + 14B training track ready 🔥

---

## What just landed

### 1) Bigger Grade 9 dataset
- `data/sft/grade9_math_large.jsonl` — multi-topic math teaching pairs
- `data/sft/grade9_physics_seed.jsonl` — physics seeds
- Expanded `topic_seeds.jsonl`
- Holdout eval: `evaluation/benchmarks/grade9_math_holdout.jsonl`

### 2) 7B + 14B training configs
- `training/configs/nova_7b_qlora.yaml`
- `training/configs/nova_14b_qlora.yaml`
- `training/CLOUD_GPU.md` — exact cloud/GPU playbook

### 3) Extra factory tools
- dataset coverage report
- full CPT → SFT → DPO → merge pipeline
- pedagogy filtering
- synthetic expansion

---

## Fast path

```bash
# build mixed dataset
python data/pipeline/build_dataset.py \
  --inputs data/examples/*.jsonl data/sft/*.jsonl \
  --out-dir data/sft/build

# coverage report
python data/pipeline/report_dataset.py data/sft/build/*.jsonl

# 7B smoke train
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-7b-sft

# 14B production-style train
python training/train_sft.py \
  --model Qwen/Qwen2.5-14B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-14b-sft \
  --batch-size 1 --grad-accum 16 --lr 1.5e-4 --lora-r 32
```

See `training/CLOUD_GPU.md` for VRAM strategy.

---

## System map

| Layer | Path |
|------|------|
| Data factory | `data/pipeline/` |
| Neural brain | `neural/` |
| Agents/memory | `core/` |
| Training | `training/` |
| API | `api/` |
| UI | `app/` |

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**
