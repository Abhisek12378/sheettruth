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
| flagged_windows | 249 |
| false_alarm_windows | 222 |
| recall_covered | 0.621 |
| recall_all | 0.562 |
| precision_windows | 0.108 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | sheet1 | F28, G28 | Range error | found | skipped_rows | yes | The SUM range stops short: Enron belong to the same block but are left out. |
| 2 | 2 | sheet1 | I34 | Range error | found | skipped_rows | yes | The SUM range stops short: he 6 belong to the same block but are left out. |
| 3 | 3 | bmspt066 | W43 | Range error | found | skipped_rows |  | The SUM range stops short: Estimated, Estimated, Estimated, Estimated, Estimated, Estimated, Estimated belong to the same block but are left out. |
| 4 | 3 | bmspt066 | C43, D43, E43, F43, G43, H43, I43, J43,  | Range error | missed |  |  |  |
| 5 | 4 | sheet1 | L16 | Range error | found | extra_rows | yes | The Transco Z5 average for Summer 04 should cover only the Z5 column (H46:H52), as the peer rows do, but the range was widened to F46:H52 and now averages the Z4 column (F) and the Z4+Z5 sum column (G) as well. |
| 6 | 5 | jul01 | AL44 | Range error | found | extra_rows | yes | The TOTAL for the Management Services Fee should cover only the daily fee rows 12�42, but the range now starts at row 11 and pulls in the 'Price' header value (0.115), unlike the peer totals in AJ44 and AN44, which start at row 12. |
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
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | found | wrong_reference |  | "Fuel - %" (O37) is used where "IF Index" (O36) belongs. |
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

## False alarms (222)

