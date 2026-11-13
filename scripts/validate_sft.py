#!/usr/bin/env python3
"""
Validate SFT JSONL files for Nova-Edu.

Checks:
- Valid JSON lines
- Required message structure (system / user / assistant)
- Required metadata fields
- Basic content presence
"""

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_ROLES = {"system", "user", "assistant"}
REQUIRED_META = {"subject", "grade", "topic", "source", "difficulty", "type"}


def validate_example(obj: dict[str, Any], line_no: int) -> list[str]:
    errors = []

    if "messages" not in obj:
        errors.append(f"Line {line_no}: missing 'messages'")
        return errors

    messages = obj["messages"]
    if not isinstance(messages, list) or len(messages) < 3:
        errors.append(f"Line {line_no}: 'messages' must be a list with at least 3 items")
        return errors

    roles = [m.get("role") for m in messages]
    if roles[0] != "system":
        errors.append(f"Line {line_no}: first message must be system")
    if "user" not in roles or "assistant" not in roles:
        errors.append(f"Line {line_no}: must contain user and assistant roles")

    for i, m in enumerate(messages):
        if "content" not in m or not str(m["content"]).strip():
            errors.append(f"Line {line_no}: message {i} has empty content")

    meta = obj.get("metadata")
    if not isinstance(meta, dict):
        errors.append(f"Line {line_no}: missing or invalid 'metadata'")
    else:
        missing = REQUIRED_META - set(meta.keys())
        if missing:
            errors.append(f"Line {line_no}: metadata missing keys: {sorted(missing)}")

    return errors


def validate_file(path: str | Path) -> bool:
    path = Path(path)
    if not path.exists():
        print(f"File not found: {path}")
        return False

    all_errors = []
    count = 0

    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"Line {line_no}: invalid JSON ({e})")
                continue
            all_errors.extend(validate_example(obj, line_no))

    if all_errors:
        print(f"❌ {path} — {len(all_errors)} error(s) in {count} examples:")
        for e in all_errors[:20]:
            print("  ", e)
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")
        return False

    print(f"✅ {path} — {count} examples OK")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_sft.py <file.jsonl> [more files...]")
        sys.exit(1)

    ok = True
    for p in sys.argv[1:]:
        if not validate_file(p):
            ok = False

    sys.exit(0 if ok else 1)
