#!/usr/bin/env python3
"""
Long-term Student Memory Store for Nova-Edu.

Simple but powerful JSON-based memory that tracks:
- strengths / weaknesses
- mistake history
- topic mastery scores
- recent sessions
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class StudentMemory:
    def __init__(self, student_id: str, data_dir: str | Path = "data/memory"):
        self.student_id = student_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / f"{student_id}.json"
        self.data = self._load()

    def _default(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "created_at": _now(),
            "updated_at": _now(),
            "profile": {
                "grade": None,
                "goals": [],
            },
            "strengths": [],
            "weaknesses": [],
            "mistake_history": [],
            "topic_mastery": {},
            "recent_sessions": [],
        }

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return self._default()

    def save(self) -> None:
        self.data["updated_at"] = _now()
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---------- Profile ----------
    def set_grade(self, grade: int) -> None:
        self.data["profile"]["grade"] = grade
        self.save()

    def add_goal(self, goal: str) -> None:
        goals = self.data["profile"].setdefault("goals", [])
        if goal not in goals:
            goals.append(goal)
            self.save()

    # ---------- Strengths / Weaknesses ----------
    def add_strength(self, topic: str) -> None:
        if topic not in self.data["strengths"]:
            self.data["strengths"].append(topic)
        if topic in self.data["weaknesses"]:
            self.data["weaknesses"].remove(topic)
        self.save()

    def add_weakness(self, topic: str) -> None:
        if topic not in self.data["weaknesses"]:
            self.data["weaknesses"].append(topic)
        self.save()

    # ---------- Mistakes ----------
    def log_mistake(
        self,
        topic: str,
        mistake_type: str,
        example: str = "",
        severity: str = "medium",
    ) -> None:
        entry = {
            "topic": topic,
            "mistake_type": mistake_type,
            "example": example,
            "severity": severity,
            "timestamp": _now(),
        }
        self.data["mistake_history"].append(entry)
        # Keep last 100 mistakes
        self.data["mistake_history"] = self.data["mistake_history"][-100:]
        self.add_weakness(topic)
        self.save()

    # ---------- Mastery ----------
    def update_mastery(self, topic: str, score: float) -> None:
        """score between 0.0 and 1.0"""
        score = max(0.0, min(1.0, score))
        old = self.data["topic_mastery"].get(topic)
        if old is None:
            self.data["topic_mastery"][topic] = score
        else:
            # Exponential moving average
            self.data["topic_mastery"][topic] = round(0.7 * old + 0.3 * score, 3)

        # Auto promote/demote
        current = self.data["topic_mastery"][topic]
        if current >= 0.8:
            self.add_strength(topic)
        elif current <= 0.45:
            self.add_weakness(topic)

        self.save()

    # ---------- Sessions ----------
    def log_session(self, summary: str, topics: list[str] | None = None) -> None:
        entry = {
            "timestamp": _now(),
            "summary": summary,
            "topics": topics or [],
        }
        self.data["recent_sessions"].append(entry)
        self.data["recent_sessions"] = self.data["recent_sessions"][-30:]
        self.save()

    # ---------- Insights ----------
    def get_focus_topics(self, limit: int = 3) -> list[str]:
        """Return topics that need the most attention."""
        weaknesses = self.data.get("weaknesses", [])
        mastery = self.data.get("topic_mastery", {})

        scored = []
        for t in weaknesses:
            scored.append((t, mastery.get(t, 0.3)))

        for t, score in mastery.items():
            if t not in weaknesses and score < 0.55:
                scored.append((t, score))

        scored.sort(key=lambda x: x[1])
        return [t for t, _ in scored[:limit]]

    def summary(self) -> str:
        focus = self.get_focus_topics()
        strengths = self.data.get("strengths", [])
        return (
            f"Student `{self.student_id}`\n"
            f"Strengths: {', '.join(strengths) or '—'}\n"
            f"Focus now: {', '.join(focus) or '—'}\n"
            f"Tracked topics: {len(self.data.get('topic_mastery', {}))}\n"
            f"Mistakes logged: {len(self.data.get('mistake_history', []))}"
        )


if __name__ == "__main__":
    mem = StudentMemory("demo_student")
    mem.set_grade(9)
    mem.add_goal("konkur")
    mem.update_mastery("sets", 0.85)
    mem.update_mastery("equations", 0.4)
    mem.log_mistake("equations", "sign_error", "2x = 8 → x = 2 (forgot divide)")
    mem.log_session("Practiced sets and equations", ["sets", "equations"])
    print(mem.summary())
    print("Focus topics:", mem.get_focus_topics())
