"""Ways to obtain verdicts for context windows.

The audit graph only needs an object with `score(records) -> dict`, mapping "sheet!addr" to the
model's verdict for that window. Two implementations: the deployed Modal predictor, and a file of
verdicts produced earlier (useful for tests and for re-running the verify step without the GPU).
"""
from __future__ import annotations

import json
from typing import Protocol

MODAL_APP = "sheettruth-predict"
MODAL_CLASS = "Predictor"
BATCH_SIZE = 16


def window_key(record: dict) -> str:
    return f"{record['sheet']}!{record['addr']}"


class ModelClient(Protocol):
    def score(self, records: list[dict]) -> dict[str, dict]: ...


class ModalPredictorClient:
    """Calls the Predictor class deployed with `python -m modal deploy training/predict_glimmer_modal.py`.
    Batches are sent with map, so Modal spreads them over as many containers as the deployment allows."""

    def __init__(self, adapter_dir: str):
        self.adapter_dir = adapter_dir

    def score(self, records: list[dict]) -> dict[str, dict]:
        import modal

        predictor = modal.Cls.from_name(MODAL_APP, MODAL_CLASS)(adapter_dir=self.adapter_dir)
        batches = [records[i:i + BATCH_SIZE] for i in range(0, len(records), BATCH_SIZE)]
        out: dict[str, dict] = {}
        for batch, verdicts in zip(batches, predictor.predict.map(batches, order_outputs=True)):
            for row, verdict in zip(batch, verdicts):
                out[window_key(row)] = verdict
            print(f"scored {len(out)}/{len(records)} windows", flush=True)
        return out


class SavedPredictionsClient:
    """Verdicts read from a JSONL file; ids like 'case:sheet!addr' are matched on their 'sheet!addr' part."""

    def __init__(self, path: str):
        self.verdicts: dict[str, dict] = {}
        with open(path) as f:
            for line in f:
                if line.strip():
                    verdict = json.loads(line)
                    self.verdicts[verdict["id"].split(":", 1)[-1]] = verdict

    def score(self, records: list[dict]) -> dict[str, dict]:
        return {window_key(r): self.verdicts[window_key(r)] for r in records if window_key(r) in self.verdicts}
