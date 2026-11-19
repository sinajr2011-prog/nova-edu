#!/usr/bin/env python3
"""
Local independent inference engine for Nova.

Goal: run Nova without cloud APIs when a local model is available.

Supports:
1) Hugging Face / Unsloth-style local transformers model
2) Fallback note for GGUF / llama.cpp / vLLM deployment
"""

from __future__ import annotations

import os
from typing import Optional


class LocalNovaEngine:
    def __init__(
        self,
        model_path: str,
        max_seq_length: int = 4096,
        load_in_4bit: bool = True,
    ):
        self.model_path = model_path
        self.max_seq_length = max_seq_length
        self.load_in_4bit = load_in_4bit
        self.model = None
        self.tokenizer = None

    def load(self):
        from unsloth import FastLanguageModel

        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.model_path,
            max_seq_length=self.max_seq_length,
            dtype=None,
            load_in_4bit=self.load_in_4bit,
        )
        FastLanguageModel.for_inference(self.model)
        return self

    def chat(self, system: str, user: str, max_new_tokens: int = 700) -> str:
        if self.model is None or self.tokenizer is None:
            self.load()

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.3,
            top_p=0.9,
            do_sample=True,
        )
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Best-effort: return only the completion tail
        if prompt in decoded:
            return decoded.split(prompt)[-1].strip()
        return decoded.strip()

    def __call__(self, system: str, user: str) -> str:
        return self.chat(system, user)


def get_best_engine():
    """
    Preference order:
    1. Local Nova model if NOVA_LOCAL_MODEL is set
    2. Cloud OpenAI-compatible API
    3. Fake demo LLM
    """
    local_path = os.getenv("NOVA_LOCAL_MODEL")
    if local_path:
        return LocalNovaEngine(local_path).load()

    from core.llm import get_llm_or_fake
    return get_llm_or_fake()
