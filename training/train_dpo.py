#!/usr/bin/env python3
"""
Nova DPO trainer (preference optimization for teaching quality).

Expected JSONL:
{"prompt": "...", "chosen": "...", "rejected": "..."}

Example:
  python training/train_dpo.py \
    --model outputs/nova-edu-7b-sft \
    --data data/sft/build/dpo_pairs.jsonl \
    --out outputs/nova-edu-7b-dpo
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, help="SFT model or adapter path")
    p.add_argument("--data", required=True)
    p.add_argument("--out", default="outputs/nova-edu-dpo")
    p.add_argument("--max-seq-length", type=int, default=4096)
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--lr", type=float, default=5e-6)
    p.add_argument("--beta", type=float, default=0.1)
    return p.parse_args()


def main():
    args = parse_args()
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(data_path)

    import torch
    from datasets import load_dataset
    from transformers import TrainingArguments
    from trl import DPOTrainer
    from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    dataset = load_dataset("json", data_files=str(data_path), split="train")

    keep = {"prompt", "chosen", "rejected"}
    dataset = dataset.remove_columns([c for c in dataset.column_names if c not in keep])

    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=TrainingArguments(
            output_dir=args.out,
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=args.grad_accum,
            num_train_epochs=args.epochs,
            learning_rate=args.lr,
            logging_steps=5,
            save_strategy="epoch",
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            optim="adamw_8bit",
            lr_scheduler_type="cosine",
            warmup_ratio=0.05,
            report_to="none",
            remove_unused_columns=False,
        ),
        beta=args.beta,
        train_dataset=dataset,
        tokenizer=tokenizer,
        max_length=args.max_seq_length,
        max_prompt_length=min(1024, args.max_seq_length // 2),
    )

    trainer.train()
    model.save_pretrained(args.out)
    tokenizer.save_pretrained(args.out)
    print(f"DPO model saved → {args.out}")


if __name__ == "__main__":
    main()
