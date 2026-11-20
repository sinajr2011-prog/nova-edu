# Nova Best-Model Playbook

This is the operational plan to push Nova from a strong specialist prototype toward a top educational model.

## Truth first

"Best model in history" is not a slogan you code once.
It is a loop:

**Data quality → Train → Hard eval → Find failures → Make better data → Train again**

Nova can become best **in Iranian educational teaching** if this loop is executed relentlessly.

## Non-negotiable pillars

1. Curriculum fidelity
2. Mistake diagnosis quality
3. Pedagogical clarity
4. Practice generation usefulness
5. Persian educational language quality
6. Local independent deployment

## The full system now coded in-repo

1. Multi-agent teaching loop
2. Student memory
3. Subject routing (MoE-style)
4. Educational RAG
5. Pedagogy reward filtering
6. Curriculum learning stages
7. Dataset factory + batch synthesis
8. SFT / DPO / CPT / merge
9. Local serve path
10. Platform API

## Execution order (do this for real)

### Phase A — Data dominance
- Run `scripts/bootstrap_data.sh`
- Add real textbook/exam/solved solutions continuously
- Keep only high pedagogy samples

### Phase B — Specialist training
- Smoke 7B
- Full 14B SFT
- DPO on pedagogy-ranked pairs

### Phase C — Failure mining
- Eval holdout
- Collect model mistakes
- Convert failures into new SFT/DPO pairs

### Phase D — Independence
- Merge weights
- Serve local
- Integrate into platforms (Kharazmika etc.)

## What "winning" looks like

Nova wins when teachers/students prefer it over general chat models for:
- explaining Iranian curriculum
- finding student mistakes
- generating useful practice
- exam preparation workflows
