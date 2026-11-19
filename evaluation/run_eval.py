#!/usr/bin/env python3
"""
Educational evaluation harness for Nova.

This is what makes Nova "best" in a real sense:
we score teaching usefulness, not only final answers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def simple_contains_score(prediction: str, gold: str) -> float:
    pred = prediction.strip().replace(" ", "")
    g = gold.strip().replace(" ", "")
    if not g:
        return 0.0
    return 1.0 if g in pred else 0.0


def pedagogy_heuristic(text: str) -> float:
    """Very lightweight proxy until human raters / stronger judges exist."""
    score = 0.0
    checks = [
        ("مرحله", 0.2),
        ("چون", 0.1),
        ("پس", 0.1),
        ("مثال", 0.2),
        ("بنابراین", 0.1),
        ("اول", 0.1),
        ("در نهایت", 0.1),
    ]
    for needle, w in checks:
        if needle in text:
            score += w
    if len(text) > 120:
        score += 0.1
    return min(score, 1.0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="evaluation/benchmarks/grade9_sets_sample.jsonl")
    parser.add_argument("--predictions", help="Optional JSONL with id + prediction fields")
    args = parser.parse_args()

    bench = load_jsonl(Path(args.benchmark))
    preds = {}
    if args.predictions:
        for row in load_jsonl(Path(args.predictions)):
            preds[row["id"]] = row.get("prediction", "")

    exact_scores = []
    pedagogy_scores = []

    print(f"Evaluating {len(bench)} items from {args.benchmark}\n")
    for item in bench:
        item_id = item.get("id", "unknown")
        gold = str(item.get("answer", ""))
        pred = preds.get(item_id, "")
        exact = simple_contains_score(pred, gold) if pred else None
        ped = pedagogy_heuristic(pred) if pred else None

        if exact is not None:
            exact_scores.append(exact)
        if ped is not None:
            pedagogy_scores.append(ped)

        print(f"- {item_id}: gold={gold!r}")
        if pred:
            print(f"  exact={exact:.1f} pedagogy={ped:.2f}")
        else:
            print("  no prediction provided")

    print("\nSummary")
    if exact_scores:
        print(f"Exact/containment accuracy: {sum(exact_scores)/len(exact_scores):.3f}")
    else:
        print("Exact/containment accuracy: n/a")
    if pedagogy_scores:
        print(f"Pedagogy heuristic: {sum(pedagogy_scores)/len(pedagogy_scores):.3f}")
    else:
        print("Pedagogy heuristic: n/a")


if __name__ == "__main__":
    main()
