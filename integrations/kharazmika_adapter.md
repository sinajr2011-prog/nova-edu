# Kharazmika / Arena Adapter Notes

How a platform like **Kharazmika** or **Kharazmika Arena** can integrate Nova.

## Recommended Integration Points

### 1. After a student submits an answer in a duel / practice / homework
Call:
```http
POST /v1/mistake-analysis
```

Send:
- `student_id`
- question text
- student solution
- topic (e.g. sets, equations)

Receive:
- exact mistake analysis
- targeted practice questions
- updated focus topics

### 2. Practice generator for class / league
Call:
```http
POST /v1/generate-questions
```

Use returned questions inside Arena practice mode or weekly league prep.

### 3. Student profile / dashboard
Call:
```http
GET /v1/students/{id}/memory
```

Show strengths, weaknesses, and recommended focus topics in the student panel.

### 4. In-app tutor button
Call:
```http
POST /v1/tutor-chat
```

## Minimal Frontend Hook (example)

```js
async function analyzeMistake(studentId, problem, solution, topic) {
  const res = await fetch("https://nova-api.example.com/v1/mistake-analysis", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_id: studentId,
      problem,
      student_solution: solution,
      topic,
      n_questions: 2
    })
  });
  return res.json();
}
```

## Design Principle
Kharazmika remains the product UX.  
Nova becomes the intelligence layer behind practice, feedback, and personalization.
