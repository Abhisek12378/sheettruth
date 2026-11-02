# Model card: SheetTruth meaning model

**Base model:** Muse Glimmer 30B (open weights, Apache 2.0).
**Adaptation:** LoRA (rank 16, alpha 32, dropout 0.05) on the attention and MLP projections of the
language model only; the vision tower is untouched. Trained with QLoRA on a single GPU, one epoch
over 16,107 examples, cosine schedule, learning rate 1e-4, effective batch 16, sequence cap 2,048
tokens. Loss on the assistant reply only.

**Task:** read one context window describing a formula cell and answer with a JSON verdict:
`{"verdict": ok | error | unsupported, "type": <one of nine error types or null>, "expected": <corrected formula or null>, "reason": <one sentence>}`.
The prompt is in `sheettruth/prompt.py`; the chat template's own reasoning-strength line is used,
set to `low`, and the model answers without a thinking block.

**Training data:** built by code from the public Enron spreadsheet corpus (no test-set workbooks by
hash, name or label content). Errors are injected by nine deterministic mutators or proposed by a
reviewer model and then applied and checked by code; half the `ok` examples are hard negatives
(cells a mutator could have broken, left as written). Every corrupted copy is recalculated so the
cached values match the broken formula.

**Validation (same distribution, split by workbook):** loss 0.079 on 1,830 examples.

**Held-out test (real errors):** the Enron Errors Corpus, 30 workbooks, 33 formula errors found by
Enron staff. See the evaluation section of the README and `reports/`.

**Intended use:** one component of the SheetTruth audit; its findings are meant to pass through the
verify agent before anyone acts on them. It covers SUM, AVERAGE, COUNT, MIN, MAX and plain
arithmetic; anything else is answered `unsupported`.

**Known limits:** it over-flags subtraction patterns where the sign convention is a matter of
intent (margin shown as cost minus revenue), and it cannot see cross-sheet or external links.
Rare error types (missing factor, wrong operator) have few training examples.
