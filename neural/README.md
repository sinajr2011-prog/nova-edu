# Nova Neural Stack

This is the deep-learning core of Nova-Edu.

Goal: build an educational specialist that beats generic chat models **on teaching**, not on random internet trivia.

## What makes Nova different

Generic LLMs optimize for fluent answers.
Nova optimizes for:

1. Curriculum fidelity
2. Mistake diagnosis
3. Step-by-step pedagogy
4. Targeted practice generation
5. Long-term student adaptation

## Stack

```
neural/
├── architecture/          # model design ideas + modules
├── training/              # advanced training recipes
├── retrieval/             # neural RAG over textbooks/exams
├── reward/                # teaching-quality reward models
└── eval/                  # neural + hard educational evaluation
```

## Design pillars

- **Base intelligence**: strong open foundation model (Qwen-class)
- **Domain specialization**: SFT + preference optimization on Iranian educational data
- **Pedagogical control**: agents + memory + retrieval
- **Independence**: local inference path, own eval suite, own data engine

We do not win by copying ChatGPT.
We win by becoming the best teacher for a real curriculum.
