# Data Guide — Nova-Edu

## Directory Layout (Recommended)

```
data/
├── raw/                  # Original PDFs or extracted text (not committed if large)
├── cleaned/              # Normalized text
├── chunks/               # Pedagogical chunks
├── sft/                  # Final instruction-response pairs (jsonl)
├── curriculum/           # Topic definitions
└── examples/             # Small high-quality samples (committed)
```

> Large raw files should stay local or in private storage. Only clean, high-quality SFT data and small samples belong in the public repo.

## Workflow for Real Data

1. **Extract**
   ```bash
   python scripts/extract_pdf_text.py textbook.pdf -o data/raw/grade9_math.txt
   ```

2. **Normalize**
   ```bash
   python -c "
   from scripts.normalize_persian import normalize_persian
   from pathlib import Path
   text = Path('data/raw/grade9_math.txt').read_text(encoding='utf-8')
   Path('data/cleaned/grade9_math.txt').write_text(normalize_persian(text), encoding='utf-8')
   "
   ```

3. **Chunk**
   ```bash
   python scripts/chunk_text.py data/cleaned/grade9_math.txt -o data/chunks/grade9_math
   ```

4. **Convert to SFT**
   Use `scripts/build_sft_example.py` or the upcoming conversion helpers to turn chunks into proper instruction-response pairs.

5. **Validate**
   ```bash
   python scripts/validate_sft.py data/sft/*.jsonl
   ```

## Quality Rules

- Prefer pedagogical value over quantity
- Every assistant response should teach, not just answer
- Keep metadata accurate (subject, grade, topic, difficulty, type)
- Use consistent Persian normalization
