#!/usr/bin/env python3
"""
Demo of the full cool loop with real or fake LLM.

Student makes a mistake → Mistake Finder → Memory update → Targeted questions.
"""

from core.agents import NovaOrchestrator
from core.memory_store import StudentMemory
from core.llm import get_llm_or_fake


def main():
    llm = get_llm_or_fake()
    memory = StudentMemory("sina_demo")
    memory.set_grade(9)
    memory.add_goal("konkur")

    orchestrator = NovaOrchestrator(llm_call=llm)

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
