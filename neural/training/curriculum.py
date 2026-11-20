#!/usr/bin/env python3
"""
Curriculum learning utilities for Nova.

Instead of dumping all training samples randomly, we can stage learning:

Stage A: easy concept explanations
Stage B: worked examples
Stage C: mistake repair
Stage D: hard exam / olympiad items

This improves stability and educational specialization.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


STAGE_ORDER = [
    "concept_explanation",
    "worked_example",
    "mistake_repair",
    "exam_item",
    "olympiad_item",
]


@dataclass
class CurriculumConfig:
    stages: list[str]
    epoch_to_stage: dict[int, str]
    seed: int = 42


DEFAULT_SCHEDULE = CurriculumConfig(
    stages=STAGE_ORDER,
    epoch_to_stage={
        0: "concept_explanation",
        1: "worked_example",
        2: "mistake_repair",
        3: "exam_item",
        4: "olympiad_item",
    },
)


class CurriculumSampler:
    def __init__(self, data: list[dict[str, Any]], config: CurriculumConfig = DEFAULT_SCHEDULE):
        self.data = data
        self.config = config
        self.rng = random.Random(config.seed)
        self.buckets: dict[str, list[dict[str, Any]]] = {s: [] for s in STAGE_ORDER}
        self.buckets["other"] = []

        for row in data:
            meta = row.get("metadata", {})
            t = meta.get("type", "other")
            if t in self.buckets:
                self.buckets[t].append(row)
            else:
                self.buckets["other"].append(row)

    def stage_for_epoch(self, epoch: int) -> str:
        if epoch in self.config.epoch_to_stage:
            return self.config.epoch_to_stage[epoch]
        # after schedule ends, mix hard stages
        return "exam_item"

    def iter_epoch(self, epoch: int, mix_previous: bool = True) -> Iterator[dict[str, Any]]:
        stage = self.stage_for_epoch(epoch)
        pool = list(self.buckets.get(stage, []))

        if mix_previous:
            idx = STAGE_ORDER.index(stage) if stage in STAGE_ORDER else 0
            for prev in STAGE_ORDER[:idx]:
                prev_items = self.buckets.get(prev, [])
                if prev_items:
                    k = max(1, len(prev_items) // 5)
                    pool.extend(self.rng.sample(prev_items, min(k, len(prev_items))))

        if not pool:
            pool = list(self.data)

        self.rng.shuffle(pool)
        for row in pool:
            yield row


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


if __name__ == "__main__":
    demo = [
        {"messages": [], "metadata": {"type": "concept_explanation"}},
        {"messages": [], "metadata": {"type": "worked_example"}},
        {"messages": [], "metadata": {"type": "exam_item"}},
    ]
    sampler = CurriculumSampler(demo)
    print("epoch0", [x["metadata"]["type"] for x in sampler.iter_epoch(0)])
    print("epoch3", [x["metadata"]["type"] for x in sampler.iter_epoch(3)])
