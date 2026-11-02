# Held-out evaluation

| metric | value |
|---|---|
| errors | 32 |
| covered | 29 |
| found | 16 |
| missed | 13 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 2817 |
| flagged_windows | 249 |
| false_alarm_windows | 231 |
| recall_covered | 0.552 |
| recall_all | 0.5 |
| precision_windows | 0.072 |

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
| 11 | 10 | epsundevil | F10 | Wrong reference | missed |  |  |  |
| 12 | 11 | data | D13 | Wrong calculation | missed |  |  |  |
| 13 | 12 | curves | V10, V100, V101, V102, V103, V104, V105, | Wrong calculation | missed |  |  |  |
| 14 | 13 | sheet1 | H33 | Wrong calculation | found | extra_rows |  | The range is stretched up past the blank separator row into the 'Total' subtotal of the government-ban costs, so those 875 are counted again in the unusual-items total. |
| 15 | 13 | sheet1 | I35 | Wrong calculation | found | wrong_reference |  | "Total" (H33) is used where "Unusual loss from government ban of certain preservatives" (H32) belongs. |
| 16 | 13 | sheet1 | I38 | Wrong calculation | missed |  |  |  |
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | missed |  |  |  |
| 22 | 18 | crack spread option | M10, M11, M12, M13, M14, M9 | Wrong calculation | not_covered |  |  |  |
| 23 | 19 | may(2) | AE18, AE19, AE20, AE21, AE22, AE23, AE24 | Range error | found | skipped_rows |  | The SUM range stops short: DIRECT BILL belong to the same block but are left out. |
| 24 | 20 | sheet1 | D112 | Range error | missed |  |  |  |
| 25 | 21 | sheet1 (2) | F94 | Wrong calculation | missed |  |  |  |
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
| Range error | 11 | 4 | 0 | 0 |
| Wrong calculation | 2 | 6 | 0 | 2 |
| Wrong formula | 1 | 0 | 0 | 0 |
| Wrong reference | 2 | 1 | 0 | 0 |

## False alarms (231)

