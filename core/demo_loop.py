#!/usr/bin/env python3
"""
Demo of the full cool loop:

Student makes a mistake → Mistake Finder analyzes it →
Memory is updated → Question Designer creates targeted practice.

This file uses a fake LLM so you can run it without API keys.
Replace `fake_llm` with a real call later.
"""

from core.agents import NovaOrchestrator
from core.memory_store import StudentMemory


def fake_llm(system: str, user: str) -> str:
    """
    Very simple mock for demonstration.
    In production, replace with OpenAI / Qwen / local model call.
    """
    if "Mistake Finder" in system or "نقطه اشتباه" in user:
        return """نقطه اشتباه: وقتی دو طرف معادله را بر ۲ تقسیم نکرد
نوع اشتباه: محاسبه / بی‌دقتی جبری
توضیح اشتباه: بعد از رسیدن به ۲x = ۸، باید دو طرف بر ۲ تقسیم می‌شد تا x = ۴ به دست آید.
راه‌حل صحیح:
۲x + ۵ = ۱۳
۲x = ۱۳ - ۵
۲x = ۸
x = ۴
درس کلیدی: همیشه بعد از ایزوله کردن ضریب مجهول، آن را با تقسیم حذف کن.
"""
    return """سوال: معادله ۳x - ۷ = ۱۱ را حل کنید.
پاسخ نهایی: x = ۶
راه‌حل کامل:
۳x - ۷ = ۱۱
۳x = ۱۸
x = ۶
"""


def main():
    memory = StudentMemory("sina_demo")
    memory.set_grade(9)
    memory.add_goal("konkur")

    orchestrator = NovaOrchestrator(llm_call=fake_llm)

    problem = "معادله ۲x + ۵ = ۱۳ را حل کن."
    student_solution = "۲x + ۵ = ۱۳ → ۲x = ۸ → x = ۲"  # intentional mistake

    result = orchestrator.mistake_to_practice(
        problem=problem,
        student_solution=student_solution,
        topic="equations",
        memory=memory,
        style="kind",
        n_questions=2,
    )

    print("=" * 50)
    print("MISTAKE REPORT")
    print("=" * 50)
    print(result.mistake_report.to_prompt_block())

    print("\n" + "=" * 50)
    print("TARGETED PRACTICE QUESTIONS")
    print("=" * 50)
    for i, q in enumerate(result.practice_questions, 1):
        print(f"\n--- Question {i} ---")
        print(q.question)
        print("Answer:", q.answer)

    print("\n" + "=" * 50)
    print("STUDENT MEMORY SUMMARY")
    print("=" * 50)
    print(memory.summary())


if __name__ == "__main__":
    main()
