# Window audit on the Enron Errors Corpus

For each formula error: the corpus fix, then the window the model would see. 
Question for the reader: can you see the fix from the window alone?


Rendered 31, skipped 5, over budget 0.


## Error 1: 2_HPLN0601.xls / Sheet1!F28:G28

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(F25:F25)`
- corpus fix: `=SUM(F25:F26)`

tokens~279 truncated=False unsupported=None

```
TARGET|Sheet1!F28|=SUM(F25:F25)|value=8|fmt=0.000|bold=1
TARGET_R1C1|=SUM(R[-3]C:R[-3]C)
ROW_PATH|Enron North America Spot/3959 > Firm Summary > DELIVERY POINT > Fax # 713-646-2391
COL_PATH|PRIOR
SHEET|Sheet1|title=HPLN0601.XLS|sheets_in_workbook=3
GRID|row\col|D|E|F|G|H
GRID|26|(blank)|"Enron"|0|13|(blank)
GRID|27|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*28|(blank)|(blank)|=SUM(F25:F25) -> 8|=SUM(G25:G25) -> 0|(blank)
GRID|29|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|30|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!F18:F22|||(5 blank cells)
COL|Sheet1!F23|Firm Summary|=SUM(F18:F21)|0
COL|Sheet1!F24|||(blank)
COL|Sheet1!F25|Enron||8
COL|Sheet1!F31|||(blank)
ROW|Sheet1!C28|Koch TOG #3||"Enron North America Spot/3959"
PEERS_ROW|formula_cells=1|same_r1c1=1
PEERS_COL|formula_cells=2|same_r1c1=0
PEER_DIFF|Sheet1!F23|=SUM(R[-5]C:R[-2]C)|=SUM(F18:F21)|0
PEER_DIFF|Sheet1!F40|=SUM(R[-5]C:R[-1]C)|=SUM(F35:F39)|0
REF_CELL|Sheet1!F25|Enron|PRIOR||8|fmt=0.000
```


## Error 2: 1_Southpoint Gas Model.xls / Sheet1!I34

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(I9:I33)`
- corpus fix: `=SUM(I8:I33)`

tokens~521 truncated=False unsupported=None

```
TARGET|Sheet1!I34|=SUM(I9:I33)|value=79625|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=SUM(R[-25]C:R[-1]C)
ROW_PATH|Southpoint
COL_PATH|Total Gas Usage
SHEET|Sheet1|title=Southpoint|sheets_in_workbook=3
UNIT_NOTE|G6=Total MW
GRID|row\col|G|H|I|J|K
GRID|32|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|33|=SUM(G8:G32) -> 11865|(blank)|(blank)|(blank)|(blank)
GRID|*34|(blank)|(blank)|=SUM(I9:I33) -> 79625|(blank)|(blank)
GRID|35|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|36|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!I24|he22|=G24*H24|3430
COL|Sheet1!I25|he23|=G25*H25|3535
COL|Sheet1!I26|he24|=G26*H26|3535
COL|Sheet1!I27|he1|=G27*H27|3535
COL|Sheet1!I28|he2|=G28*H28|3535
COL|Sheet1!I29|he3|=G29*H29|3535
COL|Sheet1!I30|he4|=G30*H30|3535
COL|Sheet1!I31|he5|=G31*H31|3535
COL|Sheet1!I37|||(blank)
PEERS_ROW|none
PEERS_COL|formula_cells=13|same_r1c1=0
PEER_DIFF|Sheet1!I19|=RC[-2]*RC[-1]|=G19*H19|3430
PEER_DIFF|Sheet1!I20|=RC[-2]*RC[-1]|=G20*H20|3430
PEER_DIFF|Sheet1!I21|=RC[-2]*RC[-1]|=G21*H21|3430
REF_RANGE|Sheet1!I9:I33|cells=25|all_positive|min=3430|max=3535|numbers=23|blanks=2
IN_RANGE|Sheet1!I9|he 7|=G9*H9|3430
IN_RANGE|Sheet1!I10|he8|=G10*H10|3430
IN_RANGE|Sheet1!I11|he9|=G11*H11|3430
IN_RANGE_OMITTED|17 ordinary cells not shown
IN_RANGE|Sheet1!I29|he3|=G29*H29|3535
IN_RANGE|Sheet1!I30|he4|=G30*H30|3535
IN_RANGE|Sheet1!I31|he5|=G31*H31|3535
IN_RANGE|Sheet1!I32|||(blank)
IN_RANGE|Sheet1!I33|||(blank)
BEFORE_RANGE|Sheet1!I4|San Juan Gas Price||(blank)
BEFORE_RANGE|Sheet1!I5|||(blank)
BEFORE_RANGE|Sheet1!I6|HR||"Total Gas Usage"
BEFORE_RANGE|Sheet1!I7|||(blank)
BEFORE_RANGE|Sheet1!I8|he 6|=G8*H8|3430
AFTER_RANGE|Sheet1!I34|(target cell)
AFTER_RANGE|Sheet1!I35|||(blank)
AFTER_RANGE|Sheet1!I36|||(blank)
AFTER_RANGE|Sheet1!I37|||(blank)
AFTER_RANGE|Sheet1!I38|||(blank)
```


## Error 3: 1-BMSPT051.xls / BMSPT066!W43

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(W38:W38)`
- corpus fix: `=SUM(W37:W38)`

tokens~512 truncated=False unsupported=None

```
TARGET|BMSPT066!W43|=SUM(W38:W38)|value=-115816|fmt=[$-409]#,##0_);[RED]\(#,##0\)|bold=1
TARGET_R1C1|=SUM(R[-5]C:R[-5]C)
ROW_PATH|Total Projected > Variances: > Ending Balance > Projected
COL_PATH|Net LONG/ (SHORT) > LONG/(SHORT)
SHEET|BMSPT066|title=BAMMEL STORAGE ACTIVITY|sheets_in_workbook=2
GRID|row\col|U|V|W|X|Y
GRID|41|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|42|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*43|=SUM(U32:U38) -> 1407198|=SUM(V32:V38) -> 0|=SUM(W38:W38) -> -115816|(blank)|(blank)
GRID|44|=IF(U43>0,"SHORT","LONG") -> "SHORT"|=IF(V43>0,"SHORT","LONG") -> "LONG"|=IF(W43>0,"SHORT","LONG") -> "LONG"|(blank)|(blank)
GRID|45|"Previous Position:"|(blank)|-2802|(blank)|(blank)
COL|BMSPT066!W33|Estimated|=SUM(U33:V33)|301160
COL|BMSPT066!W34|Estimated|=SUM(U34:V34)|310200
COL|BMSPT066!W35|Estimated|=SUM(U35:V35)|236664
COL|BMSPT066!W36|Estimated|=SUM(U36:V36)|215000
COL|BMSPT066!W37|Projected|=SUM(U37:V37)|151000
COL|BMSPT066!W38|Projected|=SUM(U38:V38)|-115816
COL|BMSPT066!W39|||(blank)
COL|BMSPT066!W40||=SUM(W8:W38)|6500000
COL|BMSPT066!W46|Variance:|=+W45-W43|113014
PEERS_ROW|formula_cells=6|same_r1c1=0
PEER_DIFF|BMSPT066!O43|=SUM(R[-11]C:R[-5]C)|=SUM(O32:O38)|190297
PEER_DIFF|BMSPT066!Q43|=SUM(R[-11]C:R[-5]C)|=SUM(Q32:Q38)|1.46774e+06
PEER_DIFF|BMSPT066!R43|=SUM(R[-11]C:R[-5]C)|=SUM(R32:R38)|19703
PEERS_COL|formula_cells=14|same_r1c1=0
PEER_DIFF|BMSPT066!W28|=SUM(RC[-2]:RC[-1])|=SUM(U28:V28)|212476
PEER_DIFF|BMSPT066!W29|=SUM(RC[-2]:RC[-1])|=SUM(U29:V29)|232181
PEER_DIFF|BMSPT066!W30|=SUM(RC[-2]:RC[-1])|=SUM(U30:V30)|264388
REF_CELL|BMSPT066!W38|Projected|Net LONG/ (SHORT)|=SUM(U38:V38)|-115816|fmt=[$-409]#,##0_);[RED]\(#,##0\)
ASSUMPTION|BMSPT066!L5|HPLC Total|0|used_by=24|fmt=General
ASSUMPTION|BMSPT066!M5|HPLC Total|0|used_by=24|fmt=General
```


## Error 4: 1-BMSPT051.xls / BMSPT066!C43:V43

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(C32:C38)`
- corpus fix: `(unfixed by authors)`

tokens~529 truncated=False unsupported=None

```
TARGET|BMSPT066!C43|=SUM(C32:C38)|value=0|fmt=[$-409]#,##0_);[RED]\(#,##0\)|bold=1
TARGET_R1C1|=SUM(R[-11]C:R[-5]C)
ROW_PATH|Total Projected > Variances: > Ending Balance > Projected
COL_PATH|MTD Adjustment > HPL INDEX > VOLUME SPLIT BY Counterparties
SHEET|BMSPT066|title=BAMMEL STORAGE ACTIVITY|sheets_in_workbook=2
GRID|row\col|A|B|C|D|E
GRID|41|"Ending Balance"|(blank)|(blank)|(blank)|(blank)
GRID|42|"Variances:"|(blank)|(blank)|(blank)|=E40-E6 -> 0
GRID|*43|"Total Projected"|(blank)|=SUM(C32:C38) -> 0|=SUM(D32:D38) -> 0|=SUM(E32:E38) -> 1407198
GRID|44|"April 28 thru May 4"|(blank)|(blank)|(blank)|(blank)
GRID|45|"May 5 thru May 11"|(blank)|(blank)|(blank)|(blank)
COL|BMSPT066!C33:C39|||(7 blank cells)
COL|BMSPT066!C40||=SUM(C8:C38)|0
COL|BMSPT066!C46|||(blank)
ROW|BMSPT066!F43|MTD Adjustment|=SUM(F32:F38)|0
PEERS_ROW|formula_cells=8|same_r1c1=8
PEERS_COL|formula_cells=1|same_r1c1=0
PEER_DIFF|BMSPT066!C40|=SUM(R[-32]C:R[-2]C)|=SUM(C8:C38)|0
REF_RANGE|BMSPT066!C32:C38|cells=7|no_numbers|blanks=7
IN_RANGE|BMSPT066!C32|Estimated||(blank)
IN_RANGE|BMSPT066!C33|Estimated||(blank)
IN_RANGE|BMSPT066!C34|Estimated||(blank)
IN_RANGE|BMSPT066!C35|Estimated||(blank)
IN_RANGE|BMSPT066!C36|Estimated||(blank)
IN_RANGE|BMSPT066!C37|Projected||(blank)
IN_RANGE|BMSPT066!C38|Projected||(blank)
BEFORE_RANGE|BMSPT066!C27|Scheduled||(blank)
BEFORE_RANGE|BMSPT066!C28|Scheduled||(blank)
BEFORE_RANGE|BMSPT066!C29|Scheduled||(blank)
BEFORE_RANGE|BMSPT066!C30|Scheduled||(blank)
BEFORE_RANGE|BMSPT066!C31|Estimated||(blank)
AFTER_RANGE|BMSPT066!C39|||(blank)
AFTER_RANGE|BMSPT066!C40||=SUM(C8:C38)|0
AFTER_RANGE|BMSPT066!C41|Ending Balance||(blank)
AFTER_RANGE|BMSPT066!C42|Variances:||(blank)
AFTER_RANGE|BMSPT066!C43|(target cell)
ASSUMPTION|BMSPT066!L5|HPLC Total|0|used_by=24|fmt=General
ASSUMPTION|BMSPT066!M5|HPLC Total|0|used_by=24|fmt=General
```


