# Nova-Edu Model Card

## Model summary

**Nova-Edu** is a specialized educational model family for Iranian secondary learning.

It is optimized for:
- curriculum-aligned explanations
- mistake diagnosis
- worked examples
- exam-style reasoning (Konkur / Tizhooshan / Olympiad prep)
- Persian pedagogical language

## Intended use

- tutoring assistants
- practice generation
- educational platform backends
- offline/local teaching aids

## Out-of-scope

- general web search replacement
- medical / legal advice
- unrestricted open-domain entertainment chat as primary goal

## Training pipeline

1. **Data build** — clean + pedagogy filter + train/val split
2. **Optional CPT** — continued pretraining on textbook-like corpus
3. **SFT** — instruction/teaching pairs
4. **DPO** — chosen/rejected pairs ranked by pedagogy quality
5. **Merge** — independent deployable weights
6. **Eval** — answer correctness + teaching heuristics

## Base model candidates

- Qwen2.5-7B-Instruct (fast iteration)
- Qwen2.5-14B-Instruct (stronger production target)

## Evaluation focus

Not only final-answer accuracy.
Also:
- step quality
- clarity
- mistake localization quality
- usefulness of generated practice

## Risks

- curriculum hallucination if retrieval/data are weak
- overconfident wrong solutions
- uneven subject coverage during early dataset stages

## Mitigations

- grounded RAG over textbook chunks
- pedagogy reward filtering
- hard hold-out exam sets
- human review sampling

## Release stages

- `nova-edu-7b-sft`
- `nova-edu-7b-dpo`
- `nova-edu-7b-merged`
- later: 14B variants
