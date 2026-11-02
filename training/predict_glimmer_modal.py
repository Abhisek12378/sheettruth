"""Run the fine-tuned meaning model over a file of context windows on Modal.

The adapter trained by train_glimmer_modal.py is applied to the bf16 base weights and merged, so
generation runs at full speed. Every window gets the greedy reply plus the probability of each
verdict (ok, error, unsupported), read from the token distribution at the step where the model
writes the verdict word. Windows with enough error probability but a non-error reply get a second,
forced pass in which the model fills in the error type, the corrected formula and a reason, so a
lower flagging threshold still comes with an explanation. Windows that do not fit the sequence
budget are answered "unsupported" without calling the model.

Usage (from the project folder):
  python -m modal run training/predict_glimmer_modal.py --input data/test/windows.jsonl \\
      --out data/test/predictions.jsonl
  python -m modal run training/predict_glimmer_modal.py --input data/test/windows.jsonl \\
      --out data/test/predictions.jsonl --limit 40          # quick check on the first 40 windows

Input lines need "id" and "window"; "unsupported_reason" is honoured when present. Output lines
carry the id, the parsed verdict and the raw reply. Finished ids are skipped on a rerun.

Deployment (the audit command and the web app call this):
  python -m modal deploy training/predict_glimmer_modal.py
Environment knobs read at deploy time: SHEETTRUTH_GPU (default H100), SHEETTRUTH_MAX_CONTAINERS
(default 4, GPUs that may work on one audit in parallel), SHEETTRUTH_MIN_CONTAINERS (default 0;
set 1 to keep a GPU warm so the first call has no cold start).
"""
import json
import os
from pathlib import Path

import modal

from sheettruth.prompt import REASONING_STRENGTH, build_messages, parse_reply

APP_NAME = "sheettruth-predict"
BASE_MODEL = "unsloth/Muse-Glimmer-30B"      # bf16 copy of meta-models/Muse-Glimmer-30B
ADAPTER_DIR = "/models/glimmer-sheettruth-v2/adapter"
GPU = os.environ.get("SHEETTRUTH_GPU", "H100")
MAX_CONTAINERS = int(os.environ.get("SHEETTRUTH_MAX_CONTAINERS", "4"))   # GPUs working on one audit at most
MIN_CONTAINERS = int(os.environ.get("SHEETTRUTH_MIN_CONTAINERS", "0"))   # 1 keeps one GPU warm (no cold start)
SCALEDOWN_SECONDS = 120
DEFAULT_BATCH_SIZE = 16
MAX_PROMPT_TOKENS = 1900
MAX_NEW_TOKENS = 160
CANDIDATE_VERDICTS = ("ok", "error", "unsupported")
VERDICT_PREFIX = '{"verdict": "'
ERROR_PREFIX = '{"verdict": "error", "type": "'
EXPLAIN_ABOVE = 0.1        # forced error reply when P(error) is at least this and the greedy reply was not "error"
TOP_TOKENS_FOR_VERDICT = 50
MODEL_VOLUME = "sheettruth-models"
HF_CACHE_VOLUME = "sheettruth-hf-cache"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.8.0",
        "transformers==5.22.1",
        "peft>=0.21",
        "accelerate>=1.10",
        "sentencepiece",
        "protobuf",
        "huggingface_hub",
    )
    .env({"HF_XET_HIGH_PERFORMANCE": "1", "HF_HOME": "/hf-cache"})
    .add_local_python_source("sheettruth")
)

app = modal.App(APP_NAME, image=image)
model_vol = modal.Volume.from_name(MODEL_VOLUME)
hf_cache_vol = modal.Volume.from_name(HF_CACHE_VOLUME, create_if_missing=True)


def _too_long_reply(reason: str) -> dict:
    return {"verdict": "unsupported", "type": None, "expected": None, "reason": reason, "parsed": True,
            "raw": "", "p_ok": 0.0, "p_error": 0.0, "p_unsupported": 1.0}


