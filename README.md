# Nova-Edu

> **Specialized Iranian educational neural system**  
> Multi-agent tutor + deep learning stack + platform API + path to independent model weights.

**Status:** Neural stack ignited 🔥

---

## Why Nova can beat generic giants on this battlefield

ChatGPT-class systems are generalists.
Nova is being built as a **curriculum-specialist teaching machine**:

- mistake diagnosis
- pedagogical step-by-step answers
- targeted practice generation
- student memory
- subject-aware routing
- textbook-grounded retrieval
- pedagogy reward filtering
- independent fine-tuning path

Generic models win open chat.
Specialists win when the metric is **teaching Iranian students better**.

---

## Neural / Deep Learning Core

```
neural/
├── brain.py                      # MoE routing + RAG + pedagogy scoring
├── architecture/moe_subjects.py  # subject-aware expert routing
├── training/curriculum.py        # curriculum learning stages
├── retrieval/edu_rag.py          # educational retrieval
└── reward/pedagogy_reward.py     # teaching-quality reward signals
```

Plus:
- `training/train_sft.py` — real SFT pipeline
- `training/train_dpo.py` — preference optimization path
- `core/local_engine.py` — local independent inference
- `evaluation/` — educational eval harness

---

## Full system

| Layer | Role |
|------|------|
| Agents | Mistake Finder, Question Designer, Visual Explainer |
| Memory | long-term student model |
| Neural Brain | routing + retrieval + pedagogy scoring |
| API | integrate into Kharazmika / LMS / apps |
| Training | SFT → DPO → local specialist weights |

---

## Run

```bash
pip install -r requirements.txt

# UI
python app/ui.py

# API
uvicorn api.main:app --reload --port 8000

# Train specialist
python training/train_sft.py --data data/sft/your_data.jsonl --out outputs/nova-edu-sft

# Local independent mode
export NOVA_LOCAL_MODEL=outputs/nova-edu-sft
```

---

## Roadmap to true dominance in EdTech AI

1. High-quality Iranian educational dataset at scale
2. SFT on Qwen2.5-7B/14B
3. Pedagogy-ranked DPO pairs
4. Subject experts / adapters
5. Hard eval on Konkur-style + teaching quality
6. Local-first deployment

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
