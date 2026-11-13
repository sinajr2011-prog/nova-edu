#!/usr/bin/env python3
"""
Image generation client for Nova-Edu.

Provides a clean interface so the rest of the system doesn't care
which backend (fal, Replicate, Stability, etc.) is being used.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import requests


class ImageGenerator(ABC):
    """Abstract image generator."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
    ) -> bytes:
        """Generate an image and return raw bytes (usually PNG/JPEG)."""
        ...

    def generate_to_file(
        self,
        prompt: str,
        output_path: str | Path,
        **kwargs,
    ) -> Path:
        data = self.generate(prompt, **kwargs)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path


class FalFluxGenerator(ImageGenerator):
    """
    Flux image generation via fal.ai

    Docs: https://fal.ai/models/fal-ai/flux/dev
    Requires: FAL_KEY environment variable
    """

    def __init__(self, model: str = "fal-ai/flux/dev"):
        self.model = model
        self.api_key = os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError("FAL_KEY environment variable is required")

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
    ) -> bytes:
        import fal_client  # pip install fal-client

        arguments = {
            "prompt": prompt,
            "image_size": {
                "width": width,
                "height": height,
            },
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed is not None:
            arguments["seed"] = seed

        result = fal_client.subscribe(
            self.model,
            arguments=arguments,
            with_logs=False,
        )

        image_url = result["images"][0]["url"]
        response = requests.get(image_url, timeout=60)
        response.raise_for_status()
        return response.content


class ReplicateFluxGenerator(ImageGenerator):
    """
    Flux via Replicate

    Requires: REPLICATE_API_TOKEN
    """

    def __init__(self, model: str = "black-forest-labs/flux-dev"):
        self.model = model
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN environment variable is required")

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
    ) -> bytes:
        import replicate  # pip install replicate

        input_data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 28,
            "guidance": 3.5,
        }
        if negative_prompt:
            input_data["negative_prompt"] = negative_prompt
        if seed is not None:
            input_data["seed"] = seed

        output = replicate.run(self.model, input=input_data)

        # output is usually a list of URLs or file-like objects
        if isinstance(output, list):
            url = output[0]
        else:
            url = output

        if hasattr(url, "read"):
            return url.read()

        response = requests.get(str(url), timeout=60)
        response.raise_for_status()
        return response.content


def get_default_generator() -> ImageGenerator:
    """
    Factory: tries fal first, then Replicate.
    """
    if os.getenv("FAL_KEY"):
        return FalFluxGenerator()
    if os.getenv("REPLICATE_API_TOKEN"):
        return ReplicateFluxGenerator()
    raise RuntimeError(
        "No image generation API key found. "
        "Set FAL_KEY or REPLICATE_API_TOKEN."
    )


if __name__ == "__main__":
    # Simple manual test
    gen = get_default_generator()

    prompt = (
        "Clean educational diagram of two overlapping sets A and B, "
        "Venn diagram, labeled in Persian, textbook style, white background, "
        "high clarity, simple and precise"
    )

    out = gen.generate_to_file(prompt, "outputs/test_venn.png")
    print(f"Saved → {out}")
