# Nova-Edu

> **The first specialized Iranian educational LLM + Visual + Multi-Agent Tutor**  
> Built to power learning platforms, not just chat.

**Status:** Core engine + Platform API are live 🔥

---

## What Nova is now

- Multi-agent educational brain (Mistake Finder, Question Designer, Memory, Visual)
- Real LLM connection (OpenRouter / Qwen / OpenAI-compatible)
- Gradio UI for direct use
- **REST API for integration into educational platforms**

---

## Run options

### 1) Local UI
```bash
pip install -r requirements.txt
python app/ui.py
```

### 2) Platform API
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Open docs: `http://localhost:8000/docs`

### 3) Terminal demo
```bash
python -m core.demo_loop
```

---

## Platform Integration

Any learning product can call Nova:

| Endpoint | Use case |
|----------|----------|
| `POST /v1/mistake-analysis` | Analyze student work + generate practice |
| `POST /v1/generate-questions` | Create targeted questions |
| `POST /v1/tutor-chat` | In-app tutor |
| `GET /v1/students/{id}/memory` | Personalization data |

Guides:
- `api/README.md`
- `integrations/README.md`
- `integrations/kharazmika_adapter.md`

---

## Core architecture

```
Educational Platform (Kharazmika / LMS / App)
                ↓ REST
           Nova API layer
                ↓
     Agents + Memory + LLM + Multimodal
```

Nova = intelligence engine  
Platform = student experience

---

## Environment

```bash
export OPENROUTER_API_KEY="..."
export NOVA_MODEL="qwen/qwen2.5-14b-instruct"
# optional image/video
export FAL_KEY="..."
```

---

**Built with fire by [Sina Jafari](https://github.com/sinajr2011-prog)**  
Started: November 2026
