#!/usr/bin/env python3
"""
Subject-aware Mixture-of-Experts routing (design + lightweight prototype).

Idea:
Instead of one generic brain for everything, Nova can route educational
queries toward specialist pathways:

- math expert
- physics expert
- chemistry expert
- literature expert
- exam-strategy expert

This file provides:
1) a clean routing interface
2) a simple prototype router (keyword + optional embedding hook)
3) a place to later plug real neural MoE / adapter experts
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


EXPERTS = (
    "math",
    "physics",
    "chemistry",
    "biology",
    "literature",
    "exam_strategy",
    "general",
)


@dataclass
class RouteDecision:
    expert: str
    confidence: float
    reasons: list[str]


class SubjectRouter:
    """Lightweight router that can later be replaced by a trained gate network."""

    def __init__(self, embed_fn: Optional[Callable[[str], list[float]]] = None):
        self.embed_fn = embed_fn
        self.keywords = {
            "math": ["معادله", "مجموعه", "انتگرال", "مشتق", "هندسه", "احتمال", "equations", "sets"],
            "physics": ["نیرو", "شتاب", "مدار", "الکتریسیته", "نور", "physics"],
            "chemistry": ["واکنش", "مول", "اسید", "پیوند", "شیمی", "chemistry"],
            "biology": ["سلول", "ژنتیک", "زیست", "photosynthesis", "biology"],
            "literature": ["آرایه", "شعر", "نثر", "ادبیات", "عروض"],
            "exam_strategy": ["کنکور", "زمان‌بندی", "تست", "دام آموزشی", "بودجه‌بندی"],
        }

    def route(self, text: str) -> RouteDecision:
        text_l = text.lower()
        scores: dict[str, float] = {e: 0.0 for e in EXPERTS}
        reasons: dict[str, list[str]] = {e: [] for e in EXPERTS}

        for expert, words in self.keywords.items():
            for w in words:
                if w.lower() in text_l:
                    scores[expert] += 1.0
                    reasons[expert].append(f"keyword:{w}")

        # Optional neural embedding hook can be added later for soft routing.
        best = max(scores.items(), key=lambda x: x[1])
        if best[1] <= 0:
            return RouteDecision(expert="general", confidence=0.35, reasons=["fallback:general"])

        total = sum(scores.values()) or 1.0
        conf = best[1] / total
        return RouteDecision(expert=best[0], confidence=round(conf, 3), reasons=reasons[best[0]])


class ExpertEnsemble:
    """
    Prototype ensemble:
    route -> choose specialist system prompt flavor.
    Later this can map to real LoRA experts / MoE experts.
    """

    SPECIALIST_PROMPTS = {
        "math": "You are Nova-Math, obsessive about exact reasoning and clean steps.",
        "physics": "You are Nova-Physics, connect formulas to real intuition and units.",
        "chemistry": "You are Nova-Chemistry, prioritize reactions, mechanisms and precision.",
        "biology": "You are Nova-Biology, explain living systems clearly and structurally.",
        "literature": "You are Nova-Literature, sensitive to language, devices and meaning.",
        "exam_strategy": "You are Nova-Exam, optimize for high-yield tactics and trap avoidance.",
        "general": "You are Nova, a precise Iranian educational tutor.",
    }

    def __init__(self, router: Optional[SubjectRouter] = None):
        self.router = router or SubjectRouter()

    def build_system_prompt(self, user_text: str, base: str = "") -> tuple[str, RouteDecision]:
        decision = self.router.route(user_text)
        specialist = self.SPECIALIST_PROMPTS[decision.expert]
        prompt = specialist if not base else f"{base}\n\n{specialist}"
        return prompt, decision


if __name__ == "__main__":
    ensemble = ExpertEnsemble()
    prompt, decision = ensemble.build_system_prompt("معادله ۲x + ۵ = ۱۳ را حل کن")
    print(decision)
    print(prompt)
