# Nova-Edu API

REST API for integrating Nova into educational platforms.

## Run

```bash
pip install -r requirements.txt

# optional real model
export OPENROUTER_API_KEY="..."
export NOVA_MODEL="qwen/qwen2.5-14b-instruct"

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Docs UI: `http://localhost:8000/docs`

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Health check |
| POST | `/v1/mistake-analysis` | Analyze student solution + generate practice |
| POST | `/v1/generate-questions` | Create practice questions |
| POST | `/v1/tutor-chat` | Free-form tutoring reply |
| GET | `/v1/students/{id}/memory` | Read student memory |
| POST | `/v1/students/{id}/memory` | Update student memory |

## Example: Mistake Analysis

```bash
curl -X POST http://localhost:8000/v1/mistake-analysis \
  -H 'Content-Type: application/json' \
  -d '{
    "student_id": "s001",
    "problem": "معادله ۲x + ۵ = ۱۳ را حل کن",
    "student_solution": "۲x = ۸ → x = ۲",
    "topic": "equations",
    "n_questions": 2
  }'
```
