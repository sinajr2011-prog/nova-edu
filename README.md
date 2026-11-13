# Nova-Edu

> **The first specialized Iranian educational LLM**  
> Fine-tuned on Iranian textbooks + Konkur + Tizhooshan + Olympiad, with a powerful agentic layer designed to act as a real private tutor.

**Status:** Phase 0 — Real Data Ingestion (Active)

---

## Vision

Most existing Persian AI projects are either simple chatbots or prompt-engineering wrappers.  
**Nova-Edu** aims to go deeper:

- Fine-tune a strong open-weight model on the entire Iranian secondary education curriculum
- Build a multi-agent system (Concept Teacher, Problem Solver, Exam Designer, Grader, Advisor)
- Add long-term student memory and progress tracking
- Support both online and fully offline (GGUF) usage

This is not another wrapper. We are modifying the model itself.

---

## Current Stage

Tooling for Phase 0 is ready. We are now in the **real data ingestion** stage:

1. Extract real textbook content (start with Grade 9 Math)
2. Clean → Chunk → Convert to high-quality SFT pairs
3. Review and expand evaluation sets
4. Run the first experimental fine-tune

See `data/README.md` for the recommended data workflow.

---

## Quick Start

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
pip install -r requirements.txt

make normalize
make pipeline
make validate
```

---

## Key Folders

- `data/` — curriculum, examples, and data workflow
- `scripts/` — extraction, normalization, chunking, SFT tools
- `training/` — Unsloth QLoRA template
- `agents/` — system prompts
- `evaluation/` — benchmarks

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
