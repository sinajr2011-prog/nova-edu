# Nova-Edu

> **The first specialized Iranian educational LLM + Visual Tutor**  
> Text + Image + Video generation focused on Iranian curriculum, Konkur, Tizhooshan and Olympiad.

**Status:** Phase 0 — Data + Multimodal Foundation (Active)

---

## Vision

Nova is designed to be a real educational companion:

- Deep understanding of Iranian secondary school curriculum
- Strong reasoning and explanation ability (fine-tuned LLM)
- Clear educational **image** generation (diagrams, illustrations)
- Short educational **video** generation (concept animations)
- Multi-agent system (Teacher, Solver, Visual Explainer, Grader, Advisor…)

---

## Current Capabilities

### Text
- Data pipeline (extract → normalize → chunk → SFT)
- Curriculum slices (Grade 9 Sets & Equations)
- Training template (Unsloth QLoRA)

### Multimodal
- Image generation client (fal / Replicate + Flux)
- Video generation client (initial fal support)
- Educational helpers + unified `MultimodalService`
- Visual Explainer agent definition

---

## Quick Start

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
pip install -r requirements.txt
```

For image generation:
```bash
export FAL_KEY="your_key"
pip install fal-client
```

---

## Project Structure

```
nova-edu/
├── data/
├── scripts/
├── training/
├── agents/
├── multimodal/          # Image + Video
├── evaluation/
└── docs/
```

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
