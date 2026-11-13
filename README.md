# Nova-Edu

> **The first specialized Iranian educational LLM + Visual Tutor**  
> Text + Image + Video generation focused on Iranian curriculum, Konkur, Tizhooshan and Olympiad.

**Status:** Phase 0 — Data + Multimodal Foundation (Active)

---

## Vision

Nova is designed to be a real educational companion, not just a chatbot:

- Deep understanding of Iranian secondary school curriculum
- Strong reasoning and explanation ability (fine-tuned LLM)
- Clear educational **image** generation (diagrams, illustrations, step-by-step visuals)
- Short educational **video** generation (concept animations & solution walkthroughs)
- Multi-agent system (Teacher, Solver, Visual Explainer, Grader, Advisor…)

---

## Current Focus

### Text Side
- Data pipeline ready
- Moving toward real textbook ingestion and first fine-tune

### Multimodal Side (Just started)
- Image & Video prompt systems
- Visual Explainer agent
- Integration layer coming next

---

## Project Structure

```
nova-edu/
├── data/                 # Educational text data
├── scripts/              # Text processing tools
├── training/             # LLM fine-tuning
├── agents/               # Text + Visual agents
├── multimodal/           # Image & Video generation
│   ├── prompts/
│   └── README.md
├── evaluation/
└── docs/
```

---

## Quick Start

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
pip install -r requirements.txt
```

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
