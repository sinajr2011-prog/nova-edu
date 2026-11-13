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
- Ultimately become a credible alternative to expensive private tutoring

This is not another wrapper. We are modifying the model itself.

---

## Current Progress (Phase 0)

- [x] Full project structure & documentation
- [x] Persian text normalization
- [x] PDF text extraction
- [x] SFT example builder + sample data
- [x] Grade 9 Math curriculum slice defined
- [x] Unsloth QLoRA training template
- [x] Evaluation goals defined
- [ ] Large-scale clean dataset
- [ ] First real fine-tune

---

## Project Structure

```
nova-edu/
├── data/
│   ├── SCHEMA.md
│   ├── PRIORITY_SOURCES.md
│   ├── curriculum/
│   │   └── grade9_math.md
│   └── examples/
│       └── sample_sft.jsonl
├── scripts/
│   ├── normalize_persian.py
│   ├── extract_pdf_text.py
│   └── build_sft_example.py
├── training/
│   ├── README.md
│   └── unsloth_sft_example.py
├── agents/
│   └── SYSTEM_PROMPTS.md
├── evaluation/
│   └── README.md
├── docs/
│   └── ROADMAP.md
├── Makefile
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

# Test normalization
make normalize

# Generate a demo SFT example
make demo-sft
```

---

## Contributing

Clean educational data, better extraction pipelines, evaluation sets, and training improvements are highly welcome.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
