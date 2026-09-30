---
name: llm-finetuning
description: "Fine-tunes open-source LLMs (Llama, Mistral, Qwen) using LoRA/QLoRA with HuggingFace and Unsloth. Use for domain-specific model adaptation."
category: ai
tags: [finetuning, lora, llama, mistral, unsloth, llm]
models: [opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# LLM Fine-Tuning

> Fine-tune open-source LLMs with LoRA/QLoRA for domain-specific tasks.

## Quick Start
```python
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer

# Load model with LoRA
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B",
    max_seq_length=2048,
    load_in_4bit=True,  # QLoRA
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
)

# Train
dataset = load_dataset("json", data_files="training_data.json")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
)
trainer.train()
```

## When to Use
- Domain-specific model adaptation
- Task-specific fine-tuning (chat, code, classification)
- Not for simple prompt engineering tasks

## Best Practices
- Start with a small LoRA adapter (r=16) on a capable base model.
- Use QLoRA (4-bit) to fit larger models on consumer GPUs.
- Prepare a clean, formatted dataset with validation split.
- Track loss and a held-out metric per epoch; stop early.
- Keep the base model frozen; adapt, not retrain.
- Version datasets, base model, and adapter together.

## Step-by-Step Instructions
1. Choose base model (Llama 3, Mistral, Qwen)
2. Prepare training dataset in chat format
3. Configure LoRA/QLoRA parameters
4. Train and save adapter
5. Evaluate on a held-out set
6. Merge or serve the adapter

## Dependencies
```bash
pip install unsloth transformers datasets trl accelerate
```

## Examples
Input: Training dataset of 1000 examples → Output: Fine-tuned LoRA adapter (50MB)

```python
# Inference with a fine-tuned adapter
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B",
    load_in_4bit=True,
)
model.load_adapter("lora-adapters/my-domain")

FastLanguageModel.for_inference(model)
output = model.generate(
    tokenizer(["Explain the domain rule:"], return_tensors="pt")["input_ids"],
    max_new_tokens=128,
)
print(tokenizer.batch_decode(output))
```

```python
# Dataset formatting for chat fine-tuning
def format_example(example):
    return {
        "text": "### User: {}\n### Assistant: {}".format(
            example["prompt"], example["completion"]
        )
    }

dataset = dataset.map(format_example)
```

## Resources
- [Unsloth](https://github.com/unslothai/unsloth)
- [HuggingFace SFT](https://huggingface.co/docs/trl/sft_trainer)
- [Examples](./examples/)

## Troubleshooting
- **Loss plateaus early** — the learning rate is too high. Cut it by 10×
  and lower batch size so validation loss keeps dropping.
- **Catastrophic forgetting** — mix 5–10% of the original dataset into
  each epoch, or freeze the first third of the network with LoRA.
- **OOM during training** — use gradient accumulation, `gradient_checkpointing`
  (training-time), and 4-bit QLoRA quantization for consumer GPUs.
- **Model regurgitates training data** — you overfit. Raise dropout,
  shrink epochs, and add a validation split with early stopping.

## Validation
1. Training loss decreases consistently
2. Model generates coherent responses post-training
3. Adapter merges successfully (if needed)
