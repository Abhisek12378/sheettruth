---
base_model: unsloth/Muse-Glimmer-30B
library_name: peft
license: apache-2.0
language:
  - en
tags:
  - lora
  - spreadsheet
  - formula-auditing
  - excel
pipeline_tag: text-generation
---

# SheetTruth meaning model (LoRA adapter for Muse Glimmer 30B)

A LoRA adapter that turns Muse Glimmer 30B into a spreadsheet formula auditor. It reads a plain-text
description of one formula cell and its surroundings (labels, neighbouring formulas, the referenced
ranges and their boundaries) and answers whether the formula computes the wrong thing, with the
error type, a corrected formula and a one-sentence reason.

It is one component of [SheetTruth](https://github.com/Abhisek12378/sheettruth): the model proposes,
a verify agent tests every finding against the workbook itself, and an optional reviewer model
gives a second opinion.

## Task

Input: one context window, built by `sheettruth/windows/` from the workbook. Output: one JSON object.

```
{"verdict": "ok" | "error" | "unsupported", "type": <error type or null>, "expected": <corrected formula or null>, "reason": <one sentence>}
```

Nine error types: `wrong_function`, `skipped_rows`, `extra_rows`, `double_count`, `wrong_sign`,
`wrong_reference`, `missing_term`, `wrong_operator`, `missing_factor`. Formulas built on functions
outside SUM, AVERAGE, COUNT, MIN, MAX and plain arithmetic are answered `unsupported`.

The system prompt and the reply parser are in `sheettruth/prompt.py` of the repository. The chat
template's own reasoning-strength line is used, set to `low`; the model answers without a thinking
block. The probability of the `error` verdict is read from the generation step that writes the verdict word, so the
flagging cutoff is a parameter at inference time.

## Training

- Base: Muse Glimmer 30B (open weights). LoRA rank 16, alpha 32, dropout 0.05 on the attention and
  MLP projections of the language model; the vision tower is untouched.
- QLoRA on a single H100, one epoch over 16,107 examples, cosine schedule, learning rate 1e-4,
  effective batch 16, sequence cap 2,048 tokens, loss on the assistant reply only.
- Validation loss 0.079 on 1,830 examples (same distribution, split by workbook).

Training data was built by code from the public Enron spreadsheet corpus, with every workbook that
overlaps the test set removed by hash, name or label content. Errors were injected by nine
deterministic mutators or proposed by a reviewer model and then applied and checked by code. Half
the `ok` examples are hard negatives: cells a mutator could have broken, left as written. Every
corrupted copy was recalculated so cached values match the broken formula.

## Evaluation

Held-out test: the Enron Errors Corpus (Schmitz and Jannach, 2016), 30 real workbooks with 33
formula errors that Enron staff found and fixed themselves, never used in training. 16,286
formula cells in 2,817 windows; 29 errors are covered by the model's scope.

| system | documented errors found (of 29) | flagged windows outside the documented set | precision |
|---|---|---|---|
| this adapter, P(error) >= 0.5 | 18 | 222 | 0.11 |
| + verify agent (code checks on the workbook) | 18 | 76 | 0.23 |
| + reviewer second opinion | 17 | 31 | 0.38 |

Ten of the 18 finds come with the exact documented correction. The corpus lists only the errors
people noticed, so some flagged cells outside the list are real inconsistencies; an independent
review of 160 of them judged 59 to be real errors. Full reports are in the repository under
`reports/`.

## How to use

```python
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoTokenizer

base = "unsloth/Muse-Glimmer-30B"
tokenizer = AutoTokenizer.from_pretrained(base)
model = AutoModelForImageTextToText.from_pretrained(base, dtype="bfloat16", device_map="auto")
model = PeftModel.from_pretrained(model, "Abhisek987/sheettruth-glimmer-30b-lora")
```

Build the prompt with `sheettruth.prompt.build_messages(window)` from the repository, apply the chat
template with `reasoning_strength="low"`, and parse the reply with `sheettruth.prompt.parse_reply`.
`training/predict_glimmer_modal.py` in the repository is the batched inference server used in
production.

## Intended use and limits

Meant to run inside the SheetTruth audit, where the verify agent tests each finding before anyone
acts on it. It over-flags subtraction patterns where the sign convention is a matter of intent,
it cannot see cross-sheet or external links, and the rarer error types (missing factor, wrong
operator) have few training examples.
