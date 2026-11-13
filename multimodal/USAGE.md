# Image Generation Usage

## 1. Setup

```bash
# Choose one provider
export FAL_KEY="your_fal_key"
# or
export REPLICATE_API_TOKEN="your_replicate_token"

pip install fal-client        # if using fal
# or
pip install replicate         # if using Replicate
```

## 2. Low-level client

```python
from multimodal.image_client import get_default_generator

gen = get_default_generator()

prompt = "Clean educational Venn diagram of two sets, textbook style, white background"
gen.generate_to_file(prompt, "outputs/venn.png")
```

## 3. Educational helper (recommended)

```python
from multimodal.educational_image import generate_educational_image

generate_educational_image(
    concept="Venn diagram showing intersection of set A and set B",
    output_path="outputs/sets_intersection.png",
    extra_instructions="labeled clearly, simple colors",
)
```

## Supported Backends (current)

- **fal.ai** → Flux (recommended for quality/speed)
- **Replicate** → Flux

You can easily add more backends by implementing the `ImageGenerator` interface.
