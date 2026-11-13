# Training

## Planned Stack (Phase 1)

- **Base models**: Qwen2.5-7B-Instruct / Qwen2.5-14B-Instruct (primary candidates)
- **Method**: QLoRA (4-bit) via Unsloth for speed and memory efficiency
- **Framework options**: Unsloth, Axolotl, or plain Hugging Face + PEFT

## Current Status

No training runs yet.  
We are still in Phase 0 (building the dataset).

## Next Steps

1. Finalize first clean dataset slice (start with Grade 9 Math – Sets & related topics)
2. Create a minimal Unsloth training script
3. Run a small experimental fine-tune and evaluate

---

When ready, training configs and scripts will live in this folder.
