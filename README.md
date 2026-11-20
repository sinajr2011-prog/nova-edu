# Nova-Edu

> Path to a top specialized Iranian educational model — not a generic chatbot clone.

**Status:** Full specialist stack operational 🔥

---

## Reality check

Being the best educational model is not magic text in a README.
It is this loop, executed hard:

**Better data → Train → Hard eval → Mine failures → Flywheel → Train again**

All of that is now coded.

---

## Everything implemented

| Pillar | Path |
|--------|------|
| Agents + memory | `core/` |
| Neural brain (MoE routing, RAG, pedagogy) | `neural/` |
| Self-improvement flywheel | `neural/flywheel.py` |
| Dataset factory + batch synthesis | `data/pipeline/` |
| SFT / DPO / CPT / merge | `training/` |
| Local deploy | `deployment/` |
| Platform API + UI | `api/`, `app/` |
| Best-model playbook | `docs/BEST_MODEL_PLAYBOOK.md` |

---

## Run the full path

```bash
# data bootstrap + SFT + DPO(if pairs) + merge
bash scripts/run_best_path.sh

# 14B version
MODEL=Qwen/Qwen2.5-14B-Instruct PREFIX=outputs/nova-edu-14b bash scripts/run_best_path.sh
```

Flywheel (generate ranked SFT/DPO from hard prompts):
```bash
python neural/flywheel.py --prompts evaluation/benchmarks/grade9_math_holdout.jsonl
```

Serve:
```bash
export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged
python deployment/serve_local.py --ui
```

---

## How Nova can beat general giants

On the battlefield of:
- Iranian curriculum teaching
- mistake diagnosis
- targeted practice
- exam prep workflows

A focused specialist + superior data loop can outperform a general model.

That is the plan. The code is ready. The remaining fuel is **data + GPU cycles + iteration**.

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**
