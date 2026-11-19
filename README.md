# Nova-Edu

> **The first specialized Iranian educational LLM + Visual Tutor**  
> Text + Image + Video + Multi-Agent system focused on Iranian curriculum, Konkur, Tizhooshan and Olympiad.

**Status:** Core Intelligence Layer is live 🔥

---

## What's Cool Right Now

### 1. Student Memory (`core/memory_store.py`)
Long-term memory per student:
- Strengths & weaknesses
- Mistake history
- Topic mastery scores (with EMA)
- Smart focus topic recommendation

### 2. Multi-Agent System (`core/agents.py`)
- **Mistake Finder** → finds the exact error and explains it
- **Question Designer** → generates targeted practice from that mistake
- **Visual Explainer** → connected to image/video generation
- **Teacher Styles** → مهربون / سرسخت / کنکوری / مفهومی

### 3. The Magic Loop
```
Student mistake → Mistake Finder → Memory update → Targeted questions
```
Fully implemented in `NovaOrchestrator.mistake_to_practice()`

### 4. Multimodal
Image + Video generation ready (`multimodal/`)

---

## Quick Demo

```bash
python -m core.demo_loop
```

This runs a full fake example:
- Student solves an equation wrong
- Nova finds the mistake
- Updates memory
- Generates new practice questions

---

## Project Structure

```
nova-edu/
├── core/
│   ├── memory_store.py      # Long-term student memory
│   ├── agents.py            # All agents + orchestrator
│   └── demo_loop.py         # Full working demo
├── multimodal/              # Image + Video generation
├── agents/                  # Agent design docs
├── memory/                  # Memory design docs
├── modes/                   # Konkur sim, Night-before-exam...
├── data/
├── training/
└── docs/
```

---

## Next Power Moves

1. Plug a real LLM (Qwen / OpenAI / local) into `llm_call`
2. Connect Visual Explainer to real image generation in the loop
3. Build a simple web UI around the orchestrator
4. Start fine-tuning on real Grade 9 data

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
