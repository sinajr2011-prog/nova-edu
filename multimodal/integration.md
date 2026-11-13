# Multimodal Integration Plan

## Phase A — Prompt + Agent Layer (Current)

- Strong educational prompt templates
- Visual Explainer agent
- Clear interface between text agents and visual generation

## Phase B — Model Integration

Connect to external generation APIs / local models:

**Image (priority order for experiments):**
- Flux (Schnell / Dev)
- Stable Diffusion 3.5
- Other strong open models

**Video:**
- Kling
- Luma Ray
- Runway Gen-3
- HunyuanVideo / other open options

## Phase C — Educational Adaptation

- Collect high-quality educational visual examples
- Build evaluation criteria for pedagogical quality
- Optionally fine-tune or heavily prompt-engineer for Iranian textbook style

## Interface Sketch (Future Code)

```python
class VisualGenerator:
    def generate_image(self, prompt: str, style: str = "textbook") -> str:
        ...

    def generate_video(self, prompt: str, duration: int = 10) -> str:
        ...
```

The Visual Explainer agent will call this interface.
