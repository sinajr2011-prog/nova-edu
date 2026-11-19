# Nova as a Fully Independent Neural Model

## Vision

Nova must not stay an API wrapper forever.

The end goal is a **specialized Iranian educational foundation model**:
- Deep mastery of secondary curriculum, Konkur, Tizhooshan, Olympiad
- Strong pedagogical reasoning
- Native Persian educational style
- Local/offline inference capability
- Agentic behavior on top of the model itself

## Independence Levels

### Level 0 — API Dependent (current demo)
Uses external models through OpenRouter/OpenAI-compatible APIs.

### Level 1 — Specialized Fine-Tune (near-term)
Fine-tune a strong open model (Qwen2.5 / Qwen3 / Llama-class) on high-quality Iranian educational data.
Result: Nova-Edu-7B / 14B adapters + merged weights.

### Level 2 — Domain-Specialist Model
Larger curated dataset + preference optimization (DPO/ORPO) for teaching quality, not just correctness.
Result: Nova becomes clearly better than general models on Iranian exam pedagogy.

### Level 3 — Independent Stack
- Own fine-tuned weights
- Local inference (vLLM / llama.cpp / GGUF)
- Own evaluation suite
- Optional continued pretraining on textbook corpus
- Multimodal educational adapters later

## Strategic Base Model Choices

Priority order for training:
1. **Qwen2.5-14B-Instruct** (best balance of quality and Persian strength)
2. Qwen2.5-7B-Instruct (faster iteration / consumer GPU)
3. Qwen3 family when stable and well-supported
4. Strong Llama/Gemma alternatives only if data advantage is huge

## What “Best” Means for Nova

Not generic chatbot elo.

Nova wins if it is best at:
1. Correct curriculum-aligned explanations
2. Finding student mistakes precisely
3. Generating useful practice
4. Teaching step-by-step with clarity
5. Handling Konkur-style reasoning
6. Working well in Persian educational language

## Training Doctrine

- Data quality > data quantity
- Pedagogy labels matter (concept / worked example / mistake repair / exam item)
- Always keep a hard hold-out set from real exam styles
- Evaluate teaching quality, not only final-answer accuracy
- Prefer reproducible open training recipes
