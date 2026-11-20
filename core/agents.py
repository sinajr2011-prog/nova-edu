#!/usr/bin/env python3
"""
Nova Agent System — core orchestration.

Coordinates Mistake Finder, Question Designer, Visual Explainer,
and optional NovaBrain (routing + RAG + pedagogy).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from core.memory_store import StudentMemory

BASE_PERSONA = (
    "You are Nova, an expert Iranian educational tutor for secondary school, "
    "Konkur, Tizhooshan and Olympiad. Always answer in clear Persian with proper نیم‌فاصله. "
    "Be precise, pedagogical, and never invent curriculum facts."
)

STYLES = {
    "kind": "سبک: مهربون، تشویق‌کننده و صبور باش.",
    "strict": "سبک: مستقیم، جدی و دقیق باش. نقاط ضعف را واضح بگو.",
    "konkur": "سبک: کنکوری، سریع، نکته‌ای و متمرکز روی دام‌ها و تست.",
    "deep": "سبک: مفهومی و عمیق. روی چرایی‌ها تمرکز کن.",
}


def style_prefix(style: str = "kind") -> str:
    return STYLES.get(style, STYLES["kind"])


@dataclass
class MistakeReport:
    error_location: str
    error_type: str
    explanation: str
    correct_solution: str
    key_lesson: str
    topic: str = "general"

    def to_prompt_block(self) -> str:
        return (
            f"نقطه اشتباه: {self.error_location}\n"
            f"نوع اشتباه: {self.error_type}\n"
            f"توضیح: {self.explanation}\n"
            f"راه‌حل صحیح:\n{self.correct_solution}\n"
            f"درس کلیدی: {self.key_lesson}"
        )


@dataclass
class GeneratedQuestion:
    question: str
    answer: str
    solution: str
    difficulty: str
    topic: str
    question_type: str = "short_answer"


class BaseAgent:
    def __init__(self, llm_call):
        self.llm = llm_call


class MistakeFinderAgent(BaseAgent):
    def analyze(
        self,
        problem: str,
        student_solution: str,
        topic: str = "general",
        style: str = "kind",
    ) -> MistakeReport:
        system = f"{BASE_PERSONA}\n{style_prefix(style)}\n\nYou are the Mistake Finder agent."
        user = f"""صورت مسئله:
{problem}

راه‌حل دانش‌آموز:
{student_solution}

خروجی را دقیقاً با این ساختار بده:
نقطه اشتباه:
نوع اشتباه:
توضیح اشتباه:
راه‌حل صحیح:
درس کلیدی:
"""
        raw = self.llm(system, user)
        return self._parse(raw, topic)

    def _parse(self, raw: str, topic: str) -> MistakeReport:
        import re

        def extract(label: str) -> str:
            m = re.search(rf"{label}:\s*(.*?)(?=\n(?:نقطه|نوع|توضیح|راه‌حل|درس)|$)", raw, re.S)
            return m.group(1).strip() if m else raw.strip()

        return MistakeReport(
            error_location=extract("نقطه اشتباه"),
            error_type=extract("نوع اشتباه"),
            explanation=extract("توضیح اشتباه"),
            correct_solution=extract("راه‌حل صحیح"),
            key_lesson=extract("درس کلیدی"),
            topic=topic,
        )


class QuestionDesignerAgent(BaseAgent):
    def generate(
        self,
        topic: str,
        difficulty: str = "medium",
        based_on_mistake: Optional[MistakeReport] = None,
        count: int = 1,
        style: str = "kind",
    ) -> list[GeneratedQuestion]:
        system = f"{BASE_PERSONA}\n{style_prefix(style)}\n\nYou are the Question Designer agent."

        extra = ""
        if based_on_mistake:
            extra = (
                "\nاین سوال باید روی ضعفی که در این اشتباه دیده شده تمرکز کند:\n"
                + based_on_mistake.to_prompt_block()
            )

        user = f"""یک سوال {difficulty} در موضوع «{topic}» طراحی کن.{extra}

خروجی را دقیقاً با این ساختار بده:
سوال:
پاسخ نهایی:
راه‌حل کامل:
"""
        questions = []
        for _ in range(count):
            raw = self.llm(system, user)
            questions.append(self._parse(raw, topic, difficulty))
        return questions

    def _parse(self, raw: str, topic: str, difficulty: str) -> GeneratedQuestion:
        import re

        def extract(label: str) -> str:
            m = re.search(rf"{label}:\s*(.*?)(?=\n(?:سوال|پاسخ|راه‌حل)|$)", raw, re.S)
            return m.group(1).strip() if m else raw.strip()

        return GeneratedQuestion(
            question=extract("سوال"),
            answer=extract("پاسخ نهایی"),
            solution=extract("راه‌حل کامل"),
            difficulty=difficulty,
            topic=topic,
        )


class VisualExplainerAgent(BaseAgent):
    def __init__(self, llm_call, multimodal_service=None):
        super().__init__(llm_call)
        self.mm = multimodal_service

    def create_diagram(self, concept: str, output_path: str, extra: str = "") -> str:
        if self.mm is None:
            raise RuntimeError("MultimodalService not attached")
        path = self.mm.create_diagram(concept=concept, output_path=output_path, extra=extra)
        return str(path)

    def create_animation(self, concept: str, output_path: str, duration: int = 5) -> str:
        if self.mm is None:
            raise RuntimeError("MultimodalService not attached")
        path = self.mm.create_animation(
            concept=concept, output_path=output_path, duration=duration
        )
        return str(path)


@dataclass
class PracticeLoopResult:
    mistake_report: MistakeReport
    practice_questions: list[GeneratedQuestion] = field(default_factory=list)


@dataclass
class TeachResult:
    answer: str
    route_expert: str = "general"
    pedagogy_score: float = 0.0
    used_rag: bool = False


class NovaOrchestrator:
    """Central orchestrator for Nova agents + optional neural brain."""

    def __init__(self, llm_call, multimodal_service=None, brain=None):
        self.llm = llm_call
        self.mistake_finder = MistakeFinderAgent(llm_call)
        self.question_designer = QuestionDesignerAgent(llm_call)
        self.visual = VisualExplainerAgent(llm_call, multimodal_service)
        self.brain = brain

    def teach(self, user_text: str, style: str = "kind") -> TeachResult:
        """Best-effort teaching path using NovaBrain when available."""
        base = f"{BASE_PERSONA}\n{style_prefix(style)}"
        if self.brain is not None:
            result = self.brain.think(user_text, base_system=base, use_rag=True)
            return TeachResult(
                answer=result.answer,
                route_expert=result.route.expert,
                pedagogy_score=result.pedagogy.total,
                used_rag=result.used_rag,
            )
        answer = self.llm(base, user_text)
        return TeachResult(answer=answer)

    def mistake_to_practice(
        self,
        problem: str,
        student_solution: str,
        topic: str,
        memory: Optional[StudentMemory] = None,
        style: str = "kind",
        n_questions: int = 2,
    ) -> PracticeLoopResult:
        report = self.mistake_finder.analyze(
            problem=problem,
            student_solution=student_solution,
            topic=topic,
            style=style,
        )

        if memory:
            memory.log_mistake(
                topic=report.topic,
                mistake_type=report.error_type,
                example=report.error_location,
            )
            memory.update_mastery(topic, 0.35)

        questions = self.question_designer.generate(
            topic=topic,
            difficulty="medium",
            based_on_mistake=report,
            count=n_questions,
            style=style,
        )

        return PracticeLoopResult(mistake_report=report, practice_questions=questions)
