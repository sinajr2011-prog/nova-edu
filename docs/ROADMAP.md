# Nova-Edu Development Roadmap

## Phase 0 — Data Foundation (Current Focus)

### Completed tooling
- [x] Project structure & schema
- [x] Persian normalization
- [x] PDF extraction
- [x] Text chunking
- [x] SFT builder + validator
- [x] Heuristic chunk → SFT converter
- [x] Data directory layout + workflow guide
- [x] Grade 9 Sets & Equations samples + mini eval set
- [x] Unsloth training template
- [x] Agent prompts

### Current stage (Real Data Ingestion)
- [ ] Ingest real Grade 9 Math textbook pages
- [ ] Clean → chunk → convert to high-quality SFT pairs
- [ ] Human / strong-model review of generated pairs
- [ ] Expand evaluation set (more topics + exam style)
- [ ] First small experimental fine-tune on the new data

---

## Phase 1 — Base Fine-Tuning

- Qwen2.5-7B / 14B (primary)
- QLoRA + Unsloth
- Proper evaluation on held-out questions

---

## Phase 2 — Agentic Layer

Multi-agent system + student memory

---

## Phase 3 — Product

Interface + offline support + progress tracking
