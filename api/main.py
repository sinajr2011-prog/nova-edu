#!/usr/bin/env python3
"""
Nova-Edu REST API

This is the main integration surface for educational platforms.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.local_engine import get_best_engine
from core.memory_store import StudentMemory
from core.agents import NovaOrchestrator

app = FastAPI(
    title="Nova-Edu API",
    description="Educational multi-agent engine for Iranian learning platforms",
    version="0.1.0",
)

llm = get_best_engine()
orchestrator = NovaOrchestrator(llm_call=llm)


class MistakeAnalysisRequest(BaseModel):
    student_id: str = Field(..., examples=["student_01"])
    problem: str
    student_solution: str
    topic: str = "general"
    style: str = "kind"
    n_questions: int = 2


class QuestionRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    style: str = "kind"
    count: int = 2
    student_id: Optional[str] = None


class TutorChatRequest(BaseModel):
    student_id: str
    message: str
    style: str = "kind"
    topic: Optional[str] = None


class MemoryUpdateRequest(BaseModel):
    grade: Optional[int] = None
    goal: Optional[str] = None
    strength: Optional[str] = None
    weakness: Optional[str] = None


def get_memory(student_id: str) -> StudentMemory:
    return StudentMemory(student_id)


@app.get("/health")
def health():
    return {"status": "ok", "service": "nova-edu"}


@app.post("/v1/mistake-analysis")
def mistake_analysis(payload: MistakeAnalysisRequest) -> dict[str, Any]:
    try:
        memory = get_memory(payload.student_id)
        result = orchestrator.mistake_to_practice(
            problem=payload.problem,
            student_solution=payload.student_solution,
            topic=payload.topic,
            memory=memory,
            style=payload.style,
            n_questions=payload.n_questions,
        )

        return {
            "student_id": payload.student_id,
            "mistake_report": {
                "error_location": result.mistake_report.error_location,
                "error_type": result.mistake_report.error_type,
                "explanation": result.mistake_report.explanation,
                "correct_solution": result.mistake_report.correct_solution,
                "key_lesson": result.mistake_report.key_lesson,
                "topic": result.mistake_report.topic,
            },
            "practice_questions": [
                {
                    "question": q.question,
                    "answer": q.answer,
                    "solution": q.solution,
                    "difficulty": q.difficulty,
                    "topic": q.topic,
                }
                for q in result.practice_questions
            ],
            "memory_summary": memory.summary(),
            "focus_topics": memory.get_focus_topics(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/generate-questions")
def generate_questions(payload: QuestionRequest) -> dict[str, Any]:
    try:
        questions = orchestrator.question_designer.generate(
            topic=payload.topic,
            difficulty=payload.difficulty,
            count=payload.count,
            style=payload.style,
        )
        return {
            "topic": payload.topic,
            "questions": [
                {
                    "question": q.question,
                    "answer": q.answer,
                    "solution": q.solution,
                    "difficulty": q.difficulty,
                    "topic": q.topic,
                }
                for q in questions
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/tutor-chat")
def tutor_chat(payload: TutorChatRequest) -> dict[str, Any]:
    try:
        memory = get_memory(payload.student_id)
        focus = ", ".join(memory.get_focus_topics()) or "عمومی"

        system = (
            "You are Nova, an expert Iranian educational tutor. "
            "Answer in clear Persian with proper نیم‌فاصله. "
            f"Student focus topics: {focus}."
        )
        if payload.topic:
            system += f" Current topic: {payload.topic}."

        answer = llm(system, payload.message)
        memory.log_session(
            summary=payload.message[:120],
            topics=[payload.topic] if payload.topic else [],
        )

        return {
            "student_id": payload.student_id,
            "reply": answer,
            "focus_topics": memory.get_focus_topics(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/students/{student_id}/memory")
def student_memory(student_id: str) -> dict[str, Any]:
    memory = get_memory(student_id)
    return {
        "student_id": student_id,
        "summary": memory.summary(),
        "data": memory.data,
        "focus_topics": memory.get_focus_topics(),
    }


@app.post("/v1/students/{student_id}/memory")
def update_memory(student_id: str, payload: MemoryUpdateRequest) -> dict[str, Any]:
    memory = get_memory(student_id)
    if payload.grade is not None:
        memory.set_grade(payload.grade)
    if payload.goal:
        memory.add_goal(payload.goal)
    if payload.strength:
        memory.add_strength(payload.strength)
    if payload.weakness:
        memory.add_weakness(payload.weakness)
    return {"ok": True, "summary": memory.summary()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
