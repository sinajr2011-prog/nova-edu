#!/usr/bin/env python3
"""
Serve Nova locally from merged/finetuned weights.

Priority:
1) NOVA_LOCAL_MODEL (HF folder or adapter path)
2) fallback to API LLM / fake for wiring tests

Examples:
  export NOVA_LOCAL_MODEL=outputs/nova-edu-7b-merged
  python deployment/serve_local.py

  # Open UI with local engine
  python deployment/serve_local.py --ui

  # Open API with local engine
  python deployment/serve_local.py --api --port 8000
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def get_engine():
    from core.local_engine import get_best_engine
    return get_best_engine()


def run_cli(engine):
    print("Nova local CLI. Empty line to exit.")
    system = (
        "You are Nova, an expert Iranian educational tutor. "
        "Answer in clear Persian with step-by-step reasoning."
    )
    while True:
        try:
            user = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            break
        print("\nNova> " + engine(system, user))


def run_ui():
    # Reuse Gradio app; engine selection happens through env NOVA_LOCAL_MODEL
    from app.ui import build_ui
    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)


def run_api(port: int):
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true")
    parser.add_argument("--api", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model", default=os.getenv("NOVA_LOCAL_MODEL", ""))
    args = parser.parse_args()

    if args.model:
        os.environ["NOVA_LOCAL_MODEL"] = args.model
        print(f"Using local model: {args.model}")
    else:
        print("NOVA_LOCAL_MODEL not set — engine will fallback to API/fake.")

    if args.ui:
        run_ui()
    elif args.api:
        run_api(args.port)
    else:
        engine = get_engine()
        run_cli(engine)


if __name__ == "__main__":
    main()