| id | formula | type | reason |
|---|---|---|---|
| 3:BMSPT066!Y40 | `=X40*AA42` | wrong_reference | "Variances:" (AA42) is used where "Fuel:" (AA40) belongs. |
| 3:BMSPT066!K44 | `=SUM([5]BMSPT066!$K$34:$K$37)+SUM(K8:K10)` | skipped_rows | The SUM range stops short: Projected belong to the same block but are left out. |
| 5:jul01!AS44 | `=AL44+AN44-AQ44` | wrong_sign | "TOTAL" (AQ44) is subtracted here but should be added. |
| 6:Real Time!J26 | `=J23+J15` | wrong_reference | "Sr. Specialist" (J15) is used where "Sr. Manager" (J12) belongs. |
| 6:Real Time!L122 | `=SUM(L118:L120)` | skipped_rows | The SUM range stops short: Billable Expense Clearing belong to the same block but are left out. |
| 6:Real Time!J122 | `=SUM(J118:J121)` | extra_rows | The Total Other Expenses range runs one row too far and picks up the Billable Expense Clearing line (J121), which is not an expense. |
| 6:Real Time!N122 | `=SUM(N118:N121)` | extra_rows | The Total Other Expenses range runs one row too far and picks up Billable Expense Clearing (N121), which is not an Other Expense line. |
| 6:Real Time!V122 | `=SUM(V118:V121)` | skipped_rows | The SUM range stops short: Corporate Rent (EPSC charges) belong to the same block but are left out. |
| 7:Preschedule!AA41 | `=-Economics!D34/Economics!I34` | wrong_sign | "Newman 1" (Economics!D34) is subtracted here but should be added. |
| 7:Preschedule!Z59 | `=SUM(Economics!D28:D45)` | skipped_rows | The SUM range stops short: Total belong to the same block but are left out. |
| 7:Preschedule!AA59 | `=Economics!D47` | wrong_reference | The MMBtu/Day total should pull the 'Total' row in Economics!D46, but this points one row down to the 'Total' label in D47, which breaks the pattern of the peer totals in Y59 and Z59. |
| 7:Preschedule!B80 | `=Deals!AD160` | wrong_reference | The 'Prescheduled Purch.' cell should pull the same row as the 'Prescheduled Sales' cell (Deals!AD161), but it points one row up to AD160, which breaks the row alignment with its peers. |
| 7:Preschedule!Z91 | `=Z89-Z90` | wrong_sign | "Total Costs:" (Z89) is subtracted here but should be added. |
| 7:Preschedule!Z94 | `=Z92-Z93` | wrong_sign | "Total Costs:" (Z92) is subtracted here but should be added. |
| 7:Preschedule!Z97 | `=Z95-Z96` | wrong_sign | "Total Costs:" (Z95) is subtracted here but should be added. |
| 7:Preschedule!Z100 | `=Z98-Z99` | wrong_sign | "Total Costs:" (Z98) is subtracted here but should be added. |
| 7:Preschedule!Z103 | `=Z101-Z102` | wrong_sign | "Total Costs:" (Z101) is subtracted here but should be added. |
| 7:Preschedule!M89 | `=M57` | wrong_reference | The x column of the Scratch Area row should pull the same row (56) from every column, as its peers K89, L89, N89 and O89 do, but this cell points one row down to M57, which breaks the row-33 offset pattern. |
| 7:Preschedule!Z108 | `=Z105-Z107` | wrong_sign | "Total Costs:" (Z105) is subtracted here but should be added. |
| 7:Preschedule!Z113 | `=Z110-Z112` | wrong_sign | "Total Costs:" (Z110) is subtracted here but should be added. |
| 7:Preschedule!Z118 | `=Z115-Z117` | wrong_sign | "Total Costs:" (Z115) is subtracted here but should be added. |
| 7:Preschedule!Z123 | `=Z120-Z122` | wrong_sign | "Total Costs:" (Z120) is subtracted here but should be added. |
| 7:Preschedule!Z128 | `=Z125-Z127` | wrong_sign | "Total Costs:" (Z125) is subtracted here but should be added. |
| 7:Preschedule!Z133 | `=Z130-Z132` | wrong_sign | "Total Costs:" (Z130) is subtracted here but should be added. |
| 7:Preschedule!Z138 | `=Z135-Z137` | wrong_sign | "Total Costs:" (Z135) is subtracted here but should be added. |
| 7:Preschedule!Z143 | `=Z140-Z142` | wrong_sign | "Total Costs:" (Z140) is subtracted here but should be added. |
| 7:Preschedule!Z148 | `=Z145-Z147` | wrong_sign | "Total Costs:" (Z145) is subtracted here but should be added. |
| 7:Preschedule!Z153 | `=Z150-Z152` | wrong_sign | "Total Costs:" (Z150) is subtracted here but should be added. |
| 7:Preschedule!Z158 | `=Z155-Z157` | wrong_sign | "Total Costs:" (Z155) is subtracted here but should be added. |
| 7:Preschedule!Z163 | `=Z160-Z162` | wrong_sign | "Total Costs:" (Z160) is subtracted here but should be added. |
| 7:Preschedule!A144 | `=Economics!A42` | wrong_reference | The unit name in A144 should come from Economics!A43, the row directly above the price in A145 (=Economics!$I43), but it points one row up to A42, which is the unit name for the Newman 4 test above. |
| 7:Preschedule!Z169 | `=Z166+Z167` | wrong_sign | "Net Position after sales (taken from row 53)" (Z167) is added here but should be subtracted. |
| 7:Deals!AD15 | `=SUM(F15:AC15)` | skipped_rows | The SUM range stops short: belong to the same block but are left out. |
| 7:Deals!F169 | `=D170-0.25` | wrong_reference | "D170" (D170) is used where "D169" (D169) belongs. |
| 7:Deals!AE142 | `=SUM(AE121:AE131)` | extra_rows | The 'Total per Model' subtotal for the EPE Purch from EPMI block should cover only rows 129-131, as its peer AD142 does, but the range is stretched up to row 121 and pulls in the PV rows that already belong to the main total in AE141. |
| 7:Fuel!C7 | `=J49` | wrong_reference | "Variable Price" (J49) is used where "Fixed Price" (J48) belongs. |
| 7:Fuel!C8 | `=J49` | wrong_reference | The 'Interstate Fixed Price (NM)' cell should pull the San Juan fixed price from J50, but it points one row up to J49, which is the Rio Grande fixed price already used by the 'Interstate Fixed Price (RG)' cell above. |
| 7:Fuel!F18 | `=C18*G7+D18*G6` | wrong_reference | The weighted average for Copper should weight % Fixed by the Intrastate Fixed Price (G6) and % Spot by the Intrastate Spot Price (G7), but the references are swapped, so the fixed share is multiplied by the spot price and vice versa. |
| 9:Jan01!P5 | `=+A6` | wrong_reference | "A6" (A6) is used where "A5" (A5) belongs. |
| 9:Feb01!P5 | `=+A6` | wrong_reference | "A6" (A6) is used where "A5" (A5) belongs. |
| 9:Feb01!Q34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:Mar01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:Mar01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:Apr01!AA5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:Apr01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:Apr01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:May 01!X5 | `=+A6` | wrong_reference | "A6" (A6) is used where "A5" (A5) belongs. |
| 9:May 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F7" (F7) belongs. |
| 9:May 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:May 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:June 01!X5 | `=+A6` | wrong_reference | "A6" (A6) is used where "A5" (A5) belongs. |
| 9:June 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:June 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:June 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:June 01!B39 | `=B5+B38` | wrong_sign | "MAY CUMULATIVE" (B38) is added here but should be subtracted. |
| 9:July 01!AA5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:July 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F7" (F7) belongs. |
| 9:July 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:AUGUST 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:AUGUST 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:SEPT 01 !AA5 | `=+F6` | wrong_reference | The HUGO beginning balance should pull the HUGO column's own row-5 value (F5), but it points one row down to F6, which is the next period's figure and duplicates the PVR column's reference. |
| 9:SEPT 01 !AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:SEPT 01 !Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:OCT 01!AA5 | `=+F6` | wrong_reference | The HUGO total in row 5 should pull the HUGO column value from the same row (F5), but it points one row down to F6, which is the next row's value. |
| 9:OCT 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:OCT 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:OCT 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:NOV 01!AA5 | `=+F6` | wrong_reference | The HUGO (EST) BEGINNING BALANCE should pull the HUGO column's own row-6 value (F5), but it points one row down to F6, which is the next period's balance and duplicates the PVR column's reference. |
| 9:NOV 01!AB5 | `=+F6` | wrong_reference | "F6" (F6) is used where "F5" (F5) belongs. |
| 9:NOV 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 11:Data!C12 | `=C7+C10` | missing_term | "Exchange Fee $/MMBtu" (C11) should be added here but is left out. |
| 11:Data!F54 | `=F51/D49` | wrong_reference | "Total delivered volume" (D49) is used where "Total delivered volume" (D51) belongs. |
| 12:Summary!F6 | `=-AVERAGE(Exposure!E12:E18)` | None | unparseable reply |
| 12:Summary!F7 | `=F4+F5` | missing_term | "IF NGPL MidContinent Index minus $0.01" (F6) should be added here but is left out. |
| 12:Summary!F13 | `=-AVERAGE(Exposure!F7:F12)` | skipped_rows | The AVERAGE range stops short: F13 belong to the same block but are left out. |
| 12:Summary!F18 | `=F14` | missing_term | The 'Total Payables as of July 25, 2002' total should add both the CIG Rocky Mtns. and the Gas Daily PG&E Topock payables, but the CIG term (F13) is left out, so the total equals only the PG&E line. |
| 12:Exposure!L6 | `=J6/Volumes!I4/25` | missing_factor | The WA Price should be the Total dollar exposure divided by the Total volume (Volumes!I4) and by the 25-day period, but the 25-day factor is dropped, so the result is 25 times too high. |
| 12:Exposure!C7 | `=$A6*Volumes!B4*Curves!F5+25*Volumes!B5*Curves!F6` | wrong_reference | "A6" (A6) is used where "A7" (A7) belongs. |
| 12:Exposure!L7 | `=J7/Volumes!I5/(25+A6)` | wrong_reference | "A6" (A6) is used where "A7" (A7) belongs. |
| 16:Sheet1!R31 | `=SUM(F26:F29)+N24` | wrong_reference | "IF Index" (N24) is used where "Fuel - %" (N25) belongs. |
| 20:Sheet1!J84 | `=C84*E84` | missing_term | The VALUE for the GE long stock position should be shares times the price difference (E84-F84), as in the peer row 85 and the PROFIT/(LOSS) column, but the cost term F84 is dropped, so the formula returns the gross market value instead of the net value. |
| 20:Sheet1!J18 | `=+C18` | missing_factor | The VALUE for the Margin Account Payable short options position should be SHARES times the price in E18, but the price factor is dropped, so the cell just repeats the share count. |
| 20:Sheet1!N107 | `=+M107/M109` | wrong_reference | "Income Taxes due 2003" (M109) is used where "total" (M112) belongs. |
| 20:Sheet1!M109 | `=K112` | wrong_reference | "TOTAL" (K112) is used where "Income Taxes due 2003" (K109) belongs. |
| 20:Sheet1!N109 | `=+M109/K112` | wrong_reference | "TOTAL" (K112) is used where "Income Taxes due 2003" (K109) belongs. |
| 20:Sheet1!C112 | `=SUM(C53:C65)+C32+C38+C45+C48+C49+C50` | skipped_rows | The SUM range stops short: Cash, Muni Bonds, Govt. paper, ENE jan 02 35 calls, ENE jan 02 40 calls belong to the same block but are left out. |
| 20:Sheet1!M112 | `=SUM(K45:K65)+K32+K38` | skipped_rows | The SUM range stops short: Stable Asset, Stable Asset belong to the same block but are left out. |
| 20:Sheet1!M129 | `=SUM(K112:K129)+K138` | wrong_reference | "ENE 8/11/07 (0%) 106892" (K138) is used where "ENE 8/11/07 (0%) 106892" (K139) belongs. |
| 20:Sheet1!M141 | `=+M107` | wrong_reference | "Income Taxes due 2001" (M107) is used where "Income Taxes due 2002" (M108) belongs. |
| 20:Sheet1!N143 | `=+M143/K149` | wrong_reference | "TOTAL" (K149) is used where "ENE 12/29/07 (0%) 160388" (K143) belongs. |
| 20:Sheet1!M149 | `=SUM(K129:K146)+M112` | skipped_rows | The SUM range stops short: TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL belong to the same block but are left out. |
| 20:Sheet1!K153 | `=K112*K152` | wrong_reference | "TOTAL" (K112) is used where "TOTAL" (K149) belongs. |
| 20:unvested!E4 | `=SUM(C25:C25)+C33` | skipped_rows | The SUM range stops short: options, options, options, options, options, restricted stock belong to the same block but are left out. |
| 21:Sheet1!F92 | `=SUM(E86:E91)` | skipped_rows | The SUM range stops short: , , , , ,  belong to the same block but are left out. |
| 21:Sheet1!B105 | `=SUM(B94:B102)+SUM(B89:B91)` | wrong_reference | The 12 Month Ave total should add the 9-month subtotal in B103 (B94:B102) to the 3-month subtotal in B92 (B89:B91), but the second range was shifted down to B89:B91, so it no longer matches the 3-month block that B92 sums. |
| 21:Sheet1!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 21:Sheet1!F115 | `=D115` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' in D115, but the /2 is dropped, so the split equals the full amount and no longer matches the peer rows F114 and F117. |
| 21:Sheet1!F117 | `=D117` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' amount, but this cell copies D117 in full, unlike the peer rows F115 and F116, which divide by 2. |
| 21:Sheet1!E116 | `=D116` | missing_factor | The column header says 'Split Retro-active Amount 50/50', so the amount should be halved, but the formula returns the full 'Amt in Dispute' from D116, unlike the peer rows that divide by 2. |
| 21:Sheet1!E118 | `=D118` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' amount, but this cell copies D118 without dividing by 2, unlike the peer row E114 (=D114/2). |
| 21:Sheet1!E124 | `=E116` | missing_factor | The 'Split Retro-active Amount 50/50' label requires halving the revenue, but the formula returns the full Feb, 2001 - Oct, 2001 Revenue amount, unlike the peer row E114 which divides by 2. |
| 21:Sheet1 (2)!B105 | `=SUM(B94:B102)+SUM(B89:B91)` | wrong_reference | The 12-month total should add the prior 9-month subtotal in B92 (SUM(B4:B91)), but the range was shifted up to B89:B91, so only three months are added and the 12 Month Ave drops to 48,811. |
| 21:Sheet1 (2)!E105 | `=+E103+E92` | wrong_reference | "(Retro billed March 20, 2001)" (E92) is used where "E93" (E93) belongs. |
| 21:Sheet1 (2)!F115 | `=D115` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' in D115, but the /2 is dropped, so the split equals the full amount and no longer matches the peer split in F114 (=D114/2). |
| 21:Sheet1 (2)!F125 | `=D125` | missing_term | "SoCal Pays" (E125) should be subtracted here but is left out. |
| 21:Sheet1 (2)!E116 | `=D116` | missing_factor | The column header says 'Split Retro-active Amount 50/50', so the disputed amount should be halved, but the formula returns the full amount, unlike the peer row 114 which divides by 2. |
| 21:Sheet1 (2)!E126 | `=D126` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' amount, but this cell passes the full amount through, unlike the peer rows that divide by 2. |
| 21:Sheet1 (2)!E128 | `=D128` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' total, but this cell copies D128 in full, unlike the peer rows E124 and E126, which divide by 2. |
| 21:Sheet1 (2)!F117 | `=H103` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the in-dispute amount, but this cell returns the full H103, unlike the peer F114 (=D114/2) and F115 (=D115) which follow the split pattern. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: 'ENA IS'!C21 belong to the same block but are left out. |
| 23:Europe Burn!E30 | `=-E24` | wrong_sign | "Depreciation & Amortization" (E24) is subtracted here but should be added. |
| 23:Europe Burn!G30 | `=-G24` | wrong_sign | "Depreciation & Amortization" (G24) is subtracted here but should be added. |
| 23:Europe Burn!I30 | `=-I24` | wrong_sign | "Depreciation & Amortization" (I24) is subtracted here but should be added. |
| 23:Europe Burn!K30 | `=-K24` | wrong_sign | "Depreciation & Amortization" (K24) is subtracted here but should be added. |
| 23:Europe Burn!M30 | `=-M24` | wrong_sign | "Depreciation & Amortization" (M24) is subtracted here but should be added. |
| 23:Europe Burn!O30 | `=-O24` | wrong_sign | "Depreciation & Amortization" (O24) is subtracted here but should be added. |
| 23:Europe Burn!Q30 | `=-Q24` | wrong_reference | "Depreciation & Amortization" (Q24) is used where "Total Expenses net of Capitalized Expense" (Q26) belongs. |
| 23:Europe Burn!G33 | `=+G26+G28+G31` | missing_term | "Other Cash Payments" (G29) should be added here but is left out. |
| 23:Europe Burn!I33 | `=+I26+I28+I31` | missing_term | "Other Cash Payments" (I29) should be added here but is left out. |
| 23:Europe Burn!K33 | `=+K26+K28+K31` | missing_term | "Other Cash Payments" (K29) should be added here but is left out. |
| 23:Europe Burn!M33 | `=+M26+M28+M31` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (M29) and Less: DD&A (M30), unlike the peer total in K33. |
| 23:ENA Burn!E24 | `=-E18` | wrong_sign | "Depreciation & Amortization" (E18) is subtracted here but should be added. |
| 23:ENA Burn!K24 | `=-K18` | wrong_sign | "Depreciation & Amortization" (K18) is subtracted here but should be added. |
| 23:ENA Burn!M24 | `=-M18` | wrong_sign | "Depreciation & Amortization" (M18) is subtracted here but should be added. |
| 23:ENA Burn!Q24 | `=-Q18` | wrong_sign | "Depreciation & Amortization" (Q18) is subtracted here but should be added. |
| 23:ENA Burn!G27 | `=+G20+G22+G25` | missing_term | "Other Cash Payments" (G23) should be added here but is left out. |
| 23:ENA Burn!I27 | `=+I20+I22+I25` | missing_term | "Other Cash Payments" (I23) should be added here but is left out. |
| 23:ENA Burn!K27 | `=+K20+K22+K25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:ENA Burn!M27 | `=+M20+M22+M25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:ENA Burn!Q27 | `=+Q20+Q22+Q25` | missing_term | "Other Cash Payments" (Q23) should be added here but is left out. |
| 23:EGM Burn!E18 | `=SUM(E15:E17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in E15, which is a separate line. |
| 23:EGM Burn!G18 | `=SUM(G15:G17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in G15, which already sums the expense lines above. |
| 23:EGM Burn!Q18 | `=SUM(Q15:Q17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in Q15, which is not an expense line. |
| 23:EGM Burn!E22 | `=-E16` | wrong_sign | "Depreciation & Amortization" (E16) is subtracted here but should be added. |
| 23:EGM Burn!O22 | `=-O16` | wrong_sign | "Depreciation & Amortization" (O16) is subtracted here but should be added. |
| 23:EGM Burn!G25 | `=+G18+G20+G23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments, Less: DD&A and the October amount in G23, but the formula leaves out Other Cash Payments (G21) and Less: DD&A (G22), unlike the peer total in E25. |
| 23:EGM Burn!I25 | `=+I18+I20+I23` | missing_term | "Less: DD&A" (I22) should be added here but is left out. |
| 23:EGM Burn!K25 | `=+K18+K20+K23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms, unlike the peer totals in I25 and M25. |
| 23:EGM Burn!M25 | `=+M18+M20+M23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EGM Burn!O25 | `=+O18+O20+O23` | missing_term | "Less: DD&A" (O22) should be added here but is left out. |
| 23:EGM Burn!Q25 | `=+Q18+Q20+Q23` | missing_term | "Less: DD&A" (Q22) should be added here but is left out. |
| 23:EGS Burn!X4 | `=2.9*1.15+0.6-0.1` | wrong_reference | "*" (2.9) is used where "*" (3.9) belongs. |
| 23:EGS Burn!Z4 | `=4*1.15+0.6` | missing_term | "-0.1" (U4) should be subtracted here but is left out. |
| 23:EGS Burn!G15 | `=SUM(G12:G14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was extended up to include the 'Total' subtotal in G12, so the result is 10.2 instead of 1.7. |
| 23:EGS Burn!K15 | `=SUM(K12:K14)` | wrong_sign | "Depreciation & Amortization" (K13) is added here but should be subtracted. |
| 23:EGS Burn!E19 | `=-E13` | wrong_sign | "Depreciation & Amortization" (E13) is subtracted here but should be added. |
| 23:EGS Burn!E22 | `=+E15+E17+E20+E19` | missing_term | "Other Cash Payments" (E18) should be added here but is left out. |
| 23:EIM Burn!E15 | `=SUM(E12:E14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in E12, which is already the sum of the mill rows above. |
| 23:EIM Burn!E19 | `=-E13` | wrong_sign | "Depreciation & Amortization" (E13) is subtracted here but should be added. |
| 23:EIM Burn!G22 | `=+G15+G17+G20` | missing_term | "Other Cash Payments" (G18) should be added here but is left out. |
| 23:EIM Burn!I22 | `=+I15+I17+I20` | missing_term | "Less: DD&A" (I19) should be added here but is left out. |
| 23:EIM Burn!K22 | `=+K15+K17+K20` | missing_term | "Other Cash Payments" (K18) should be added here but is left out. |
| 23:EIM Burn!M22 | `=+M15+M17+M20` | missing_term | "Less: DD&A" (M19) should be added here but is left out. |
| 23:EIM Burn!O22 | `=+O15+O17+O20` | missing_term | "Less: DD&A" (O19) should be added here but is left out. |
| 23:EIM Burn!Q22 | `=+Q15+Q17+Q20` | missing_term | "Less: DD&A" (Q19) should be added here but is left out. |
| 23:EBS Burn!E10 | `=SUM(E7:E9)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should cover only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' row (E7), which is a separate subtotal. |
| 23:EBS Burn!E14 | `=-E8` | wrong_sign | "Depreciation & Amortization" (E8) is subtracted here but should be added. |
| 23:EBS Burn!G14 | `=-G8` | wrong_reference | "Depreciation & Amortization" (G8) is used where "Total Expenses net of Capitalized Expense" (G10) belongs. |
| 23:EBS Burn!I14 | `=-I8` | wrong_reference | "Depreciation & Amortization" (I8) is used where "Total Expenses net of Capitalized Expense" (I10) belongs. |
| 23:EBS Burn!K14 | `=-K8` | wrong_reference | "Depreciation & Amortization" (K8) is used where "Total Expenses net of Capitalized Expense" (K10) belongs. |
| 23:EBS Burn!M14 | `=-M8` | wrong_reference | "Depreciation & Amortization" (M8) is used where "Total Expenses net of Capitalized Expense" (M10) belongs. |
| 23:EBS Burn!O14 | `=-O8` | wrong_reference | "Depreciation & Amortization" (O8) is used where "Total Expenses net of Capitalized Expense" (O10) belongs. |
| 23:EBS Burn!Q14 | `=-Q8` | wrong_reference | "Depreciation & Amortization" (Q8) is used where "Total Expenses net of Capitalized Expense" (Q10) belongs. |
| 23:EBS Burn!G17 | `=+G10+G12+G15` | missing_term | "Other Cash Payments" (G13) should be added here but is left out. |
| 23:EBS Burn!I17 | `=+I10+I12+I15` | missing_term | "Other Cash Payments" (I13) and "Less: DD&A" (I14) should be added here but are left out. |
| 23:EBS Burn!K17 | `=+K10+K12+K15` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms, unlike the peer totals in I17 and M17. |
| 23:EBS Burn!M17 | `=+M10+M12+M15` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EBS Burn!O17 | `=+O10+O12+O15` | missing_term | "Less: DD&A" (O14) should be added here but is left out. |
| 23:EBS Burn!Q17 | `=+Q10+Q12+Q15` | missing_term | "Other Cash Payments" (Q13) should be added here but is left out. |
| 23:ENW Burn!E17 | `=-E11` | wrong_sign | "Depreciation & Amortization" (E11) is subtracted here but should be added. |
| 23:ENW Burn!K17 | `=-K11` | wrong_sign | "Depreciation & Amortization" (K11) is subtracted here but should be added. |
| 23:ENW Burn!O17 | `=-O11` | wrong_sign | "Depreciation & Amortization" (O11) is subtracted here but should be added. |
| 23:ENW Burn!Q17 | `=-Q11` | wrong_reference | "Depreciation & Amortization" (Q11) is used where "Total Expenses net of Capitalized Expense" (Q13) belongs. |
| 23:ENW Burn!G20 | `=+G13+G15+G18` | missing_term | "Other Cash Payments" (G16) should be added here but is left out. |
| 23:ENW Burn!I20 | `=+I13+I15+I18` | missing_term | "Other Cash Payments" (I16) and "Less: DD&A" (I17) should be added here but are left out. |
| 23:ENW Burn!K20 | `=+K13+K15+K18` | missing_term | "Other Cash Payments" (K16) and "Less: DD&A" (K17) should be added here but are left out. |
| 23:ENW Burn!M20 | `=+M13+M15+M18` | missing_term | "Other Cash Payments" (M16) and "Less: DD&A" (M17) should be added here but are left out. |
| 23:ENW Burn!O20 | `=+O13+O15+O18` | missing_term | "Other Cash Payments" (O16) should be added here but is left out. |
| 23:ENW Burn!Q20 | `=+Q13+Q15+Q18` | missing_term | "Other Cash Payments" (Q16) should be added here but is left out. |
| 23:EES Burn!E24 | `=-E18` | wrong_sign | "Depreciation & Amortization" (E18) is subtracted here but should be added. |
| 23:EES Burn!G27 | `=+G20+G22+G25` | missing_term | "Other Cash Payments" (G23) should be added here but is left out. |
| 23:EES Burn!I27 | `=+I20+I22+I25` | missing_term | "Other Cash Payments" (I23) should be added here but is left out. |
| 23:EES Burn!K27 | `=+K20+K22+K25` | missing_term | "Other Cash Payments" (K23) should be added here but is left out. |
| 23:EES Burn!M27 | `=+M20+M22+M25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EES Burn!O27 | `=+O20+O22+O25` | missing_term | "Less: DD&A" (O24) should be added here but is left out. |
| 23:EES Burn!Q27 | `=+Q20+Q22+Q25` | missing_term | "Other Cash Payments" (Q23) should be added here but is left out. |
| 23:EPI Burn!E12 | `=-E6` | wrong_sign | "Depreciation & Amortization" (E6) is subtracted here but should be added. |
| 23:EPI Burn!O12 | `=-O6` | wrong_reference | "Depreciation & Amortization" (O6) is used where "Total Expenses net of Capitalized Expense" (O8) belongs. |
| 23:EPI Burn!Q12 | `=-Q6` | wrong_reference | "Depreciation & Amortization" (Q6) is used where "Total Expenses net of Capitalized Expense" (Q8) belongs. |
| 23:EPI Burn!E15 | `=E8+E10+E11+E12` | wrong_reference | "Other Cash Payments" (E11) is used where "Other Cash Payments" (E13) belongs. |
| 23:EPI Burn!G15 | `=+G8+G10+G13` | missing_term | "Other Cash Payments" (G11) should be added here but is left out. |
| 23:EPI Burn!I15 | `=+I8+I10+I13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (I11) and Less: DD&A (I12), unlike the peer total in G15. |
| 23:EPI Burn!K15 | `=+K8+K10+K13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (K11) and Less: DD&A (K12), unlike the peer totals in I15 and M15. |
| 23:EPI Burn!M15 | `=+M8+M10+M13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (M11) and Less: DD&A (M12), unlike the peer total in K15. |
| 23:EPI Burn!O15 | `=+O8+O10+O13` | missing_term | "Less: DD&A" (O12) should be added here but is left out. |
| 23:EPI Burn!Q15 | `=+Q8+Q10+Q13` | missing_term | "Other Cash Payments" (Q11) and "Less: DD&A" (Q12) should be added here but are left out. |
| 23:EGS EXP!S19 | `=1+0.6` | wrong_reference | "1" (1) is used where "0.9" (0.9) belongs. |
| 23:EGS OFF BS!G18 | `=G17+B10` | wrong_reference | "Recall of debt by Hong Kong bank" (B10) is used where "TOTAL Commitments and Contingencies" (B18) belongs. |
| 24:Legacy!H36 | `=Description!$I$34` | wrong_reference | "SDGE" (Description!$I$34) is used where "SDGE" (Description!$I$36) belongs. |
| 25:external!E12 | `=3025+1472` | wrong_sign | "DAY AHEAD" (1472) is added here but should be subtracted. |
| 25:external!F36 | `=(D36-E36)+F34` | wrong_reference | "F34" (F34) is used where "F35" (F35) belongs. |
| 25:external!F40 | `=F39` | wrong_reference | The IMBALANCE total should sum the daily IMBALANCE rows F8:F39, but the range was shortened to F39, so the total returns 0 instead of the running imbalance. |
| 26:Nov 2001!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!L193 | `=COUNT(C191:C206)` | extra_rows | The December turbine count should cover only the December acceptance dates in C192:C206, but the range was stretched up into C191, the last November date, so November is counted twice in the 'Project Total to date'. |
| 26:Nov 2001!L214 | `=COUNT(C212:C228)` | extra_rows | The December turbine count range is stretched up into the blank row above the 'November' header, so it no longer covers only the December acceptance dates in C213:C228. |
| 26:Dec 2001!J17 | `=J172+J208+J229+J251` | missing_term | The December total leaves out the December turbine count in J172, which the November total in J16 adds twice (J171 and J207), so the December total no longer matches the pattern of the monthly totals. |
| 26:Dec 2001!G45 | `=SUM(G25:G44)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!F46 | `=F45` | missing_factor | The 'Weighted Average' should be the 'Average' availability (F45) weighted by the number of units (G45), but the unit count is dropped, so the result is just the unweighted average. |
| 26:Dec 2001!F151 | `=F150` | missing_factor | The 'Weighted Average' should be the 'Average' availability (F150) weighted by the number of units (G150), but the unit count is dropped, so the weighted average just repeats the simple average. |
| 26:Dec 2001!G150 | `=SUM(G50:G149)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G201 | `=SUM(G195:G200)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J229 | `=COUNT(C227:C243)` | extra_rows | The December turbine count range is stretched up into the blank row above the November header, so it no longer covers only the December acceptance dates in C228:C243. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!L193 | `=COUNT(C191:C206)` | extra_rows | The December turbine count range is stretched up into the blank row C191, which sits above the November row, so it no longer covers only the December acceptance dates. |
| 26:Jan 2002!L214 | `=COUNT(C212:C228)` | extra_rows | The December turbine count range is stretched up into the blank row above the November header, so it no longer covers only the December acceptance dates in C213:C228. |
| 26:Feb 2002!L213 | `=COUNT(C211:C227)` | extra_rows | The December turbine count range is stretched up into the blank row above the November header, so it no longer covers only the December acceptance dates in C212:C227. |
| 30:Hotlist - Identified !M67 | `=+M11+M22+M28+M37+M43+M65+M50+M55+M60` | wrong_reference | "SUBTOTAL" (M11) is used where "SUBTOTAL" (M6) belongs. |
| 30:Hotlist - Identified !Q67 | `=+Q11+Q22+Q28+Q37+Q43+Q65+Q50+Q55+Q60` | wrong_reference | "SUBTOTAL" (Q65) is used where "SUBTOTAL" (Q61) belongs. |