| id | formula | type | reason |
|---|---|---|---|
| 6:Real Time!J26 | `=J23+J15` | wrong_reference | "Sr. Specialist" (J15) is used where "Sr. Manager" (J12) belongs. |
| 6:Real Time!L122 | `=SUM(L118:L120)` | skipped_rows | The SUM range stops short: Billable Expense Clearing belong to the same block but are left out. |
| 6:Real Time!N122 | `=SUM(N118:N121)` | extra_rows | The Total Other Expenses range runs one row too far and picks up Billable Expense Clearing (N121), which is not an Other Expense line. |
| 6:Real Time!V122 | `=SUM(V118:V121)` | skipped_rows | The SUM range stops short: Corporate Rent (EPSC charges) belong to the same block but are left out. |
| 7:Preschedule!Z59 | `=SUM(Economics!D28:D45)` | skipped_rows | The SUM range stops short: Total belong to the same block but are left out. |
| 7:Preschedule!Z91 | `=Z89-Z90` | wrong_sign | "Total Costs:" (Z89) is subtracted here but should be added. |
| 7:Preschedule!Z94 | `=Z92-Z93` | wrong_sign | "Total Costs:" (Z92) is subtracted here but should be added. |
| 7:Preschedule!Z97 | `=Z95-Z96` | wrong_sign | "Total Costs:" (Z95) is subtracted here but should be added. |
| 7:Preschedule!Z100 | `=Z98-Z99` | wrong_sign | "Total Costs:" (Z98) is subtracted here but should be added. |
| 7:Preschedule!Z103 | `=Z101-Z102` | wrong_sign | "Total Costs:" (Z101) is subtracted here but should be added. |
| 7:Preschedule!M89 | `=M57` | wrong_reference | The x column of the Scratch Area row should pull the same row (56) from every column, as its peers K89, L89, N89 and O89 do, but this cell points one row down to M57, which breaks the row-33 offset pattern. |
| 7:Preschedule!M92 | `=#REF!` | wrong_reference | The 'Total Purchases' scratch row should carry forward the same source cell (M57) as its row peers K92, L92, N92 and O92, but this version points one row lower to M58. |
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
| 7:Deals!AD15 | `=SUM(F15:AC15)` | skipped_rows | The SUM range stops short: belong to the same block but are left out. |
| 7:Deals!AD120 | `=SUM(F120:AC120)` | skipped_rows | The SUM range stops short: belong to the same block but are left out. |
| 7:Deals!AD73 | `=SUM(E73:AC73)` | extra_rows | The Total Volume range is stretched one column left into E73, which is not a volume column, while every peer Total Volume formula in column AD sums only F:AC. |
| 7:Deals!F139 | `=D140-0.25` | wrong_reference | "D140" (D140) is used where "D139" (D139) belongs. |
| 7:Deals!F169 | `=D170-0.25` | wrong_reference | "D170" (D170) is used where "D169" (D169) belongs. |
| 7:Deals!AE142 | `=SUM(AE121:AE131)` | extra_rows | The 'Total per Model' subtotal for the EPE Purch from EPMI block should cover only rows 129-131, as its peer AD142 does, but the range is stretched up to row 121 and pulls in the PV rows that already belong to the main total in AE141. |
| 7:Deals!AD146 | `=SUM(AD132:AD133)` | skipped_rows | The SUM range stops short: leave this row blank belong to the same block but are left out. |
| 7:Fuel!C8 | `=J49` | wrong_reference | The 'Interstate Fixed Price (NM)' cell should pull the San Juan fixed price from J50, but it points one row up to J49, which is the Rio Grande fixed price already used by the 'Interstate Fixed Price (RG)' cell above. |
| 7:Economics!B6 | `=Balancing!L29` | wrong_reference | "Short" (Balancing!L29) is used where "Long" (Balancing!D29) belongs. |
| 7:Economics!C47 | `=SUM(C5:C45)` | skipped_rows | The SUM range stops short: SPS Avg. Cost Est. belong to the same block but are left out. |
| 8:Req-Chkist!Z30 | `=SUM(H26:L30,R26:V30,AB26:AF28)` | skipped_rows | The SUM range stops short: Right-of-Way, Inspection & X-ray belong to the same block but are left out. |
| 9:Feb01!Q34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:Mar01!V5 | `=SUM(D5:T5)` | skipped_rows | The SUM range stops short: SUBLETTE, HOLCOMB belong to the same block but are left out. |
| 9:Mar01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:Mar01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:Apr01!V5 | `=SUM(D5:T5)` | skipped_rows | The SUM range stops short: SUBLETTE, HOLCOMB belong to the same block but are left out. |
| 9:May 01!V5 | `=SUM(D5:T5)` | skipped_rows | The SUM range stops short: SUBLETTE, HOLCOMB belong to the same block but are left out. |
| 9:May 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:May 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:June 01!V5 | `=SUM(D5:T5)` | skipped_rows | The SUM range stops short: SUBLETTE, HOLCOMB belong to the same block but are left out. |
| 9:June 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B34" (B34) belongs. |
| 9:June 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:July 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:July 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:AUGUST 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:SEPT 01 !H39 | `=H5+H38` | wrong_sign | "SEPTEMBER CUMULATIVE" (H38) is added here but should be subtracted. |
| 9:OCT 01!Y34 | `=+B36` | wrong_reference | "B36" (B36) is used where "B35" (B35) belongs. |
| 9:OCT 01!AA34 | `=+F36` | wrong_reference | "F36" (F36) is used where "F35" (F35) belongs. |
| 9:OCT 01!AA35 | `=+F38` | wrong_reference | "VOLUME ADJ." (F38) is used where "(EST) BEGINNING BALANCE" (F36) belongs. |
| 11:Data!D5 | `=D13-D11` | wrong_reference | "Exchange Fee $/MMBtu" (D11) is used where "Exchange Fee $/MMBtu" (D12) belongs. |
| 12:Summary!F8 | `=F6+F7` | wrong_sign | "Total Payables as of Jan 25, 2002" (F7) is added here but should be subtracted. |
| 12:Summary!F13 | `=-AVERAGE(Exposure!F7:F12)` | skipped_rows | The AVERAGE range stops short: F13 belong to the same block but are left out. |
| 12:Summary!F15 | `=-AVERAGE(Exposure!H7:H11)` | skipped_rows | The AVERAGE range stops short: H12 belong to the same block but are left out. |
| 16:Sheet1!L42 | `=SUM(L36:L41)` | extra_rows | The Sta. #65 contract price total should add only the Fuel - %, Transport., ACA, GRI and GPS components, but the range now starts at L36 and pulls in the IF Index (1.86), which is not a price component. |
| 19:MAY(1)!AE46 | `=SUM(W46:AD46)` | skipped_rows | The SUM range stops short: DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL, DIRECT BILL belong to the same block but are left out. |
| 20:Sheet1!J68 | `=C68*E68` | missing_term | The VALUE for the 'ENE Bonus Phantom' row should be SHARES times the price spread (E68-F68), as in the peer rows, but the F68 term is dropped, so the formula returns the full SHARES amount instead of the spread. |
| 20:Sheet1!J84 | `=C84*E84` | missing_term | The VALUE for the GE long stock position should be shares times the price difference (E84-F84), as in the peer row 85 and the PROFIT/(LOSS) column, but the cost term F84 is dropped, so the formula returns the gross market value instead of the net value. |
| 20:Sheet1!J116 | `=C116*E116` | missing_factor | The VALUE for Am. Century Growth should be SHARES times the per-share gain (E116-F116), but the formula drops the F116 term and multiplies shares by the price alone, unlike the peer rows J117 and J118. |
| 20:Sheet1!M109 | `=K112` | wrong_reference | "TOTAL" (K112) is used where "Income Taxes due 2003" (K109) belongs. |
| 20:Sheet1!C112 | `=SUM(C53:C65)+C32+C38+C45+C48+C49+C50` | skipped_rows | The SUM range stops short: Cash, Muni Bonds, Govt. paper, ENE jan 02 35 calls, ENE jan 02 40 calls belong to the same block but are left out. |
| 20:Sheet1!M112 | `=SUM(K45:K65)+K32+K38` | skipped_rows | The SUM range stops short: Stable Asset, Stable Asset belong to the same block but are left out. |
| 20:Sheet1!M136 | `=M102` | wrong_reference | "cash value 9859605" (M102) is used where "cash value 9859605" (M103) belongs. |
| 20:Sheet1!M143 | `=SUM(K116:K138)+K112` | skipped_rows | The SUM range stops short: ENE 1/18/07 (0%) 122617 belong to the same block but are left out. |
| 20:Sheet1!G149 | `=SUM(G112:G147)` | extra_rows | The TOTAL range is stretched up into the 'TOTAL' subtotal row (G112), so the ENE Stock mark-to-market total picks up the prior block's subtotal instead of starting at the first blank separator row. |
| 20:Sheet1!J149 | `=SUM(J112:J147)` | extra_rows | The SUM range reaches into "TOTAL" (J112), which is not part of the block. |
| 20:Sheet1!M149 | `=SUM(K129:K146)+M112` | skipped_rows | The SUM range stops short: TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL, TOTAL belong to the same block but are left out. |
| 20:unvested!E4 | `=SUM(C25:C25)+C33` | skipped_rows | The SUM range stops short: options, options, options, options, options, restricted stock belong to the same block but are left out. |
| 21:Sheet1!F92 | `=SUM(E86:E91)` | skipped_rows | The SUM range stops short: , , , , ,  belong to the same block but are left out. |
| 21:Sheet1!E105 | `=+E103+E92` | wrong_reference | "(Retro billed March 20, 2001)" (E92) is used where "E93" (E93) belongs. |
| 21:Sheet1!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short:  belong to the same block but are left out. |
| 21:Sheet1!H117 | `=D117` | missing_term | The 'TW Gives Up & No Interest 6 Months Back' amount should be the 'Amt in Dispute' (D117) minus the '6 Months Back' interest (G117), but the broken formula drops the G117 term and just repeats D117, unlike the peer row H115 (=D115-G115). |
| 21:Sheet1!E118 | `=D118` | missing_factor | The 'Split Retro-active Amount 50/50' column should halve the 'Amt in Dispute' amount, but this cell copies D118 without dividing by 2, unlike the peer row E114 (=D114/2). |
| 21:Sheet1 (2)!H115 | `=D115` | missing_factor | The 'TW Gives Up' amount should be the 'Amt in Dispute' (D115) multiplied by the '6 Months Back & No Interest' rate (G115), but the rate factor is dropped, so the cell just repeats the dispute amount. |
| 21:Sheet1 (2)!E105 | `=+E103+E92` | wrong_reference | "(Retro billed March 20, 2001)" (E92) is used where "E93" (E93) belongs. |
| 21:Sheet1 (2)!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short: 51828.2, 40635.9, 46607.7, 43796.6, 45280.4 belong to the same block but are left out. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: 'ENA IS'!C21 belong to the same block but are left out. |
| 23:Europe Burn!E26 | `=SUM(E23:E25)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in E23, which is not an expense line. |
| 23:Europe Burn!K26 | `=SUM(K23:K25)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was extended up to include the 'Total' row (K23), which is the sum of the expense lines above. |
| 23:Europe Burn!M26 | `=SUM(M23:M25)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in M23, which is a separate line. |
| 23:Europe Burn!O26 | `=SUM(O23:O25)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should cover only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was extended up to include the 'Total' row, which is a separate subtotal. |
| 23:Europe Burn!Q26 | `=SUM(Q23:Q25)` | wrong_sign | "Depreciation & Amortization" (Q24) is added here but should be subtracted. |
| 23:Europe Burn!E30 | `=-E24` | wrong_sign | "Depreciation & Amortization" (E24) is subtracted here but should be added. |
| 23:Europe Burn!G30 | `=-G24` | wrong_sign | "Depreciation & Amortization" (G24) is subtracted here but should be added. |
| 23:Europe Burn!I30 | `=-I24` | wrong_sign | "Depreciation & Amortization" (I24) is subtracted here but should be added. |
| 23:Europe Burn!K30 | `=-K24` | wrong_sign | "Depreciation & Amortization" (K24) is subtracted here but should be added. |
| 23:Europe Burn!M30 | `=-M24` | wrong_sign | "Depreciation & Amortization" (M24) is subtracted here but should be added. |
| 23:Europe Burn!O30 | `=-O24` | wrong_sign | "Depreciation & Amortization" (O24) is subtracted here but should be added. |
| 23:Europe Burn!Q30 | `=-Q24` | wrong_reference | "Depreciation & Amortization" (Q24) is used where "Total Expenses net of Capitalized Expense" (Q26) belongs. |
| 23:Europe Burn!E33 | `=E26+E28+E29+E30` | wrong_reference | "Less: DD&A" (E30) is used where "Total Cash Burn Rate" (E31) belongs. |
| 23:Europe Burn!G33 | `=+G26+G28+G31` | missing_term | "Other Cash Payments" (G29) should be added here but is left out. |
| 23:Europe Burn!I33 | `=+I26+I28+I31` | missing_term | "Other Cash Payments" (I29) should be added here but is left out. |
| 23:Europe Burn!K33 | `=+K26+K28+K31` | missing_term | "Other Cash Payments" (K29) should be added here but is left out. |
| 23:Europe Burn!M33 | `=+M26+M28+M31` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (M29) and Less: DD&A (M30), unlike the peer total in K33. |
| 23:Europe Burn!O33 | `=+O26+O28+O31` | missing_term | "Other Cash Payments" (O29) should be added here but is left out. |
| 23:Europe Burn!Q33 | `=+Q26+Q28+Q31` | missing_term | "Other Cash Payments" (Q29) should be added here but is left out. |
| 23:ENA Burn!E20 | `=SUM(E17:E19)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should cover only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in E17, which is not an expense line. |
| 23:ENA Burn!Q20 | `=SUM(Q17:Q19)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in Q17, which is not an expense line. |
| 23:ENA Burn!E24 | `=-E18` | wrong_sign | "Depreciation & Amortization" (E18) is subtracted here but should be added. |
| 23:ENA Burn!G24 | `=-G18` | wrong_sign | "Depreciation & Amortization" (G18) is subtracted here but should be added. |
| 23:ENA Burn!K24 | `=-K18` | wrong_sign | "Depreciation & Amortization" (K18) is subtracted here but should be added. |
| 23:ENA Burn!M24 | `=-M18` | wrong_sign | "Depreciation & Amortization" (M18) is subtracted here but should be added. |
| 23:ENA Burn!O24 | `=-O18` | wrong_sign | "Depreciation & Amortization" (O18) is subtracted here but should be added. |
| 23:ENA Burn!Q24 | `=-Q18` | wrong_sign | "Depreciation & Amortization" (Q18) is subtracted here but should be added. |
| 23:ENA Burn!E27 | `=E20+E22+E23+E24` | wrong_reference | "Less: DD&A" (E24) is used where "Less: Taxes Other Than Income" (E25) belongs. |
| 23:ENA Burn!G27 | `=+G20+G22+G25` | missing_term | "Other Cash Payments" (G23) should be added here but is left out. |
| 23:ENA Burn!I27 | `=+I20+I22+I25` | missing_term | "Other Cash Payments" (I23) should be added here but is left out. |
| 23:ENA Burn!K27 | `=+K20+K22+K25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:ENA Burn!M27 | `=+M20+M22+M25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:ENA Burn!O27 | `=+O20+O22+O25` | missing_term | "Less: DD&A" (O24) should be added here but is left out. |
| 23:ENA Burn!Q27 | `=+Q20+Q22+Q25` | missing_term | "Other Cash Payments" (Q23) should be added here but is left out. |
| 23:EGM Burn!E18 | `=SUM(E15:E17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in E15, which is a separate line. |
| 23:EGM Burn!G18 | `=SUM(G15:G17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in G15, which already sums the expense lines above. |
| 23:EGM Burn!I18 | `=SUM(I15:I17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in I15, which is already the sum of the expense lines. |
| 23:EGM Burn!K18 | `=SUM(K15:K17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was extended up to include the 'Total' subtotal in K15, which is not an expense line. |
| 23:EGM Burn!M18 | `=SUM(M15:M17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was extended up to include the 'Total' subtotal in M15, which is not an expense line. |
| 23:EGM Burn!Q18 | `=SUM(Q15:Q17)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in Q15, which is not an expense line. |
| 23:EGM Burn!E22 | `=-E16` | wrong_sign | "Depreciation & Amortization" (E16) is subtracted here but should be added. |
| 23:EGM Burn!G22 | `=-G16` | wrong_sign | "Depreciation & Amortization" (G16) is subtracted here but should be added. |
| 23:EGM Burn!M22 | `=-M16` | wrong_sign | "Depreciation & Amortization" (M16) is subtracted here but should be added. |
| 23:EGM Burn!O22 | `=-O16` | wrong_sign | "Depreciation & Amortization" (O16) is subtracted here but should be added. |
| 23:EGM Burn!Q22 | `=-Q16` | wrong_sign | "Depreciation & Amortization" (Q16) is subtracted here but should be added. |
| 23:EGM Burn!E25 | `=E18+E20+E21+E22` | wrong_reference | "Other Cash Payments" (E21) is used where "Other Cash Payments" (E23) belongs. |
| 23:EGM Burn!G25 | `=+G18+G20+G23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments, Less: DD&A and the October amount in G23, but the formula leaves out Other Cash Payments (G21) and Less: DD&A (G22), unlike the peer total in E25. |
| 23:EGM Burn!I25 | `=+I18+I20+I23` | missing_term | "Less: DD&A" (I22) should be added here but is left out. |
| 23:EGM Burn!K25 | `=+K18+K20+K23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms, unlike the peer totals in I25 and M25. |
| 23:EGM Burn!M25 | `=+M18+M20+M23` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EGM Burn!O25 | `=+O18+O20+O23` | missing_term | "Less: DD&A" (O22) should be added here but is left out. |
| 23:EGM Burn!Q25 | `=+Q18+Q20+Q23` | missing_term | "Less: DD&A" (Q22) should be added here but is left out. |
| 23:EGS Burn!X4 | `=2.9*1.15+0.6-0.1` | wrong_reference | "*" (2.9) is used where "*" (3.9) belongs. |
| 23:EIM Burn!E15 | `=SUM(E12:E14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in E12, which is already the sum of the mill rows above. |
| 23:EIM Burn!G15 | `=SUM(G12:G14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in G12, which is already the sum of the expense lines above. |
| 23:EIM Burn!I15 | `=SUM(I12:I14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in I12, which is also used in the grand total in I22. |
| 23:EIM Burn!M15 | `=SUM(M12:M14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was extended up to include the 'Total' subtotal in M12, which is already the sum of the expense lines above. |
| 23:EIM Burn!O15 | `=SUM(O12:O14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in O12, which is already the sum of the expense lines above. |
| 23:EIM Burn!Q15 | `=SUM(Q12:Q14)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in Q12, which is already the sum of the expense lines. |
| 23:EIM Burn!E19 | `=-E13` | wrong_sign | "Depreciation & Amortization" (E13) is subtracted here but should be added. |
| 23:EIM Burn!G19 | `=-G13` | wrong_sign | "Depreciation & Amortization" (G13) is subtracted here but should be added. |
| 23:EIM Burn!K19 | `=-K13` | wrong_sign | "Depreciation & Amortization" (K13) is subtracted here but should be added. |
| 23:EIM Burn!O19 | `=-O13` | wrong_sign | "Depreciation & Amortization" (O13) is subtracted here but should be added. |
| 23:EIM Burn!Q19 | `=-Q13` | wrong_reference | "Depreciation & Amortization" (Q13) is used where "Total Expenses net of Capitalized Expense" (Q15) belongs. |
| 23:EIM Burn!E22 | `=E15+E17+E18+E19` | wrong_reference | "Other Cash Payments" (E18) is used where "Other Cash Payments" (E20) belongs. |
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
| 23:EBS Burn!E17 | `=E10+E12+E13+E14` | wrong_reference | "Other Cash Payments" (E13) is used where "Other Cash Payments" (E15) belongs. |
| 23:EBS Burn!G17 | `=+G10+G12+G15` | missing_term | "Other Cash Payments" (G13) should be added here but is left out. |
| 23:EBS Burn!I17 | `=+I10+I12+I15` | missing_term | "Other Cash Payments" (I13) and "Less: DD&A" (I14) should be added here but are left out. |
| 23:EBS Burn!K17 | `=+K10+K12+K15` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms, unlike the peer totals in I17 and M17. |
| 23:EBS Burn!M17 | `=+M10+M12+M15` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EBS Burn!O17 | `=+O10+O12+O15` | missing_term | "Less: DD&A" (O14) should be added here but is left out. |
| 23:EBS Burn!Q17 | `=+Q10+Q12+Q15` | missing_term | "Other Cash Payments" (Q13) should be added here but is left out. |
| 23:ENW Burn!E13 | `=SUM(E10:E12)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' row (E10), which is a separate subtotal. |
| 23:ENW Burn!E17 | `=-E11` | wrong_sign | "Depreciation & Amortization" (E11) is subtracted here but should be added. |
| 23:ENW Burn!G17 | `=-G11` | wrong_sign | "Depreciation & Amortization" (G11) is subtracted here but should be added. |
| 23:ENW Burn!K17 | `=-K11` | wrong_sign | "Depreciation & Amortization" (K11) is subtracted here but should be added. |
| 23:ENW Burn!M17 | `=-M11` | wrong_sign | "Depreciation & Amortization" (M11) is subtracted here but should be added. |
| 23:ENW Burn!O17 | `=-O11` | wrong_sign | "Depreciation & Amortization" (O11) is subtracted here but should be added. |
| 23:ENW Burn!Q17 | `=-Q11` | wrong_reference | "Depreciation & Amortization" (Q11) is used where "Total Expenses net of Capitalized Expense" (Q13) belongs. |
| 23:ENW Burn!E20 | `=E13+E15+E16+E17` | wrong_reference | "Other Cash Payments" (E16) is used where "Other Cash Payments" (E18) belongs. |
| 23:ENW Burn!G20 | `=+G13+G15+G18` | missing_term | "Other Cash Payments" (G16) should be added here but is left out. |
| 23:ENW Burn!I20 | `=+I13+I15+I18` | missing_term | "Other Cash Payments" (I16) and "Less: DD&A" (I17) should be added here but are left out. |
| 23:ENW Burn!K20 | `=+K13+K15+K18` | missing_term | "Other Cash Payments" (K16) and "Less: DD&A" (K17) should be added here but are left out. |
| 23:ENW Burn!M20 | `=+M13+M15+M18` | missing_term | "Other Cash Payments" (M16) and "Less: DD&A" (M17) should be added here but are left out. |
| 23:ENW Burn!O20 | `=+O13+O15+O18` | missing_term | "Other Cash Payments" (O16) should be added here but is left out. |
| 23:ENW Burn!Q20 | `=+Q13+Q15+Q18` | missing_term | "Other Cash Payments" (Q16) should be added here but is left out. |
| 23:EES Burn!E20 | `=SUM(E17:E19)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should cover only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in E17, which is already summed in the grand total. |
| 23:EES Burn!O20 | `=SUM(O17:O19)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in O17, which is already the sum of the expense lines. |
| 23:EES Burn!Q20 | `=SUM(Q17:Q19)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only 'Depreciation & Amortization' and 'Taxes Other Than Income', but the range was stretched up to include the 'Total' subtotal in Q17, which is already the sum of the expense lines. |
| 23:EES Burn!E24 | `=-E18` | wrong_sign | "Depreciation & Amortization" (E18) is subtracted here but should be added. |
| 23:EES Burn!G24 | `=-G18` | wrong_sign | "Depreciation & Amortization" (G18) is subtracted here but should be added. |
| 23:EES Burn!I24 | `=-I18` | wrong_sign | "Depreciation & Amortization" (I18) is subtracted here but should be added. |
| 23:EES Burn!K24 | `=-K18` | wrong_sign | "Depreciation & Amortization" (K18) is subtracted here but should be added. |
| 23:EES Burn!M24 | `=-M18` | wrong_sign | "Depreciation & Amortization" (M18) is subtracted here but should be added. |
| 23:EES Burn!O24 | `=-O18` | wrong_sign | "Depreciation & Amortization" (O18) is subtracted here but should be added. |
| 23:EES Burn!Q24 | `=-Q18` | wrong_reference | "Depreciation & Amortization" (Q18) is used where "Total Expenses net of Capitalized Expense" (Q20) belongs. |
| 23:EES Burn!E27 | `=E20+E22+E23+E24` | wrong_reference | "Less: DD&A" (E24) is used where "Taxes Other Than Income" (E25) belongs. |
| 23:EES Burn!G27 | `=+G20+G22+G25` | missing_term | "Other Cash Payments" (G23) should be added here but is left out. |
| 23:EES Burn!I27 | `=+I20+I22+I25` | missing_term | "Other Cash Payments" (I23) should be added here but is left out. |
| 23:EES Burn!K27 | `=+K20+K22+K25` | missing_term | "Other Cash Payments" (K23) should be added here but is left out. |
| 23:EES Burn!M27 | `=+M20+M22+M25` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out the Other Cash Payments and Less: DD&A terms. |
| 23:EES Burn!O27 | `=+O20+O22+O25` | missing_term | "Less: DD&A" (O24) should be added here but is left out. |
| 23:EES Burn!Q27 | `=+Q20+Q22+Q25` | missing_term | "Other Cash Payments" (Q23) should be added here but is left out. |
| 23:EPI Burn!E8 | `=SUM(E5:E7)` | extra_rows | The 'Total Expenses net of Capitalized Expense' subtotal should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in E5, which already sums the Analysts/Associates line. |
| 23:EPI Burn!O8 | `=SUM(O5:O7)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should cover only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in O5, which is not an expense line. |
| 23:EPI Burn!Q8 | `=SUM(Q5:Q7)` | extra_rows | The 'Total Expenses net of Capitalized Expense' total should add only Depreciation & Amortization and Taxes Other Than Income, but the range was stretched up to include the 'Total' subtotal in Q5, which already sums Analysts/Associates. |
| 23:EPI Burn!E12 | `=-E6` | wrong_sign | "Depreciation & Amortization" (E6) is subtracted here but should be added. |
| 23:EPI Burn!G12 | `=-G6` | wrong_sign | "Depreciation & Amortization" (G6) is subtracted here but should be added. |
| 23:EPI Burn!I12 | `=-I6` | wrong_sign | "Depreciation & Amortization" (I6) is subtracted here but should be added. |
| 23:EPI Burn!K12 | `=-K6` | wrong_sign | "Depreciation & Amortization" (K6) is subtracted here but should be added. |
| 23:EPI Burn!M12 | `=-M6` | wrong_sign | "Depreciation & Amortization" (M6) is subtracted here but should be added. |
| 23:EPI Burn!O12 | `=-O6` | wrong_reference | "Depreciation & Amortization" (O6) is used where "Total Expenses net of Capitalized Expense" (O8) belongs. |
| 23:EPI Burn!Q12 | `=-Q6` | wrong_reference | "Depreciation & Amortization" (Q6) is used where "Total Expenses net of Capitalized Expense" (Q8) belongs. |
| 23:EPI Burn!E15 | `=E8+E10+E11+E12` | wrong_reference | "Other Cash Payments" (E11) is used where "Other Cash Payments" (E13) belongs. |
| 23:EPI Burn!G15 | `=+G8+G10+G13` | missing_term | "Other Cash Payments" (G11) should be added here but is left out. |
| 23:EPI Burn!I15 | `=+I8+I10+I13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (I11) and Less: DD&A (I12), unlike the peer total in G15. |
| 23:EPI Burn!K15 | `=+K8+K10+K13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (K11) and Less: DD&A (K12), unlike the peer totals in I15 and M15. |
| 23:EPI Burn!M15 | `=+M8+M10+M13` | missing_term | The Total Cash Burn Rate should add Total Expenses net of Capitalized Expense, Plus: Capital Expenditures, Other Cash Payments and Less: DD&A, but the formula leaves out Other Cash Payments (M11) and Less: DD&A (M12), unlike the peer total in K15. |
| 23:EPI Burn!O15 | `=+O8+O10+O13` | missing_term | "Less: DD&A" (O12) should be added here but is left out. |
| 23:EPI Burn!Q15 | `=+Q8+Q10+Q13` | missing_term | "Other Cash Payments" (Q11) and "Less: DD&A" (Q12) should be added here but are left out. |
| 23:ENA BS!B21 | `=+B19+B20+B18+B17+B13+B12` | missing_term | "Investments" (B15) should be added here but is left out. |
| 24:Legacy!H36 | `=Description!$I$34` | wrong_reference | "SDGE" (Description!$I$34) is used where "SDGE" (Description!$I$36) belongs. |
| 24:New!H36 | `=Description!$I$34` | wrong_reference | "SDGE" (Description!$I$34) is used where "SDGE" (Description!$I$36) belongs. |
| 25:external!E38 | `=+E37` | wrong_reference | The BURN GAS VOLUMES running total for the last day should carry forward the previous day's total in E36, but it points one row down to E37, which breaks the chain of =+E34, =+E35, =+E36 that the column uses. |
| 25:external!E12 | `=3025+1472` | wrong_sign | "DAY AHEAD" (1472) is added here but should be subtracted. |
| 25:external!F36 | `=(D36-E36)+F34` | wrong_reference | "F34" (F34) is used where "F35" (F35) belongs. |
| 26:Nov 2001!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!F42 | `=F74` | wrong_reference | The Trent Mesa turbine's availability should pull the weighted average from the row directly above it (F73), but it points one row too far down to F74, which is the next turbine's value. |
| 26:Dec 2001!G45 | `=SUM(G25:G44)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G150 | `=SUM(G50:G149)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G201 | `=SUM(G195:G200)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!F135 | `=AVERAGE(F35:F134)` | wrong_function | "Average" calls for SUM, but the formula uses AVERAGE. |
