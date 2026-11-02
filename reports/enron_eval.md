# Held-out evaluation

| metric | value |
|---|---|
| errors | 32 |
| covered | 29 |
| found | 6 |
| missed | 23 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 2817 |
| flagged_windows | 77 |
| false_alarm_windows | 71 |
| recall_covered | 0.207 |
| recall_all | 0.188 |
| precision_windows | 0.078 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | sheet1 | F28, G28 | Range error | missed |  |  |  |
| 2 | 2 | sheet1 | I34 | Range error | found | skipped_rows | yes | The SUM range stops short: he 6 belong to the same block but are left out. |
| 3 | 3 | bmspt066 | W43 | Range error | found | skipped_rows |  | The SUM range stops short: Estimated, Estimated, Estimated, Estimated, Projected belong to the same block but are left out. |
| 4 | 3 | bmspt066 | C43, D43, E43, F43, G43, H43, I43, J43,  | Range error | missed |  |  |  |
| 5 | 4 | sheet1 | L16 | Range error | missed |  |  |  |
| 6 | 5 | jul01 | AL44 | Range error | missed |  |  |  |
| 7 | 6 | real time | V23 | Range error | missed |  |  |  |
| 8 | 7 | deals | AD142 | Range error | missed |  |  |  |
| 9 | 8 | cost estimate summary | L23 | Range error | found | skipped_rows | yes | The SUM range stops short: Gallup CS Mods belong to the same block but are left out. |
| 10 | 9 | oct 01 | T39 | Wrong formula | missed |  |  |  |
| 11 | 10 | epsundevil | F10 | Wrong reference | missed |  |  |  |
| 12 | 11 | data | D13 | Wrong calculation | missed |  |  |  |
| 13 | 12 | curves | V10, V100, V101, V102, V103, V104, V105, | Wrong calculation | missed |  |  |  |
| 14 | 13 | sheet1 | H33 | Wrong calculation | found | wrong_sign |  | "Unusual loss from litigation associated with consumer class" (H32) is subtracted here but should be added. |
| 15 | 13 | sheet1 | I35 | Wrong calculation | missed |  |  |  |
| 16 | 13 | sheet1 | I38 | Wrong calculation | missed |  |  |  |
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | missed |  |  |  |
| 22 | 18 | crack spread option | M10, M11, M12, M13, M14, M9 | Wrong calculation | not_covered |  |  |  |
| 23 | 19 | may(2) | AE18, AE19, AE20, AE21, AE22, AE23, AE24 | Range error | missed |  |  |  |
| 24 | 20 | sheet1 | D112 | Range error | missed |  |  |  |
| 25 | 21 | sheet1 (2) | F94 | Wrong calculation | missed |  |  |  |
| 26 | 22 | sheet1 | C7 | File reference not working | missed |  |  |  |
| 27 | 23 | egs exp | W12 | Range error | found | skipped_rows | yes | The SUM range stops short: April, May, June, July, August belong to the same block but are left out. |
| 28 | 24 | new | C10, C11, C12, C13, C14, C25, C26, C27,  | Wrong calculation | missed |  |  |  |
| 29 | 25 | external | D11, D12, D13, D14, D15, D16, D17, D18,  | Wrong calculation | not_covered |  |  |  |
| 30 | 25 | external | E36, E37 | Wrong reference | missed |  |  |  |
| 31 | 26 | mar 2002 | I132 | Fixed Value | not_covered |  |  |  |
| 32 | 27 | jd-mal or cptjk trans | H12, H13, H14, H15, H16, H17, H34, H35 | Range error | missed |  |  |  |
| 33 | 28 | sheet1 | I25, I26, I27, I28, I29, I30, I31 | Wrong reference | missed |  |  |  |
| 34 | 28 | sheet1 | G33, I34 | Range error | found | skipped_rows |  | The SUM range stops short: he 6 belong to the same block but are left out. |
| 35 | 29 | sheet1 | F8 | Formula: = SUM(D8*E8) | missed |  |  |  |
| 36 | 30 | hotlist - identified | M22, M37 | Range error | missed |  |  |  |

## By category

