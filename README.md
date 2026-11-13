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

## Current Progress

### Done
- Project structure, schema, normalization, PDF extraction, chunking
- SFT tools (builder + validator + pipeline demo)
- Grade 9 Sets + Equations curriculum slices and sample data
- Mini evaluation set for Sets
- Unsloth QLoRA training template
- Agent system prompts

### Next
- Scale real textbook extraction (start with Grade 9 Math)
- Convert clean text into high-quality SFT pairs at volume
- Expand evaluation coverage
- First experimental fine-tune

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

## Project Structure

```
nova-edu/
├── data/
│   ├── curriculum/
│   │   ├── grade9_math.md
│   │   └── grade9_math_equations.md
│   └── examples/
│       ├── sets_grade9.jsonl
│       └── equations_grade9.jsonl
├── scripts/
│   ├── normalize_persian.py
│   ├── extract_pdf_text.py
│   ├── chunk_text.py
│   ├── build_sft_example.py
│   ├── validate_sft.py
│   └── pipeline_demo.py
├── training/
│   └── unsloth_sft_example.py
├── agents/
│   └── SYSTEM_PROMPTS.md
├── evaluation/
│   └── benchmarks/
├── docs/
│   └── ROADMAP.md
└── ...
```

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
