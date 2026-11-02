"""LoRA fine-tune of Muse Glimmer 30B on Modal, from the chat JSONL produced by finalize_dataset.py.

The base model is loaded in 4-bit (QLoRA) so the whole run fits on one 80 GB GPU. Only the
language model gets LoRA weights; the vision tower is left untouched. Loss is computed on the
assistant reply only: the prompt tokens are masked, so the model learns to produce the verdict
JSON, not to reproduce the window.

Prompt handling (system text, reasoning strength, message normalisation) lives in
sheettruth.prompt and is shared with inference, so training and serving see the same prompt.

One-time setup on the machine that launches the job:
  pip install modal && python -m modal setup
  python -m modal volume create sheettruth-data
  python -m modal volume put sheettruth-data train.jsonl /train.jsonl
  python -m modal volume put sheettruth-data val.jsonl /val.jsonl

Runs:
  python -m modal run training/train_glimmer_modal.py --smoke     # 20 examples, 8 steps: checks loading
  python -m modal run training/train_glimmer_modal.py             # full run on /data/train.jsonl
  python -m modal run training/train_glimmer_modal.py --run-name glimmer-sheettruth-v2 \
      --train-file /data/train_v2.jsonl --val-file /data/val_v2.jsonl --epochs 1
  python -m modal volume ls sheettruth-models                     # the adapter lands here when done
"""
from __future__ import annotations

import modal

from sheettruth.prompt import REASONING_STRENGTH, normalise_messages

APP_NAME = "sheettruth-train"
BASE_MODEL = "unsloth/Muse-Glimmer-30B-unsloth-bnb-4bit"   # pre-quantised 4-bit copy of meta-models/Muse-Glimmer-30B
MAX_SEQ_LEN = 2048
LORA_TARGETS = r".*language_model.*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)"
DATA_VOLUME = "sheettruth-data"
MODEL_VOLUME = "sheettruth-models"
HF_CACHE_VOLUME = "sheettruth-hf-cache"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.8.0",
        "transformers==5.22.1",
        "peft>=0.21",
        "bitsandbytes>=0.47",
        "accelerate>=1.10",
        "datasets>=4.0",
        "sentencepiece",
        "protobuf",
        "huggingface_hub[hf_transfer]",
    )
    .env({"HF_XET_HIGH_PERFORMANCE": "1", "HF_HOME": "/hf-cache"})
    .add_local_python_source("sheettruth")
)

app = modal.App(APP_NAME, image=image)
data_vol = modal.Volume.from_name(DATA_VOLUME, create_if_missing=True)
model_vol = modal.Volume.from_name(MODEL_VOLUME, create_if_missing=True)
hf_cache_vol = modal.Volume.from_name(HF_CACHE_VOLUME, create_if_missing=True)


def _read_jsonl(path: str, limit: int = 0) -> list[dict]:
    import json
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
            if limit and len(rows) >= limit:
                break
    return rows


def _token_ids(tokenizer, messages: list[dict], add_generation_prompt: bool) -> list[int]:
    ids = tokenizer.apply_chat_template(
        messages, add_generation_prompt=add_generation_prompt, tokenize=True,
        reasoning_strength=REASONING_STRENGTH,
    )
    if hasattr(ids, "keys"):
        ids = ids["input_ids"]
    if ids and isinstance(ids[0], list):
        ids = ids[0]
    return [int(t) for t in ids]


def _common_prefix_len(a: list[int], b: list[int]) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def _encode_example(tokenizer, messages: list[dict], max_len: int) -> dict | None:
    """Tokenise one chat example and mask everything before the assistant reply."""
    messages = normalise_messages(messages)
    prompt_ids = _token_ids(tokenizer, messages[:-1], add_generation_prompt=True)
    full_ids = _token_ids(tokenizer, messages, add_generation_prompt=False)
    masked = _common_prefix_len(prompt_ids, full_ids)
    if len(full_ids) > max_len or masked >= len(full_ids):
        return None
    labels = [-100] * masked + full_ids[masked:]
    return {"input_ids": full_ids, "labels": labels, "attention_mask": [1] * len(full_ids)}


def _padded(seq: list[int], width: int, value: int) -> list[int]:
    return seq + [value] * (width - len(seq))


class PaddingCollator:
    """Right-pads a batch of encoded examples; padded label positions are ignored by the loss."""

    def __init__(self, pad_id: int):
        self.pad_id = pad_id

    def __call__(self, features: list[dict]) -> dict:
        import torch
        width = max(len(f["input_ids"]) for f in features)
        return {
            "input_ids": torch.tensor([_padded(f["input_ids"], width, self.pad_id) for f in features]),
            "attention_mask": torch.tensor([_padded(f["attention_mask"], width, 0) for f in features]),
            "labels": torch.tensor([_padded(f["labels"], width, -100) for f in features]),
        }