@app.cls(
    gpu=GPU,
    timeout=60 * 60,
    scaledown_window=SCALEDOWN_SECONDS,
    max_containers=MAX_CONTAINERS,
    min_containers=MIN_CONTAINERS,
    volumes={"/models": model_vol, "/hf-cache": hf_cache_vol},
)
class Predictor:
    adapter_dir: str = modal.parameter(default=ADAPTER_DIR)

    @modal.enter()
    def load(self) -> None:
        import time

        import torch
        from peft import PeftModel
        from transformers import AutoModelForImageTextToText, AutoTokenizer

        t0 = time.time()
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        base = AutoModelForImageTextToText.from_pretrained(BASE_MODEL, device_map={"": 0}, dtype=torch.bfloat16)
        model = PeftModel.from_pretrained(base, self.adapter_dir)
        self.model = model.merge_and_unload().eval()
        self.eot_ids = [t for t in (self.tokenizer.convert_tokens_to_ids("<|eot|>"), self.tokenizer.eos_token_id)
                        if isinstance(t, int) and t >= 0]
        print(f"model ready in {time.time() - t0:.0f}s", flush=True)

    def _template_ids(self, messages: list[dict], add_generation_prompt: bool) -> list[int]:
        ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=add_generation_prompt, tokenize=True,
            reasoning_strength=REASONING_STRENGTH,
        )
        if hasattr(ids, "keys"):
            ids = ids["input_ids"]
        if ids and isinstance(ids[0], list):
            ids = ids[0]
        return [int(t) for t in ids]

    def _prompt_ids(self, window: str) -> list[int]:
        return self._template_ids(build_messages(window), add_generation_prompt=True)

    def _reply_prefix_ids(self, window: str, partial_reply: str) -> list[int]:
        """Prompt plus the start of an assistant reply, without the end-of-turn token."""
        messages = build_messages(window) + [{"role": "assistant", "content": partial_reply}]
        ids = self._template_ids(messages, add_generation_prompt=False)
        while ids and ids[-1] in self.eot_ids:
            ids.pop()
        return ids

    def _left_padded(self, seqs: list[list[int]]):
        import torch

        width = max(len(s) for s in seqs)
        pad = self.tokenizer.pad_token_id
        input_ids = torch.tensor([[pad] * (width - len(s)) + s for s in seqs], device="cuda")
        attention = torch.tensor([[0] * (width - len(s)) + [1] * len(s) for s in seqs], device="cuda")
        return input_ids, attention, width

    def _generate(self, prompts: list[list[int]], with_scores: bool = False):
        """Greedy continuation of each prompt: the new token ids per row, and per-step logits if asked."""
        import torch

        input_ids, attention, width = self._left_padded(prompts)
        with torch.no_grad():
            out = self.model.generate(
                input_ids=input_ids, attention_mask=attention, max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False, eos_token_id=self.eot_ids, pad_token_id=self.tokenizer.pad_token_id,
                output_scores=with_scores, return_dict_in_generate=True,
            )
        new_tokens = [seq[width:].tolist() for seq in out.sequences]
        return new_tokens, (out.scores if with_scores else None)

    def _verdict_step(self, tokens: list[int]) -> int:
        """Index of the generated token that starts the verdict word, or -1 when there is none."""
        for t in range(len(tokens)):
            text = self.tokenizer.decode(tokens[:t + 1], skip_special_tokens=True)
            at = text.find(VERDICT_PREFIX)
            if at >= 0 and len(text) > at + len(VERDICT_PREFIX):
                return t
        return -1

    def _verdict_probs(self, step_logits, row: int) -> dict:
        """Probability mass of each verdict word at one generation step, read from the top tokens."""
        import torch

        probs = torch.softmax(step_logits[row].float(), dim=-1)
        top_p, top_i = probs.topk(TOP_TOKENS_FOR_VERDICT)
        mass = {v: 0.0 for v in CANDIDATE_VERDICTS}
        for p, i in zip(top_p.tolist(), top_i.tolist()):
            word = self.tokenizer.decode([i]).strip().lstrip('"').lower()
            for v in CANDIDATE_VERDICTS:
                if word.startswith(v) or (len(word) >= 2 and v.startswith(word)):
                    mass[v] += p
                    break
        total = sum(mass.values()) or 1.0
        return {f"p_{v}": round(mass[v] / total, 5) for v in CANDIDATE_VERDICTS}

    def _score_rows(self, rows: list[dict]) -> dict[str, dict]:
        """Greedy reply plus verdict probabilities for each row, from one generation pass."""
        prompts = [self._prompt_ids(r["window"]) for r in rows]
        tokens, scores = self._generate(prompts, with_scores=True)
        out = {}
        for i, row in enumerate(rows):
            step = self._verdict_step(tokens[i])
            raw = self.tokenizer.decode(tokens[i], skip_special_tokens=True)
            probs = self._verdict_probs(scores[step], i) if step >= 0 else {"p_ok": 0.0, "p_error": 0.0, "p_unsupported": 1.0}
            out[row["id"]] = {**parse_reply(raw), "raw": raw, **probs}
        return out

    def _explain_errors(self, rows: list[dict], scored: dict[str, dict]) -> None:
        """Rows with enough error probability but a non-error greedy reply get a forced error reply,
        so a lower threshold still comes with a type, a fix and a reason."""
        chosen = [r for r in rows if scored[r["id"]]["verdict"] != "error" and scored[r["id"]]["p_error"] >= EXPLAIN_ABOVE]
        if not chosen:
            return
        prefixes = [self._reply_prefix_ids(r["window"], ERROR_PREFIX) for r in chosen]
        tokens, _ = self._generate(prefixes)
        for row, toks in zip(chosen, tokens):
            raw = ERROR_PREFIX + self.tokenizer.decode(toks, skip_special_tokens=True)
            detail = parse_reply(raw)
            scored[row["id"]].update(type=detail["type"], expected=detail["expected"], reason=detail["reason"], raw=raw)

    @modal.method()
    def predict(self, rows: list[dict]) -> list[dict]:
        """rows: [{"id", "window", "unsupported_reason"?}] -> one verdict per row, same order."""
        results: dict[str, dict] = {}
        scorable = []
        for row in rows:
            if row.get("unsupported_reason"):
                results[row["id"]] = _too_long_reply(row["unsupported_reason"])
            elif len(self._prompt_ids(row["window"])) > MAX_PROMPT_TOKENS:
                results[row["id"]] = _too_long_reply("window exceeds the sequence budget")
            else:
                scorable.append(row)
        if scorable:
            scored = self._score_rows(scorable)
            self._explain_errors(scorable, scored)
            results.update(scored)
        return [{"id": row["id"], **results[row["id"]]} for row in rows]


def _read_rows(path: str, limit: int, done: set[str]) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if row["id"] not in done:
                rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def _done_ids(path: str) -> set[str]:
    if not Path(path).exists():
        return set()
    with open(path) as f:
        return {json.loads(line)["id"] for line in f if line.strip()}


@app.local_entrypoint()
def main(input: str, out: str, batch_size: int = DEFAULT_BATCH_SIZE, limit: int = 0, adapter_dir: str = ADAPTER_DIR):
    done = _done_ids(out)
    rows = _read_rows(input, limit, done)
    print(f"{len(rows)} windows to score ({len(done)} already in {out})", flush=True)
    batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
    predictor = Predictor(adapter_dir=adapter_dir)
    scored = 0
    with open(out, "a") as f:
        for result in predictor.predict.map(batches, order_outputs=True):
            for r in result:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
            scored += len(result)
            if scored % (batch_size * 10) < batch_size:
                print(f"scored {scored}/{len(rows)}", flush=True)
    print(f"done: {scored} verdicts written to {out}")
