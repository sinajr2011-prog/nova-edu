#!/usr/bin/env python3
"""
Unified multimodal service for Nova-Edu.

This is the main entry point that agents (especially Visual Explainer)
should use.
"""

from pathlib import Path
from typing import Optional

from educational_image import generate_educational_image
from educational_video import generate_educational_video


class MultimodalService:
    """
    High-level service for generating educational visuals.
    """

    def create_diagram(
        self,
        concept: str,
        output_path: str | Path,
        extra: str = "",
    ) -> Path:
        return generate_educational_image(
            concept=concept,
            output_path=output_path,
            extra_instructions=extra,
        )

    def create_animation(
        self,
        concept: str,
        output_path: str | Path,
        duration: int = 5,
        extra: str = "",
    ) -> Path:
        return generate_educational_video(
            concept=concept,
            output_path=output_path,
            duration=duration,
            extra_instructions=extra,
        )


def get_multimodal_service() -> MultimodalService:
    return MultimodalService()


if __name__ == "__main__":
    service = get_multimodal_service()

    # Example: image
    img_path = service.create_diagram(
        concept="Venn diagram of set A and set B",
        output_path="outputs/demo_venn.png",
        extra="clean textbook style",
    )
    print("Image:", img_path)

    # Example: video (requires working video backend)
    # vid_path = service.create_animation(
    #     concept="intersection of two sets",
    #     output_path="outputs/demo_venn.mp4",
    #     duration=5,
    # )
    # print("Video:", vid_path)
