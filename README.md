# SheetTruth

An AI auditor that finds spreadsheet formulas that compute the wrong thing, and proves each finding
by recalculation before it shows it.

## The problem

Most spreadsheet checkers catch broken formulas: `#REF!`, hard-coded numbers, a formula that breaks
the pattern of its row. They do not catch formulas that run fine and show a normal number but do the
wrong thing: `SUM` where the label says average, a total that stops two rows before the data ends,
a subtotal counted twice, a cost added instead of subtracted, a factor left out of a product.

## How it works

1. **Shape layer (rules).** One-cell ranges, omitted adjacent cells, hard-codes in formula columns,
   broken links, pattern breaks. Every formula, every function.
2. **Meaning layer (fine-tuned language model).** For each formula cell, a text window (labels,
   neighbours, referenced cells, peers, assumptions) goes to the model, which returns a verdict:
   `ok`, `error` (type, expected formula, reason) or `unsupported`.
3. **Verify layer (agent).** Applies the proposed fix in a copy, recalculates with LibreOffice,
   checks the sheet's own tie-outs, and records `passed_independent_check`, `failed_check` or
   `no_independent_check`.

Five error types in scope: `wrong_function`, `skipped_rows`, `double_count`, `wrong_sign`,
`missing_factor`. Logic errors inside lookup and branching functions are reported as `unsupported`.

## Repository layout

sheettruth/windows/ cellinfo.py (workbook model, refs, R1C1, header paths), builder.py (the context window)
sheettruth/mutators/ one file per error type; base.py is the contract and registry
sheettruth/data/ recalc.py (LibreOffice recalculation)
scripts/ convert_corpus.py, index_corpus.py, filter_leakage.py, build_dataset.py, audit_windows.py
tests/ must-fire / must-not-fire tests for every mutator
configs/default.yaml every knob in one place
docs/window_design.md the context window and the reason for each part


## Training data

Built by code, not labelled by hand or by a model. Real formulas from public spreadsheet corpora are
broken by one of five deterministic mutators, then the workbook is recalculated so cached values match
the broken formula. Half the examples are untouched cells labelled `ok`. The evaluation set is kept
out of training by file hash, file name and label overlap.

## Requirements

Python 3.10+, LibreOffice (conversion and recalculation). `pip install -r requirements.txt`.