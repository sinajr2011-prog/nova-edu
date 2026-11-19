# Educational Platform Integrations — Nova-Edu

Nova is designed to plug into existing educational platforms, not replace them.

## Goal

Any Iranian (or international) learning platform should be able to call Nova as a **smart educational engine**:

- Analyze student mistakes
- Generate targeted practice
- Maintain long-term student memory
- Power tutoring chat
- (Later) Generate educational images/videos

## Integration Styles

### 1. REST API (Primary)
Best for web platforms, LMS, mobile apps, and custom dashboards.

Base idea:
```
POST /v1/mistake-analysis
POST /v1/generate-questions
POST /v1/tutor-chat
GET  /v1/students/{id}/memory
```

See `api/` for the implementation.

### 2. Platform Adapters
Thin wrappers for specific products:
- Kharazmika / Kharazmika Arena
- School LMS
- Custom teacher dashboards

### 3. Future Standards
- LTI 1.3 (Learning Tools Interoperability)
- xAPI / Caliper for learning analytics events

## Typical Flow (Platform → Nova)

1. Student submits a solution inside the host platform
2. Platform calls Nova `/v1/mistake-analysis`
3. Nova returns structured feedback + updates memory
4. Platform optionally requests targeted questions
5. Teacher/student sees results inside the original UI

Nova stays the brain. The platform stays the product surface.
