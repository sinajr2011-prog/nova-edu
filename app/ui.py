#!/usr/bin/env python3
"""
Nova-Edu — Gradio Interface

A clean and powerful UI around the multi-agent system.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import gradio as gr

from core.local_engine import get_best_engine
from core.memory_store import StudentMemory
from core.agents import NovaOrchestrator

llm = get_best_engine()
orchestrator = NovaOrchestrator(llm_call=llm)


def get_memory(student_id: str) -> StudentMemory:
    sid = (student_id or "default_student").strip() or "default_student"
    return StudentMemory(sid)


def run_mistake_loop(
    student_id: str,
    problem: str,
    student_solution: str,
    topic: str,
    style: str,
    n_questions: int,
):
    if not problem.strip() or not student_solution.strip():
        return "لطفاً صورت مسئله و راه‌حل دانش‌آموز را وارد کن.", "", ""

    memory = get_memory(student_id)
    result = orchestrator.mistake_to_practice(
        problem=problem.strip(),
        student_solution=student_solution.strip(),
        topic=topic.strip() or "general",
        memory=memory,
        style=style,
        n_questions=int(n_questions),
    )

    report = result.mistake_report.to_prompt_block()

    questions_text = []
    for i, q in enumerate(result.practice_questions, 1):
        questions_text.append(
            f"### سوال {i}\n{q.question}\n\n"
            f"**پاسخ:** {q.answer}\n\n"
            f"**راه‌حل:**\n{q.solution}"
        )

    memory_summary = memory.summary()
    return report, "\n\n---\n\n".join(questions_text), memory_summary


def run_question_designer(topic: str, difficulty: str, style: str, count: int):
    questions = orchestrator.question_designer.generate(
        topic=topic.strip() or "math",
        difficulty=difficulty,
        count=int(count),
        style=style,
    )
    blocks = []
    for i, q in enumerate(questions, 1):
        blocks.append(
            f"### سوال {i} ({q.difficulty})\n{q.question}\n\n"
            f"**پاسخ:** {q.answer}\n\n**راه‌حل:**\n{q.solution}"
        )
    return "\n\n---\n\n".join(blocks)


def show_memory(student_id: str):
    memory = get_memory(student_id)
    data = memory.data
    lines = [
        memory.summary(),
        "",
        "**Weaknesses:** " + ", ".join(data.get("weaknesses", []) or ["—"]),
        "**Strengths:** " + ", ".join(data.get("strengths", []) or ["—"]),
        "",
        "**Topic Mastery:**",
    ]
    for t, score in data.get("topic_mastery", {}).items():
        lines.append(f"- {t}: {score:.2f}")

    if data.get("mistake_history"):
        lines.append("\n**Recent Mistakes:**")
        for m in data["mistake_history"][-5:]:
            lines.append(
                f"- [{m.get('topic')}] {m.get('mistake_type')}: {m.get('example', '')[:80]}"
            )

    return "\n".join(lines)


def build_ui():
    with gr.Blocks(
        title="Nova-Edu",
        theme=gr.themes.Soft(primary_hue="indigo"),
        css="""
        .rtl textarea, .rtl input, .rtl .prose { direction: rtl; text-align: right; }
        """,
    ) as demo:
        gr.Markdown(
            """
            # نِوا | Nova-Edu
            **معلم هوشمند چندعاملی ایرانی** — Mistake Finder + Question Designer + Memory
            """
        )

        student_id = gr.Textbox(
            label="شناسه دانش‌آموز",
            value="student_01",
            placeholder="مثلاً sina_9th",
        )

        with gr.Tab("🔍 پیدا کردن اشتباه + تمرین هدفمند"):
            with gr.Row():
                with gr.Column():
                    problem = gr.Textbox(
                        label="صورت مسئله",
                        lines=3,
                        placeholder="معادله ۲x + ۵ = ۱۳ را حل کن.",
                        elem_classes=["rtl"],
                    )
                    student_sol = gr.Textbox(
                        label="راه‌حل دانش‌آموز",
                        lines=4,
                        placeholder="راه‌حل دانش‌آموز را اینجا بنویس...",
                        elem_classes=["rtl"],
                    )
                    topic = gr.Textbox(label="موضوع", value="equations")
                    style = gr.Dropdown(
                        choices=["kind", "strict", "konkur", "deep"],
                        value="kind",
                        label="سبک معلم",
                    )
                    n_q = gr.Slider(1, 5, value=2, step=1, label="تعداد سوال تمرینی")
                    btn = gr.Button("تحلیل کن و سوال بساز", variant="primary")

                with gr.Column():
                    report_out = gr.Markdown(label="گزارش اشتباه")
                    questions_out = gr.Markdown(label="سوالات تمرینی")
                    memory_out = gr.Markdown(label="وضعیت حافظه")

            btn.click(
                run_mistake_loop,
                inputs=[student_id, problem, student_sol, topic, style, n_q],
                outputs=[report_out, questions_out, memory_out],
            )

        with gr.Tab("🎯 طراح سوال"):
            with gr.Row():
                topic2 = gr.Textbox(label="موضوع", value="sets")
                difficulty = gr.Dropdown(
                    choices=["easy", "medium", "hard", "konkur"],
                    value="medium",
                    label="سختی",
                )
                style2 = gr.Dropdown(
                    choices=["kind", "strict", "konkur", "deep"],
                    value="kind",
                    label="سبک",
                )
                count = gr.Slider(1, 5, value=2, step=1, label="تعداد")
            btn2 = gr.Button("سوال بساز", variant="primary")
            out2 = gr.Markdown()
            btn2.click(
                run_question_designer,
                inputs=[topic2, difficulty, style2, count],
                outputs=out2,
            )

        with gr.Tab("🧠 حافظه دانش‌آموز"):
            btn3 = gr.Button("نمایش حافظه")
            mem_view = gr.Markdown()
            btn3.click(show_memory, inputs=[student_id], outputs=mem_view)

        gr.Markdown(
            """
            ---
            **Engine priority:** `NOVA_LOCAL_MODEL` → cloud API → fake demo
            """
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
