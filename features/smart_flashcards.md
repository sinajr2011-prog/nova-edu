# Smart Flashcards

## Goal
Automatically generate high-quality flashcards from any chapter or topic.

## Card Types
1. **Concept Card**: Term / Definition
2. **Process Card**: Steps of a method
3. **Trap Card**: Common mistake → Correct version
4. **Visual Card**: Diagram + short explanation (uses multimodal)

## Generation Flow
1. Take a topic or textbook chunk
2. Extract key concepts and relationships
3. Generate front/back of cards
4. Optionally generate a supporting image
5. Store in spaced-repetition friendly format

## Output Format (example)
```json
{
  "front": "اشتراک دو مجموعه چیست؟",
  "back": "مجموعه عضوهای مشترک بین دو مجموعه",
  "type": "concept",
  "topic": "sets",
  "difficulty": "easy"
}
```
