# Nova-Edu Development Roadmap

## Phase 0 — Data Foundation (Current)

**Goal:** Create a clean, high-quality supervised fine-tuning dataset focused on Iranian secondary education.

### Completed
- [x] Project structure, schema, and documentation
- [x] Persian text normalization
- [x] Basic PDF text extraction
- [x] Text chunking helper
- [x] SFT example builder + validation
- [x] Pipeline demo
- [x] Grade 9 Sets curriculum + samples + mini evaluation set
- [x] Grade 9 Equations curriculum + samples
- [x] Unsloth training template
- [x] Specialized agent prompts

### Next focus
- [ ] Scale up real textbook extraction (Grade 9 Math first)
- [ ] Systematic conversion of textbook content into high-quality SFT pairs
- [ ] Expand evaluation set (more topics + Konkur-style items)
- [ ] First small experimental fine-tune

---

## Phase 1 — Base Model Fine-Tuning

- Primary candidates: Qwen2.5-7B / 14B Instruct
- Method: QLoRA + Unsloth
- Evaluation on held-out exam questions + pedagogical quality

Template ready at `training/unsloth_sft_example.py`.

---

## Phase 2 — Agentic System

Agents: Concept Teacher, Problem Solver, Exam Designer, Grader, Advisor  
+ long-term student memory

---

## Phase 3 — Productization

Web interface + offline GGUF + progress tracking
