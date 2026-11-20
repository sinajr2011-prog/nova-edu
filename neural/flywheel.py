#!/usr/bin/env python3
"""
Nova self-improvement flywheel.

Loop:
1) take hard prompts / eval failures
2) generate multiple candidate answers
3) rank by pedagogy reward
4) emit SFT rows + DPO pairs
5) feed back into training
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from neural.reward.pedagogy_reward import score_pedagogy
from neural.brain import NovaBrain


SYSTEM = (
    "You are Nova, an expert Iranian educational tutor. "
    "Give complete step-by-step teaching answers in Persian."
)


def load_prompts(path: Path) -> list[str]:
    prompts = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("{"):
                obj = json.loads(line)
                prompts.append(obj.get("prompt") or obj.get("question") or "")
            else:
                prompts.append(line)
    return [p for p in prompts if p]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True, help="text or jsonl prompts/failures")
    parser.add_argument("--out-sft", default="data/sft/build/flywheel_sft.jsonl")
    parser.add_argument("--out-dpo", default="data/sft/build/flywheel_dpo.jsonl")
    parser.add_argument("--n-candidates", type=int, default=3)
    args = parser.parse_args()

    from core.local_engine import get_best_engine

    llm = get_best_engine()
    brain = NovaBrain(llm_call=llm)

    prompts = load_prompts(Path(args.prompts))
    sft_path = Path(args.out_sft)
    dpo_path = Path(args.out_dpo)
    sft_path.parent.mkdir(parents=True, exist_ok=True)

    n_sft = n_dpo = 0
    with sft_path.open("w", encoding="utf-8") as fsft, dpo_path.open("w", encoding="utf-8") as fdpo:
        for prompt in prompts:
            cands = []
            for i in range(args.n_candidates):
                # slight instruction variation for diversity
                user = prompt if i == 0 else prompt + "\n\nلطفاً کامل‌تر و مرحله‌به‌مرحله‌تر توضیح بده."
                result = brain.think(user, base_system=SYSTEM, use_rag=False)
                cands.append(result.answer)

            ranked = brain.rank_candidates(cands)
            best, best_score = ranked[0]
            worst, worst_score = ranked[-1]

            fsft.write(json.dumps({
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": best},
                ],
                "metadata": {
                    "subject": "math",
                    "grade": 9,
                    "topic": "flywheel",
                    "source": "flywheel",
                    "difficulty": "hard",
                    "type": "worked_example",
                    "pedagogy_score": best_score.total,
                },
            }, ensure_ascii=False) + "\n")
            n_sft += 1

            if best_score.total - worst_score.total >= 0.1 and best != worst:
                fdpo.write(json.dumps({
                    "prompt": prompt,
                    "chosen": best,
                    "rejected": worst,
                    "score_chosen": best_score.total,
                    "score_rejected": worst_score.total,
                }, ensure_ascii=False) + "\n")
                n_dpo += 1

    print(f"flywheel SFT={n_sft} → {sft_path}")
    print(f"flywheel DPO={n_dpo} → {dpo_path}")


if __name__ == "__main__":
    main()
