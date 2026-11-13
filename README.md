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
- [x] Project structure & schema defined
- [x] Persian normalization script
- [x] Basic PDF extraction script
- [ ] Collect and clean secondary school textbooks
- [ ] Collect Konkur / Tizhooshan / Olympiad questions
- [ ] Build high-quality instruction–response pairs

### Phase 1 — Base Fine-Tuning
- Select base model (priority: Qwen2.5 / Qwen3 7B–14B)
- Fine-tune with QLoRA + Unsloth
- Evaluate on real Konkur questions

### Phase 2 — Agentic Layer
- Specialized agents (Teacher, Solver, Exam Designer, Grader, Advisor)
- Long-term student memory

### Phase 3 — Product
- Web + offline (GGUF) interfaces
- Progress tracking

Full details → [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## Project Structure

```
nova-edu/
├── data/
│   ├── SCHEMA.md
│   ├── PRIORITY_SOURCES.md
│   └── examples/
│       └── sample_sft.jsonl
├── scripts/
│   ├── normalize_persian.py
│   └── extract_pdf_text.py
├── training/
│   └── README.md
├── agents/
│   └── SYSTEM_PROMPTS.md
├── docs/
│   └── ROADMAP.md
├── requirements.txt
├── CONTRIBUTING.md
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
pip install -r requirements.txt
```

---

## Contributing

Clean data, better extraction, evaluation sets, and training ideas are all welcome.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
