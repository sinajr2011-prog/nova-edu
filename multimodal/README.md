# Multimodal Generation — Nova-Edu

Nova is not only a text tutor.  
It also needs strong **image** and **video** generation capabilities to explain concepts visually.

## Goals

- Generate clear educational diagrams (sets, equations, geometry, physics, chemistry…)
- Create step-by-step visual explanations
- Produce short educational animations / concept videos
- Keep everything pedagogically useful and consistent with Iranian curriculum style

## Planned Capabilities

### 1. Image Generation
- Concept diagrams
- Geometric figures
- Step-by-step solution illustrations
- Illustrated examples and analogies

### 2. Video Generation
- Short concept animations (10–30 seconds)
- Step-by-step solution walkthroughs
- Process visualizations (e.g. chemical reactions, physical motions)

## Architecture Direction

We will **not** train foundation image/video models from scratch in the beginning.

Instead:

1. Design strong educational prompt systems and agents
2. Integrate with the best available open/closed models (Flux, SD3.5, Kling, Luma, Runway, Hunyuan, etc.)
3. Later: collect educational visual data and fine-tune / adapt models for Persian educational style and curriculum accuracy

## Current Status

- Structure created
- Prompt templates and agent roles being defined
- Integration layer coming next
