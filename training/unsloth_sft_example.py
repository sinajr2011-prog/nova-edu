#!/usr/bin/env python3
"""
Example Unsloth QLoRA fine-tuning script for Nova-Edu.

This is a template. Do not run until you have a real dataset.
Adjust model name, paths, and hyperparameters as needed.
"""

# pip install unsloth transformers datasets trl peft accelerate bitsandbytes

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# -----------------------------
# Config
# -----------------------------
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"   # change later if needed
MAX_SEQ_LENGTH = 4096
LOAD_IN_4BIT = True

OUTPUT_DIR = "outputs/nova-edu-qwen2.5-7b-lora"
DATASET_PATH = "data/examples/sample_sft.jsonl"   # replace with real dataset

# -----------------------------
# Load model
# -----------------------------
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=LOAD_IN_4BIT,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

# -----------------------------
# Dataset
# -----------------------------
def formatting_prompts_func(examples):
    texts = []
    for messages in examples["messages"]:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
        texts.append(text)
    return {"text": texts}


dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
dataset = dataset.map(formatting_prompts_func, batched=True)

# -----------------------------
# Trainer
# -----------------------------
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=20,
        num_train_epochs=1,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=5,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=42,
        output_dir=OUTPUT_DIR,
        report_to="none",
    ),
)

# trainer.train()          # uncomment when ready
# model.save_pretrained(OUTPUT_DIR)
# tokenizer.save_pretrained(OUTPUT_DIR)

print("Template ready. Uncomment trainer.train() when you have real data.")
