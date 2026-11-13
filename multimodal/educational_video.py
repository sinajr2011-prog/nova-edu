#!/usr/bin/env python3
"""
High-level educational video generation helper for Nova.
"""

from pathlib import Path
from typing import Optional

from video_client import VideoGenerator, get_default_video_generator


def build_concept_video_prompt(concept: str, extra: str = "") -> str:
    base = (
        f"Short clean educational animation explaining {concept}, "
        f"simple motion, textbook style, high clarity, smooth camera, "
        f"minimal distractions, focused on learning"
    )
    if extra:
        base += ", " + extra
    return base


def generate_educational_video(
    concept: str,
    output_path: str | Path,
    duration: int = 5,
    extra_instructions: str = "",
    generator: Optional[VideoGenerator] = None,
) -> Path:
    if generator is None:
        generator = get_default_video_generator()

    prompt = build_concept_video_prompt(concept, extra=extra_instructions)

    return generator.generate_to_file(
        prompt=prompt,
        output_path=output_path,
        duration=duration,
    )


if __name__ == "__main__":
    path = generate_educational_video(
        concept="the intersection of two sets using a Venn diagram",
        output_path="outputs/sets_intersection_anim.mp4",
        duration=6,
        extra_instructions="clear and simple for grade 9 students",
    )
    print(f"Video saved to: {path}")
