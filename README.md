# Nova-Edu

> **The first specialized Iranian educational LLM**  
> Fine-tuned on Iranian textbooks + Konkur + Tizhooshan + Olympiad, with a powerful agentic layer designed to act as a real private tutor.

**Status:** Phase 0 — Dataset Preparation (Active Development)

---

## Vision

Most existing Persian AI projects are either simple chatbots or prompt-engineering wrappers.  
**Nova-Edu** aims to go deeper:

- Fine-tune a strong open-weight model on the entire Iranian secondary education curriculum
- Build a multi-agent system (Concept Teacher, Problem Solver, Exam Designer, Grader, Advisor)
- Add long-term student memory and progress tracking
- Support both online and fully offline (GGUF) usage
- Ultimately become a credible alternative to expensive private tutoring for a large portion of Iranian students

This is not another wrapper. We are modifying the model itself.

---

## Roadmap

### Phase 0 — Data Foundation (1–2 weeks)
- [ ] Collect and clean secondary school textbooks (PDF → high-quality text)
- [ ] Collect Konkur, Tizhooshan, and Olympiad questions with detailed solutions
- [ ] Normalize Persian text (ZWNJ, punctuation, consistency)
- [ ] Build high-quality instruction–response pairs (SFT format)

### Phase 1 — Base Fine-Tuning
- Select base model (priority: Qwen2.5 / Qwen3 7B–14B)
- Fine-tune with QLoRA + Unsloth
- Evaluate on real Konkur questions
- Iterate on data quality and training recipes

### Phase 2 — Agentic Layer
- Specialized agents (Teacher, Solver, Exam Designer, Grader, Advisor)
- Long-term student memory system
- Tool use and structured output

### Phase 3 — Product
- Clean web + mobile interface
- Offline (GGUF) + online versions
- Progress tracking and reporting dashboard

See full details in [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Project Structure

```
nova-edu/
├── data/
│   └── SCHEMA.md              # SFT data format & quality rules
├── scripts/
│   └── normalize_persian.py   # Persian text normalization
├── training/                  # Training configs (coming)
├── agents/
│   └── SYSTEM_PROMPTS.md      # Core + specialized agent prompts
├── evaluation/                # Benchmarks (coming)
├── docs/
│   └── ROADMAP.md
├── CONTRIBUTING.md
└── README.md
```

---

## Getting Started

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
```

More setup and training instructions will be added as Phase 0 progresses.

---

## Contributing

This is an open project. Clean datasets, evaluation ideas, training improvements, and agent designs are all welcome.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
