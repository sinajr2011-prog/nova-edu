#!/usr/bin/env python3
"""
Flexible LLM client for Nova-Edu.

Supports any OpenAI-compatible API:
- OpenAI
- OpenRouter
- Together
- Fireworks
- DashScope (Qwen)
- Local vLLM / Ollama (OpenAI-compatible endpoint)
"""

from __future__ import annotations

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


class LLMClient:
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.4,
    ):
        if OpenAI is None:
            raise ImportError("Please install openai: pip install openai")

        self.model = model or os.getenv("NOVA_MODEL", "qwen/qwen2.5-14b-instruct")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        self.temperature = temperature

        if not self.api_key:
            raise ValueError(
                "No API key found. Set OPENAI_API_KEY or OPENROUTER_API_KEY"
            )

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""

    def __call__(self, system: str, user: str) -> str:
        return self.chat(system, user)


def get_llm() -> LLMClient:
    """Factory with sensible defaults for Nova."""
    return LLMClient()


def get_llm_or_fake():
    """
    Returns a real LLM if keys exist, otherwise a fake one for demos.
    """
    try:
        return get_llm()
    except Exception:
        def fake(system: str, user: str) -> str:
            if "Mistake Finder" in system or "نقطه اشتباه" in user:
                return (
                    "نقطه اشتباه: تقسیم نکردن دو طرف معادله\n"
                    "نوع اشتباه: محاسبه جبری\n"
                    "توضیح اشتباه: بعد از ۲x = ۸ باید بر ۲ تقسیم می‌شد.\n"
                    "راه‌حل صحیح:\n۲x + ۵ = ۱۳\n۲x = ۸\nx = ۴\n"
                    "درس کلیدی: همیشه ضریب مجهول را با تقسیم حذف کن."
                )
            return (
                "سوال: معادله ۳x - ۷ = ۱۱ را حل کنید.\n"
                "پاسخ نهایی: x = ۶\n"
                "راه‌حل کامل:\n۳x - ۷ = ۱۱\n۳x = ۱۸\nx = ۶"
            )
        return fake
