#!/usr/bin/env python3
"""
Batch-synthesize educational SFT samples for Nova.

Modes:
1) --mode template  : offline high-volume generation (no API)
2) --mode llm       : use OpenAI-compatible / local LLM if configured

Example:
  python data/pipeline/batch_synthesize.py \
    --topics data/curriculum/topic_seeds.jsonl \
    --out data/sft/synthetic_batch.jsonl \
    --per-topic 20 --mode template
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SYSTEM = (
    "You are Nova, an expert Iranian educational tutor specialized in "
    "secondary school curriculum, Konkur, Tizhooshan and Olympiad preparation. "
    "Explain clearly in Persian with correct نیم‌فاصله and step-by-step reasoning."
)


def load_topics(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def gen_sets(rng: random.Random, difficulty: str, kind: str) -> tuple[str, str]:
    A = sorted(rng.sample(range(1, 12), k=rng.randint(3, 5)))
    B = sorted(rng.sample(range(1, 12), k=rng.randint(3, 5)))
    setA, setB = set(A), set(B)
    if kind == "concept_explanation":
        user = "اتحاد و اشتراک دو مجموعه را با یک مثال عددی توضیح بده."
        assistant = (
            f"فرض کن A = {{{', '.join(map(str, A))}}} و "
            f"B = {{{', '.join(map(str, B))}}}.\n\n"
            f"اتحاد یعنی همه عضوهایی که حداقل در یکی هستند:\n"
            f"A ∪ B = {{{', '.join(map(str, sorted(setA | setB)))}}}\n\n"
            f"اشتراک یعنی عضوهای مشترک:\n"
            f"A ∩ B = {{{', '.join(map(str, sorted(setA & setB))) if setA & setB else '∅'}}}\n\n"
            "نکته: در اتحاد تکرار نمی‌نویسیم و ترتیب مهم نیست."
        )
    elif kind == "worked_example":
        user = f"اگر A={{{', '.join(map(str, A))}}} و B={{{', '.join(map(str, B))}}} باشد، A−B و B−A را پیدا کن."
        assistant = (
            f"A − B = {{{', '.join(map(str, sorted(setA - setB))) if setA - setB else '∅'}}}\n"
            f"B − A = {{{', '.join(map(str, sorted(setB - setA))) if setB - setA else '∅'}}}\n\n"
            "تفاضل جابه‌جایی ندارد؛ عضوهایی را برمی‌داریم که فقط در مجموعه اول باشند."
        )
    elif kind == "mistake_repair":
        user = "دانش‌آموز نوشته چون A ⊆ B پس A ∪ B = A. اشتباه را درست کن."
        assistant = (
            "اشتباه در نتیجه‌گیری از زیرمجموعه بودن است.\n"
            "اگر A ⊆ B باشد، آن‌گاه:\n"
            "A ∪ B = B و A ∩ B = A\n\n"
            "پس اتحاد برابر مجموعه بزرگ‌تر است، نه A."
        )
    else:
        nA, nB, nI = rng.randint(8, 15), rng.randint(6, 12), rng.randint(2, 5)
        user = f"اگر n(A)={nA} و n(B)={nB} و n(A∩B)={nI} باشد، n(A∪B) را پیدا کن."
        ans = nA + nB - nI
        assistant = (
            "از فرمول:\nn(A ∪ B) = n(A) + n(B) − n(A ∩ B)\n\n"
            f"{nA} + {nB} − {nI} = {ans}\n\nجواب: {ans}"
        )
    return user, assistant


def gen_equations(rng: random.Random, difficulty: str, kind: str) -> tuple[str, str]:
    a = rng.randint(2, 9)
    x = rng.randint(-6, 12)
    b = rng.randint(-12, 12)
    c = a * x + b
    if kind == "concept_explanation":
        user = "معادله خطی یک‌مجهولی را تعریف کن و یک مثال بزن."
        assistant = (
            "معادله خطی یک‌مجهولی معادله‌ای با یک مجهول و توان ۱ است.\n"
            f"مثال: {a}x + ({b}) = {c}\n"
            f"با جدا کردن مجهول به x = {x} می‌رسیم."
        )
    elif kind == "worked_example":
        user = f"معادله {a}x + ({b}) = {c} را حل کن."
        assistant = (
            f"مرحله ۱: عدد ثابت را جابه‌جا می‌کنیم.\n{a}x = {c} - ({b}) = {c - b}\n\n"
            f"مرحله ۲: دو طرف را بر {a} تقسیم می‌کنیم.\nx = {x}\n\n"
            f"بررسی: {a}({x}) + ({b}) = {c} ✓"
        )
    elif kind == "mistake_repair":
        user = f"دانش‌آموز برای {a}(x - 3) = {a*5} نوشته x - 3 = {a*5}. اشتباه چیست؟"
        assistant = (
            f"ضریب {a} روی کل پرانتز اثر دارد و باید دو طرف بر {a} تقسیم شود.\n"
            f"شکل درست: x - 3 = 5 → x = 8\n\n"
            "درس کلیدی: ضریب بیرون پرانتز را حذف بی‌مورد نکن."
        )
    else:
        user = f"معادله {a}x - {a+1} = {a-1}x + {b} را حل کن."
        # solve: a x - (a+1) = (a-1)x + b => a x - (a-1)x = b + a + 1 => x = ...
        left_coef = a - (a - 1)
        right = b + a + 1
        sol = right // left_coef if left_coef else 0
        assistant = (
            f"{a}x - {a+1} = {a-1}x + {b}\n"
            f"{a}x - {a-1}x = {b} + {a+1}\n"
            f"{left_coef}x = {right}\n"
            f"x = {sol}"
        )
    return user, assistant


def gen_generic(topic: str, difficulty: str, kind: str) -> tuple[str, str]:
    user = f"درباره موضوع «{topic}» یک آموزش {difficulty} از نوع {kind} ارائه بده."
    assistant = (
        f"موضوع: {topic}\n\n"
        "مرحله ۱: تعریف مفهوم را ساده بیان می‌کنیم.\n"
        "مرحله ۲: یک مثال مشخص می‌زنیم.\n"
        "مرحله ۳: نکته یا اشتباه رایج را یادآوری می‌کنیم.\n\n"
        "این الگو برای یادگیری پایدار مفید است و بعداً با داده تخصصی‌تر جایگزین می‌شود."
    )
    return user, assistant


def synthesize_one(spec: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    topic = spec.get("topic", "general")
    difficulty = spec.get("difficulty", "medium")
    kind = spec.get("type", "concept_explanation")
    subject = spec.get("subject", "math")

    if topic == "sets":
        user, assistant = gen_sets(rng, difficulty, kind)
    elif topic in {"equations", "word_problems"}:
        user, assistant = gen_equations(rng, difficulty, kind)
    else:
        user, assistant = gen_generic(topic, difficulty, kind)

    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": {
            "subject": subject,
            "grade": spec.get("grade", 9),
            "topic": topic,
            "source": "batch_synthetic",
            "difficulty": difficulty,
            "type": kind,
        },
    }


def synthesize_llm(spec: dict[str, Any], llm) -> dict[str, Any]:
    topic = spec.get("topic", "general")
    difficulty = spec.get("difficulty", "medium")
    kind = spec.get("type", "concept_explanation")
    user = (
        f"یک نمونه آموزشی فارسی برای پایه {spec.get('grade', 9)} بساز.\n"
        f"موضوع: {topic}\nنوع: {kind}\nسختی: {difficulty}\n"
        "خروجی فقط متن آموزش کامل باشد."
    )
    assistant = llm(SYSTEM, user)
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": {
            "subject": spec.get("subject", "math"),
            "grade": spec.get("grade", 9),
            "topic": topic,
            "source": "batch_llm",
            "difficulty": difficulty,
            "type": kind,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", default="data/curriculum/topic_seeds.jsonl")
    parser.add_argument("--out", default="data/sft/synthetic_batch.jsonl")
    parser.add_argument("--per-topic", type=int, default=15)
    parser.add_argument("--mode", choices=["template", "llm"], default="template")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    topics = load_topics(Path(args.topics))
    rng = random.Random(args.seed)
    llm = None
    if args.mode == "llm":
        from core.llm import get_llm_or_fake
        llm = get_llm_or_fake()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    with out.open("w", encoding="utf-8") as f:
        for spec in topics:
            for _ in range(args.per_topic):
                row = synthesize_llm(spec, llm) if args.mode == "llm" else synthesize_one(spec, rng)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                n += 1

    print(f"wrote {n} samples → {out}")


if __name__ == "__main__":
    main()
