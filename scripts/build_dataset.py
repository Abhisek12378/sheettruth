"""Build the training set from an indexed, leakage-filtered corpus.

Each sampled formula cell becomes one example:
  ok           the cell untouched, window built from the original workbook
  error        the cell broken by one mutator; the workbook copy is recalculated and the window
               is built from that copy only, so cached values match the broken formula
  unsupported  the cell's function is outside the supported set; window from the original workbook

Modes:
  mixed           ok, error and unsupported examples in the configured shares (default)
  hard_negatives  only ok examples, taken from cells where a mutator could have fired: the
                  formula looks like an error candidate but is left as written
  errors_only     only error examples, useful to top up rare types with --only-mutators

Safeguards:
  * workbooks are split into train/val before any sampling, so no workbook is in both
  * if recalculation fails, cached values of all formula cells are hidden for that example
  * mutators are tried rarest-first, and each type stops once it reaches its target
  * --exclude-workbooks keeps a top-up run away from workbooks an earlier run already used

Usage:
  python scripts/build_dataset.py --source enron --index data/index/enron \\
      --xlsx data/xlsx/enron --out data/dataset/enron --workers 4
  python scripts/build_dataset.py --source enron_hn --index data/index/enron --xlsx data/xlsx/enron \\
      --out data/dataset/enron_hn --mode hard_negatives --exclude-workbooks data/dataset/enron/examples.jsonl
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import resource
import sys
import tempfile
import time
import warnings
from multiprocessing import Pool, TimeoutError as PoolTimeout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import openpyxl
import yaml
from openpyxl.formula.translate import Translator

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.mutators.base import Mutation, Mutator, registry  # noqa: E402
from sheettruth.windows.builder import WindowConfig, build_window  # noqa: E402
from sheettruth.windows.cellinfo import CellContext, Workbook, build_context, to_r1c1  # noqa: E402

_RECALC: Optional[Recalculator] = None
UNSUPPORTED_KEEP_PROBABILITY = 0.5
PROGRESS_EVERY = 50
RESULT_WAIT_SECONDS = 600       # give up on the pool when no workbook finishes for this long
WORKER_MEMORY_BYTES = 4_000 * 1024 * 1024
TASKS_PER_WORKER_BEFORE_RECYCLE = 20


def _worker_init(timeout: int) -> None:
    """Each worker gets its own LibreOffice profile and a hard memory cap, so one oversized workbook
    raises MemoryError inside the worker instead of taking the whole pool down."""
    global _RECALC
    warnings.filterwarnings("ignore")
    try:
        resource.setrlimit(resource.RLIMIT_AS, (WORKER_MEMORY_BYTES, WORKER_MEMORY_BYTES))
    except (ValueError, OSError):
        pass
    _RECALC = Recalculator(timeout=timeout)


def func_family(funcs: list[str]) -> str:
    return funcs[0] if funcs else "ARITH"


def window_config(cfg: dict) -> WindowConfig:
    allowed = WindowConfig.__dataclass_fields__
    return WindowConfig(**{k: v for k, v in cfg["window"].items() if k in allowed})


# ----------------------------------------------------------------------------------------------
# worker side: one workbook, several cells
# ----------------------------------------------------------------------------------------------

@dataclass
class WorkbookTask:
    path: str
    rel: str
    cells: list[dict]
    roles: list[str]
    priority: list[str]
    cfg: dict
    split: str
    source: str
    seed: int


def _base_record(task: WorkbookTask, cell: dict, ctx: CellContext) -> dict:
    return {
        "source": task.source, "split": task.split, "workbook": task.rel,
        "sheet": cell["sheet"], "addr": cell["addr"], "func_family": func_family(cell["funcs"]),
        "original_formula": ctx.cell.formula,
    }


def _window_fields(window) -> dict:
    return {"window": window.text, "tokens": window.tokens, "truncated": window.truncated}


def _unsupported_example(base: dict, ctx: CellContext, wcfg: WindowConfig) -> dict:
    window = build_window(ctx, wcfg)
    return {**base, "verdict": "unsupported", "type": None, "expected": None,
            "reason": "function outside the supported set", "unsupported_reason": "out_of_scope_function",
            "recalc": "n/a", **_window_fields(window)}


def _ok_example(base: dict, ctx: CellContext, wcfg: WindowConfig) -> Optional[dict]:
    window = build_window(ctx, wcfg)
    if window.unsupported_reason:
        return None
    return {**base, "verdict": "ok", "type": None, "expected": None,
            "reason": "formula matches its labels and neighbours", "recalc": "n/a", **_window_fields(window)}


def _first_applicable_mutation(ctx: CellContext, priority: list[str], rng: random.Random) -> tuple[Optional[Mutator], Optional[Mutation]]:
    reg = registry()
    for name in priority:
        mutator = reg[name]
        try:
            if mutator.applies(ctx):
                mutation = mutator.mutate(ctx, rng)
                if mutation:
                    return mutator, mutation
        except Exception:
            continue
    return None, None


def _run_cells(ctx: CellContext) -> list[str]:
    """Addresses of the cells next to the target, in a straight line, that hold the same R1C1
    formula: the filled-down (or filled-across) run the target belongs to. The target is excluded."""
    sheet, cell = ctx.sheet, ctx.cell
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = cell.row + dr, cell.col + dc
        while r >= 1 and c >= 1:
            other = sheet.get(r, c)
            if not other.is_formula or to_r1c1(other.formula, r, c) != ctx.r1c1:
                break
            out.append(other.addr)
            r, c = r + dr, c + dc
    return out


def _write_corrupted_copy(src_path: str, sheet_name: str, addr: str, formula: str, dst_path: str,
                          also: list[str] = ()) -> None:
    """Write the broken formula into the target cell and, for a block-wide error, its translated
    form into every other cell of the run."""
    wb = openpyxl.load_workbook(src_path)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.worksheets[0]
    ws[addr] = formula
    for other in also:
        ws[other] = Translator(formula, origin=addr).translate_formula(other)
    wb.save(dst_path)


def _recalculate(path: str) -> tuple[bool, str]:
    if _RECALC is None:
        return False, "no_recalc"
    return _RECALC.recalc(path)


def _hard_negative_example(task: WorkbookTask, base: dict, ctx: CellContext, wcfg: WindowConfig, rng: random.Random) -> Optional[dict]:
    """An untouched cell that a mutator could have broken, labelled ok. Mutators are tried in random
    order here, so the candidate types are spread rather than dominated by the rarest one."""
    order = list(task.priority)
    rng.shuffle(order)
    mutator, mutation = _first_applicable_mutation(ctx, order, rng)
    if not mutation:
        return None
    record = _ok_example(base, ctx, wcfg)
    if record:
        record.update(hard_negative=True, candidate_type=mutator.name)
    return record


def _error_example(task: WorkbookTask, base: dict, cell: dict, ctx: CellContext, wcfg: WindowConfig, rng: random.Random) -> Optional[dict]:
    mutator, mutation = _first_applicable_mutation(ctx, task.priority, rng)
    if not mutation:
        return None
    run = _run_cells(ctx)
    block_wide = bool(run) and rng.random() < task.cfg["mutators"].get("block_wide_probability", 0.0)
    with tempfile.TemporaryDirectory(prefix="st-mut-") as tmp:
        copy = os.path.join(tmp, "copy.xlsx")
        try:
            _write_corrupted_copy(task.path, ctx.sheet.name, cell["addr"], mutation.broken_formula, copy,
                                  run if block_wide else ())
        except Exception as ex:
            return {**base, "_error": f"write_failed: {ex}"}
        ok, status = _recalculate(copy)
        if not ok and task.cfg["recalc"]["on_failure"] == "drop_example":
            return None
        try:
            corrupted = Workbook(copy, strip_formula_values=not ok)
        except Exception as ex:
            return {**base, "_error": f"reload_failed: {ex}"}
        cctx = build_context(corrupted, ctx.sheet.name, cell["addr"], task.cfg["window"]["max_header_levels"])
        if cctx is None:
            return None
        window = build_window(cctx, wcfg)
    if window.unsupported_reason:
        return None
    return {**base, "verdict": "error", "type": mutation.error_type, "expected": mutation.expected_formula,
            "broken_formula": mutation.broken_formula, "reason": mutation.reason_template,
            "touched_cells": mutation.touched_cells, "mutator_version": mutator.version,
            "block_wide": block_wide, "run_size": len(run) + 1, "recalc": status, **_window_fields(window)}


def process_workbook(task: WorkbookTask) -> list[dict]:
    """Runs in a worker process. Never raises: failures come back as records with an _error key."""
    try:
        return _process_workbook(task)
    except MemoryError:
        return [{"_error": "memory_limit", "workbook": task.rel}]
    except Exception as ex:
        return [{"_error": f"worker_failed: {str(ex)[:120]}", "workbook": task.rel}]


def _process_workbook(task: WorkbookTask) -> list[dict]:
    wcfg = window_config(task.cfg)
    rng = random.Random(task.seed)
    try:
        wb = Workbook(task.path)
    except Exception as ex:
        return [{"_error": f"load_failed: {ex}", "workbook": task.rel}]

    out: list[dict] = []
    for cell, role in zip(task.cells, task.roles):
        ctx = build_context(wb, cell["sheet"], cell["addr"], task.cfg["window"]["max_header_levels"])
        if ctx is None:
            continue
        base = _base_record(task, cell, ctx)
        if role == "unsupported":
            record = _unsupported_example(base, ctx, wcfg)
        elif role == "ok":
            record = _ok_example(base, ctx, wcfg)
        elif role == "hard_negative":
            record = _hard_negative_example(task, base, ctx, wcfg, rng)
        else:
            record = _error_example(task, base, cell, ctx, wcfg, rng)
        if record:
            out.append(record)
    return out


# ----------------------------------------------------------------------------------------------
# driver side: sampling, planning, writing
# ----------------------------------------------------------------------------------------------

def load_sampled_cells(index_dir: Path) -> dict[str, list[dict]]:
    """Allowed workbooks mapped to one representative cell per formula block."""
    allowed = set(json.load(open(index_dir / "allowed.json"))["allowed"])
    by_workbook: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    with open(index_dir / "cells.jsonl") as f:
        for line in f:
            cell = json.loads(line)
            if cell["workbook"] in allowed:
                by_workbook[cell["workbook"]].setdefault(cell["block_id"], cell)
    return {w: list(blocks.values()) for w, blocks in by_workbook.items()}


SINGLE_ROLE_MODES = {"hard_negatives": "hard_negative", "errors_only": "mutate"}


def assign_roles(cells: list[dict], clean_share: float, rng: random.Random, mode: str = "mixed") -> list[str]:
    """ok, unsupported, mutate, hard_negative or skip for each cell. Mutator choice happens in the worker."""
    roles = []
    for cell in cells:
        if mode in SINGLE_ROLE_MODES:
            roles.append(SINGLE_ROLE_MODES[mode] if cell["in_scope"] else "skip")
        elif not cell["in_scope"]:
            roles.append("unsupported" if rng.random() < UNSUPPORTED_KEEP_PROBABILITY else "skip")
        elif rng.random() < clean_share:
            roles.append("ok")
        else:
            roles.append("mutate")
    return roles


def mutator_priority(cfg: dict, only: str) -> list[str]:
    priority = [n for n in cfg["mutators"]["enabled"] if n in registry()]
    if only:
        wanted = set(only.split(","))
        priority = [n for n in priority if n in wanted]
    return priority


def used_workbooks(examples_paths: str) -> set[str]:
    """Workbooks that appear in one or more earlier examples.jsonl files (comma-separated paths)."""
    used: set[str] = set()
    for path in filter(None, examples_paths.split(",")):
        with open(path) as f:
            used.update(json.loads(line)["workbook"] for line in f if line.strip())
    return used


def plan_tasks(sampled: dict[str, list[dict]], cfg: dict, args, rng: random.Random) -> list[WorkbookTask]:
    sampling = cfg["sampling"]
    priority = mutator_priority(cfg, args.only_mutators)
    excluded = used_workbooks(args.exclude_workbooks)
    workbooks = sorted(w for w in sampled if w not in excluded)
    rng.shuffle(workbooks)
    if args.max_workbooks:
        workbooks = workbooks[: args.max_workbooks]
    n_val = int(len(workbooks) * args.val_share)

    tasks = []
    for i, name in enumerate(workbooks):
        cells = list(sampled[name])
        rng.shuffle(cells)
        cells = cells[: sampling["max_cells_per_workbook"]]
        roles = assign_roles(cells, sampling["clean_share"], rng, args.mode)
        kept = [(c, r) for c, r in zip(cells, roles) if r != "skip"]
        if not kept:
            continue
        tasks.append(WorkbookTask(
            path=str(Path(args.xlsx) / name), rel=name,
            cells=[c for c, _ in kept], roles=[r for _, r in kept], priority=priority,
            cfg=cfg, split="val" if i < n_val else "train", source=args.source, seed=rng.randrange(1 << 30),
        ))
    print(f"{len(workbooks)} workbooks ({n_val} val), mutators={priority}, per_type_target={cfg['mutators']['per_type_target']}", flush=True)
    return tasks


@dataclass
class Tally:
    counts: collections.Counter = field(default_factory=collections.Counter)
    by_family: dict = field(default_factory=lambda: collections.defaultdict(collections.Counter))
    errors: list[dict] = field(default_factory=list)

    def accept(self, record: dict, per_type_target: int) -> bool:
        if "_error" in record:
            self.errors.append(record)
            return False
        key = record["type"] or ("hard_negative" if record.get("hard_negative") else record["verdict"])
        if record["verdict"] == "error" and self.counts[key] >= per_type_target:
            return False
        self.counts[key] += 1
        self.by_family[record["func_family"]][record["verdict"]] += 1
        return True


def run_tasks(tasks: list[WorkbookTask], cfg: dict, args, out_dir: Path) -> Tally:
    tally = Tally()
    per_type_target = cfg["mutators"]["per_type_target"]
    started = time.time()
    n_written = 0
    with open(out_dir / "examples.jsonl", "w") as f, Pool(
        args.workers, initializer=_worker_init, initargs=(cfg["recalc"]["timeout_s"],),
        maxtasksperchild=TASKS_PER_WORKER_BEFORE_RECYCLE,
    ) as pool:
        results = pool.imap_unordered(process_workbook, tasks, chunksize=1)
        for i in range(1, len(tasks) + 1):
            try:
                records = results.next(timeout=RESULT_WAIT_SECONDS)
            except StopIteration:
                break
            except PoolTimeout:
                print(f"no workbook finished in {RESULT_WAIT_SECONDS}s; stopping with {i - 1} done", flush=True)
                pool.terminate()
                break
            for record in records:
                if not tally.accept(record, per_type_target):
                    continue
                record["id"] = f"{args.source}-{n_written:06d}"
                n_written += 1
                f.write(json.dumps(record) + "\n")
            if i % PROGRESS_EVERY == 0:
                f.flush()
                print(f"{i}/{len(tasks)} workbooks, {n_written} examples, {dict(tally.counts)}, {time.time() - started:.0f}s", flush=True)
    tally.counts["_total"] = n_written
    tally.counts["_seconds"] = round(time.time() - started)
    return tally


def write_report(tally: Tally, n_tasks: int, out_dir: Path) -> None:
    report = {
        "counts": dict(tally.counts),
        "per_function_family": {k: dict(v) for k, v in tally.by_family.items()},
        "workbooks": n_tasks, "errors": len(tally.errors), "error_samples": tally.errors[:20],
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k != "error_samples"}, indent=1))


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--source", required=True, help="short name of the corpus, used in example ids")
    ap.add_argument("--index", required=True, help="folder with cells.jsonl, workbooks.jsonl, allowed.json")
    ap.add_argument("--xlsx", required=True, help="root of the converted .xlsx files for this corpus")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=3, help="keep workers x 4 GB under the machine's RAM")
    ap.add_argument("--max-workbooks", type=int, default=0)
    ap.add_argument("--val-share", type=float, default=0.1)
    ap.add_argument("--mode", choices=["mixed", "hard_negatives", "errors_only"], default="mixed")
    ap.add_argument("--only-mutators", default="", help="comma-separated mutator names to restrict to")
    ap.add_argument("--exclude-workbooks", default="", help="examples.jsonl of earlier runs (comma-separated); their workbooks are skipped")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    cfg = yaml.safe_load(open(args.config))
    rng = random.Random(cfg["sampling"]["seed"])
    sampled = load_sampled_cells(Path(args.index))
    tasks = plan_tasks(sampled, cfg, args, rng)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    tally = run_tasks(tasks, cfg, args, out_dir)
    write_report(tally, len(tasks), out_dir)


if __name__ == "__main__":
    main()
