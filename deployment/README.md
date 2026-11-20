# Deployment

## Local model serve

```bash
export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged

# CLI
python deployment/serve_local.py

# UI
python deployment/serve_local.py --ui

# API
python deployment/serve_local.py --api --port 8000
```

Engine priority inside UI/API:
1. `NOVA_LOCAL_MODEL`
2. OpenAI-compatible API
3. fake demo engine

## After training

```bash
python training/merge_lora.py \
  --base Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/nova-edu-7b-sft \
  --out outputs/nova-edu-7b-merged
```
