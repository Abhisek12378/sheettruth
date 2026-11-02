# SheetTruth

SheetTruth finds spreadsheet formulas that compute the wrong thing, such as a total that stops one
row short, a sum that reaches into the price row, a reference pointing one row off, or a cost
added instead of subtracted. Excel accepts all of these; they only show up when someone reads the
labels. SheetTruth reads the labels with a fine-tuned open-weights model, then checks every finding
against the workbook itself before it reports it.

## How it works

```
workbook ──> structure checks ──> context windows ──> meaning model ──> verify agent ──> report
             (rules, no model)    (one per run of      (fine-tuned,      (recalculation and
                                   identical formulas)  one cell a call)  tie-out checks)
```

1. **Structure checks** (`sheettruth/shape.py`). Rules that need no model: a number typed over a
   formula inside a filled-down run, and a formula whose shape differs from the formulas on both
   sides of it. Each comes with the formula the run implies.
2. **Context windows** (`sheettruth/windows/`). Cells that touch each other and share one R1C1
   formula form a run; one text window is built per run. The window holds the target formula,
   its row and column labels, the 5x5 grid around it, the cells above and below, the neighbours'
   formulas, the referenced ranges with their boundaries, and the labelled constants on the
   sheet. The same builder serves training and inference. Design notes: `docs/window_design.md`.
3. **Meaning model**. A LoRA fine-tune of Muse Glimmer 30B (open weights) reads one window and answers
   with a JSON verdict: `ok`, `error` (type, corrected formula, one-line reason) or
   `unsupported`. The probability of `error` is read from the generation step, so the flagging
   cutoff is a parameter. Nine error types: `wrong_function`, `skipped_rows`, `extra_rows`,
   `double_count`, `wrong_sign`, `wrong_reference`, `missing_term`, `wrong_operator`,
   `missing_factor`. Functions outside SUM, AVERAGE, COUNT, MIN, MAX and plain arithmetic are
   reported as `unsupported`.
4. **Verify agent** (`sheettruth/verify.py`, orchestrated by the LangGraph workflow in
   `sheettruth/agent/graph.py`). Every flagged cell is tested without trusting the model's reason:
   the proposed fix is written into a copy and recalculated with LibreOffice; the fix is compared
   with the formula pattern of neighbouring cells and of the same cell on sibling sheets; the
   cells a range fix adds or drops are inspected; double counting is checked in code; the fixed
   value is compared with peer values. Outcome per finding: `passed`, `failed` or
   `no_independent_check`. Details: `docs/verify_agent.md`.
5. **Report**. Markdown for people, JSON for software, through the CLI or the web page.

## Training data

Built by code from real workbooks in the public Enron corpus (15,871 files indexed, 14,901 kept
after removing anything that overlaps the test set by hash, name or label content).

- **Errors**: a real formula broken by one of nine deterministic mutators, each modelled on an
  error shape seen in audited workbooks. Half the time the broken formula is written into the
  whole run of identical formulas, so the model cannot rely on "the odd one out". The copy is
  recalculated so cached values match the broken formula, and the window is built from that
  copy only.
- **Hard negatives**: untouched cells where a mutator could have fired, labelled `ok`. They make
  up half the `ok` examples, so labels alone cannot separate the classes.
- **Reviewer-model proposals**: a reviewer model proposes a realistic mistake for a correct cell;
  code applies it, recalculates, rebuilds the window and keeps it only if the evidence cells the
  reviewer named are still in the window.
- A sample of labels was audited by an independent model (`scripts/audit_labels.py`).

Final set: 16,107 training and 1,830 validation examples, split by workbook.

## Evaluation

Held-out test: the Enron Errors Corpus (Schmitz and Jannach, 2016), 30 real workbooks with 33
formula errors that Enron staff found and fixed themselves. Never used in training. The audit
scans every in-scope formula cell of the 30 files (16,286 cells in 2,817 windows); an error counts
as found when a window covering one of its cells is flagged. Flagged windows outside the
documented set are reported as false alarms, although the corpus lists only the errors people
noticed, not every error in the files.

| system | documented errors found (of 29 covered) | flagged windows outside the documented set |
|---|---|---|
| first fine-tune (v1), greedy verdict | 6 | 71 |
| second fine-tune (v2), P(error) >= 0.5 | 18 | 222 |
| v2 + verify agent, contradicted findings dropped | 17 | 159 |
| v2 + verify agent, only supported findings kept | 15 | 142 |

Ten of the 18 finds come with the exact documented correction. Lowering the cutoff to 0.3 finds
21 before verification at 395 flagged windows.

Three of the 33 errors are not covered: one uses a custom add-in function, one uses ROUND, one is
a value cell. Per-error tables, categories and the full false-alarm lists are in `reports/`.

## Running it

```
pip install -r requirements.txt
python -m pytest -q tests

# model server (Modal account required; the adapter path is a parameter)
python -m modal deploy training/predict_glimmer_modal.py

# one workbook
python scripts/audit_workbook.py path/to/book.xlsx --out reports/audit_book.md

# web page
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

LibreOffice is needed on the machine that runs the verify agent (recalculation). Without it the
other checks still run and recalculation is reported as skipped.

## Repository layout

```
sheettruth/windows/     cellinfo.py (workbook model, refs, R1C1, header paths), builder.py (the window), runs.py (runs)
sheettruth/mutators/    one file per error type; base.py is the contract and registry
sheettruth/verify.py    the verify agent's checks
sheettruth/shape.py     structure checks without a model
sheettruth/agent/       LangGraph audit workflow, model clients, report rendering
sheettruth/prompt.py    the prompt and reply parser shared by training and inference
sheettruth/data/        recalc.py (LibreOffice recalculation)
training/               LoRA fine-tune (QLoRA, one GPU) and batched inference, both on Modal
scripts/                corpus conversion and indexing, leakage filter, dataset build, label audit,
                        reviewer-model proposals, test windows, evaluation, hosted baselines, the audit CLI
app/                    FastAPI front end
tests/                  mutators, prompt, verify agent, structure checks, the audit graph
configs/default.yaml    every knob in one place
docs/                   window design, verify agent
reports/                evaluation reports
```

## Data pipeline

```
python scripts/convert_corpus.py data/raw/enron data/xlsx/enron --workers 4
python scripts/index_corpus.py   data/xlsx/enron data/index/enron --workers 4
python scripts/filter_leakage.py data/index/enron/workbooks.jsonl data/test/enron_errors_xlsx data/index/enron/allowed.json
bash scripts/build_v2.sh
python -m modal run training/train_glimmer_modal.py --run-name <run> --train-file /data/train.jsonl --val-file /data/val.jsonl --epochs 1
python scripts/build_test_windows.py --out data/test/windows.jsonl
python -m modal run training/predict_glimmer_modal.py --input data/test/windows.jsonl --out data/test/predictions.jsonl --adapter-dir /models/<run>/adapter
python scripts/evaluate_enron.py --predictions data/test/predictions.jsonl --verify
```

## Requirements

Python 3.11+, LibreOffice for conversion, recalculation and the verify agent.