## Error 5: 1_Tricia Roome.xls / Sheet1!L16

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=AVERAGE(F46:H52)`
- corpus fix: `=AVERAGE(H46:H52)`

tokens~495 truncated=False unsupported=None

```
TARGET|Sheet1!L16|=AVERAGE(F46:H52)|value=0.28|fmt=\$#,##0.0000_);"($"#,##0.0000\)|bold=0
TARGET_R1C1|=AVERAGE(R[30]C[-6]:R[36]C[-4])
ROW_PATH|Summer 04 > Transco Z4
COL_PATH|Transco Z5
SHEET|Sheet1|title=curves as of:|sheets_in_workbook=3
GRID|row\col|J|K|L|M|N
GRID|14|"Summer 02"|=AVERAGE(E22:E28) -> 0.0445|=AVERAGE(H22:H28) -> 0.42|(blank)|(blank)
GRID|15|"Summer 03"|=AVERAGE(E34:E40) -> 0.0465|=AVERAGE(H34:H40) -> 0.42|(blank)|(blank)
GRID|*16|"Summer 04"|=AVERAGE(E46:E52) -> 0.0485|=AVERAGE(F46:H52) -> 0.28|(blank)|(blank)
GRID|17|"Summer 05"|=AVERAGE(E58:E64) -> 0.0505|=AVERAGE(H58:H64) -> 0.42|(blank)|(blank)
GRID|18|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!L6|Winter 02|=AVERAGE(H17:H21)|0.961
COL|Sheet1!L7|Winter 03|=AVERAGE(H29:H33)|1.03
COL|Sheet1!L8|Winter 04|=AVERAGE(H41:H45)|1.04
COL|Sheet1!L9|Winter 05|=AVERAGE(H53:H57)|1.05
COL|Sheet1!L10:L11|||(2 blank cells)
COL|Sheet1!L12|Transco Z4||"Transco Z5"
COL|Sheet1!L13|Summer 01|=AVERAGE(H10:H16)|0.42
COL|Sheet1!L19|||(blank)
PEERS_ROW|formula_cells=3|same_r1c1=0
PEER_DIFF|Sheet1!E16|=RC[-2]+RC[-1]|=C16+D16|0.0425
PEER_DIFF|Sheet1!H16|=RC[-2]+RC[-1]|=F16+G16|0.385
PEER_DIFF|Sheet1!K16|=AVERAGE(R[30]C[-6]:R[36]C[-6])|=AVERAGE(E46:E52)|0.0485
PEERS_COL|formula_cells=9|same_r1c1=0
PEER_DIFF|Sheet1!L5|=AVERAGE(RC[-4]:R[4]C[-4])|=AVERAGE(H5:H9)|1.27
PEER_DIFF|Sheet1!L6|=AVERAGE(R[11]C[-4]:R[15]C[-4])|=AVERAGE(H17:H21)|0.961
PEER_DIFF|Sheet1!L7|=AVERAGE(R[22]C[-4]:R[26]C[-4])|=AVERAGE(H29:H33)|1.03
REF_RANGE|Sheet1!F46:H52|cells=21|mixed(pos=14,neg=7)|min=-0.085|max=0.5|numbers=21|blanks=0
REF_RANGE_2D|rows=7|cols=3
IN_RANGE|Sheet1!F46|||0.5
IN_RANGE|Sheet1!H46||=F46+G46|0.415
IN_RANGE|Sheet1!F52|||0.47
IN_RANGE|Sheet1!H52||=F52+G52|0.385
```


## Error 6: 1_July01invoice rev1.xls / jul01!AL44

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(AL11:AL43)`
- corpus fix: `=SUM(AL12:AL43)`

tokens~675 truncated=False unsupported=None

```
TARGET|jul01!AL44|=SUM(AL11:AL43)|value=20101.3|fmt=_(\$* #,##0.00_);_(\$* \(#,##0.00\);_(\$* \-??_);_(@_)|bold=0
TARGET_R1C1|=SUM(R[-33]C:R[-1]C)
ROW_PATH|TOTAL
COL_PATH|Fee > Services > Management
SHEET|jul01|title=Invoice Calculation|sheets_in_workbook=1
UNIT_NOTE|B3=%
UNIT_NOTE|B4=MMBtu/day
UNIT_NOTE|B5=MMBtu/day
GRID|row\col|AJ|AK|AL|AM|AN
GRID|42|=AD42*AD$11 -> 0|(blank)|=L42*$AL$11 -> 685.617|(blank)|=AJ42+AI42+AG42+AF42 -> 15021.6
GRID|43|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*44|=SUM(AJ12:AJ42) -> 3234.55|(blank)|=SUM(AL11:AL43) -> 20101.3|(blank)|=SUM(AN12:AN42) -> 438362
GRID|45|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|46|(blank)|(blank)|(blank)|(blank)|(blank)
COL|jul01!AL34||=L34*$AL$11|655.239
COL|jul01!AL35||=L35*$AL$11|642.386
COL|jul01!AL36||=L36*$AL$11|643.905
COL|jul01!AL37||=L37*$AL$11|639.465
COL|jul01!AL38||=L38*$AL$11|650.799
COL|jul01!AL39||=L39*$AL$11|591.561
COL|jul01!AL40||=L40*$AL$11|593.197
COL|jul01!AL41||=L41*$AL$11|691.576
COL|jul01!AL47|||(blank)
ROW|jul01!AI44|$|=SUM(AI12:AI42)|422845
PEERS_ROW|formula_cells=9|same_r1c1=0
PEER_DIFF|jul01!AD44|=SUM(R[-32]C:R[-2]C)|=SUM(AD12:AD42)|837.967
PEER_DIFF|jul01!AF44|=SUM(R[-32]C:R[-2]C)|=SUM(AF12:AF42)|0
PEER_DIFF|jul01!AG44|=SUM(R[-32]C:R[-2]C)|=SUM(AG12:AG42)|12282.2
PEERS_COL|formula_cells=14|same_r1c1=0
PEER_DIFF|jul01!AL29|=RC[-26]*R11C38|=L29*$AL$11|695.665
PEER_DIFF|jul01!AL30|=RC[-26]*R11C38|=L30*$AL$11|689.122
PEER_DIFF|jul01!AL31|=RC[-26]*R11C38|=L31*$AL$11|720.786
REF_RANGE|jul01!AL11:AL43|cells=33|all_positive|min=0.115|max=767.989|numbers=32|blanks=1
IN_RANGE|jul01!AL11|Price||0.115
IN_RANGE|jul01!AL12||=L12*$AL$11|588.64
IN_RANGE|jul01!AL13||=L13*$AL$11|589.925
IN_RANGE_OMITTED|25 ordinary cells not shown
IN_RANGE|jul01!AL39||=L39*$AL$11|591.561
IN_RANGE|jul01!AL40||=L40*$AL$11|593.197
IN_RANGE|jul01!AL41||=L41*$AL$11|691.576
IN_RANGE|jul01!AL42||=L42*$AL$11|685.617
IN_RANGE|jul01!AL43|||(blank)
BEFORE_RANGE|jul01!AL6|$/MMBtu/Mo||(blank)
BEFORE_RANGE|jul01!AL7|$/MMBtu||(blank)
BEFORE_RANGE|jul01!AL8|Cost of Bidweek Gas||"Management"
BEFORE_RANGE|jul01!AL9|Citgate||"Services"
BEFORE_RANGE|jul01!AL10|$||"Fee"
AFTER_RANGE|jul01!AL44|(target cell)
AFTER_RANGE|jul01!AL45|||(blank)
AFTER_RANGE|jul01!AL46|||(blank)
AFTER_RANGE|jul01!AL47|||(blank)
AFTER_RANGE|jul01!AL48|||(blank)
ASSUMPTION|jul01!C3|%|0.0137|used_by=62|fmt=0.00%
```


## Error 7: 1_Plan - Real-Time Trading.xls / Real Time!V23

- corpus type: Quantitative / Logical / Range error
- faulty formula: `=SUM(V11:V22)`
- corpus fix: `=SUM(V11:V16)`

tokens~627 truncated=False unsupported=None

```
TARGET|Real Time!V23|=SUM(V11:V22)|value=817000|fmt=[$-409]#,##0_);[RED]\(#,##0\)|bold=0
TARGET_R1C1|=SUM(R[-12]C:R[-1]C)
ROW_PATH|Total Headcount. > Title > Staffing Summary: > CC #: 107302
COL_PATH|2002 > FORECAST > 2002 Plan
SHEET|Real Time|title=West Power|sheets_in_workbook=1
GRID|row\col|T|U|V|W|X
GRID|21|(blank)|(blank)|=D21*A21 -> 42000|"Slinger, Ryan - Spec Trading Supt"|(blank)
GRID|22|(blank)|(blank)|=D22*A22 -> 0|"Solberg, Geir R - Analyst"|(blank)
GRID|*23|(blank)|(blank)|=SUM(V11:V22) -> 817000|"Symes, Mary K - Staff Tradind Supt"|(blank)
GRID|24|(blank)|(blank)|(blank)|"Williams, William J - Analyst - Rotation 2"|(blank)
GRID|25|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Real Time!V13|Dir|=D13*A13|0
COL|Real Time!V14|Mgr|=D14*A14|0
COL|Real Time!V15|Sr. Specialist|=D15*A15|130000
COL|Real Time!V16|Specialist|=D16*A16|440000
COL|Real Time!V17|Associate|=D17*A17|85000
COL|Real Time!V18|Analyst|=D18*A18|120000
COL|Real Time!V19|Technical|=D19*A19|0
COL|Real Time!V20|Admin|=D20*A20|0
COL|Real Time!V26|Jan|=V23/12|68083.3
PEERS_ROW|formula_cells=1|same_r1c1=1
PEERS_COL|formula_cells=16|same_r1c1=0
PEER_DIFF|Real Time!V11|=RC[-18]*RC[-21]|=D11*A11|0
PEER_DIFF|Real Time!V12|=RC[-18]*RC[-21]|=D12*A12|0
PEER_DIFF|Real Time!V13|=RC[-18]*RC[-21]|=D13*A13|0
REF_RANGE|Real Time!V11:V22|cells=12|all_positive|min=0|max=440000|numbers=12|blanks=0
IN_RANGE|Real Time!V11|Managing Dir|=D11*A11|0
IN_RANGE|Real Time!V12|VP|=D12*A12|0
IN_RANGE|Real Time!V13|Dir|=D13*A13|0
IN_RANGE_OMITTED|4 ordinary cells not shown
IN_RANGE|Real Time!V18|Analyst|=D18*A18|120000
IN_RANGE|Real Time!V19|Technical|=D19*A19|0
IN_RANGE|Real Time!V20|Admin|=D20*A20|0
IN_RANGE|Real Time!V21|Other|=D21*A21|42000
IN_RANGE|Real Time!V22||=D22*A22|0
BEFORE_RANGE|Real Time!V6|||(blank)
BEFORE_RANGE|Real Time!V7|Planned||"FORECAST"
BEFORE_RANGE|Real Time!V8|2000||"2002"
BEFORE_RANGE|Real Time!V9|Staffing Summary:||(blank)
BEFORE_RANGE|Real Time!V10|2002 HC||(blank)
AFTER_RANGE|Real Time!V23|(target cell)
AFTER_RANGE|Real Time!V24|Total Hdcnt w/o A & A||(blank)
AFTER_RANGE|Real Time!V25|||(blank)
AFTER_RANGE|Real Time!V26|Jan|=V23/12|68083.3
AFTER_RANGE|Real Time!V27|Merit Increase||(blank)
```


## Error 8: 1_5_14act.xls / Deals!AD142

- corpus type: Quantitative / Logical / Range error
- faulty formula: `=SUM(AD129:AD131)`
- corpus fix: `=SUM(AD120:AD131)`

tokens~457 truncated=False unsupported=None

