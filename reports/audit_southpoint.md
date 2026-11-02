# Audit of 1_Southpoint Gas Model.xlsx

Formula cells scanned: 26 in 3 windows. Flagged at P(error) >= 0.5: 2 (verified 1, contradicted 1, unverifiable 0). Structure findings: 0.

## Model findings

| cell | run | P(error) | type | formula | proposed fix | verification | evidence |
|---|---|---|---|---|---|---|---|
| Sheet1!I34 | 1 cell | 0.81 | skipped_rows | `=SUM(I9:I33)` | `=SUM(I8:I33)` | passed | range_delta supports: the fix adds 1 real values (1 labelled) such as I8=3430 |
| Sheet1!G33 | 1 cell | 0.61 | skipped_rows | `=SUM(G8:G32)` | `=SUM(G8:G31)` | failed | value_change contradicts: the fix does not change the cell's value |

## Structure findings (no model involved)

| cell | kind | current | implied formula | detail |
|---|---|---|---|---|
