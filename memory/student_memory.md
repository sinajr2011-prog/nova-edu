# Long-term Student Memory

## Goal
Nova should remember each student's strengths, weaknesses, past mistakes, and learning history so it can personalize teaching.

## Data to Store (per student)

```json
{
  "student_id": "...",
  "profile": {
    "grade": 9,
    "goals": ["konkur", "improve_math"]
  },
  "strengths": ["sets", "basic_equations"],
  "weaknesses": ["word_problems", "inequalities"],
  "mistake_history": [
    {
      "topic": "equations",
      "mistake_type": "sign_error",
      "timestamp": "...",
      "example": "..."
    }
  ],
  "topic_mastery": {
    "sets": 0.82,
    "equations": 0.61
  },
  "recent_sessions": []
}
```

## Memory Types
1. **Summary Memory** — Compressed overview of the student
2. **Episodic Memory** — Important past interactions and mistakes
3. **Mastery Vector** — Numeric understanding level per topic

## Usage
- Question Designer uses weaknesses to generate targeted practice
- Mistake Finder updates mistake_history
- Advisor recommends next topics based on mastery
