# Multimodal Generation — Nova-Edu

Nova supports educational **image** and **video** generation.

## Structure

```
multimodal/
├── image_client.py          # Low-level image backends (fal, Replicate)
├── video_client.py          # Low-level video backends (fal)
├── educational_image.py     # Educational image helper
├── educational_video.py     # Educational video helper
├── service.py               # Unified service for agents
├── prompts/
│   ├── image_prompts.md
│   └── video_prompts.md
├── USAGE.md
└── integration.md
```

## Quick Usage

### Image

```python
from multimodal.service import get_multimodal_service

service = get_multimodal_service()
service.create_diagram(
    concept="Venn diagram of two sets A and B",
    output_path="outputs/venn.png",
    extra="textbook style, clear labels"
)
```

### Video

```python
service.create_animation(
    concept="intersection of two sets",
    output_path="outputs/venn.mp4",
    duration=5
)
```

## Setup

```bash
export FAL_KEY="your_key"          # recommended
# or
export REPLICATE_API_TOKEN="..."

pip install fal-client requests
# optional: pip install replicate
```

## Design Principles

- Pedagogical clarity > visual beauty
- Clean textbook-like style preferred for diagrams
- Short and focused videos
- Agents should use `MultimodalService`, not call backends directly
