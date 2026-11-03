# Held-out evaluation

| metric | value |
|---|---|
| errors | 32 |
| covered | 29 |
| found | 18 |
| missed | 11 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 2817 |
| flagged_windows | 99 |
| false_alarm_windows | 76 |
| recall_covered | 0.621 |
| recall_all | 0.562 |
| precision_windows | 0.232 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | sheet1 | F28, G28 | Range error | found | skipped_rows | yes | The SUM range stops short: Enron belong to the same block but are left out. |
| 2 | 2 | sheet1 | I34 | Range error | found | skipped_rows | yes | The SUM range stops short: he 6 belong to the same block but are left out. |
| 3 | 3 | bmspt066 | W43 | Range error | found | skipped_rows |  | The SUM range stops short: Estimated, Estimated, Estimated, Estimated, Estimated, Estimated, Estimated belong to the same block but are left out. |
| 4 | 3 | bmspt066 | C43, D43, E43, F43, G43, H43, I43, J43,  | Range error | missed |  |  |  |
| 5 | 4 | sheet1 | L16 | Range error | found | extra_rows | yes | The Transco Z5 average for Summer 04 should cover only the Z5 column (H46:H52), as the peer rows do, but the range was widened to F46:H52 and now averages the Z4 column (F) and the Z4+Z5 sum column (G) as well. |
| 6 | 5 | jul01 | AL44 | Range error | found | extra_rows | yes | The TOTAL for the Management Services Fee should cover only the daily fee rows 12–42, but the range now starts at row 11 and pulls in the 'Price' header value (0.115), unlike the peer totals in AJ44 and AN44, which start at row 12. |
| 7 | 6 | real time | V23 | Range error | missed |  |  |  |
| 8 | 7 | deals | AD142 | Range error | missed |  |  |  |
| 9 | 8 | cost estimate summary | L23 | Range error | found | skipped_rows | yes | The SUM range stops short: Gallup CS Mods belong to the same block but are left out. |
| 10 | 9 | oct 01 | T39 | Wrong formula | found | wrong_reference |  | "VOLUME ADJ." (N38) is used where "VOLUME ADJ." (T38) belongs. |
| 11 | 10 | epsundevil | F10 | Wrong reference | found | wrong_reference | yes | "Added Compression" (D5) is used where "Added Compression" (D10) belongs. |
| 12 | 11 | data | D13 | Wrong calculation | missed |  |  |  |
| 13 | 12 | curves | V10, V100, V101, V102, V103, V104, V105, | Wrong calculation | missed |  |  |  |
| 14 | 13 | sheet1 | H33 | Wrong calculation | found | extra_rows |  | The range is stretched up past the blank separator row into the 'Total' subtotal of the government-ban costs, so those 875 are counted again in the unusual-items total. |
| 15 | 13 | sheet1 | I35 | Wrong calculation | found | wrong_reference |  | "Total" (H33) is used where "Unusual loss from government ban of certain preservatives" (H32) belongs. |
| 16 | 13 | sheet1 | I38 | Wrong calculation | missed |  |  |  |
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | found | wrong_operator |  | Parentheses are missing: "B12/C13" must be computed before subtracting B12. |
| 22 | 18 | crack spread option | M10, M11, M12, M13, M14, M9 | Wrong calculation | not_covered |  |  |  |
| 23 | 19 | may(2) | AE18, AE19, AE20, AE21, AE22, AE23, AE24 | Range error | missed |  |  |  |
| 24 | 20 | sheet1 | D112 | Range error | missed |  |  |  |
| 25 | 21 | sheet1 (2) | F94 | Wrong calculation | found | missing_term | yes | The running total in column F should add the 'in Dispute' amount in B94 to the prior subtotal in F91, but the broken formula drops the F91 term and returns only B94, unlike the peer rows F95 and F96. |
| 26 | 22 | sheet1 | C7 | File reference not working | missed |  |  |  |
| 27 | 23 | egs exp | W12 | Range error | found | skipped_rows | yes | The SUM range stops short: April, May, June, July, August, September, October belong to the same block but are left out. |
| 28 | 24 | new | C10, C11, C12, C13, C14, C25, C26, C27,  | Wrong calculation | missed |  |  |  |
| 29 | 25 | external | D11, D12, D13, D14, D15, D16, D17, D18,  | Wrong calculation | not_covered |  |  |  |
| 30 | 25 | external | E36, E37 | Wrong reference | found | wrong_reference | yes | "E34" (E34) is used where "E35" (E35) belongs. |
| 31 | 26 | mar 2002 | I132 | Fixed Value | not_covered |  |  |  |
| 32 | 27 | jd-mal or cptjk trans | H12, H13, H14, H15, H16, H17, H34, H35 | Range error | found | skipped_rows |  | The SUM range stops short: NOT FOR TOM, ET AL belong to the same block but are left out. |
| 33 | 28 | sheet1 | I25, I26, I27, I28, I29, I30, I31 | Wrong reference | found | wrong_reference | yes | "he22" (G24) is used where "he23" (G25) belongs. |
| 34 | 28 | sheet1 | G33, I34 | Range error | found | skipped_rows |  | The SUM range stops short: he 6 belong to the same block but are left out. |
| 35 | 29 | sheet1 | F8 | Formula: = SUM(D8*E8) | missed |  |  |  |
| 36 | 30 | hotlist - identified | M22, M37 | Range error | found | skipped_rows |  | The SUM range stops short: M&G - UK, M&G - UK, M&G - UK, M&G - UK, M&G - UK, M&G - UK, M&G - UK, M&G - UK belong to the same block but are left out. |