| category | found | missed | unsupported | not covered |
|---|---|---|---|---|
| File reference not working | 0 | 1 | 0 | 0 |
| Fixed Value | 0 | 0 | 0 | 1 |
| Formula: = SUM(D8*E8) | 0 | 1 | 0 | 0 |
| Range error | 5 | 10 | 0 | 0 |
| Wrong calculation | 1 | 7 | 0 | 2 |
| Wrong formula | 0 | 1 | 0 | 0 |
| Wrong reference | 0 | 3 | 0 | 0 |

## False alarms (71)

| id | formula | type | reason |
|---|---|---|---|
| 5:jul01!AS44 | `=AL44+AN44-AQ44` | wrong_sign | "TOTAL" (AQ44) is subtracted here but should be added. |
| 5:jul01!L45 | `=AVERAGE(L12:L42)` | wrong_function | "Invoice Calculation" calls for SUM, but the formula uses AVERAGE. |
| 6:Real Time!J26 | `=J23+J15` | wrong_sign | "Sr. Specialist" (J15) is added here but should be subtracted. |
| 6:Real Time!Q31 | `=+N31-P31` | wrong_sign | "Total 2002 Salaries Post Merit" (P31) is subtracted here but should be added. |
| 7:Preschedule!AA58 | `=SUM(AA41:AA55)` | skipped_rows | The SUM range stops short: 4 CORNERS UNIT 4, 4 CORNERS UNIT 5 belong to the same block but are left out. |
| 7:Preschedule!B80 | `=Deals!AD160` | wrong_sign | "Total Volume" (Deals!AD160) is subtracted here but should be added. |
| 7:Preschedule!Z91 | `=Z89-Z90` | wrong_sign | "Total Costs:" (Z89) is subtracted here but should be added. |
| 7:Preschedule!Z94 | `=Z92-Z93` | wrong_sign | "Total Costs:" (Z92) is subtracted here but should be added. |
| 7:Preschedule!Z97 | `=Z95-Z96` | wrong_sign | "Total Costs:" (Z95) is subtracted here but should be added. |
| 7:Preschedule!Z100 | `=Z98-Z99` | wrong_sign | "Total Costs:" (Z98) is subtracted here but should be added. |
| 7:Preschedule!Z103 | `=Z101-Z102` | wrong_sign | "Total Costs:" (Z101) is subtracted here but should be added. |
| 7:Preschedule!Z108 | `=Z105-Z107` | wrong_sign | "Total Costs:" (Z105) is subtracted here but should be added. |
| 7:Preschedule!Z113 | `=Z110-Z112` | wrong_sign | "Total Costs:" (Z110) is subtracted here but should be added. |
| 7:Preschedule!Z118 | `=Z115-Z117` | wrong_sign | "Total Costs:" (Z115) is subtracted here but should be added. |
| 7:Preschedule!Z123 | `=Z120-Z122` | wrong_sign | "Total Costs:" (Z120) is subtracted here but should be added. |
| 7:Preschedule!Z128 | `=Z125-Z127` | wrong_sign | "Total Costs:" (Z127) is subtracted here but should be added. |
| 7:Preschedule!Z133 | `=Z130-Z132` | wrong_sign | "Total Costs:" (Z130) is subtracted here but should be added. |
| 7:Preschedule!Z138 | `=Z135-Z137` | wrong_sign | "Total Costs:" (Z137) is subtracted here but should be added. |
| 7:Preschedule!Z143 | `=Z140-Z142` | wrong_sign | "Total Costs:" (Z140) is subtracted here but should be added. |
| 7:Preschedule!Z148 | `=Z145-Z147` | wrong_sign | "Total Costs:" (Z147) is subtracted here but should be added. |
| 7:Preschedule!Z153 | `=Z150-Z152` | wrong_sign | "Total Costs:" (Z150) is subtracted here but should be added. |
| 7:Preschedule!Z158 | `=Z155-Z157` | wrong_sign | "Total Costs:" (Z155) is subtracted here but should be added. |
| 7:Preschedule!Z163 | `=Z160-Z162` | wrong_sign | "Total Costs:" (Z160) is added here but should be subtracted. |
| 7:Preschedule!Z169 | `=Z166+Z167` | wrong_sign | "Net Position after sales (taken from row 53)" (Z167) is added here but should be subtracted. |
| 7:Fuel!F18 | `=C18*G7+D18*G6` | wrong_sign | "Copper" (D18) is added here but should be subtracted. |
| 7:Economics!D47 | `=SUM(D5:D45,B3)` | double_count | "SPS Avg. Cost Est." (B3) is already inside the summed range and is added again. |
| 11:Data!F51 | `=C5+D5` | wrong_sign | "Swap amount" (D5) is added here but should be subtracted. |
| 11:Data!B52 | `=B51-B36` | wrong_sign | "tot volume" (B36) is subtracted here but should be added. |
| 12:Summary!F8 | `=F6+F7` | wrong_sign | "Total Payables as of Jan 25, 2002" (F7) is added here but should be subtracted. |
| 12:Summary!F18 | `=F14` | skipped_rows | The SUM range stops short: IF CIG Rocky Mtns. index minus $0.03 belong to the same block but are left out. |
| 13:Sheet1!H19 | `=H17-H18` | wrong_sign | "Less income tax credits" (H18) is subtracted here but should be added. |
| 20:Sheet1!M112 | `=SUM(K45:K65)+K32+K38` | double_count | "ENE" (K38) is already inside the summed range and is added again. |
| 20:Sheet1!M143 | `=SUM(K116:K138)+K112` | skipped_rows | The SUM range stops short: ENE 1/18/07 (0%) 122617, ENE 1/18/07 (0%) 135367, ENE (0%) 2000 LTIP 151261, ENE 8/1/05 (0%) 149389, ENE 12/29/07 (0%) 160388 belong to the same block but are left out. |
| 21:Sheet1!C94 | `=+B94+C91` | wrong_sign | "in Dispute" (B94) is added here but should be subtracted. |
| 21:Sheet1!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short: & No Interest belong to the same block but are left out. |
| 21:Sheet1!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 21:Sheet1 (2)!C94 | `=+B94+C91` | wrong_sign | "by Month" (C91) is added here but should be subtracted. |
| 21:Sheet1 (2)!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short: & No Interest belong to the same block but are left out. |
| 21:Sheet1 (2)!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 22:Sheet1!D5 | `=D4-D3` | wrong_sign | "LTD Liquidations as of 11/30" (D3) is subtracted here but should be added. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: 'ENA IS'!C21 belong to the same block but are left out. |
| 23:EGS OFF BS!G18 | `=G17+B10` | wrong_sign | "Recall of debt by Hong Kong bank" (B10) is added here but should be subtracted. |
| 23:ENW OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 26:Nov 2001!I30 | `=SUM(I10:I29)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I186 | `=SUM(I180:I185)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!L195 | `=16-L194` | wrong_sign | "Turbines 6, 7 & 8 Previously commissioned on 9/27" (L194) is subtracted here but should be added. |
| 26:Nov 2001!I207 | `=SUM(I191:I206)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I229 | `=SUM(I212:I228)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I324 | `=SUM(I234:I323)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G45 | `=SUM(G25:G44)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G201 | `=SUM(G195:G200)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J208 | `=COUNT(C206:C221)` | wrong_function | "December" calls for SUM, but the formula uses COUNT. |
| 26:Dec 2001!J210 | `=16-J209` | wrong_sign | "Turbines 6, 7 & 8 Previously commissioned on 9/27" (J209) is subtracted here but should be added. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I30 | `=SUM(I10:I29)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I186 | `=SUM(I180:I185)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!L195 | `=16-L194` | wrong_sign | "Turbines 6, 7 & 8 Previously commissioned on 9/27" (L194) is subtracted here but should be added. |
| 26:Jan 2002!I207 | `=SUM(I191:I206)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I229 | `=SUM(I212:I228)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I324 | `=SUM(I234:I323)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!I174 | `=SUM(I154:I173)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!L183 | `=L182-6` | wrong_sign | "Turbines 6, 7 & 8 Previously commissioned on 9/27" (L182) is subtracted here but should be added. |
| 26:Feb 2002!L194 | `=16-L193` | wrong_sign | "Turbines 6, 7 & 8 Previously commissioned on 9/27" (L193) is subtracted here but should be added. |
| 26:Feb 2002!I228 | `=SUM(I211:I227)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Mar 2002!I29 | `=SUM(I9:I28)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
