# Verify agent

The meaning model proposes; the verify agent tests the proposal against the workbook itself.
No check below reads the model's reason text or its probability.

| Check | What it does | Can support | Can contradict |
|---|---|---|---|
| recalculated_fix | writes the proposed fix into a copy and recalculates it with LibreOffice | no | yes, when the fix evaluates to an error value |
| value_change | compares the cell's value before and after the fix | no | no; an unchanged value is reported as "no impact with today's data", since the data may be zero or blank right now |
| peer_pattern | compares the R1C1 shape of the current formula and of the fix with the formulas around the cell | yes, when the fix matches the shared shape and the current formula does not | yes, when the current formula already matches the shared shape |
| sibling_sheets | compares the formula at the same address on the workbook's other sheets (a template repeated per unit or per period) | yes, when the fix matches the shared sibling formula and the current one does not | yes, when the current formula already matches the siblings |
| range_delta | looks at the cells a range or reference fix adds or drops | yes, for a range extension when added cells hold real values, or for a range cut when the dropped cell looks foreign (parameter label, other number format, far-off magnitude); for a moved reference or an added term, a real added cell is only a precondition | yes, when added cells are blank or text, or dropped cells look like ordinary block members |
| double_count | checks whether the current formula counts a cell twice or sums a subtotal of itself | yes | yes |
| value_plausibility | compares the distance of the old and new value from the median of peer values | yes, when the fix moves the value much closer | yes, when it moves it much farther |

Outcome per finding:

- `passed`: at least one check supports the finding
- `failed`: no check supports it and at least one contradicts it
- `no_independent_check`: nothing could be tested

Recalculation is a necessary condition only: it can sink a finding whose fix evaluates to an
error, but never carries one, because any fix that changes a value would otherwise pass.

Structure checks (`sheettruth/shape.py`) run before the model and need none of this: a typed
number inside a run of identical formulas, and a formula whose shape differs from the formulas on
both sides of it, each reported with the formula the run implies.