```
TARGET|Deals!AD142|=SUM(AD129:AD131)|value=-8|fmt=_(* #,##0.00_);_(* \(#,##0.00\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=SUM(R[-13]C:R[-11]C)
ROW_PATH|EPE Purch from EPMI > Total per Model
COL_PATH|Total Volume
SHEET|Deals|title=(none)|sheets_in_workbook=14
GRID|row\col|AB|AC|AD|AE|AF
GRID|140|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|141|(blank)|(blank)|=SUM(AD22:AD120) -> 3368|=SUM(AE22:AE120) -> 553800|(blank)
GRID|*142|(blank)|(blank)|=SUM(AD129:AD131) -> -8|=SUM(AE121:AE131) -> -725320|(blank)
GRID|143|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|144|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Deals!AD132:AD145|||(9 blank cells)
PEERS_ROW|formula_cells=1|same_r1c1=0
PEER_DIFF|Deals!AE142|=SUM(R[-21]C:R[-11]C)|=SUM(AE121:AE131)|-725320
PEERS_COL|formula_cells=4|same_r1c1=0
PEER_DIFF|Deals!AD127|=SUM(RC[-25]:RC[-1])|=SUM(E127:AC127)|-800
PEER_DIFF|Deals!AD130|=SUM(RC[-25]:RC[-1])|=SUM(E130:AC130)|-8
PEER_DIFF|Deals!AD141|=SUM(R[-119]C:R[-21]C)|=SUM(AD22:AD120)|3368
REF_RANGE|Deals!AD129:AD131|cells=3|all_negative|min=-8|max=-8|numbers=1|blanks=2
IN_RANGE|Deals!AD129|||(blank)
IN_RANGE|Deals!AD130|PV|=SUM(E130:AC130)|-8
IN_RANGE|Deals!AD131|||(blank)
BEFORE_RANGE|Deals!AD124|PV|=SUM(E124:AC124)|-400
BEFORE_RANGE|Deals!AD125|PV|=SUM(E125:AC125)|-400
BEFORE_RANGE|Deals!AD126|PV|=SUM(E126:AC126)|-48
BEFORE_RANGE|Deals!AD127|PV|=SUM(E127:AC127)|-800
BEFORE_RANGE|Deals!AD128|||(blank)
AFTER_RANGE|Deals!AD132|||(blank)
AFTER_RANGE|Deals!AD133|||(blank)
AFTER_RANGE|Deals!AD134|leave this row blank||(blank)
AFTER_RANGE|Deals!AD135|||(blank)
AFTER_RANGE|Deals!AD136|AZ3||(blank)
```


