# Nova-Edu

> **The first specialized Iranian educational LLM + Visual + Multi-Agent Tutor**  
> Text + Image + Video + Memory + Agents focused on Iranian curriculum, Konkur, Tizhooshan and Olympiad.

**Status:** Core system is live and detonated 🔥

---

## What just exploded

### 1. Real LLM Connection (`core/llm.py`)
- Works with **OpenRouter / OpenAI / Qwen / any OpenAI-compatible API**
- Automatic fallback to fake LLM for demos when no key is present

### 2. Full Gradio UI (`app/ui.py`)
Three powerful tabs:
- **Mistake Finder + Targeted Practice** (the magic loop)
- **Question Designer**
- **Student Memory Viewer**

### 3. Multi-Agent Brain (`core/agents.py`)
- Mistake Finder
- Question Designer
- Visual Explainer
- Teacher styles (kind / strict / konkur / deep)
- Full `mistake_to_practice()` orchestration

### 4. Long-term Memory (`core/memory_store.py`)
Tracks strengths, weaknesses, mistakes, mastery scores, and recommends focus topics.

---

## Quick Start

```bash
git clone https://github.com/sinajr2011-prog/nova-edu.git
cd nova-edu
pip install -r requirements.txt

# Optional: real model
export OPENROUTER_API_KEY="your_key"
export NOVA_MODEL="qwen/qwen2.5-14b-instruct"

# Run the UI
python app/ui.py
```

Then open `http://localhost:7860`

### Or run the terminal demo
```bash
python -m core.demo_loop
```

---

## The Magic Loop

```
Student wrong solution
        ↓
Mistake Finder (analyzes exact error)
        ↓
Student Memory (logs weakness + mastery)
        ↓
Question Designer (creates targeted practice)
```

All wired and working.

---

## Project Structure

```
nova-edu/
├── core/
│   ├── llm.py              # Real LLM client
│   ├── memory_store.py     # Long-term memory
│   ├── agents.py           # Multi-agent system
│   └── demo_loop.py
├── app/
│   └── ui.py               # Gradio interface 🔥
├── multimodal/             # Image + Video
├── agents/ modes/ features/
├── data/ training/ docs/
└── requirements.txt
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` or `OPENAI_API_KEY` | API key |
| `OPENAI_BASE_URL` | Default: `https://openrouter.ai/api/v1` |
| `NOVA_MODEL` | Default: `qwen/qwen2.5-14b-instruct` |
| `FAL_KEY` | For image/video generation |

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
