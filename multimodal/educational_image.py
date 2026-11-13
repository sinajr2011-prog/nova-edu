#!/usr/bin/env python3
"""
High-level educational image generation for Nova.

This layer sits on top of the raw image client and applies
educational prompt templates.
"""

from pathlib import Path
from typing import Optional

from image_client import ImageGenerator, get_default_generator


DEFAULT_NEGATIVE = (
    "blurry, low quality, watermark, text errors, cluttered, "
    "decorative, cinematic lighting, photorealistic, 3d render"
)


def build_diagram_prompt(
    concept: str,
    extra: str = "",
    style: str = "textbook",
) -> str:
    base = (
        f"Clean educational diagram of {concept}, "
        f"{style} style, white background, clear labels, "
        f"simple and precise, high clarity, no decorative clutter"
    )
    if extra:
        base += ", " + extra
    return base


def generate_educational_image(
    concept: str,
    output_path: str | Path,
    extra_instructions: str = "",
    width: int = 1024,
    height: int = 1024,
    generator: Optional[ImageGenerator] = None,
) -> Path:
    """
    Generate a clean educational image for a given concept.
    """
    if generator is None:
        generator = get_default_generator()

    prompt = build_diagram_prompt(concept, extra=extra_instructions)

    return generator.generate_to_file(
        prompt=prompt,
        output_path=output_path,
        negative_prompt=DEFAULT_NEGATIVE,
        width=width,
        height=height,
    )


if __name__ == "__main__":
    path = generate_educational_image(
        concept="Venn diagram of two sets A and B with intersection highlighted",
        output_path="outputs/sets_venn.png",
        extra_instructions="labeled in Persian if possible",
    )
    print(f"Image saved to: {path}")
