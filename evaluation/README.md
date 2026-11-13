# Evaluation

## Goals

We need reliable ways to measure whether Nova is actually useful for Iranian students.

### Primary Metrics (Phase 1+)

1. **Konkur-style accuracy**  
   Multiple-choice and short-answer questions from real exams.

2. **Pedagogical quality**  
   Human evaluation of explanations (clarity, correctness, step-by-step reasoning, use of proper Persian).

3. **Robustness**  
   Handling of common student mistakes and follow-up questions.

## Planned Structure

```
evaluation/
├── benchmarks/
│   ├── konkur_sample/          # Small hold-out set
│   └── grade9_math/            # Topic-specific sets
├── scripts/
│   └── run_eval.py             # (future)
└── reports/
```

## Current Status

No official evaluation set yet.  
First target: Grade 9 Mathematics – Sets chapter + related Konkur questions.
