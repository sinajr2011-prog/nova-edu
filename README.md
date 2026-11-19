# Nova-Edu

> **Toward the best independent Iranian educational neural model**  
> Not just a chatbot wrapper — a specialized multi-agent teaching system with its own training path.

**Status:** Intelligence layer + platform API + independent-model roadmap are live 🔥

---

## The Ambition

Nova is being built to become:

1. A **specialized educational model** fine-tuned on Iranian curriculum / Konkur / Tizhooshan / Olympiad pedagogy
2. A **multi-agent tutor** (Mistake Finder, Question Designer, Memory, Visual)
3. A **platform engine** other edtech products can call
4. Eventually **independent** from cloud APIs through local weights + local inference

---

## What exists today

### Core intelligence
- Multi-agent orchestration
- Long-term student memory
- Mistake → practice loop
- Gradio UI
- REST API for platforms

### Independent model path
- Serious SFT trainer (`training/train_sft.py`)
- DPO skeleton (`training/train_dpo.py`)
- Local inference engine (`core/local_engine.py`)
- Educational evaluation harness (`evaluation/run_eval.py`)
- Doctrine doc (`docs/INDEPENDENT_MODEL.md`)

---

## Run

```bash
pip install -r requirements.txt

# UI
python app/ui.py

# API
uvicorn api.main:app --reload --port 8000

# Train your own Nova adapter
python training/train_sft.py --data data/sft/your_data.jsonl --out outputs/nova-edu-sft

# Use local model instead of cloud
export NOVA_LOCAL_MODEL=outputs/nova-edu-sft
```

---

## Independence Ladder

| Level | State |
|------|------|
| 0 | Cloud API demo |
| 1 | Fine-tuned Nova adapters |
| 2 | Preference-optimized teaching specialist |
| 3 | Local-first independent stack |

We are building Level 1–3 infrastructure now.

---

## Why this can become the best

Because “best” is defined correctly:
- curriculum fidelity
- pedagogical clarity
- mistake diagnosis
- practice generation
- Persian educational language
- measurable evaluation

Not generic chat entertainment.

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
