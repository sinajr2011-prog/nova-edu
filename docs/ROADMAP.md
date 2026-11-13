# Nova-Edu Development Roadmap

## Phase 0 — Data Foundation (Current)

**Goal:** Create a clean, high-quality supervised fine-tuning dataset focused on Iranian secondary education.

### Completed so far
- [x] Project structure, schema, and documentation
- [x] Persian text normalization script
- [x] Basic PDF text extraction
- [x] SFT example builder
- [x] Sample SFT data (Grade 9 – Sets)
- [x] Priority sources & Grade 9 Math curriculum slice defined
- [x] Unsloth training template
- [x] Evaluation goals defined

### Still in progress
- [ ] Large-scale textbook extraction & cleaning
- [ ] Systematic conversion of textbook content into SFT pairs
- [ ] Collection of real Konkur / Tizhooshan questions with solutions
- [ ] First hold-out evaluation set

### Priority Data Sources
1. Official secondary school textbooks (Roshd / Ministry of Education)
2. National University Entrance Exam (Konkur)
3. Tizhooshan entrance exams
4. Olympiad stage 1 & 2 problems

### Data Pipeline
1. PDF → text extraction
2. Cleaning & normalization (ZWNJ, punctuation, numbers)
3. Chunking into pedagogical units
4. Conversion into instruction-response pairs
5. Quality filtering

---

## Phase 1 — Base Model Fine-Tuning

- Base model candidates:
  1. Qwen2.5-7B-Instruct / Qwen2.5-14B-Instruct
  2. Qwen3 series
  3. Gemma variants
- Method: QLoRA (4-bit) + Unsloth
- Evaluation on real exam questions + pedagogical quality

Template already available in `training/unsloth_sft_example.py`.

---

## Phase 2 — Agentic System

Planned agents:
- Concept Teacher
- Problem Solver
- Exam Designer
- Grader
- Advisor

Memory: per-student long-term memory

---

## Phase 3 — Productization

- Web interface
- Offline GGUF
- Progress tracking
