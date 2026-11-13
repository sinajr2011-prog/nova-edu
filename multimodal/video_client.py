#!/usr/bin/env python3
"""
Video generation client for Nova-Edu (initial version).

Currently focused on providers that expose a relatively simple API.
This is a starting point and will evolve.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import requests


class VideoGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9",
    ) -> str:
        """
        Generate a video and return a downloadable URL (or local path later).
        """
        ...

    def generate_to_file(
        self,
        prompt: str,
        output_path: str | Path,
        **kwargs,
    ) -> Path:
        url = self.generate(prompt, **kwargs)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            with path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return path


class FalVideoGenerator(VideoGenerator):
    """
    Example using fal.ai video models.

    Note: Model IDs change over time. Update self.model as needed.
    Requires FAL_KEY.
    """

    def __init__(self, model: str = "fal-ai/minimax-video"):
        self.model = model
        self.api_key = os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError("FAL_KEY environment variable is required")

    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9",
    ) -> str:
        import fal_client

        arguments = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
        }

        result = fal_client.subscribe(
            self.model,
            arguments=arguments,
            with_logs=False,
        )

        # Different models return slightly different structures
        if "video" in result:
            return result["video"]["url"]
        if "video_url" in result:
            return result["video_url"]
        if "videos" in result:
            return result["videos"][0]["url"]

        raise RuntimeError(f"Unexpected response structure: {result.keys()}")


def get_default_video_generator() -> VideoGenerator:
    if os.getenv("FAL_KEY"):
        return FalVideoGenerator()
    raise RuntimeError("No video generation API key found. Set FAL_KEY.")


if __name__ == "__main__":
    gen = get_default_video_generator()
    prompt = (
        "Short clean educational animation explaining the intersection of two sets, "
        "simple motion, textbook style, high clarity"
    )
    path = gen.generate_to_file(prompt, "outputs/sets_intersection.mp4", duration=5)
    print(f"Saved → {path}")
