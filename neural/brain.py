#!/usr/bin/env python3
"""
Nova Neural Brain

High-level composition of:
- subject routing (MoE-style)
- educational retrieval (RAG)
- pedagogy reward scoring
- LLM / local engine call

This is the "serious mode" reasoning path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from neural.architecture.moe_subjects import ExpertEnsemble, RouteDecision
from neural.retrieval.edu_rag import EduRetriever, grounded_system_prompt
from neural.reward.pedagogy_reward import score_pedagogy, PedagogyScore


@dataclass
class BrainResult:
    answer: str
    route: RouteDecision
    pedagogy: PedagogyScore
    used_rag: bool
    context: str = ""


class NovaBrain:
    def __init__(
        self,
        llm_call: Callable[[str, str], str],
        retriever: Optional[EduRetriever] = None,
        ensemble: Optional[ExpertEnsemble] = None,
    ):
        self.llm = llm_call
        self.retriever = retriever
        self.ensemble = ensemble or ExpertEnsemble()

    def think(
        self,
        user_text: str,
        base_system: str = "You are Nova, an expert Iranian educational tutor.",
        use_rag: bool = True,
        k: int = 3,
    ) -> BrainResult:
        system, route = self.ensemble.build_system_prompt(user_text, base=base_system)
        context = ""
        if use_rag and self.retriever is not None:
            context = self.retriever.build_context(user_text, k=k)
            if context.strip():
                system = grounded_system_prompt(context) + "\n\n" + system

        answer = self.llm(system, user_text)
        ped = score_pedagogy(answer)
        return BrainResult(
            answer=answer,
            route=route,
            pedagogy=ped,
            used_rag=bool(context.strip()),
            context=context,
        )

    def rank_candidates(self, candidates: list[str]) -> list[tuple[str, PedagogyScore]]:
        ranked = [(c, score_pedagogy(c)) for c in candidates]
        ranked.sort(key=lambda x: x[1].total, reverse=True)
        return ranked


if __name__ == "__main__":
    def fake_llm(system: str, user: str) -> str:
        return (
            "مرحله ۱: مسئله را ساده می‌کنیم.\n"
            "مرحله ۲: مجهول را پیدا می‌کنیم.\n"
            "بنابراین جواب برابر ۴ است. مثال: ۲x=۸ → x=۴"
        )

    brain = NovaBrain(llm_call=fake_llm)
    result = brain.think("معادله ۲x+۵=۱۳ را توضیح بده")
    print(result.route)
    print(result.pedagogy)
    print(result.answer)
