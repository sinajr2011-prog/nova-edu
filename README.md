# Nova-Edu

> Specialized Iranian educational neural system with a full dataset → CPT → SFT → DPO → merge pipeline.

**Status:** Data + training factory is online 🔥

---

## Bigger than fine-tuning

Nova now has the full specialist-model factory:

1. **Dataset build** with pedagogy filtering
2. **Synthetic topic expansion**
3. **Optional Continued PreTraining**
4. **SFT**
5. **DPO pair mining + preference optimization**
6. **LoRA merge for independent deployment**
7. **Local inference + API + agents + neural brain**

```bash
# build data
python data/pipeline/build_dataset.py --inputs data/examples/*.jsonl --out-dir data/sft/build

# full pipeline
python training/run_full_pipeline.py \
  --inputs data/examples/*.jsonl \
  --model Qwen/Qwen2.5-7B-Instruct \
  --out-prefix outputs/nova-edu-7b
```

---

## Core capabilities

- Multi-agent tutoring (mistake analysis, practice generation)
- Student memory
- Subject routing + educational RAG + pedagogy rewards
- Platform API
- Independent model path

---

## Quick run

```bash
pip install -r requirements.txt
python app/ui.py
# or
uvicorn api.main:app --reload --port 8000
```

Local model:
```bash
export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged
```

---

## Key folders

- `data/pipeline/` — dataset factory
- `training/` — CPT / SFT / DPO / merge / orchestrator
- `neural/` — MoE routing, RAG, pedagogy reward, brain
- `core/` — agents, memory, local engine
- `api/` — platform integration

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**
