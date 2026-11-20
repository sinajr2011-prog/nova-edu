#!/usr/bin/env python3
"""
Pedagogy reward signals for Nova.

Before a trained neural reward model exists, we use strong heuristics that
approximate what a good teacher response should contain.

These scores can already be used for:
- filtering synthetic data
- ranking candidate answers
- building DPO pairs (chosen vs rejected)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PedagogyScore:
    total: float
    breakdown: dict[str, float]

    def as_dict(self) -> dict:
        return {"total": self.total, "breakdown": self.breakdown}


POSITIVE_MARKERS = [
    "مرحله", "ابتدا", "سپس", "در نهایت", "چون", "بنابراین", "مثال",
    "نکته", "اشتباه رایج", "پس", "فرض", "نتیجه",
]

NEGATIVE_MARKERS = [
    "نمی‌دانم دقیقا", "خودت سرچ کن", "واضح است", "بدون توضیح",
]


def score_pedagogy(text: str) -> PedagogyScore:
    t = text.strip()
    breakdown: dict[str, float] = {}

    # structure / process
    structure = 0.0
    for m in ["مرحله", "ابتدا", "سپس", "در نهایت", "گام"]:
        if m in t:
            structure += 0.08
    breakdown["structure"] = min(structure, 0.3)

    # explanatory language
    explain = 0.0
    for m in ["چون", "زیرا", "بنابراین", "یعنی", "در نتیجه"]:
        if m in t:
            explain += 0.07
    breakdown["explanation"] = min(explain, 0.25)

    # examples
    breakdown["example"] = 0.15 if "مثال" in t else 0.0

    # length sweet spot (too short = weak teaching; absurdly long = noisy)
    n = len(t)
    if n < 40:
        length = 0.0
    elif n < 120:
        length = 0.08
    elif n < 1200:
        length = 0.2
    else:
        length = 0.1
    breakdown["length"] = length

    # penalties
    penalty = 0.0
    for m in NEGATIVE_MARKERS:
        if m in t:
            penalty += 0.15
    breakdown["penalty"] = -min(penalty, 0.4)

    total = max(0.0, min(1.0, sum(breakdown.values())))
    return PedagogyScore(total=round(total, 3), breakdown=breakdown)


def choose_better(a: str, b: str) -> tuple[str, str, PedagogyScore, PedagogyScore]:
    """Return (chosen, rejected, score_a, score_b) for DPO pair mining."""
    sa, sb = score_pedagogy(a), score_pedagogy(b)
    if sa.total >= sb.total:
        return a, b, sa, sb
    return b, a, sa, sb


if __name__ == "__main__":
    weak = "x=4"
    strong = (
        "مرحله ۱: ۵ را از دو طرف کم می‌کنیم.\n"
        "۲x = ۸\n"
        "مرحله ۲: دو طرف را بر ۲ تقسیم می‌کنیم.\n"
        "x = ۴\n"
        "چون ضریب x برابر ۲ بود، با تقسیم حذف شد. مثال مشابه: ۳x=۱۲ → x=۴"
    )
    print(score_pedagogy(weak))
    print(score_pedagogy(strong))
    print(choose_better(weak, strong)[0][:40])