def _encode_rows(tokenizer, rows: list[dict]):
    """Encode every row that fits the sequence budget and report the token length spread."""
    from datasets import Dataset

    encoded = [_encode_example(tokenizer, r["messages"], MAX_SEQ_LEN) for r in rows]
    kept = [e for e in encoded if e is not None]
    lengths = sorted(len(e["input_ids"]) for e in kept)
    longest = lengths[-1] if lengths else 0
    median = lengths[len(lengths) // 2] if lengths else 0
    print(f"encoded {len(kept)}/{len(rows)} (rest exceeded {MAX_SEQ_LEN} tokens); "
          f"median {median} tokens, longest {longest}", flush=True)
    return Dataset.from_list(kept)


def _load_base_model():
    """The checkpoint is a vision-language model; the text-only path is what we train."""
    import torch
    from transformers import AutoModelForCausalLM, AutoModelForImageTextToText

    kwargs = {"device_map": {"": 0}, "dtype": torch.bfloat16}
    try:
        return AutoModelForImageTextToText.from_pretrained(BASE_MODEL, **kwargs)
    except ValueError:
        return AutoModelForCausalLM.from_pretrained(BASE_MODEL, **kwargs)


def _training_args(out_dir: str, smoke: bool, n_train: int, has_val: bool, epochs: float, lr: float,
                   batch_size: int, grad_accum: int, eval_every: int = 250):
    """Build TrainingArguments, keeping only the fields this transformers version accepts."""
    import dataclasses
    import math

    from transformers import TrainingArguments

    steps_per_epoch = math.ceil(n_train / (batch_size * grad_accum))
    total_steps = 8 if smoke else math.ceil(epochs * steps_per_epoch)
    wanted = {
        "output_dir": out_dir,
        "num_train_epochs": epochs,
        "max_steps": 8 if smoke else -1,
        "per_device_train_batch_size": batch_size,
        "per_device_eval_batch_size": batch_size,
        "gradient_accumulation_steps": grad_accum,
        "learning_rate": lr,
        "lr_scheduler_type": "cosine",
        "warmup_steps": max(1, int(0.05 * total_steps)),
        "bf16": True,
        "logging_steps": 5,
        "eval_strategy": "steps" if has_val else "no",
        "eval_steps": 4 if smoke else eval_every,
        "save_strategy": "steps",
        "save_steps": 200,
        "save_total_limit": 2,
        "gradient_checkpointing": True,
        "gradient_checkpointing_kwargs": {"use_reentrant": False},
        "report_to": [],
        "remove_unused_columns": False,
        "dataloader_num_workers": 0,
    }
    accepted = {f.name for f in dataclasses.fields(TrainingArguments)}
    dropped = sorted(k for k in wanted if k not in accepted)
    if dropped:
        print(f"TrainingArguments fields not in this transformers version, skipped: {dropped}", flush=True)
    return TrainingArguments(**{k: v for k, v in wanted.items() if k in accepted})


@app.function(
    gpu="H100",
    timeout=12 * 60 * 60,
    volumes={"/data": data_vol, "/models": model_vol, "/hf-cache": hf_cache_vol},
)
def train(smoke: bool = False, epochs: float = 2.0, lora_rank: int = 16, learning_rate: float = 1e-4,
          batch_size: int = 4, grad_accum: int = 4, run_name: str = "glimmer-sheettruth-v1",
          train_file: str = "/data/train.jsonl", val_file: str = "/data/val.jsonl", max_val_rows: int = 400,
          eval_every: int = 250) -> str:
    import json
    import time

    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoTokenizer, Trainer

    train_rows = _read_jsonl(train_file, 20 if smoke else 0)
    val_rows = _read_jsonl(val_file, 8 if smoke else max_val_rows)
    print(f"loaded {len(train_rows)} train, {len(val_rows)} val rows", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    train_ds, val_ds = _encode_rows(tokenizer, train_rows), _encode_rows(tokenizer, val_rows)
    sample = train_ds[0]
    print("sample reply tokens:", tokenizer.decode([t for t in sample["labels"] if t != -100]), flush=True)

    t0 = time.time()
    model = _load_base_model()
    print(f"model loaded in {time.time() - t0:.0f}s; type={type(model).__name__}", flush=True)
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    lora = LoraConfig(r=lora_rank, lora_alpha=2 * lora_rank, lora_dropout=0.05, bias="none",
                      task_type="CAUSAL_LM", target_modules=LORA_TARGETS)
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    out_dir = f"/models/{run_name}" + ("-smoke" if smoke else "")
    args = _training_args(out_dir, smoke, len(train_ds), len(val_ds) > 0, epochs, learning_rate,
                          batch_size, grad_accum, eval_every)
    trainer = Trainer(
        model=model, args=args, train_dataset=train_ds, eval_dataset=val_ds if len(val_ds) else None,
        data_collator=PaddingCollator(tokenizer.pad_token_id),
    )
    trainer.train()
    model.save_pretrained(out_dir + "/adapter")
    tokenizer.save_pretrained(out_dir + "/adapter")
    metrics = trainer.evaluate() if len(val_ds) else {}
    with open(out_dir + "/metrics.json", "w") as f:
        json.dump({"train_rows": len(train_ds), "val_rows": len(val_ds), "eval": metrics,
                   "epochs": epochs, "lora_rank": lora_rank, "learning_rate": learning_rate}, f, indent=1)
    model_vol.commit()
    print(f"saved adapter to {out_dir}/adapter; eval={metrics}", flush=True)
    return out_dir


@app.local_entrypoint()
def main(smoke: bool = False, epochs: float = 2.0, lora_rank: int = 16, learning_rate: float = 1e-4,
         run_name: str = "glimmer-sheettruth-v1", train_file: str = "/data/train.jsonl",
         val_file: str = "/data/val.jsonl"):
    out = train.remote(smoke=smoke, epochs=epochs, lora_rank=lora_rank, learning_rate=learning_rate,
                       run_name=run_name, train_file=train_file, val_file=val_file)
    print("done:", out)
