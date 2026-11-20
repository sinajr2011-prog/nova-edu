#!/usr/bin/env python3
"""
Educational RAG for Nova.

Why this matters:
A specialist model becomes much stronger when it can ground answers in
textbook chunks, definitions, and worked examples.

This module starts with a simple local TF-IDF retriever so the system
works without external vector DBs. Later it can be swapped for FAISS / embedding search.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


@dataclass
class Doc:
    doc_id: str
    text: str
    metadata: dict[str, Any]


class EduRetriever:
    def __init__(self, docs: list[Doc]):
        self.docs = docs
        self.doc_tokens = [tokenize(d.text) for d in docs]
        self.df: Counter[str] = Counter()
        for toks in self.doc_tokens:
            for w in set(toks):
                self.df[w] += 1
        self.n = max(len(docs), 1)

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "EduRetriever":
        docs: list[Doc] = []
        with Path(path).open(encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                text = obj.get("text")
                if not text and "messages" in obj:
                    # fallback: join assistant contents
                    parts = [m.get("content", "") for m in obj["messages"] if m.get("role") == "assistant"]
                    text = "\n".join(parts)
                docs.append(
                    Doc(
                        doc_id=str(obj.get("id", i)),
                        text=text or "",
                        metadata=obj.get("metadata", {}),
                    )
                )
        return cls(docs)

    def _tfidf(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        vec = {}
        for w, c in tf.items():
            idf = math.log((self.n + 1) / (self.df.get(w, 0) + 1)) + 1.0
            vec[w] = (c / total) * idf
        return vec

    @staticmethod
    def _cos(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        dot = sum(v * b.get(k, 0.0) for k, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def search(self, query: str, k: int = 3) -> list[tuple[Doc, float]]:
        q = self._tfidf(tokenize(query))
        scored = []
        for doc, toks in zip(self.docs, self.doc_tokens):
            s = self._cos(q, self._tfidf(toks))
            scored.append((doc, s))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def build_context(self, query: str, k: int = 3) -> str:
        hits = self.search(query, k=k)
        blocks = []
        for i, (doc, score) in enumerate(hits, 1):
            blocks.append(
                f"[Source {i} | score={score:.3f} | id={doc.doc_id}]\n{doc.text}"
            )
        return "\n\n".join(blocks)


def grounded_system_prompt(context: str) -> str:
    return (
        "You are Nova, an Iranian educational tutor. "
        "Use the provided curriculum sources when relevant. "
        "If sources are insufficient, say what is missing instead of inventing curriculum facts.\n\n"
        f"SOURCES:\n{context}"
    )


if __name__ == "__main__":
    docs = [
        Doc("1", "اشتراک دو مجموعه عضوهای مشترک آن‌هاست.", {"topic": "sets"}),
        Doc("2", "برای حل معادله خطی، مجهول را ایزوله می‌کنیم.", {"topic": "equations"}),
    ]
    retriever = EduRetriever(docs)
    print(retriever.build_context("اشتراک مجموعه"))
