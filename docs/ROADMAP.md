# Nova-Edu Development Roadmap

## Phase 0 — Data Foundation (Current)

**Goal:** Create a clean, high-quality supervised fine-tuning dataset focused on Iranian secondary education.

### Priority Data Sources
1. Official secondary school textbooks (Roshd / Ministry of Education)
   - Mathematics (Grade 9–12)
   - Physics, Chemistry, Biology
   - Persian Literature & Arabic (selected chapters)
2. National University Entrance Exam (Konkur) – all recent years
3. Tizhooshan (gifted students) entrance exams
4. Olympiad stage 1 & 2 problems (Math, Physics, Chemistry, Informatics)

### Data Pipeline
1. PDF → text extraction (with layout awareness)
2. Cleaning & normalization (ZWNJ, punctuation, numbers)
3. Chunking into pedagogical units (concept explanation, worked example, exercise)
4. Conversion into instruction-response pairs
5. Quality filtering + human review samples

### Target Format (SFT)
```json
{
  "messages": [
    {"role": "system", "content": "You are Nova, an expert Iranian educational tutor..."},
    {"role": "user", "content": "Explain the concept of ..."},
    {"role": "assistant", "content": "..."}
  ],
  "metadata": {
    "subject": "math",
    "grade": 9,
    "topic": "sets",
    "source": "textbook",
    "difficulty": "medium"
  }
}
```

---

## Phase 1 — Base Model Fine-Tuning

- Base model candidates (priority order):
  1. Qwen2.5-7B-Instruct / Qwen2.5-14B-Instruct
  2. Qwen3 series (when available and stable)
  3. Gemma-2-9B / Gemma-3 equivalents
- Method: QLoRA (4-bit) + Unsloth for speed
- Evaluation: Hold-out set of real Konkur questions + open-ended concept explanations

---

## Phase 2 — Agentic System

Planned agents:
- **Concept Teacher**: Explains topics step-by-step with examples
- **Problem Solver**: Solves questions with detailed reasoning
- **Exam Designer**: Generates new questions of controlled difficulty
- **Grader**: Evaluates student answers and gives feedback
- **Advisor**: Tracks long-term progress and recommends next topics

Memory: Per-student vector store + summary memory

---

## Phase 3 — Productization

- Web interface
- Offline GGUF support
- Progress dashboard
- Teacher / parent views (optional)
