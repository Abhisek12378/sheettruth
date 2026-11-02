# Audit of 1_Southpoint Gas Model.xlsx

Formula cells scanned: 26 in 3 windows. Flagged at P(error) >= 0.5: 1 (verified 1, contradicted 0, unverifiable 0). Structure findings: 0.

## Model findings

| cell | run | P(error) | type | formula | proposed fix | verification | evidence |
|---|---|---|---|---|---|---|---|
| Sheet1!I34 | 1 cell | 0.98 | skipped_rows | `=SUM(I9:I33)` | `=SUM(I8:I33)` | passed | range_delta supports: the fix adds 1 real values (1 labelled) such as I8=3430 |

## Structure findings (no model involved)

| cell | kind | current | implied formula | detail |
|---|---|---|---|---|
