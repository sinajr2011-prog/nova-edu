# Dataset Schema

## Instruction-Response Format (SFT)

Every training example should follow this structure:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are Nova, an expert and patient Iranian educational tutor specialized in secondary school curriculum, Konkur, Tizhooshan and Olympiad preparation. Explain concepts clearly, use step-by-step reasoning, and adapt to the student's level."
    },
    {
      "role": "user",
      "content": "..."
    },
    {
      "role": "assistant",
      "content": "..."
    }
  ],
  "metadata": {
    "subject": "math | physics | chemistry | biology | literature | ...",
    "grade": 9 | 10 | 11 | 12,
    "topic": "sets | equations | ...",
    "source": "textbook | konkur | tizhooshan | olympiad",
    "year": 1402 | null,
    "difficulty": "easy | medium | hard | olympiad",
    "type": "concept_explanation | worked_example | exercise | full_solution"
  }
}
```

## Quality Rules

- Persian text must use proper ZWNJ (نیم‌فاصله)
- Numbers should be consistent (preferably Persian or Arabic digits — decide and stick to one)
- No OCR garbage or broken layout text
- Assistant responses must be pedagogically useful (not just the final answer)
- Prefer multi-turn when it improves learning (e.g. student asks for clarification)
