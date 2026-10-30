# Context window design and the reason for each part

One target cell per model call. Same builder for training and inference. Target ~1,000 tokens, cap 1,500.

| Section | What | Why |
|---|---|---|
| TARGET | address, formula (A1 and R1C1), recalculated value, number format, bold, comment | the cell under review; R1C1 makes neighbour comparison a string match |
| ROW_PATH / COL_PATH | nearest label plus section headers found by walking bold/indented cells upward | the label is the specification; nearest text alone picks wrong labels in indented statements |
| SHEET / UNIT_NOTE | sheet title, text near the top with $, %, thousands, MW... | unit and scale errors |
| GRID | 5x5 around the target with explicit letters and row numbers | position is hard to rebuild from a flat list |
| COL / ROW | 10 above, 3 below, 3 left, 3 right (5 right when the formula references its own row); blank runs collapsed | totals sit below data; skipped cells sit just past a range end |
| PEERS_* / PEER_DIFF | formula cells in the same row/column, how many share the target's R1C1, and the ones that differ | a dragged formula's siblings are the strongest evidence; a yes/no flag would become a shortcut |
| REF_RANGE / IN_RANGE / IN_RANGE_NOTE | per range: sign summary, head 3, tail 5, anomalies inside (minority cell kind, total words, bold, hidden, negatives), omitted count | this is where skipped rows, double counts and sign errors show |
| BEFORE_RANGE / AFTER_RANGE | 5 cells past each end with labels | omitted adjacent cells, blank-separator cases |
| REF_CELL | each single referenced cell with label, header, formula, value | missing factor, wrong reference |
| OVERLAP | leaf cells counted twice across additive terms, computed by code | double counting is arithmetic; code does it exactly |
| ASSUMPTION | up to 10 constants referenced with fully absolute refs ($B$2) by 2+ formulas | the missing multiplier is usually one of these |

Rules: windows for error examples are built from the corrupted, recalculated copy only; if the
window cannot fit the formula plus minimum evidence in the cap, the example is `unsupported: truncated_evidence`.
Audit: `reports/window_audit.md` renders the window for every real corpus error next to its fix.