## Error 9: 1_Sun Devil Project Request.XLS / Cost Estimate Summary!L23

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(L14:L20)`
- corpus fix: `=SUM(L14:L21)`

tokens~838 truncated=False unsupported=None

```
TARGET|Cost Estimate Summary!L23|=SUM(L14:L20)|value=140765104|fmt=_(\$* #,##0_);_(\$* \(#,##0\);_(\$* \-??_);_(@_)|bold=1
TARGET_R1C1|=SUM(R[-9]C:R[-3]C)
ROW_PATH|Total San Juan Expansion > To > 810 MMCF/D EXPANSION (2020 MMCF/D TOTAL) > SUN DEVIL FROM STATION #2 DISCHARGE
COL_PATH|Est. Costs
SHEET|Cost Estimate Summary|title=(none)|sheets_in_workbook=15
GRID|row\col|J|K|L|M|N
GRID|21|(blank)|(blank)|5000000|(blank)|(blank)
GRID|22|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*23|(blank)|(blank)|=SUM(L14:L20) -> 140765104|(blank)|=1630-850 -> 780
GRID|24|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|25|"""|(blank)|=I25*28000*1.1*G25 -> 48676320|(blank)|(blank)
COL|Cost Estimate Summary!L13|Size (")||"Est. Costs"
COL|Cost Estimate Summary!L14|"|=I14*28000*1.1*G14|107365104
COL|Cost Estimate Summary!L15|Bloomfield Hp (7000 Hp)|=13000000|13000000
COL|Cost Estimate Summary!L16|Bloomfield Mods||1000000
COL|Cost Estimate Summary!L17|Bloomfield Compressor Mods||2400000
COL|Cost Estimate Summary!L18|Blanco Hub Mods||2000000
COL|Cost Estimate Summary!L19|Bisti CS Mods||1000000
COL|Cost Estimate Summary!L20|Standing Rock CS (9,500 Hp)||14000000
COL|Cost Estimate Summary!L26|"|=I26*28000*1.1*G26|94802400
PEERS_ROW|formula_cells=3|same_r1c1=0
PEER_DIFF|Cost Estimate Summary!G23|=SUM(R[-9]C:R[-1]C)|=SUM(G14:G22)|96.83
PEER_DIFF|Cost Estimate Summary!N23|=1630-850|=1630-850|780
PEER_DIFF|Cost Estimate Summary!R23|=SUM(R[-9]C:R[-1]C)|=SUM(R14:R22)|19520928
PEERS_COL|formula_cells=11|same_r1c1=0
PEER_DIFF|Cost Estimate Summary!L14|=RC[-3]*28000*1.1*RC[-5]|=I14*28000*1.1*G14|107365104
PEER_DIFF|Cost Estimate Summary!L15|=13000000|=13000000|13000000
PEER_DIFF|Cost Estimate Summary!L25|=RC[-3]*28000*1.1*RC[-5]|=I25*28000*1.1*G25|48676320
REF_RANGE|Cost Estimate Summary!L14:L20|cells=7|all_positive|min=1e+06|max=1.07365e+08|numbers=7|blanks=0
IN_RANGE|Cost Estimate Summary!L14|"|=I14*28000*1.1*G14|107365104
IN_RANGE|Cost Estimate Summary!L15|Bloomfield Hp (7000 Hp)|=13000000|13000000
IN_RANGE|Cost Estimate Summary!L16|Bloomfield Mods||1000000
IN_RANGE|Cost Estimate Summary!L17|Bloomfield Compressor Mods||2400000
IN_RANGE|Cost Estimate Summary!L18|Blanco Hub Mods||2000000
IN_RANGE|Cost Estimate Summary!L19|Bisti CS Mods||1000000
IN_RANGE|Cost Estimate Summary!L20|Standing Rock CS (9,500 Hp)||14000000
BEFORE_RANGE|Cost Estimate Summary!L9|SUN DEVIL FROM STATION #2 DISCHARGE||(blank)
BEFORE_RANGE|Cost Estimate Summary!L10|810 MMCF/D EXPANSION (2020 MMCF/D TOTAL)||(blank)
BEFORE_RANGE|Cost Estimate Summary!L11|||(blank)
BEFORE_RANGE|Cost Estimate Summary!L12|||(blank)
BEFORE_RANGE|Cost Estimate Summary!L13|Size (")||"Est. Costs"
AFTER_RANGE|Cost Estimate Summary!L21|Gallup CS Mods||5000000
AFTER_RANGE|Cost Estimate Summary!L22|||(blank)
AFTER_RANGE|Cost Estimate Summary!L23|(target cell)
AFTER_RANGE|Cost Estimate Summary!L24|||(blank)
AFTER_RANGE|Cost Estimate Summary!L25|"|=I25*28000*1.1*G25|48676320
```


## Error 10: 1_ONEOKRECAP2001.xls / OCT 01!T39

- corpus type: Quantitative / Mechanical / Wrong formula
- faulty formula: `=N38-9=SUM(T6:T36)+T38`
- corpus fix: `=SUM(T6:T36)+T38`

tokens~688 truncated=False unsupported=None

```
TARGET|OCT 01!T39|=N38-9=SUM(T6:T36)+T38|value=0|fmt=[$-409]#,##0_);[RED]\(#,##0\)|bold=0
TARGET_R1C1|=R[-1]C[-6]-9=SUM(R[-33]C:R[-3]C)+R[-1]C
ROW_PATH|OC TOBER CUMULATIVE > VOLUME ADJ. > (EST) BEGINNING BALANCE > SUBLETTE
COL_PATH|HEMPHILL/CANADIAN > 65, 62867
SHEET|OCT 01|title=INTERNAL REPORT ONLY|sheets_in_workbook=12
GRID|row\col|R|S|T|U|V
GRID|37|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|38|(blank)|(blank)|16|(blank)|=SUM(D38:T38) -> 5804
GRID|*39|=SUM(R6:R36)+R38 -> -661|(blank)|=N38-9=SUM(T6:T36)+T38 -> 0|(blank)|=SUM(D39:T39) -> 144008
GRID|40|=R5+R39 -> 14744|(blank)|=T5+T39 -> 144771|(blank)|=SUM(D40:T40) -> 173478
GRID|41|(blank)|(blank)|(blank)|(blank)|(blank)
COL|OCT 01!T29|||-1996
COL|OCT 01!T30:T42|||(8 blank cells)
PEERS_ROW|formula_cells=5|same_r1c1=0
PEER_DIFF|OCT 01!L39|=SUM(R[-33]C:R[-3]C)+R[-1]C|=SUM(L6:L36)+L38|0
PEER_DIFF|OCT 01!N39|=SUM(R[-33]C:R[-3]C)+R[-1]C|=SUM(N6:N36)+N38|13897
PEER_DIFF|OCT 01!P39|=SUM(R[-33]C:R[-3]C)+R[-1]C|=SUM(P6:P36)+P38|-564
PEERS_COL|formula_cells=1|same_r1c1=0
PEER_DIFF|OCT 01!T40|=R[-35]C+R[-1]C|=T5+T39|144771
REF_CELL|OCT 01!N38|VOLUME ADJ.|ELLIS CO #1/#2||-9|fmt=[$-409]#,##0_);[RED]\(#,##0\)
REF_RANGE|OCT 01!T6:T36|cells=31|mixed(pos=10,neg=14)|min=-4494|max=850|numbers=24|blanks=7
IN_RANGE|OCT 01!T6|||-2458
IN_RANGE|OCT 01!T7|||627
IN_RANGE|OCT 01!T8|||-2856
IN_RANGE_NOTE|OCT 01!T9|||-4494|negative
IN_RANGE_NOTE|OCT 01!T13|||-137|negative
IN_RANGE_NOTE|OCT 01!T15|||-17|negative
IN_RANGE_NOTE|OCT 01!T16|||-255|negative
IN_RANGE_NOTE|OCT 01!T19|||-225|negative
IN_RANGE_NOTE|OCT 01!T20|||-394|negative
IN_RANGE_NOTE|OCT 01!T21|||-562|negative
IN_RANGE_NOTE|OCT 01!T22|||-659|negative
IN_RANGE_OMITTED|15 ordinary cells not shown
IN_RANGE|OCT 01!T32|||(blank)
IN_RANGE|OCT 01!T33|||(blank)
IN_RANGE|OCT 01!T34|||(blank)
IN_RANGE|OCT 01!T35|||(blank)
IN_RANGE|OCT 01!T36|||(blank)
BEFORE_RANGE|OCT 01!T1|POI 78107||"65, 62867"
BEFORE_RANGE|OCT 01!T2|CLARK CO #1||"HEMPHILL/CANADIAN"
BEFORE_RANGE|OCT 01!T3|TOTAL DEVIATION||108308
BEFORE_RANGE|OCT 01!T4|||(blank)
BEFORE_RANGE|OCT 01!T5|(EST) BEGINNING BALANCE||144771
AFTER_RANGE|OCT 01!T37|||(blank)
AFTER_RANGE|OCT 01!T38|VOLUME ADJ.||16
AFTER_RANGE|OCT 01!T39|(target cell)
AFTER_RANGE|OCT 01!T40|EST ENDING BALANCE|=T5+T39|144771
AFTER_RANGE|OCT 01!T41|BAD DAS||(blank)
REF_CELL|OCT 01!T38|VOLUME ADJ.|HEMPHILL/CANADIAN||16|fmt=[$-409]#,##0_);[RED]\(#,##0\)
OVERLAP|none
```


## Error 11: 1_SunDevil01CostSummary.xls / EPSunDevil!F10

- corpus type: Quantitative / Mechanical / Wrong reference
- faulty formula: `=D5*1500`
- corpus fix: `=D10*1500`

tokens~531 truncated=False unsupported=None

```
TARGET|EPSunDevil!F10|=D5*1500|value=37500000|fmt=_(\$* #,##0.00_);_(\$* \(#,##0.00\);_(\$* \-??_);_(@_)|bold=0
TARGET_R1C1|=R[-5]C[-2]*1500
ROW_PATH|Added Compression > Waha, Texas to Phoenix (Line 2000 orig. empty) > Total Cost: > San Juan Junction to Phoenix (new pipe)
COL_PATH|High End Cost > El Paso Sun Devil Competitor Analysis
SHEET|EPSunDevil|title=El Paso Sun Devil Competitor Analysis|sheets_in_workbook=1
GRID|row\col|D|E|F|G|H
GRID|8|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|9|570|0|0|"This case is more to serve as a benchmark since Line 2000 is"|(blank)
GRID|*10|32000|=D10*1200 -> 38400000|=D5*1500 -> 37500000|"This case is more to serve as a benchmark since Line 2000 is"|(blank)
GRID|11|(blank)|=SUM(E9:E10) -> 38400000|=SUM(F9:F10) -> 37500000|"This case is more to serve as a benchmark since Line 2000 is"|(blank)
GRID|12|(blank)|(blank)|(blank)|(blank)|(blank)
COL|EPSunDevil!A1|El Paso Sun Devil Competitor Analysis||"El Paso Sun Devil Competitor Analysis"
COL|EPSunDevil!F2|||(blank)
COL|EPSunDevil!F3|Low End Cost||"High End Cost"
COL|EPSunDevil!F4|Miles Pipe|=$D$4*1700000|748000000
COL|EPSunDevil!F5|Added Compression|=$D$5*1500|37500000
COL|EPSunDevil!F6|Total Cost:|=SUM(F4:F5)|785500000
COL|EPSunDevil!F7:F13|||(2 blank cells)
ROW|EPSunDevil!C10|Miles Pipe||"Added Compression"
PEERS_ROW|formula_cells=1|same_r1c1=0
PEER_DIFF|EPSunDevil!E10|=RC[-1]*1200|=D10*1200|38400000
PEERS_COL|formula_cells=6|same_r1c1=0
PEER_DIFF|EPSunDevil!F4|=R4C4*1700000|=$D$4*1700000|748000000
PEER_DIFF|EPSunDevil!F5|=R5C4*1500|=$D$5*1500|37500000
PEER_DIFF|EPSunDevil!F6|=SUM(R[-2]C:R[-1]C)|=SUM(F4:F5)|785500000
REF_CELL|EPSunDevil!D5|Added Compression|El Paso Sun Devil Competitor Analysis||25000|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)
ASSUMPTION|EPSunDevil!D4|Miles Pipe|440|used_by=2|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)
```


## Error 12: 1_Citrus Pass-Through 12.01.00.xls / Data!D13

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=C6*(1+C12*(B52/364.25))-C6`
- corpus fix: `=C6*(1+C12/2)^(2*(B52/364.25))-C6`

tokens~399 truncated=False unsupported=None

```
TARGET|Data!D13|=C6*(1+C12*(B52/364.25))-C6|value=428009|fmt=_(\$* #,##0_);_(\$* \(#,##0\);_(\$* \-??_);_(@_)|bold=0
TARGET_R1C1|=R[-7]C[-1]*(1+R[-1]C[-1]*(R[39]C[-2]/364.25))-R[-7]C[-1]
ROW_PATH|tot volume > Today > Inputs > Project Kubrick
COL_PATH|Fees to Citrus
SHEET|Data|title=Project Kubrick|sheets_in_workbook=1
UNIT_NOTE|B8=FGT Zone 2 $/MMBtu
GRID|row\col|B|C|D|E|F
GRID|11|"Exchange Fee $/MMBtu"|0.01|=C11*C13 -> 120301|(blank)|(blank)
GRID|12|"All-in Citrus price"|=C7+C10 -> 0.0742391|(blank)|(blank)|(blank)
GRID|*13|"tot volume"|=C5/C8 -> 1.20301e+07|=C6*(1+C12*(B52/364.25))-C6 -> 428009|"tot fee"|(blank)
GRID|14|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|15|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Data!D3|||(blank)
COL|Data!D4|Payables extension||"Fees to Citrus"
COL|Data!D5|Swap amount|=D13-D11|307708
COL|Data!D6:D10|||(5 blank cells)
COL|Data!D16|daily delivery to Citrus(MMBtu)||"delivery to ENA(MMBtu)"
PEERS_ROW|formula_cells=1|same_r1c1=0
PEER_DIFF|Data!C13|=R[-8]C/R[-5]C|=C5/C8|1.20301e+07
PEERS_COL|formula_cells=2|same_r1c1=0
PEER_DIFF|Data!D5|=R[8]C-R[6]C|=D13-D11|307708
PEER_DIFF|Data!D11|=RC[-1]*R[2]C[-1]|=C11*C13|120301
REF_CELL|Data!C6|Cash target|||100000000|fmt=_(\$* #,##0_);_(\$* \(#,##0\);_(\$* \-??_);_(@_)
REF_CELL|Data!C12|All-in Citrus price||=C7+C10|0.0742391|fmt=0.00%
REF_CELL|Data!B52||Total delivered volume|=B51-B36|21|fmt=0
OVERLAP|none
```


## Error 13: 1_Huber - Existing & Proposed Deals 111201.xls / Curves!V5:V341

- corpus type: Quantitative / Omission / Wrong calculation
- faulty formula: `=$B5+T5+U5`
- corpus fix: `=$B5+X5+Y5+Z5`

tokens~319 truncated=False unsupported=None

```
TARGET|Curves!V5|=$B5+T5+U5|value=2.488|fmt=_(* #,##0.00_);_(* \(#,##0.00\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=RC2+RC[-2]+RC[-1]
ROW_PATH|NYMEX
COL_PATH|Price
SHEET|Curves|title=(none)|sheets_in_workbook=4
UNIT_NOTE|L3=IF NGPL MidContinent Index minus $0.01
GRID|row\col|T|U|V|W|X
GRID|3|"Gas Daily PG&E Topock index minus $0.02 (Proposed)"|(blank)|(blank)|(blank)|"Gas Daily El Paso- San Juan index minus $0.10 (Proposed)"
GRID|4|"Basis"|"Index"|"Price"|(blank)|"Basis"
GRID|*5|-0.225|-0.02|=$B5+T5+U5 -> 2.488|(blank)|-0.485
GRID|6|-0.2|-0.02|=$B6+T6+U6 -> 2.71|(blank)|-0.38
GRID|7|-0.205|-0.02|=$B7+T7+U7 -> 2.743|(blank)|-0.34
COL|Curves!V1:V2|||(2 blank cells)
COL|Curves!V8||=$B8+T8+U8|2.693
ROW|Curves!Y5|Index||-0.1
ROW|Curves!Z5|Price|=$B5+X5+Y5|2.148
PEERS_ROW|formula_cells=4|same_r1c1=4
PEERS_COL|formula_cells=15|same_r1c1=15
REF_CELL|Curves!B5||NYMEX||2.733|fmt=_(* #,##0.00_);_(* \(#,##0.00\);_(* \-??_);_(@_)
REF_CELL|Curves!T5||Basis||-0.225|fmt=_(* #,##0.00_);_(* \(#,##0.00\);_(* \-??_);_(@_)
REF_CELL|Curves!U5||Index||-0.02|fmt=_(* #,##0.00_);_(* \(#,##0.00\);_(* \-??_);_(@_)
OVERLAP|none
```


## Error 14: 1_Agro Case Question 3--Jeff.xls / Sheet1!H33

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=SUM(H28:H32)`
- corpus fix: `=H28+H32-H30`

tokens~625 truncated=False unsupported=None

```
TARGET|Sheet1!H33|=SUM(H28:H32)|value=1875|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=SUM(R[-5]C:R[-1]C)
ROW_PATH|Total > Unusual loss from government ban of certain preservatives > of accounting changes: > Income before unusual items, extraordinary items and effect
COL_PATH|(none)
SHEET|Sheet1|title=Question 3|sheets_in_workbook=3
UNIT_NOTE|A5=Income from continuing operations ($000)
GRID|row\col|F|G|H|I|J
GRID|31|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|32|(blank)|(blank)|250|(blank)|(blank)
GRID|*33|(blank)|(blank)|=SUM(H28:H32) -> 1875|(blank)|(blank)
GRID|34|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|35|(blank)|(blank)|(blank)|=I29-H33 -> 2311|(blank)
COL|Sheet1!H23:H24|||(2 blank cells)
COL|Sheet1!H25|Cost of inventory write down||500
COL|Sheet1!H26|Costs associated with switching products||300
COL|Sheet1!H27|Litigation costs associated with government action||75
COL|Sheet1!H28|Total|=SUM(H25:H27)|875
COL|Sheet1!H29|||(blank)
COL|Sheet1!H30|Unusual gain from sale of land assets||750
COL|Sheet1!H36|Extraordinary loss due to tornado damage||135
PEERS_ROW|none
PEERS_COL|formula_cells=2|same_r1c1=0
PEER_DIFF|Sheet1!H19|=R[-2]C-R[-1]C|=H17-H18|4439
PEER_DIFF|Sheet1!H28|=SUM(R[-3]C:R[-1]C)|=SUM(H25:H27)|875
REF_RANGE|Sheet1!H28:H32|cells=5|all_positive|min=250|max=875|numbers=3|blanks=2
IN_RANGE|Sheet1!H28|Total|=SUM(H25:H27)|875
IN_RANGE|Sheet1!H29|||(blank)
IN_RANGE|Sheet1!H30|Unusual gain from sale of land assets||750
IN_RANGE|Sheet1!H31|||(blank)
IN_RANGE|Sheet1!H32|Unusual loss from litigation associated with consumer class ||250
BEFORE_RANGE|Sheet1!H23|||(blank)
BEFORE_RANGE|Sheet1!H24|Unusual loss from government ban of certain preservatives||(blank)
BEFORE_RANGE|Sheet1!H25|Cost of inventory write down||500
BEFORE_RANGE|Sheet1!H26|Costs associated with switching products||300
BEFORE_RANGE|Sheet1!H27|Litigation costs associated with government action||75
AFTER_RANGE|Sheet1!H33|(target cell)
AFTER_RANGE|Sheet1!H34|||(blank)
AFTER_RANGE|Sheet1!H35|Income before extraordinary items and effect of accounting c||(blank)
AFTER_RANGE|Sheet1!H36|Extraordinary loss due to tornado damage||135
AFTER_RANGE|Sheet1!H37|||(blank)
```


## Error 15: 1_Agro Case Question 3--Jeff.xls / Sheet1!I35

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=I29-H33`
- corpus fix: `=+I22-H33`

tokens~370 truncated=False unsupported=None

```
TARGET|Sheet1!I35|=I29-H33|value=2311|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=R[-6]C-R[-2]C[-1]
ROW_PATH|Income before extraordinary items and effect of accounting c > Unusual loss from government ban of certain preservatives > of accounting changes: > Income before unusual items, extraordinary items and effect
COL_PATH|1995
SHEET|Sheet1|title=Question 3|sheets_in_workbook=3
UNIT_NOTE|A5=Income from continuing operations ($000)
GRID|row\col|G|H|I|J|K
GRID|33|(blank)|=SUM(H28:H32) -> 1875|(blank)|(blank)|(blank)
GRID|34|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*35|(blank)|(blank)|=I29-H33 -> 2311|(blank)|(blank)
GRID|36|(blank)|135|(blank)|(blank)|(blank)
GRID|37|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!I25:I28|||(4 blank cells)
COL|Sheet1!I29||=I22-H28|4186
COL|Sheet1!I30:I32|||(3 blank cells)
COL|Sheet1!I38|Net Income|=I35-H36|2176
PEERS_ROW|none
PEERS_COL|formula_cells=3|same_r1c1=0
PEER_DIFF|Sheet1!I22|=R[-17]C-R[-3]C[-1]|=I5-H19|5061
PEER_DIFF|Sheet1!I29|=R[-7]C-R[-1]C[-1]|=I22-H28|4186
PEER_DIFF|Sheet1!I38|=R[-3]C-R[-2]C[-1]|=I35-H36|2176
REF_CELL|Sheet1!I29||1995|=I22-H28|4186|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)
REF_CELL|Sheet1!H33|Total||=SUM(H28:H32)|1875|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)
OVERLAP|none
```


## Error 16: 1_Agro Case Question 3--Jeff.xls / Sheet1!I38

- corpus type: Quantitative / Omission / Wrong calculation
- faulty formula: `=I35-H36`
- corpus fix: `=I38+H41`

tokens~368 truncated=False unsupported=None

```
TARGET|Sheet1!I38|=I35-H36|value=2176|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)|bold=1
TARGET_R1C1|=R[-3]C-R[-2]C[-1]
ROW_PATH|Net Income > Income before extraordinary items and effect of accounting c > Unusual loss from government ban of certain preservatives > of accounting changes:
COL_PATH|1995
SHEET|Sheet1|title=Question 3|sheets_in_workbook=3
UNIT_NOTE|A5=Income from continuing operations ($000)
GRID|row\col|G|H|I|J|K
GRID|36|(blank)|135|(blank)|(blank)|(blank)
GRID|37|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*38|(blank)|(blank)|=I35-H36 -> 2176|(blank)|(blank)
GRID|39|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|40|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!I28|||(blank)
COL|Sheet1!I29||=I22-H28|4186
COL|Sheet1!I30:I34|||(5 blank cells)
COL|Sheet1!I35|Income before extraordinary items and effect of accounting c|=I29-H33|2311
COL|Sheet1!I41|||(blank)
PEERS_ROW|none
PEERS_COL|formula_cells=2|same_r1c1=0
PEER_DIFF|Sheet1!I29|=R[-7]C-R[-1]C[-1]|=I22-H28|4186
PEER_DIFF|Sheet1!I35|=R[-6]C-R[-2]C[-1]|=I29-H33|2311
REF_CELL|Sheet1!I35|Income before extraordinary items and effect of accounting c|1995|=I29-H33|2311|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)
REF_CELL|Sheet1!H36|Extraordinary loss due to tornado damage|||135|fmt=General
OVERLAP|none
```


## Error 19: 1_PSEG - Enron Bankruptcy Revised.xls / Sheet1!B13:O13; B25:O25; B37:O37

- corpus type: Quantitative / Omission / Wrong calculation
- faulty formula: `=(B12/C13-B12)`
- corpus fix: `(unfixed by authors)`

tokens~515 truncated=False unsupported=None

```
TARGET|Sheet1!B13|=(B12/C13-B12)|value=0.27289|fmt=_(\$* #,##0.0000_);_(\$* \(#,##0.0000\);_(\$* \-??_);_(@_)|bold=0
TARGET_R1C1|=(R[-1]C/RC[1]-R[-1]C)
ROW_PATH|Fuel - % > Contract Price: > Term Deal - Purchase 10,000 Dths / Day (May 2001 - April 200 > PRODUCTION MONTH:
COL_PATH|Enron's invoices paid by PSE&G for gas purchases > FERC Tariff Sheets - FT transportation - Website > Trade Tickets / Transaction Confirmations
SHEET|Sheet1|title=Source:|sheets_in_workbook=3
UNIT_NOTE|A8=Term Deal - Purchase 10,000 Dths / Day (May 2001 - April 200
GRID|row\col|A|B|C|D
GRID|11|"Sta. #30 - Dths / Day"|1700|(blank)|1700
GRID|12|"IF Index"|4.79|(blank)|3.64
GRID|*13|"Fuel - %"|=(B12/C13-B12) -> 0.27289|=1-0.0539 -> 0.9461|=(D12/E13-D12) -> 0.207373
GRID|14|"Transport."|0.0392|(blank)|0.0392
GRID|15|"ACA"|0.0022|(blank)|0.0022
COL|Sheet1!B3|||"Enron's invoices paid by PSE&G for gas purchases"
COL|Sheet1!B4:B5|||(2 blank cells)
COL|Sheet1!B6|PRODUCTION MONTH:||2001-05-01 00:00:00
COL|Sheet1!B7:B10|||(4 blank cells)
COL|Sheet1!B16|GRI||0.007
ROW|Sheet1!E13||=1-0.0539|0.9461
ROW|Sheet1!F13||=(F12/G13-F12)|0.17604
ROW|Sheet1!G13||=1-0.0539|0.9461
PEERS_ROW|formula_cells=8|same_r1c1=4
PEER_DIFF|Sheet1!C13|=1-0.0539|=1-0.0539|0.9461
PEER_DIFF|Sheet1!E13|=1-0.0539|=1-0.0539|0.9461
PEER_DIFF|Sheet1!G13|=1-0.0539|=1-0.0539|0.9461
PEERS_COL|formula_cells=4|same_r1c1=1
PEER_DIFF|Sheet1!B18|=SUM(R[-6]C:R[-1]C)|=SUM(B12:B17)|5.12099
PEER_DIFF|Sheet1!B20|=+R[-2]C-R[-1]C|=+B18-B19|0.27289
PEER_DIFF|Sheet1!B21|=(R[-10]C*31)*R[-1]C|=(B11*31)*B20|14381.3
REF_CELL|Sheet1!B12|IF Index|Enron's invoices paid by PSE&G for gas purchases||4.79|fmt=_(\$* #,##0.0000_);_(\$* \(#,##0.0000\);_(\$* \-??_);_(@_)
REF_CELL|Sheet1!C13|Fuel - %||=1-0.0539|0.9461|fmt=_(* #,##0.0000_);_(* \(#,##0.0000\);_(* \-??_);_(@_)
```


## Error 22: 1_CrackSpreadOptions.xls / Crack Spread Option!M9:M14

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,M$7)`
- corpus fix: `=C9*HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,M$7)`

tokens~729 truncated=False unsupported=None

```
TARGET|Crack Spread Option!M9|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,M$7)|value=#NAME?|fmt=0.0000|bold=1
TARGET_R1C1|=HEAT(RC2,RC3,RC4,RC5,RC6,RC7,RC8,RC9-R5C3,RC11,R7C)
ROW_PATH|Fwd Price 1 > INPUTS > EffDt
COL_PATH|Price > OUTPUTS
SHEET|Crack Spread Option|title=Exotica Crack Spread Option: HEAT|sheets_in_workbook=16
UNIT_NOTE|C2=(ERCOT Example from Megawatt Daily in Case Study #2)
GRID|row\col|K|L|M|N|O
GRID|7|(blank)|"RetType"|0|1|2
GRID|8|"OptType"|(blank)|"Price"|"Delta 1"|"Delta 2"
GRID|*9|1|(blank)|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,M$7) -> #NAME?|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,N$7) -> #NAME?|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,O$7) -> #NAME?
GRID|10|1|(blank)|=HEAT($B10,$C10,$D10,$E10,$F10,$G10,$H10,$I10-$C$5,$K10,M$7) -> #NAME?|=HEAT($B10,$C10,$D10,$E10,$F10,$G10,$H10,$I10-$C$5,$K10,N$7) -> #NAME?|=HEAT($B10,$C10,$D10,$E10,$F10,$G10,$H10,$I10-$C$5,$K10,O$7) -> #NAME?
GRID|11|1|(blank)|=HEAT($B11,$C11,$D11,$E11,$F11,$G11,$H11,$I11-$C$5,$K11,M$7) -> #NAME?|=HEAT($B11,$C11,$D11,$E11,$F11,$G11,$H11,$I11-$C$5,$K11,N$7) -> #NAME?|=HEAT($B11,$C11,$D11,$E11,$F11,$G11,$H11,$I11-$C$5,$K11,O$7) -> #NAME?
COL|Crack Spread Option!M1:M5|||(5 blank cells)
COL|Crack Spread Option!M6|||"OUTPUTS"
COL|Crack Spread Option!M12||=HEAT($B12,$C12,$D12,$E12,$F12,$G12,$H12,$I12-$C$5,$K12,M$7)|#NAME?
ROW|Crack Spread Option!J9|Days|=I9-$C$5|29
ROW|Crack Spread Option!P9|Gamma 1|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,P$7)|#NAME?
ROW|Crack Spread Option!Q9|Gamma 2|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,Q$7)|#NAME?
ROW|Crack Spread Option!R9|Vega 1|=HEAT($B9,$C9,$D9,$E9,$F9,$G9,$H9,$I9-$C$5,$K9,R$7)|#NAME?
PEERS_ROW|formula_cells=9|same_r1c1=8
PEER_DIFF|Crack Spread Option!J9|=RC[-1]-R5C3|=I9-$C$5|29
PEERS_COL|formula_cells=5|same_r1c1=5
REF_CELL|Crack Spread Option!B9||Fwd Price 1||54.83|fmt=0.00
REF_CELL|Crack Spread Option!C9||Fwd Price 2||5.83|fmt=0.00
REF_CELL|Crack Spread Option!D9||(Heat Rate)/1000||7|fmt=General
REF_CELL|Crack Spread Option!E9||Ann.IntRt||0.0525|fmt=0.00%
REF_CELL|Crack Spread Option!F9||Vol.1||0.9|fmt=0%
REF_CELL|Crack Spread Option!G9||Vol.2||0.85|fmt=0%
REF_CELL|Crack Spread Option!H9||Correlation||0.5|fmt=0%
REF_CELL|Crack Spread Option!I9||ExpDt||2000-12-29 00:00:00|fmt=[$-409]m/d/yyyy
REF_CELL|Crack Spread Option!C5|EffDt|(ERCOT Example from Megawatt Daily in Case Study #2)||2000-11-30 00:00:00|fmt=[$-409]m/d/yyyy
REF_CELL|Crack Spread Option!K9||OptType||1|fmt=General
REF_CELL|Crack Spread Option!M7|RetType|OUTPUTS||0|fmt=General
```


## Error 23: 1_EPE_MAY_2002.xls / MAY(2)!AE18:AE41

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(M18:Q18,V18:V18)`
- corpus fix: `=SUM(M18:Q18,V18:X18)`

tokens~529 truncated=False unsupported=None

```
TARGET|MAY(2)!AE18|=SUM(M18:Q18,V18:V18)|value=125|fmt=0_);[RED]\(0\)|bold=0
TARGET_R1C1|=SUM(RC[-18]:RC[-14],RC[-9]:RC[-9])
ROW_PATH|0100 > 0100 > PDT > Time
COL_PATH|NET FOUR CORNERS
SHEET|MAY(2)|title=To: El Paso Marketing - fax # 915-521-4751|sheets_in_workbook=2
GRID|row\col|AC|AD|AE|AF|AG
GRID|16|"TOTAL NET"|"NET PALO VERDE"|"NET FOUR CORNERS"|"NET EDDY"|(blank)
GRID|17|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*18|=SUM(C18:AA18) -> 175|=SUM(C18:L18,S18:U18) -> 175|=SUM(M18:Q18,V18:V18) -> 125|=SUM(Y18:AA18) -> 0|(blank)
GRID|19|=SUM(C19:AA19) -> 175|=SUM(C19:L19,S19:U19) -> 175|=SUM(M19:Q19,V19:V19) -> 125|=SUM(Y19:AA19) -> 0|(blank)
GRID|20|=SUM(C20:AA20) -> 175|=SUM(C20:L20,S20:U20) -> 175|=SUM(M20:Q20,V20:V20) -> 125|=SUM(Y20:AA20) -> 0|(blank)
COL|MAY(2)!AE8:AE15|||(8 blank cells)
COL|MAY(2)!AE21|0400|=SUM(M21:Q21,V21:V21)|125
PEERS_ROW|formula_cells=3|same_r1c1=0
PEER_DIFF|MAY(2)!AC18|=SUM(RC[-26]:RC[-2])|=SUM(C18:AA18)|175
PEER_DIFF|MAY(2)!AD18|=SUM(RC[-27]:RC[-18],RC[-11]:RC[-9])|=SUM(C18:L18,S18:U18)|175
PEER_DIFF|MAY(2)!AF18|=SUM(RC[-7]:RC[-5])|=SUM(Y18:AA18)|0
PEERS_COL|formula_cells=15|same_r1c1=15
REF_RANGE|MAY(2)!M18:Q18|cells=5|all_positive|min=0|max=50|numbers=5|blanks=0
IN_RANGE|MAY(2)!M18|DIRECT BILL||50
IN_RANGE|MAY(2)!N18|DIRECT BILL||0
IN_RANGE|MAY(2)!O18|DIRECT BILL||50
IN_RANGE|MAY(2)!P18|DIRECT BILL||0
IN_RANGE|MAY(2)!Q18|DIRECT BILL||25
BEFORE_RANGE|MAY(2)!H18|DIRECT BILL||50
BEFORE_RANGE|MAY(2)!I18|DIRECT BILL||25
BEFORE_RANGE|MAY(2)!J18|DIRECT BILL||10
BEFORE_RANGE|MAY(2)!K18|DIRECT BILL||15
BEFORE_RANGE|MAY(2)!L18|DIRECT BILL||25
AFTER_RANGE|MAY(2)!R18|||(blank)
AFTER_RANGE|MAY(2)!S18|EPMI DEAL #502431||0
AFTER_RANGE|MAY(2)!T18|EPMI DEAL #502431||0
AFTER_RANGE|MAY(2)!U18|DIRECT BILL||0
AFTER_RANGE|MAY(2)!V18|DIRECT BILL||0
REF_CELL|MAY(2)!V18|0100|DIRECT BILL||0|fmt=0_);[RED]\(0\)
```


## Error 24: 1_oct2301.XLS / Sheet1!D112

- corpus type: Qualitative /  / Range error
- faulty formula: `=SUM(D5:D107)`
- corpus fix: `=SUM(D5:D109)`

tokens~711 truncated=False unsupported=None

```
TARGET|Sheet1!D112|=SUM(D5:D107)|value=-231.382|fmt=[$-409]#,##0_);\(#,##0\)|bold=0
TARGET_R1C1|=SUM(R[-107]C:R[-5]C)
ROW_PATH|TOTAL > Taxes Payable > Mass Mutual > Reliastar
COL_PATH|SHARES > ENE Vested
SHEET|Sheet1|title=PRE TAX|sheets_in_workbook=2
GRID|row\col|B|C|D|E|F
GRID|110|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|111|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*112|(blank)|=SUM(C53:C65)+C32+C38+C45+C48+C49+C50 -> 21403.6|=SUM(D5:D107) -> -231.382|(blank)|(blank)
GRID|113|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|114|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!D102:D115|||(9 blank cells)
ROW|Sheet1!A112|Taxes Payable||"TOTAL"
ROW|Sheet1!G112|PROFIT/(LOSS)|=SUM(G5:G110)|0
PEERS_ROW|formula_cells=5|same_r1c1=0
PEER_DIFF|Sheet1!C112|=SUM(R[-59]C:R[-47]C)+R[-80]C+R[-74]C+R[-67]C+R[-64]C+R[-63]C+R[-62]C|=SUM(C53:C65)+C32+C38+C45+C48+C49+C50|21403.6
PEER_DIFF|Sheet1!G112|=SUM(R[-107]C:R[-2]C)|=SUM(G5:G110)|0
PEER_DIFF|Sheet1!H112|=SUM(R[-107]C:R[-2]C)|=SUM(H5:H110)|0
PEERS_COL|none
REF_RANGE|Sheet1!D5:D107|cells=103|mixed(pos=8,neg=1)|min=-15000|max=8277|numbers=9|blanks=94
IN_RANGE|Sheet1!D5|Municipal Money Market||(blank)
IN_RANGE|Sheet1!D6|NAT||(blank)
IN_RANGE|Sheet1!D7|||(blank)
IN_RANGE_NOTE|Sheet1!D9|ENE|=C9*1|-15000|formula_among_values,negative
IN_RANGE_NOTE|Sheet1!D32|ENE|=C32*1|265.352|formula_among_values
IN_RANGE_NOTE|Sheet1!D38|ENE|=C38*1|96.793|formula_among_values
IN_RANGE_NOTE|Sheet1!D45|ENE|=C45*1|8277|formula_among_values
IN_RANGE_NOTE|Sheet1!D48|ENE savings|=C48*1|1307.59|formula_among_values
IN_RANGE_NOTE|Sheet1!D49|ENE retirement|=C49*1|178.033|formula_among_values
IN_RANGE_NOTE|Sheet1!D50|ENE special|=C50*1|402.854|formula_among_values
IN_RANGE_NOTE|Sheet1!D62|ENE (100%) 106974 97ECT|=C62*1|2317|formula_among_values
IN_RANGE_OMITTED|87 ordinary cells not shown
IN_RANGE|Sheet1!D103|cash value 8841294||(blank)
IN_RANGE|Sheet1!D104|cash value 8735621||(blank)
IN_RANGE|Sheet1!D105|equity value 7869659||(blank)
IN_RANGE|Sheet1!D106|||(blank)
IN_RANGE|Sheet1!D107|Income Taxes due 2001||(blank)
BEFORE_RANGE|Sheet1!D1|||(blank)
BEFORE_RANGE|Sheet1!D2|||"ENE Vested"
BEFORE_RANGE|Sheet1!D3|SHARES||"SHARES"
BEFORE_RANGE|Sheet1!D4|long||(blank)
AFTER_RANGE|Sheet1!D108|Income Taxes due 2002||(blank)
AFTER_RANGE|Sheet1!D109|Income Taxes due 2003||(blank)
AFTER_RANGE|Sheet1!D110|||(blank)
AFTER_RANGE|Sheet1!D111|||(blank)
AFTER_RANGE|Sheet1!D112|(target cell)
ASSUMPTION|Sheet1!E32|ENE|20.65|used_by=12|fmt=\$#,##0.00
```


## Error 25: 1_SoCalIntCalc.xls / Sheet1 (2)!F94

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=B94`
- corpus fix: `=F91+B94`

tokens~431 truncated=False unsupported=None

```
TARGET|Sheet1 (2)!F94|=B94|value=44931.5|fmt=\$#,##0.00|bold=0
TARGET_R1C1|=RC[-4]
ROW_PATH|Month > Amount
COL_PATH|(none)
SHEET|Sheet1 (2)|title=Amount|sheets_in_workbook=4
UNIT_NOTE|B2=in Dispute
GRID|row\col|D|E|F|G|H
GRID|92|(blank)|=SUM(E4:E91) -> 382763|(blank)|(blank)|=SUM(H86:H91) -> 51696.8
GRID|93|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*94|0.0073|=+C94*D94 -> 16045.4|=B94 -> 44931.5|0.0073|=F94*G94 -> 328
GRID|95|0.0081|=+C95*D95 -> 18205.7|=F94+B95 -> 94555|0.0081|=F95*G95 -> 765.896
GRID|96|0.0074|=+C96*D96 -> 16985.5|=F95+B96 -> 142271|0.0074|=F96*G96 -> 1052.81
COL|Sheet1 (2)!F84|||(blank)
COL|Sheet1 (2)!F85||=SUM(B4:B85)/2|936436
COL|Sheet1 (2)!F86||=F85+B86|981464
COL|Sheet1 (2)!F87||=F86+B87|1.02391e+06
COL|Sheet1 (2)!F88||=F87+B88|1.06771e+06
COL|Sheet1 (2)!F89||=F88+B89|1.1164e+06
COL|Sheet1 (2)!F90||=F89+B90|1.16664e+06
COL|Sheet1 (2)!F91||=F90+B91|1.21663e+06
COL|Sheet1 (2)!F97||=F96+B97|190417
ROW|Sheet1 (2)!C94|(Retro billed March 20, 2001)|=+B94+C91|2.19799e+06
PEERS_ROW|formula_cells=3|same_r1c1=0
PEER_DIFF|Sheet1 (2)!C94|=+RC[-1]+R[-3]C|=+B94+C91|2.19799e+06
PEER_DIFF|Sheet1 (2)!E94|=+RC[-2]*RC[-1]|=+C94*D94|16045.4
PEER_DIFF|Sheet1 (2)!H94|=RC[-2]*RC[-1]|=F94*G94|328
PEERS_COL|formula_cells=15|same_r1c1=0
PEER_DIFF|Sheet1 (2)!F85|=SUM(R[-81]C[-4]:RC[-4])/2|=SUM(B4:B85)/2|936436
PEER_DIFF|Sheet1 (2)!F86|=R[-1]C+RC[-4]|=F85+B86|981464
PEER_DIFF|Sheet1 (2)!F87|=R[-1]C+RC[-4]|=F86+B87|1.02391e+06
REF_CELL|Sheet1 (2)!B94||in Dispute||44931.5|fmt=\$#,##0.00
```


## Error 26: 1_ENA-Cal Dec Liq.xls / Sheet1!C7

- corpus type: Qualitative /  / File reference not working
- faulty formula: `='[3]dec pcs'!$O$576`
- corpus fix: `='[3]dec pcs'!$O$576`

tokens~263 truncated=False unsupported=None

```
TARGET|Sheet1!C7|='[3]dec pcs'!$O$576|value=-672100|fmt=#,##0.00|bold=0
TARGET_R1C1|='[3]dec pcs'!R576C15
ROW_PATH|PCS
COL_PATH|(none)
SHEET|Sheet1|title=(none)|sheets_in_workbook=3
GRID|row\col|A|B|C|D|E
GRID|5|"Dec Liquidations"|(blank)|(blank)|=D4-D3 -> -670108|(blank)
GRID|6|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*7|"PCS"|(blank)|='[3]dec pcs'!$O$576 -> -672100|(blank)|(blank)
GRID|8|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|9|"Rho/Drift"|(blank)|=[2]NP15!$D$37+[2]SP15!$D$37+'[2]MID-COLUMBIA'!$D$37 -> 1992|(blank)|(blank)
COL|Sheet1!C1:C4|||(4 blank cells)
COL|Sheet1!C10|Adjustments from Office of the Chair||0
PEERS_ROW|none
PEERS_COL|formula_cells=2|same_r1c1=0
PEER_DIFF|Sheet1!C9|=[2]NP15!$D$37+[2]SP15!$D$37+'[2]MID-COLUMBIA'!R37C4|=[2]NP15!$D$37+[2]SP15!$D$37+'[2]MID-COLUMBIA'!$D$37|1992
PEER_DIFF|Sheet1!C11|=SUM(R[-4]C:R[-1]C)|=SUM(C7:C10)|-670108
REF|'[3]dec pcs'!$O$576|unresolved_sheet
```


## Error 27: 1_enron corp infomation request - Nov 2001.xls / EGS EXP!W12

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(C12:M12)`
- corpus fix: `=SUM(C12:V12)`

tokens~641 truncated=False unsupported=None

```
TARGET|EGS EXP!W12|=SUM(C12:M12)|value=19.3|fmt=\$#,##0.0|bold=1
TARGET_R1C1|=SUM(RC[-20]:RC[-10])
ROW_PATH|Subtotal
COL_PATH|Total
SHEET|EGS EXP|title=October|sheets_in_workbook=48
GRID|row\col|U|V|W|X|Y
GRID|10|0|0|=SUM(C10:V10) -> 0.1|(blank)|(blank)
GRID|11|0|0|=SUM(C11:V11) -> 4.2|(blank)|(blank)
GRID|*12|=SUM(U2:U11) -> 2.7|=SUM(V2:V11) -> 3.3|=SUM(C12:M12) -> 19.3|(blank)|(blank)
GRID|13|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|14|(blank)|(blank)|(blank)|(blank)|(blank)
COL|EGS EXP!W2|Salaries|=SUM(C2:V2)|24.5
COL|EGS EXP!W3|Benefits|=SUM(C3:V3)|8
COL|EGS EXP!W4|Payroll Taxes|=SUM(C4:V4)|1.7
COL|EGS EXP!W5|Corporate Allocations & Other|=SUM(C5:V5)|0
COL|EGS EXP!W6|Travel|=SUM(C6:V6)|5.1
COL|EGS EXP!W7|Employee-Related Communications|=SUM(C7:V7)|0
COL|EGS EXP!W8|Other Employee Expenses|=SUM(C8:V8)|2.5
COL|EGS EXP!W9|Supplies and Computer Expenses|=SUM(C9:V9)|0.2
COL|EGS EXP!W15|||(blank)
ROW|EGS EXP!T12|October|=SUM(T2:T11)|2.8
PEERS_ROW|formula_cells=8|same_r1c1=0
PEER_DIFF|EGS EXP!O12|=SUM(R[-10]C:R[-1]C)|=SUM(O2:O11)|2.8
PEER_DIFF|EGS EXP!P12|=SUM(R[-10]C:R[-1]C)|=SUM(P2:P11)|3.4
PEER_DIFF|EGS EXP!Q12|=SUM(R[-10]C:R[-1]C)|=SUM(Q2:Q11)|2.8
PEERS_COL|formula_cells=18|same_r1c1=0
PEER_DIFF|EGS EXP!W2|=SUM(RC[-20]:RC[-1])|=SUM(C2:V2)|24.5
PEER_DIFF|EGS EXP!W3|=SUM(RC[-20]:RC[-1])|=SUM(C3:V3)|8
PEER_DIFF|EGS EXP!W4|=SUM(RC[-20]:RC[-1])|=SUM(C4:V4)|1.7
REF_RANGE|EGS EXP!C12:M12|cells=11|all_positive|min=0|max=4.4|numbers=7|blanks=4
IN_RANGE|EGS EXP!C12|October|=SUM(C2:C11)|2.4
IN_RANGE|EGS EXP!D12||=SUM(D2:D11)|0
IN_RANGE|EGS EXP!E12|November|=SUM(E2:E11)|3
IN_RANGE_NOTE|EGS EXP!F12|||(blank)|blank
IN_RANGE_NOTE|EGS EXP!G12|December|=SUM(G2:G11)|2.6|bold
IN_RANGE_NOTE|EGS EXP!H12|||(blank)|blank
IN_RANGE|EGS EXP!I12|January|=SUM(I2:I11)|3.5
IN_RANGE|EGS EXP!J12|||(blank)
IN_RANGE|EGS EXP!K12|February|=SUM(K2:K11)|3.4
IN_RANGE|EGS EXP!L12|||(blank)
IN_RANGE|EGS EXP!M12|March|=SUM(M2:M11)|4.4
BEFORE_RANGE|EGS EXP!A12|Other||"Subtotal"
BEFORE_RANGE|EGS EXP!B12|||(blank)
AFTER_RANGE|EGS EXP!N12|April|=SUM(N2:N11)|2.8
AFTER_RANGE|EGS EXP!O12|May|=SUM(O2:O11)|2.8
AFTER_RANGE|EGS EXP!P12|June|=SUM(P2:P11)|3.4
AFTER_RANGE|EGS EXP!Q12|July|=SUM(Q2:Q11)|2.8
AFTER_RANGE|EGS EXP!R12|August|=SUM(R2:R11)|2.8
```


## Error 28: 1_CA rate exposure final 8-28 rev.xls / New!C10:E14; H10:J14; M10:O14; C25:E29; etc.

- corpus type: Quantitative / Omission / Wrong calculation
- faulty formula: `=$B10*C$6*C$7`
- corpus fix: `=$B10*C$6*C$7*C$8`

tokens~837 truncated=False unsupported=None

```
TARGET|New!C10|=$B10*C$6*C$7|value=0.0152792|fmt=\$#,##0.0000_);[RED]"($"#,##0.0000\)|bold=0
TARGET_R1C1|=RC2*R6C*R7C
ROW_PATH|Amortization (years) > Scenario > PG&E > NEW CUSTOMERS (DA for first time as of 10/1/01)
COL_PATH|A > Utility Undercollection
SHEET|New|title=NEW CUSTOMERS (DA for first time as of 10/1/01)|sheets_in_workbook=4
UNIT_NOTE|B6=% Collected
UNIT_NOTE|G6=% Collected
UNIT_NOTE|L6=% Collected
GRID|row\col|A|B|C|D|E
GRID|8|(blank)|"Factor"|1|1|0
GRID|9|"Amortization (years)"|(blank)|(blank)|(blank)|(blank)
GRID|*10|5|=-PMT(Assumptions!$B$21,$A10,Assumptions!$B$33)/Assumptions!$B$5*1000000 -> 0.0201042|=$B10*C$6*C$7 -> 0.0152792|=$B10*D$6*D$7 -> 0|=$B10*E$6*E$7 -> 0.000804169
GRID|11|7|=-PMT(Assumptions!$B$21,$A11,Assumptions!$B$33)/Assumptions!$B$5*1000000 -> 0.0152219|=$B11*C$6*C$7 -> 0.0115687|=$B11*D$6*D$7 -> 0|=$B11*E$6*E$7 -> 0.000608876
GRID|12|10|=-PMT(Assumptions!$B$21,$A12,Assumptions!$B$33)/Assumptions!$B$5*1000000 -> 0.011601|=$B12*C$6*C$7 -> 0.00881676|=$B12*D$6*D$7 -> 0|=$B12*E$6*E$7 -> 0.00046404
COL|New!C1:C2|||(2 blank cells)
COL|New!B3|Utility Undercollection||"Utility Undercollection"
COL|New!C4|Scenario||"A"
COL|New!C5|||(blank)
COL|New!C6|% Collected|=Description!$I$21|0.8
COL|New!C7|Probability|=Description!$I$25|0.95
COL|New!C13||=$B13*C$6*C$7|0.00776356
ROW|New!F10|Average|=SUM(C10:E10)|0.0160834
ROW|New!G10|Probability|=-PMT(Assumptions!$B$19,$A10,Assumptions!$C$26)/Assumptions!$B$5*1000000|0.0179058
ROW|New!H10|A|=$G10*H$6*H$7|0.00358115
PEERS_ROW|formula_cells=9|same_r1c1=2
PEER_DIFF|New!B10|=-PMT(Assumptions!R21C2,RC1,Assumptions!R33C2)/Assumptions!R5C2*1000000|=-PMT(Assumptions!$B$21,$A10,Assumptions!$B$33)/Assumptions!$B$5*1000000|0.0201042
PEER_DIFF|New!F10|=SUM(RC[-3]:RC[-1])|=SUM(C10:E10)|0.0160834
PEER_DIFF|New!G10|=-PMT(Assumptions!R19C2,RC1,Assumptions!R26C3)/Assumptions!R5C2*1000000|=-PMT(Assumptions!$B$19,$A10,Assumptions!$C$26)/Assumptions!$B$5*1000000|0.0179058
PEERS_COL|formula_cells=9|same_r1c1=4
PEER_DIFF|New!C6|=Description!R21C9|=Description!$I$21|0.8
PEER_DIFF|New!C7|=Description!R25C9|=Description!$I$25|0.95
PEER_DIFF|New!C21|=Description!R22C9|=Description!$I$22|0.8
REF_CELL|New!B10||Factor|=-PMT(Assumptions!$B$21,$A10,Assumptions!$B$33)/Assumptions!$B$5*1000000|0.0201042|fmt=\$#,##0.0000_);[RED]"($"#,##0.0000\)
REF_CELL|New!C6|% Collected|A|=Description!$I$21|0.8|fmt=0%
REF_CELL|New!C7|Probability|A|=Description!$I$25|0.95|fmt=0%
ASSUMPTION|New!C8|Factor|1|used_by=7|fmt=General
ASSUMPTION|New!D8|Factor|1|used_by=7|fmt=General
ASSUMPTION|New!E8|Factor|0|used_by=7|fmt=General
ASSUMPTION|New!H8|Factor|1|used_by=5|fmt=General
ASSUMPTION|New!I8|Factor|1|used_by=5|fmt=General
ASSUMPTION|New!J8|Factor|0|used_by=5|fmt=General
ASSUMPTION|New!M8|Factor|1|used_by=5|fmt=General
ASSUMPTION|New!N8|Factor|1|used_by=5|fmt=General
ASSUMPTION|New!O8|Factor|0|used_by=5|fmt=General
ASSUMPTION|New!H23|Factor|1|used_by=5|fmt=General
```


## Error 29: 1_Ogleth200103.xls / external!D11:D35

- corpus type: Quantitative / Logical / Wrong calculation
- faulty formula: `=ROUND(+C11*(1-0.019),0)`
- corpus fix: `=C11*0.9811`

tokens~400 truncated=False unsupported=None

```
TARGET|external!D11|=ROUND(+C11*(1-0.019),0)|value=1472|fmt=0|bold=0
TARGET_R1C1|=ROUND(+RC[-1]*(1-0.019),0)
ROW_PATH|DAY > DAY AHEAD > GAS VOLUMES > March 2001
COL_PATH|DELIVERY > PURCHASES > GAS VOLUMES
SHEET|external|title=DOYLE|sheets_in_workbook=1
GRID|row\col|B|C|D|E|F
GRID|9|0|0|=C9*0.981 -> 0|=+E8 -> 0|=(D9-E9)+F8 -> 0
GRID|10|0|1500|=ROUND(+C10*(1-0.019),0) -> 1472|=+E9 -> 0|=(D10-E10)+F9 -> 1472
GRID|*11|0|1500|=ROUND(+C11*(1-0.019),0) -> 1472|=+E10 -> 0|=(D11-E11)+F10 -> 2944
GRID|12|0|1500|=ROUND(+C12*(1-0.019),0) -> 1472|=3025+1472 -> 4497|=(D12-E12)+F11 -> -81
GRID|13|0|0|=ROUND(+C13*(1-0.019),0) -> 0|2617|=(D13-E13)+F12 -> -2698
COL|external!D1:D3|||(3 blank cells)
COL|external!B4|GAS VOLUMES||"GAS VOLUMES"
COL|external!C5|PURCHASES||"PURCHASES"
COL|external!D6|RECEIPT||"DELIVERY"
COL|external!D7|||(blank)
COL|external!D8||=C8*0.981|0
COL|external!D14||=ROUND(+C14*(1-0.019),0)|0
ROW|external!A11|DAY|=+A10+1|2001-03-04 00:00:00
ROW|external!H11|GD Sta 85 + .05|=5.125+0.05|5.175
PEERS_ROW|formula_cells=6|same_r1c1=0
PEER_DIFF|external!A11|=+R[-1]C+1|=+A10+1|2001-03-04 00:00:00
PEER_DIFF|external!E11|=+R[-1]C|=+E10|0
PEER_DIFF|external!F11|=(RC[-2]-RC[-1])+R[-1]C|=(D11-E11)+F10|2944
PEERS_COL|formula_cells=18|same_r1c1=16
PEER_DIFF|external!D8|=RC[-1]*0.981|=C8*0.981|0
PEER_DIFF|external!D9|=RC[-1]*0.981|=C9*0.981|0
REF_CELL|external!C11||RECEIPT||1500|fmt=General
```


## Error 30: 1_Ogleth200103.xls / external!E36:E37

- corpus type: Qualitative /  / Wrong reference
- faulty formula: `=+E34`
- corpus fix: `=+E35`

tokens~359 truncated=False unsupported=None

```
TARGET|external!E36|=+E34|value=0|fmt=General|bold=0
TARGET_R1C1|=+R[-2]C
ROW_PATH|DAY > DAY AHEAD > GAS VOLUMES > March 2001
COL_PATH|BURN > GAS VOLUMES
SHEET|external|title=DOYLE|sheets_in_workbook=1
GRID|row\col|C|D|E|F|G
GRID|34|0|=ROUND(+C34*(1-0.019),0) -> 0|=+E33 -> 0|=(D34-E34)+F33 -> -2698|(blank)
GRID|35|0|=ROUND(+C35*(1-0.019),0) -> 0|=+E34 -> 0|=(D35-E35)+F34 -> -2698|(blank)
GRID|*36|0|0|=+E34 -> 0|=(D36-E36)+F34 -> -2698|(blank)
GRID|37|0|0|=+E35 -> 0|=(D37-E37)+F35 -> -2698|(blank)
GRID|38|0|=C38*0.981 -> 0|=+E37 -> 0|=(D38-E38)+F37 -> -2698|(blank)
COL|external!E26||=+E25|0
COL|external!E27||=+E26|0
COL|external!E28||=+E27|0
COL|external!E29||=+E28|0
COL|external!E30||=+E29|0
COL|external!E31||=+E30|0
COL|external!E32||=+E31|0
COL|external!E33||=+E32|0
COL|external!E39|||(blank)
ROW|external!B36|REQUEST||0
PEERS_ROW|formula_cells=5|same_r1c1=0
PEER_DIFF|external!A36|=+R[-1]C+1|=+A35+1|2001-03-29 00:00:00
PEER_DIFF|external!F36|=(RC[-2]-RC[-1])+R[-2]C|=(D36-E36)+F34|-2698
PEER_DIFF|external!J36|=+R[-1]C|=+J35|0.0304
PEERS_COL|formula_cells=18|same_r1c1=1
PEER_DIFF|external!E21|=+R[-1]C|=+E20|0
PEER_DIFF|external!E22|=+R[-1]C|=+E21|0
PEER_DIFF|external!E23|=+R[-1]C|=+E22|0
REF_CELL|external!E34||BURN|=+E33|0|fmt=General
```


## Error 31: 2_yr 2001 Commissioning Summary 2-26-02.xls / Mar 2002!I132

- corpus type: Qualitative /  / Fixed Value
- faulty formula: `1`
- corpus fix: `=IF(E132>0,1,0)`

_target cell has no formula or sheet not found_


## Error 32: 1_ENA_PGE_JUNE_1_2002.xls / JD-MAL OR CPTJK TRANS!H12:H17; H34:H35

- corpus type: Qualitative /  / Range error
- faulty formula: `=SUM(B12:F12)`
- corpus fix: `(unfixed by authors)`

tokens~519 truncated=False unsupported=None

```
TARGET|JD-MAL OR CPTJK TRANS!H12|=SUM(B12:F12)|value=0|fmt=General|bold=0
TARGET_R1C1|=SUM(RC[-6]:RC[-2])
ROW_PATH|0100 > (PPT) > Time > Pacific Prevailing
COL_PATH|Total In To PGE Trans > TRANSMISSION CAPACITY USED > TOTAL
SHEET|JD-MAL OR CPTJK TRANS|title=From:|sheets_in_workbook=5
GRID|row\col|F|G|H|I|J
GRID|10|(blank)|(blank)|"Total In To PGE Trans"|(blank)|(blank)
GRID|11|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*12|0|0|=SUM(B12:F12) -> 0|(blank)|(blank)
GRID|13|0|0|=SUM(B13:F13) -> 0|(blank)|(blank)
GRID|14|0|0|=SUM(B14:F14) -> 0|(blank)|(blank)
COL|JD-MAL OR CPTJK TRANS!H2:H6|||(5 blank cells)
COL|JD-MAL OR CPTJK TRANS!H7|PGE TRANNY||"TOTAL"
COL|JD-MAL OR CPTJK TRANS!H8|||(blank)
COL|JD-MAL OR CPTJK TRANS!H9|NOT FOR TOM, ET AL||"TRANSMISSION CAPACITY USED"
COL|JD-MAL OR CPTJK TRANS!H15|0400|=SUM(B15:F15)|0
PEERS_ROW|none
PEERS_COL|formula_cells=15|same_r1c1=5
PEER_DIFF|JD-MAL OR CPTJK TRANS!H18|=SUM(RC[-6]:RC[-1])|=SUM(B18:G18)|150
PEER_DIFF|JD-MAL OR CPTJK TRANS!H19|=SUM(RC[-6]:RC[-1])|=SUM(B19:G19)|150
PEER_DIFF|JD-MAL OR CPTJK TRANS!H20|=SUM(RC[-6]:RC[-1])|=SUM(B20:G20)|150
REF_RANGE|JD-MAL OR CPTJK TRANS!B12:F12|cells=5|all_positive|min=0|max=0|numbers=1|blanks=4
IN_RANGE|JD-MAL OR CPTJK TRANS!B12|NOT FOR TOM, ET AL||(blank)
IN_RANGE|JD-MAL OR CPTJK TRANS!C12|NOT FOR TOM, ET AL||(blank)
IN_RANGE|JD-MAL OR CPTJK TRANS!D12|NOT FOR TOM, ET AL||(blank)
IN_RANGE|JD-MAL OR CPTJK TRANS!E12|NOT FOR TOM, ET AL||(blank)
IN_RANGE|JD-MAL OR CPTJK TRANS!F12|NOT FOR TOM, ET AL||0
BEFORE_RANGE|JD-MAL OR CPTJK TRANS!A12|(PPT)||"0100"
AFTER_RANGE|JD-MAL OR CPTJK TRANS!G12|NOT FOR TOM, ET AL||0
AFTER_RANGE|JD-MAL OR CPTJK TRANS!H12|(target cell)
AFTER_RANGE|JD-MAL OR CPTJK TRANS!I12|||(blank)
AFTER_RANGE|JD-MAL OR CPTJK TRANS!J12|||(blank)
AFTER_RANGE|JD-MAL OR CPTJK TRANS!K12|||(blank)
```


## Error 33: 1_Southpoint Gas Model.xls / Sheet1!I25:I31

- corpus type: Quantitative / Mechanical / Wrong reference
- faulty formula: `=G24*H25`
- corpus fix: `=G25*H25`

tokens~326 truncated=False unsupported=None

```
TARGET|Sheet1!I25|=G24*H25|value=3395|fmt=_(* #,##0_);_(* \(#,##0\);_(* \-??_);_(@_)|bold=0
TARGET_R1C1|=R[-1]C[-2]*RC[-1]
ROW_PATH|he23 > Southpoint
COL_PATH|Total Gas Usage
SHEET|Sheet1|title=Southpoint|sheets_in_workbook=3
UNIT_NOTE|G6=Total MW
GRID|row\col|G|H|I|J|K
GRID|23|485|7|=G23*H23 -> 3395|(blank)|(blank)
GRID|24|485|7|=G24*H24 -> 3395|(blank)|(blank)
GRID|*25|470|7|=G24*H25 -> 3395|(blank)|(blank)
GRID|26|470|7|=G25*H26 -> 3290|(blank)|(blank)
GRID|27|215|7|=G26*H27 -> 3290|(blank)|(blank)
COL|Sheet1!I15|he13|=G15*H15|3395
COL|Sheet1!I16|he14|=G16*H16|3395
COL|Sheet1!I17|he15|=G17*H17|3395
COL|Sheet1!I18|he16|=G18*H18|3395
COL|Sheet1!I19|he17|=G19*H19|3395
COL|Sheet1!I20|he18|=G20*H20|3395
COL|Sheet1!I21|he19|=G21*H21|3395
COL|Sheet1!I22|he20|=G22*H22|3395
COL|Sheet1!I28|he2|=G27*H28|1505
ROW|Sheet1!F25|Steam TurB||0
PEERS_ROW|none
PEERS_COL|formula_cells=22|same_r1c1=6
PEER_DIFF|Sheet1!I10|=RC[-2]*RC[-1]|=G10*H10|3395
PEER_DIFF|Sheet1!I11|=RC[-2]*RC[-1]|=G11*H11|3395
PEER_DIFF|Sheet1!I12|=RC[-2]*RC[-1]|=G12*H12|3395
REF_CELL|Sheet1!G24|he22|Total MW||485|fmt=General
REF_CELL|Sheet1!H25|he23|HR||7|fmt=General
```


## Error 34: 1_Southpoint Gas Model.xls / Sheet1!G33; I34

- corpus type: Qualitative /  / Range error
- faulty formula: `=SUM(G8:G32)`
- corpus fix: `(unfixed by authors)`

tokens~422 truncated=False unsupported=None

```
TARGET|Sheet1!G33|=SUM(G8:G32)|value=10245|fmt=General|bold=0
TARGET_R1C1|=SUM(R[-25]C:R[-1]C)
ROW_PATH|Southpoint
COL_PATH|Total MW
SHEET|Sheet1|title=Southpoint|sheets_in_workbook=3
UNIT_NOTE|G6=Total MW
GRID|row\col|E|F|G|H|I
GRID|31|0|0|215|7|=G30*H31 -> 1505
GRID|32|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*33|(blank)|(blank)|=SUM(G8:G32) -> 10245|(blank)|(blank)
GRID|34|(blank)|(blank)|(blank)|(blank)|=SUM(I9:I33) -> 70315
GRID|35|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!G23|he21||485
COL|Sheet1!G24|he22||485
COL|Sheet1!G25|he23||470
COL|Sheet1!G26|he24||470
COL|Sheet1!G27|he1||215
COL|Sheet1!G28|he2||215
COL|Sheet1!G29|he3||215
COL|Sheet1!G30|he4||215
COL|Sheet1!G36|||(blank)
PEERS_ROW|none
PEERS_COL|none
REF_RANGE|Sheet1!G8:G32|cells=25|all_positive|min=215|max=485|numbers=24|blanks=1
IN_RANGE|Sheet1!G8|he 6||470
IN_RANGE|Sheet1!G9|he 7||485
IN_RANGE|Sheet1!G10|he8||485
IN_RANGE_OMITTED|17 ordinary cells not shown
IN_RANGE|Sheet1!G28|he2||215
IN_RANGE|Sheet1!G29|he3||215
IN_RANGE|Sheet1!G30|he4||215
IN_RANGE|Sheet1!G31|he5||215
IN_RANGE|Sheet1!G32|||(blank)
BEFORE_RANGE|Sheet1!G3|SoCal Gas Price||(blank)
BEFORE_RANGE|Sheet1!G4|San Juan Gas Price||(blank)
BEFORE_RANGE|Sheet1!G5|||(blank)
BEFORE_RANGE|Sheet1!G6|Steam TurB||"Total MW"
BEFORE_RANGE|Sheet1!G7|||(blank)
AFTER_RANGE|Sheet1!G33|(target cell)
AFTER_RANGE|Sheet1!G34|||(blank)
AFTER_RANGE|Sheet1!G35|||(blank)
AFTER_RANGE|Sheet1!G36|||(blank)
AFTER_RANGE|Sheet1!G37|||(blank)
```


## Error 35: 1_EI365reveff060800.xls / Sheet1!F8

- corpus type: Qualitative /  / Formula: = SUM(D8*E8)
- faulty formula: `=SUM(D8*E8)`
- corpus fix: `(unfixed by authors)`

tokens~275 truncated=False unsupported=None

```
TARGET|Sheet1!F8|=SUM(D8*E8)|value=28.6677|fmt=0|bold=0
TARGET_R1C1|=SUM(RC[-2]*RC[-1])
ROW_PATH|011220 > EI 365 > CTP NAME > Subject: Revised Availabilities Effective 6/8/00
COL_PATH|PVR Volume
SHEET|Sheet1|title=(none)|sheets_in_workbook=3
UNIT_NOTE|D7=Gross Vol. (MMBtu/d)
UNIT_NOTE|E7=PVR %
UNIT_NOTE|G7=Avail. After PVR (MMBtu/d)
GRID|row\col|D|E|F|G|H
GRID|6|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|7|"Gross Vol. (MMBtu/d)"|"PVR %"|"PVR Volume"|"Avail. After PVR (MMBtu/d)"|(blank)
GRID|*8|1334|0.02149|=SUM(D8*E8) -> 28.6677|=SUM(D8-F8) -> 1305.33|(blank)
GRID|9|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|10|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Sheet1!F1:F11|||(6 blank cells)
ROW|Sheet1!C8|Meter #||"011220"
PEERS_ROW|formula_cells=1|same_r1c1=0
PEER_DIFF|Sheet1!G8|=SUM(RC[-3]-RC[-1])|=SUM(D8-F8)|1305.33
PEERS_COL|none
REF_CELL|Sheet1!D8|011220|Gross Vol. (MMBtu/d)||1334|fmt=General
REF_CELL|Sheet1!E8|011220|PVR %||0.02149|fmt=General
```


## Error 36: 1_Global Hot List 1207.xls / Hotlist - Identified!M22; M37

- corpus type: Quantitative / Mechanical / Range error
- faulty formula: `=SUM(M21:M21)`
- corpus fix: `=SUM(I13:I21)`

tokens~391 truncated=False unsupported=None

```
TARGET|Hotlist - Identified !M22|=SUM(M21:M21)|value=0|fmt=_(\$* #,##0_);_(\$* \(#,##0\);_(\$* \-??_);_(@_)|bold=1
TARGET_R1C1|=SUM(R[-1]C:R[-1]C)
ROW_PATH|SUBTOTAL > SUBTOTAL > Deal > %
COL_PATH|Value > Second Quarter 2001
SHEET|Hotlist - Identified |title=(none)|sheets_in_workbook=2
UNIT_NOTE|D6=%
UNIT_NOTE|H6=%
UNIT_NOTE|L6=%
GRID|row\col|K|L|M|N|O
GRID|20|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|21|(blank)|(blank)|(blank)|(blank)|(blank)
GRID|*22|"SUBTOTAL"|(blank)|=SUM(M21:M21) -> 0|(blank)|"SUBTOTAL"
GRID|23|"Deal"|(blank)|"Value"|=COUNTA(K24:K27) -> 0|"Deal"
GRID|24|(blank)|(blank)|(blank)|(blank)|(blank)
COL|Hotlist - Identified !M12|Deal||"Value"
COL|Hotlist - Identified !M13|M&G - UK||1000
COL|Hotlist - Identified !M14:M25|||(7 blank cells)
PEERS_ROW|formula_cells=4|same_r1c1=0
PEER_DIFF|Hotlist - Identified !E22|=SUM(R[-9]C:R[-1]C)|=SUM(E13:E21)|62750
PEER_DIFF|Hotlist - Identified !I22|=SUM(R[-9]C:R[-1]C)|=SUM(I13:I21)|15000
PEER_DIFF|Hotlist - Identified !Q22|=SUM(R[-9]C:R[-1]C)|=SUM(Q13:Q21)|0
PEERS_COL|formula_cells=3|same_r1c1=0
PEER_DIFF|Hotlist - Identified !M11|=SUM(R[-4]C:R[-1]C)|=SUM(M7:M10)|2000
PEER_DIFF|Hotlist - Identified !M28|=SUM(R[-4]C:R[-1]C)|=SUM(M24:M27)|0
PEER_DIFF|Hotlist - Identified !M37|=SUM(R[-5]C:R[-1]C)|=SUM(M32:M36)|0
REF_CELL|Hotlist - Identified !M21|Origination & Finance|Value||(blank)|fmt=General
```