## By category

| category | found | missed | unsupported | not covered |
|---|---|---|---|---|
| File reference not working | 0 | 1 | 0 | 0 |
| Fixed Value | 0 | 0 | 0 | 1 |
| Formula: = SUM(D8*E8) | 0 | 1 | 0 | 0 |
| Range error | 10 | 5 | 0 | 0 |
| Wrong calculation | 4 | 4 | 0 | 2 |
| Wrong formula | 1 | 0 | 0 | 0 |
| Wrong reference | 3 | 0 | 0 | 0 |

## False alarms (76)

| id | formula | type | reason |
|---|---|---|---|
| 3:BMSPT066!Y40 | `=X40*AA42` | wrong_reference | "Variances:" (AA42) is used where "Fuel:" (AA40) belongs. |
| 3:BMSPT066!K44 | `=SUM([5]BMSPT066!$K$34:$K$37)+SUM(K8:K10)` | skipped_rows | The SUM range stops short: Projected belong to the same block but are left out. |
| 5:jul01!AS44 | `=AL44+AN44-AQ44` | wrong_sign | "TOTAL" (AQ44) is subtracted here but should be added. |
| 6:Real Time!J26 | `=J23+J15` | wrong_reference | "Sr. Specialist" (J15) is used where "Sr. Manager" (J12) belongs. |
| 6:Real Time!L122 | `=SUM(L118:L120)` | skipped_rows | The SUM range stops short: Billable Expense Clearing belong to the same block but are left out. |
| 6:Real Time!V122 | `=SUM(V118:V121)` | skipped_rows | The SUM range stops short: Corporate Rent (EPSC charges) belong to the same block but are left out. |
| 7:Preschedule!Z91 | `=Z89-Z90` | wrong_sign | "Total Costs:" (Z89) is subtracted here but should be added. |
| 7:Preschedule!Z97 | `=Z95-Z96` | wrong_sign | "Total Costs:" (Z95) is subtracted here but should be added. |
| 7:Preschedule!Z100 | `=Z98-Z99` | wrong_sign | "Total Costs:" (Z98) is subtracted here but should be added. |
| 7:Preschedule!Z103 | `=Z101-Z102` | wrong_sign | "Total Costs:" (Z101) is subtracted here but should be added. |
| 7:Preschedule!M89 | `=M57` | wrong_reference | The x column of the Scratch Area row should pull the same row (56) from every column, as its peers K89, L89, N89 and O89 do, but this cell points one row down to M57, which breaks the row-33 offset pattern. |
| 7:Deals!AD15 | `=SUM(F15:AC15)` | skipped_rows | The SUM range stops short: belong to the same block but are left out. |
| 7:Deals!AE142 | `=SUM(AE121:AE131)` | extra_rows | The 'Total per Model' subtotal for the EPE Purch from EPMI block should cover only rows 129-131, as its peer AD142 does, but the range is stretched up to row 121 and pulls in the PV rows that already belong to the main total in AE141. |
| 7:Fuel!C7 | `=J49` | wrong_reference | "Variable Price" (J49) is used where "Fixed Price" (J48) belongs. |
| 7:Fuel!C8 | `=J49` | wrong_reference | The 'Interstate Fixed Price (NM)' cell should pull the San Juan fixed price from J50, but it points one row up to J49, which is the Rio Grande fixed price already used by the 'Interstate Fixed Price (RG)' cell above. |
| 7:Fuel!F18 | `=C18*G7+D18*G6` | wrong_reference | The weighted average for Copper should weight % Fixed by the Intrastate Fixed Price (G6) and % Spot by the Intrastate Spot Price (G7), but the references are swapped, so the fixed share is multiplied by the spot price and vice versa. |
| 9:Feb01!Q34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:May 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:May 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:June 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:July 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:AUGUST 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:OCT 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:OCT 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 11:Data!C12 | `=C7+C10` | missing_term | "Exchange Fee $/MMBtu" (C11) should be added here but is left out. |
| 12:Summary!F6 | `=-AVERAGE(Exposure!E12:E18)` | None | unparseable reply |
| 12:Summary!F7 | `=F4+F5` | missing_term | "IF NGPL MidContinent Index minus $0.01" (F6) should be added here but is left out. |
| 12:Summary!F13 | `=-AVERAGE(Exposure!F7:F12)` | skipped_rows | The AVERAGE range stops short: F13 belong to the same block but are left out. |
| 12:Summary!F18 | `=F14` | missing_term | The 'Total Payables as of July 25, 2002' total should add both the CIG Rocky Mtns. and the Gas Daily PG&E Topock payables, but the CIG term (F13) is left out, so the total equals only the PG&E line. |
| 12:Exposure!L6 | `=J6/Volumes!I4/25` | missing_factor | The WA Price should be the Total dollar exposure divided by the Total volume (Volumes!I4) and by the 25-day period, but the 25-day factor is dropped, so the result is 25 times too high. |
| 16:Sheet1!R31 | `=SUM(F26:F29)+N24` | wrong_reference | "IF Index" (N24) is used where "Fuel - %" (N25) belongs. |
| 20:Sheet1!J84 | `=C84*E84` | missing_term | The VALUE for the GE long stock position should be shares times the price difference (E84-F84), as in the peer row 85 and the PROFIT/(LOSS) column, but the cost term F84 is dropped, so the formula returns the gross market value instead of the net value. |
| 20:Sheet1!N107 | `=+M107/M109` | wrong_reference | "Income Taxes due 2003" (M109) is used where "total" (M112) belongs. |
| 20:Sheet1!M109 | `=K112` | wrong_reference | "TOTAL" (K112) is used where "Income Taxes due 2003" (K109) belongs. |
| 20:Sheet1!N109 | `=+M109/K112` | wrong_reference | "TOTAL" (K112) is used where "Income Taxes due 2003" (K109) belongs. |
| 20:Sheet1!C112 | `=SUM(C53:C65)+C32+C38+C45+C48+C49+C50` | skipped_rows | The SUM range stops short: Cash, Muni Bonds, Govt. paper, ENE jan 02 35 calls, ENE jan 02 40 calls belong to the same block but are left out. |
| 20:Sheet1!M112 | `=SUM(K45:K65)+K32+K38` | skipped_rows | The SUM range stops short: Stable Asset, Stable Asset belong to the same block but are left out. |
| 20:Sheet1!M129 | `=SUM(K112:K129)+K138` | wrong_reference | "ENE 8/11/07 (0%) 106892" (K138) is used where "ENE 8/11/07 (0%) 106892" (K139) belongs. |
| 20:Sheet1!M149 | `=SUM(K129:K146)+M112` | skipped_rows | The SUM range stops short: TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL belong to the same block but are left out. |
| 20:Sheet1!K153 | `=K112*K152` | wrong_reference | "TOTAL" (K112) is used where "TOTAL" (K149) belongs. |
| 20:unvested!E4 | `=SUM(C25:C25)+C33` | skipped_rows | The SUM range stops short: options, options, options, options, options, restricted stock belong to the same block but are left out. |
| 21:Sheet1!F92 | `=SUM(E86:E91)` | skipped_rows | The SUM range stops short: , , , , ,  belong to the same block but are left out. |
| 21:Sheet1!B105 | `=SUM(B94:B102)+SUM(B89:B91)` | wrong_reference | The 12 Month Ave total should add the 9-month subtotal in B103 (B94:B102) to the 3-month subtotal in B92 (B89:B91), but the second range was shifted down to B89:B91, so it no longer matches the 3-month block that B92 sums. |
| 21:Sheet1!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 21:Sheet1!E116 | `=D116` | missing_factor | The column header says 'Split Retro-active Amount 50/50', so the amount should be halved, but the formula returns the full 'Amt in Dispute' from D116, unlike the peer rows that divide by 2. |
| 21:Sheet1!E118 | `=D118` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' amount, but this cell copies D118 without dividing by 2, unlike the peer row E114 (=D114/2). |
| 21:Sheet1!E124 | `=E116` | missing_factor | The 'Split Retro-active Amount 50/50' label requires halving the revenue, but the formula returns the full Feb, 2001 - Oct, 2001 Revenue amount, unlike the peer row E114 which divides by 2. |
| 21:Sheet1 (2)!B105 | `=SUM(B94:B102)+SUM(B89:B91)` | wrong_reference | The 12-month total should add the prior 9-month subtotal in B92 (SUM(B4:B91)), but the range was shifted up to B89:B91, so only three months are added and the 12 Month Ave drops to 48,811. |
| 21:Sheet1 (2)!F115 | `=D115` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' in D115, but the /2 is dropped, so the split equals the full amount and no longer matches the peer split in F114 (=D114/2). |
| 21:Sheet1 (2)!F117 | `=H103` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the in-dispute amount, but this cell returns the full H103, unlike the peer F114 (=D114/2) and F115 (=D115) which follow the split pattern. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: 'ENA IS'!C21 belong to the same block but are left out. |
| 23:EGM Burn!E18 | `=SUM(E15:E17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in E15, which is a separate line. |
| 23:EGM Burn!G18 | `=SUM(G15:G17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in G15, which already sums the expense lines above. |
| 23:EGM Burn!Q18 | `=SUM(Q15:Q17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in Q15, which is not an expense line. |
| 23:EGS Burn!X4 | `=2.9*1.15+0.6-0.1` | wrong_reference | "*" (2.9) is used where "*" (3.9) belongs. |
| 23:EGS Burn!Z4 | `=4*1.15+0.6` | missing_term | "-0.1" (U4) should be subtracted here but is left out. |
| 23:EIM Burn!E15 | `=SUM(E12:E14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in E12, which is already the sum of the mill rows above. |
| 23:EBS Burn!E10 | `=SUM(E7:E9)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should cover only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' row (E7), which is a separate subtotal. |
| 23:EGS EXP!S19 | `=1+0.6` | wrong_reference | "1" (1) is used where "0.9" (0.9) belongs. |
| 23:EGS OFF BS!G18 | `=G17+B10` | wrong_reference | "Recall of debt by Hong Kong bank" (B10) is used where "TOTAL Commitments and Contingencies" (B18) belongs. |
| 24:Legacy!H36 | `=Description!$I$34` | wrong_reference | "SDGE" (Description!$I$34) is used where "SDGE" (Description!$I$36) belongs. |
| 25:external!E12 | `=3025+1472` | wrong_sign | "DAY AHEAD" (1472) is added here but should be subtracted. |
| 25:external!F36 | `=(D36-E36)+F34` | wrong_reference | "F34" (F34) is used where "F35" (F35) belongs. |
| 25:external!F40 | `=F39` | wrong_reference | The IMBALANCE total should sum the daily IMBALANCE rows F8:F39, but the range was shortened to F39, so the total returns 0 instead of the running imbalance. |
| 26:Nov 2001!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J17 | `=J172+J208+J229+J251` | missing_term | The December total leaves out the December turbine count in J172, which the November total in J16 adds twice (J171 and J207), so the December total no longer matches the pattern of the monthly totals. |
| 26:Dec 2001!G45 | `=SUM(G25:G44)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!F46 | `=F45` | missing_factor | The 'Weighted Average' should be the 'Average' availability (F45) weighted by the number of units (G45), but the unit count is dropped, so the result is just the unweighted average. |
| 26:Dec 2001!F151 | `=F150` | missing_factor | The 'Weighted Average' should be the 'Average' availability (F150) weighted by the number of units (G150), but the unit count is dropped, so the weighted average just repeats the simple average. |
| 26:Dec 2001!G150 | `=SUM(G50:G149)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G201 | `=SUM(G195:G200)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
