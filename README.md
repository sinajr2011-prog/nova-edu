# Nova-Edu

> Specialized Iranian educational neural system — data factory, training, local deployment.

**Status:** Bootstrap + deploy ready 🔥

---

## One-command dataset bootstrap

```bash
bash scripts/bootstrap_data.sh
```

This will:
1. synthesize a large batch from topic seeds (`--per-topic 25`)
2. merge with handcrafted SFT seeds
3. filter by pedagogy score
4. write `data/sft/build/train.jsonl` + `val.jsonl`
5. print coverage report

Manual synthesis:
```bash
python data/pipeline/batch_synthesize.py \
  --topics data/curriculum/topic_seeds.jsonl \
  --out data/sft/synthetic_batch.jsonl \
  --per-topic 50 --mode template
```

LLM mode (if API key is set):
```bash
python data/pipeline/batch_synthesize.py --mode llm --per-topic 10
```

---

## Train

```bash
# 7B
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-7b-sft

# 14B
python training/train_sft.py \
  --model Qwen/Qwen2.5-14B-Instruct \
  --data data/sft/build/train.jsonl \
  --out outputs/nova-edu-14b-sft \
  --batch-size 1 --grad-accum 16 --lr 1.5e-4 --lora-r 32
```

---

## Deploy local model

```bash
python training/merge_lora.py \
  --base Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/nova-edu-7b-sft \
  --out outputs/nova-edu-7b-merged

export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged
python deployment/serve_local.py --ui
# or
python deployment/serve_local.py --api
```

---

## Stack

- `data/pipeline/` dataset factory
- `training/` SFT/DPO/CPT/merge
- `neural/` MoE + RAG + pedagogy reward
- `core/` agents + memory + local engine
- `deployment/` local serve
- `api/` + `app/` product surfaces

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**
