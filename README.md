# SheetTruth

SheetTruth finds spreadsheet formulas that compute the wrong thing, such as a total that stops one
row short, a sum that reaches into the price row, a reference pointing one row off, or a cost
added instead of subtracted. Excel accepts all of these; they only show up when someone reads the
labels. SheetTruth reads the labels with a fine-tuned open-weights model, then checks every finding
against the workbook itself before it reports it.

Live: [sheettruth.com](https://sheettruth.com). Code, data recipe, training, evaluation and the
web app are all in this repository.

## How it works

```
workbook ──> structure checks ──> context windows ──> meaning model ──> verify agent ──> second opinion ──> report
             (rules, no model)    (one per run of      (fine-tuned,      (recalculation and   (reviewer model,
                                   identical formulas)  one cell a call)  tie-out checks)      optional)
```

1. **Structure checks** (`sheettruth/shape.py`). Rules that need no model: a number typed over a
   formula inside a filled-down run, and a formula whose shape differs from the formulas on both
   sides of it. Each comes with the formula the run implies.
2. **Context windows** (`sheettruth/windows/`). Cells that touch each other and share one R1C1
   formula form a run; one text window is built per run. The window holds the target formula,
   its row and column labels, the 5x5 grid around it, the cells above and below, the neighbours'
   formulas, the referenced ranges with their boundaries, and the labelled constants on the
   sheet. The same builder serves training and inference. Design notes: `docs/window_design.md`.
3. **Meaning model**. A LoRA fine-tune of Muse Glimmer 30B (open weights; adapter published at
   [Abhisek987/sheettruth-glimmer-30b-lora](https://huggingface.co/Abhisek987/sheettruth-glimmer-30b-lora))
   reads one window and answers
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
   cells a range fix adds or drops are inspected; double counting is checked in code; a sign
   finding on a lone negated reference is treated as a convention. Outcome per finding: `passed`
   (structural checks support the fix and none contradicts it), `failed` (the fix recalculates
   to an error, or the checks only contradict it) or `no_independent_check` (nothing could be
   tested, or the checks disagree). Details: `docs/verify_agent.md`.
5. **Second opinion** (`sheettruth/agent/reviewer.py`, optional). Findings not contradicted by
   code are sent to a hosted reviewer model (any OpenAI-compatible endpoint) with the same window
   and the claim; it answers `real_error`, `not_error` or `cannot_tell` with one sentence. Each
   finding then carries a final status: `confirmed`, `unverified`, `disputed` or `contradicted`.
   Workbook evidence outranks the reviewer: a finding a code check supports stays confirmed even
   if the reviewer disagrees. The reviewer is used when its endpoint is configured through the
   environment.
6. **Report**. Markdown for people, JSON for software, and a corrected copy of the workbook with
   the confirmed fixes written in, through the CLI or the web application.

## The application

`webapp/` holds the application: `backend/` (FastAPI) and `frontend/` (React + TypeScript). Upload a
workbook, pick a strictness (the P(error) cutoff), and follow the audit step by step while it
runs in a background worker. The result page groups findings by status, and each finding opens
to show the model's reason, every code check with its evidence, the reviewer's verdict, and the
exact context window the model saw. Downloads: the corrected workbook, the Markdown report and
the full JSON detail. Earlier audits stay in the side bar. Every push to `main` runs the tests,
builds the front end and deploys to the server (`.github/workflows/deploy.yml`); details in
`docs/deploy.md`.

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

| system | documented errors found (of 29 covered) | flagged windows outside the documented set | precision |
|---|---|---|---|
| first fine-tune (v1), greedy verdict | 6 | 71 | n/a |
| second fine-tune (v2), P(error) >= 0.5 | 18 | 222 | 0.11 |
| v2 + verify agent (contradicted findings dropped) | 18 | 76 | 0.23 |
| v2 + verify agent + reviewer second opinion | 17 | 31 | 0.38 |

Precision counts windows: windows covering a documented error over all flagged windows. Ten of
the 18 finds come with the exact documented correction. Lowering the cutoff to 0.3 finds 21
before verification at 395 flagged windows. Full reports: `reports/enron_eval_v2.md`,
`reports/enron_eval_v3_verified.md`, `reports/enron_eval_v3_reviewed.md`.

**Prompted baseline.** The same windows and the same prompt sent to a hosted general model
(Muse Spark Open, 578-window subset holding all error windows and 500 random ones): 18 found,
49 flagged outside the list, precision 0.29, against 18 found and 45 outside the list for the
fine-tuned 30B model on the same subset. The two agree on only 16 finds and 25 false alarms, so the
fine-tune matches a much larger general model, and a second model sees different things, which
is why the reviewer step exists.

**What the flagged cells outside the list are.** The corpus records the errors people noticed, not
every error in the files. An independent reviewer model was given 160 flagged cells with the
same context windows, plus 10 documented errors mixed in unmarked. It recognised 9 of the 10
documented errors, and judged 59 of the 160 to be real errors (6 distinct issues; 45 of the 59 are
one omission repeated on 45 template sheets of one workbook), 67 not errors, and 33 not decidable
from the window. Of the 31 windows the full pipeline still flags outside the list, 8 are among the
cells that review called real inconsistencies. The review pack and answers are in `reports/`.

Three of the 33 errors are not covered: one uses a custom add-in function, one uses ROUND, one is
a value cell. Per-error tables, categories and the full false-alarm lists are in `reports/`.

### Second benchmark: ExceLint corpus

To check that the Enron numbers are not specific to one corpus, the same pipeline was run on the
benchmark of the ExceLint study (Barowy, Berger and Zorn, OOPSLA 2018): 70 spreadsheets from the
EUSES corpus, audited by hand by the authors, with 700 annotated cells. 587 of them hold formulas;
grouped into runs they give 317 documented formula errors in 36 workbooks, 314 of them in scope.
The audit does not record the correct formula, so the "exact fix" count is not available here.
The set is prepared by `scripts/prepare_excelint.sh`; the leakage filter found no training
workbook (Enron or Sheetpedia index) that matches any of the 70 files. The P(error) cutoff was
fixed at 0.5 on the Enron set before this benchmark was run; nothing was tuned on it.

6,210 windows covering 19,180 formula cells.

| system | documented errors found (of 314 covered) | flagged windows outside the documented set | precision |
|---|---|---|---|
| v2, P(error) >= 0.5 | 100 | 185 | 0.35 |
| v2 + verify agent | (fill in) | (fill in) | (fill in) |
| v2 + verify agent + reviewer second opinion | (fill in) | (fill in) | (fill in) |

Lowering the cutoff to 0.3 finds 120 at 343 flagged windows outside the list. Full report:
`reports/excelint_eval_v2_full.md`.

### A third fine-tune that was not shipped

A third adapter (v3) was trained on 30,736 examples, twice the v2 set, built the same way from
the Enron corpus plus the Sheetpedia corpus (web and forum spreadsheets). On the Enron set it
looked like a clear win: 24 of 29 found at P(error) >= 0.5, and 22 found with 137 flagged windows
outside the list at 0.99, against 18 and 222 for v2. On the ExceLint set, at every cutoff, it was
behind v2: 77 found with 235 outside the list at 0.5 (v2: 100 and 185), 20 found at the 0.99
cutoff that worked on Enron. The gain was specific to Enron-style workbooks and did not transfer,
so v2 stays deployed. Reports: `reports/enron_eval_v3_model*.md`, `reports/excelint_eval_v3_model.md`.

## Running it

```
pip install -r requirements.txt
python -m pytest -q tests

# model server (Modal account required; the adapter path is a parameter)
python -m modal deploy training/predict_glimmer_modal.py

# optional reviewer (any OpenAI-compatible chat endpoint)
export SHEETTRUTH_REVIEWER_BASE_URL=https://...  SHEETTRUTH_REVIEWER_MODEL=...  SHEETTRUTH_REVIEWER_API_KEY=...

# one workbook
python scripts/audit_workbook.py path/to/book.xlsx --out reports/audit_book.md

# web application (build the front end first: cd webapp/frontend && npm ci && npm run build)
uvicorn webapp.backend.server:app --host 0.0.0.0 --port 8000
```

LibreOffice is needed on the machine that runs the verify agent (recalculation). Without it the
other checks still run and recalculation is reported as skipped. Without a reviewer endpoint the
second opinion step is skipped and findings are reported from the code checks alone.

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
webapp/                 backend/ (FastAPI service, job worker), frontend/ (React + TypeScript), deploy/ (server scripts)
.github/workflows/      test, build and deploy pipeline
tests/                  mutators, prompt, verify agent, structure checks, the audit graph, the web API
configs/default.yaml    every knob in one place
docs/                   window design, verify agent, deployment, model card
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
python scripts/evaluate_enron.py --predictions data/test/predictions.jsonl --windows data/test/windows.jsonl --verify --verify-cache data/test/verify_cache.jsonl
python scripts/evaluate_enron.py --predictions data/test/predictions.jsonl --windows data/test/windows.jsonl --verify --verify-cache data/test/verify_cache.jsonl --review --review-cache data/test/review_cache.jsonl
python scripts/baseline_api.py --input data/test/windows.jsonl --out data/test/predictions_baseline.jsonl --base-url <endpoint> --model <model> --ids data/test/subset_ids.txt
```

## Requirements

Python 3.11+, LibreOffice for conversion, recalculation and the verify agent.
