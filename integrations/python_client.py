#!/usr/bin/env python3
"""
Minimal Python client for educational platforms integrating Nova-Edu.
"""

from __future__ import annotations

from typing import Any, Optional

import requests


class NovaClient:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        r = requests.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _get(self, path: str) -> dict[str, Any]:
        r = requests.get(f"{self.base_url}{path}", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def analyze_mistake(
        self,
        student_id: str,
        problem: str,
        student_solution: str,
        topic: str = "general",
        n_questions: int = 2,
        style: str = "kind",
    ) -> dict[str, Any]:
        return self._post(
            "/v1/mistake-analysis",
            {
                "student_id": student_id,
                "problem": problem,
                "student_solution": student_solution,
                "topic": topic,
                "n_questions": n_questions,
                "style": style,
            },
        )

    def generate_questions(
        self,
        topic: str,
        difficulty: str = "medium",
        count: int = 2,
        style: str = "kind",
    ) -> dict[str, Any]:
        return self._post(
            "/v1/generate-questions",
            {
                "topic": topic,
                "difficulty": difficulty,
                "count": count,
                "style": style,
            },
        )

    def tutor_chat(
        self,
        student_id: str,
        message: str,
        topic: Optional[str] = None,
        style: str = "kind",
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "student_id": student_id,
            "message": message,
            "style": style,
        }
        if topic:
            payload["topic"] = topic
        return self._post("/v1/tutor-chat", payload)

    def get_memory(self, student_id: str) -> dict[str, Any]:
        return self._get(f"/v1/students/{student_id}/memory")


if __name__ == "__main__":
    client = NovaClient()
    print(client.analyze_mistake(
        student_id="demo",
        problem="۲x + ۵ = ۱۳",
        student_solution="x = ۲",
        topic="equations",
    ))
