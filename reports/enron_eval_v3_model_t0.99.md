# Held-out evaluation

| metric | value |
|---|---|
| errors | 32 |
| covered | 29 |
| found | 22 |
| missed | 7 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 2817 |
| flagged_windows | 174 |
| false_alarm_windows | 137 |
| recall_covered | 0.759 |
| recall_all | 0.688 |
| precision_windows | 0.213 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | sheet1 | F28, G28 | Range error | found | skipped_rows | yes | The SUM range stops short: Enron belong to the same block but are left out. |
| 2 | 2 | sheet1 | I34 | Range error | found | skipped_rows | yes | The SUM range stops short: he 6 belong to the same block but are left out. |
| 3 | 3 | bmspt066 | W43 | Range error | found | skipped_rows |  | The SUM range stops short: Estimated, Estimated, Estimated, Estimated, Estimated, Projected belong to the same block but are left out. |
| 4 | 3 | bmspt066 | C43, D43, E43, F43, G43, H43, I43, J43,  | Range error | found | skipped_rows |  | The SUM range stops short: Estimated belong to the same block but are left out. |
| 5 | 4 | sheet1 | L16 | Range error | found | extra_rows | yes | The Summer 04 Transco Z5 average should cover only the seven Transco Z5 monthly values in H46:H52, but the range now starts two columns early and pulls in the Transco Z4 values from F46:G52, unlike the peer averages in L14, L15 and L17, which each average a single column. |
| 6 | 5 | jul01 | AL44 | Range error | found | extra_rows | yes | The Management Services Fee TOTAL range starts one row too high and pulls in the 'Price' rate in AL11 (0.115), which is not a daily fee amount, while the peer totals in AJ44 and AN44 start at row 12. |
| 7 | 6 | real time | V23 | Range error | missed |  |  |  |
| 8 | 7 | deals | AD142 | Range error | found | skipped_rows |  | The SUM range stops short: PV, PV, PV, PV, PV, PV, PV, PV belong to the same block but are left out. |
| 9 | 8 | cost estimate summary | L23 | Range error | found | skipped_rows | yes | The SUM range stops short: Gallup CS Mods belong to the same block but are left out. |
| 10 | 9 | oct 01 | T39 | Wrong formula | found | wrong_reference |  | "VOLUME ADJ." (N38) is used where "OC TOBER CUMULATIVE" (N39) belongs. |
| 11 | 10 | epsundevil | F10 | Wrong reference | found | wrong_reference | yes | "Added Compression" (D5) is used where "Added Compression" (D10) belongs. |
| 12 | 11 | data | D13 | Wrong calculation | found | wrong_reference |  | "Cash target" (C6) is used where "tot volume" (C13) belongs. |
| 13 | 12 | curves | V10, V100, V101, V102, V103, V104, V105, | Wrong calculation | missed |  |  |  |
| 14 | 13 | sheet1 | H33 | Wrong calculation | found | extra_rows |  | The range is stretched up past the blank separator row H29 into the prior block's 'Total' subtotal in H28, so that subtotal is counted again in the unusual items total. |
| 15 | 13 | sheet1 | I35 | Wrong calculation | found | wrong_reference |  | "Total" (H33) is used where "Unusual loss from government ban of certain preservatives" (H35) belongs. |
| 16 | 13 | sheet1 | I38 | Wrong calculation | found | wrong_reference |  | "Extraordinary loss due to tornado damage" (H36) is used where "Income before extraordinary items and effect of accounting c" (H35) belongs. |
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | found | wrong_operator |  | Parentheses are missing: "B12/C13" must be computed before multiplying by B12. |
| 22 | 18 | crack spread option | M10, M11, M12, M13, M14, M9 | Wrong calculation | not_covered |  |  |  |
| 23 | 19 | may(2) | AE18, AE19, AE20, AE21, AE22, AE23, AE24 | Range error | found | missing_term |  | The NET FOUR CORNERS total should cover both DIRECT BILL bookout columns V and W, but the range stops at V18 and drops W18, which holds -125. The peer rows still sum V:W. |
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
| 36 | 30 | hotlist - identified | M22, M37 | Range error | found | skipped_rows |  | The SUM range stops short: M&G - UK, Cline-Panther Call Option, Bremen - Germany, Coellerici (2), Project Springbok, ETOL-UK, Origination & Finance belong to the same block but are left out. |

## By category

| category | found | missed | unsupported | not covered |
|---|---|---|---|---|
| File reference not working | 0 | 1 | 0 | 0 |
| Fixed Value | 0 | 0 | 0 | 1 |
| Formula: = SUM(D8*E8) | 0 | 1 | 0 | 0 |
| Range error | 13 | 2 | 0 | 0 |
| Wrong calculation | 5 | 3 | 0 | 2 |
| Wrong formula | 1 | 0 | 0 | 0 |
| Wrong reference | 3 | 0 | 0 | 0 |

## False alarms (137)

| id | formula | type | reason |
|---|---|---|---|
| 2:Sheet1!I8 | `=G8*H8` | missing_factor | The product leaves out "he 6" (0.7), which the neighbouring cells apply. |
| 3:BMSPT066!L6 | `=L5*30` | wrong_reference | "HPLC Total" (L5) is used where "HPLC Total" (L5) belongs. |
| 3:BMSPT066!Q6 | `=+'[2]BAM-EGS'!$BC$9+'[3]BAM-EGS'!$BC$9` | wrong_reference | The ECT FIRST OF THE MONTH total should add the two BAM-EGS counterparties, but the first reference points one sheet too far to '[2]BAM-EGS' instead of '[1]BAM-EGS', so the same counterparty is counted twice. |
| 3:BMSPT066!J8 | `=SUM(H8:I8)` | missing_term | The HPLC Total in J8 should add the E8 'Total' column to the HPL FIXED PRICE columns H8:I8, as the peer TOTAL in K8 does, but the E8 term is left out. |
| 3:BMSPT066!L9 | `=((L$6)-SUM(L$8:L8))/($A$38-$A8)` | skipped_rows | The Scheduled volume for day 2 should subtract the Beginning Balance plus the day-1 Scheduled volume, but the range stops at L8 and leaves out the day-1 Scheduled amount in L9, unlike the peer formulas in M9 and L10. |
| 3:BMSPT066!Y40 | `=X40*AA42` | wrong_reference | "Variances:" (AA42) is used where "Fuel:" (AA39) belongs. |
| 3:BMSPT066!K44 | `=SUM([5]BMSPT066!$K$34:$K$37)+SUM(K8:K10)` | skipped_rows | The 'April 28 thru May 4' total should cover all five weekly rows K34:K38, but the range stops at K37 and drops the last 'Projected' row K38, while the peer totals in K45 and K46 each sum five rows. |
| 3:BMSPT066!W46 | `=+W45-W43` | wrong_reference | "Total Projected" (W43) is used where "Total" (W44) belongs. |
| 3:BMSPT066!K47 | `=SUM(K25:K31)` | extra_rows | The weekly TOTAL for the 'May 12 thru May 18' week should cover only the six Scheduled rows K25:K30, but the range runs one row too far into K31, the first Estimated row of the next week. |
| 5:jul01!C4 | `=C5*(1+C3)` | wrong_sign | "Shrink" (C3) is added here but should be subtracted. |
| 5:jul01!AN12 | `=AJ12+AI12+AG12+AF12` | missing_term | "$" (AH12) should be added here but is left out. |
| 5:jul01!AQ44 | `=AP44*C7` | wrong_reference | "$/MMBtu" (C7) is used where "$/MMBtu" (C6) belongs. |
| 5:jul01!AS44 | `=AL44+AN44-AQ44` | wrong_sign | "TOTAL" (AQ44) is subtracted here but should be added. |
| 5:jul01!AQ45 | `=AP45*C6` | wrong_reference | "$/MMBtu/Mo" (C6) is used where "$/MMBtu/Mo" (C7) belongs. |
| 6:Real Time!C24 | `=SUM(C11,C12,C13,C14,C15,C16,C19,C20,C21)` | missing_term | "Associate" (C17) should be added here but is left out. |
| 6:Real Time!J26 | `=J23+J15` | wrong_reference | "Sr. Specialist" (J15) is used where "Specialist" (J16) belongs. |
| 6:Real Time!J29 | `=SUM(J26:J28)` | extra_rows | The total of Merit Increase and Prom, Equity, Increase should cover only J27:J28, but the range now starts at J26 and adds the Jan base salary (=J23+J15), which is not an increase. |
| 6:Real Time!N29 | `=+(N26*1.0425)*11` | wrong_reference | "Jan" (N26) is used where "Feb - Dec" (N26) belongs. |
| 6:Real Time!V29 | `=+(V26*1.0425)*11` | wrong_reference | "Jan" (V26) is used where "Total Headcount." (V23) belongs. |
| 6:Real Time!H68 | `=+H67+H66+H65` | wrong_reference | "Total Travel" (H65) is used where "Travel:" (H60) belongs. |
| 6:Real Time!N122 | `=SUM(N118:N121)` | extra_rows | The Total Other Expenses range runs one row too far and pulls in the Billable Expense Clearing line (N121), which is not an Other Expense. |
| 7:Preschedule!AA61 | `=AA59` | wrong_reference | "AA59" (AA59) is used where "Position" (AA58) belongs. |
| 7:Preschedule!Z128 | `=Z125-Z127` | wrong_sign | "Total Costs:" (Z125) is added here but should be subtracted. |
| 7:Preschedule!Z148 | `=Z145-Z147` | wrong_sign | "Total Costs:" (Z145) is added here but should be subtracted. |
| 7:Deals!D23 | `=F139` | wrong_reference | "MST" (F139) is used where "MST" (F138) belongs. |
| 7:Deals!D48 | `=F169` | wrong_reference | "MST" (F169) is used where "MST" (F168) belongs. |
| 7:Deals!F139 | `=D140-0.25` | wrong_reference | "D140" (D140) is used where "D139" (D139) belongs. |
| 7:Deals!F169 | `=D170-0.25` | wrong_reference | "D170" (D170) is used where "D169" (D169) belongs. |
| 7:Deals!AE142 | `=SUM(AE121:AE131)` | extra_rows | The EPE Purch from EPMI subtotal should cover only the three EPE rows 129–131, but the range starts at row 121 and pulls in the PV rows 121–127, which are already counted in the main Total Billing subtotal at AE141. |
| 7:Deals!AD146 | `=SUM(AD132:AD133)` | skipped_rows | The SUM range stops short: leave this row blank belong to the same block but are left out. |
| 7:Fuel!C7 | `=J49` | wrong_reference | "Variable Price" (J49) is used where "Fixed Price" (J48) belongs. |
| 7:Fuel!G7 | `=K49` | wrong_reference | "Variable Price" (K49) is used where "Fixed Price" (K48) belongs. |
| 7:Fuel!C8 | `=J49` | wrong_reference | "Variable Price" (J49) is used where "Variable Price" (J50) belongs. |
| 7:Fuel!F12 | `=(D12*$C$6)+(C12*$C$7)` | wrong_reference | "Interstate Fixed Price (RG)" (C7) is used where "Interstate Fixed Price (Intrastate)" (C8) belongs. |
| 7:Fuel!F18 | `=C18*G7+D18*G6` | wrong_reference | The weighted average of the Copper % Fixed and % Spot shares should multiply % Fixed by the Intrastate Spot Price (G6) and % Spot by the Intrastate Fixed Price (G7), but the references are swapped, unlike the peer rows F12:F14. |
| 7:Fuel!E32 | `=E15+E18+E30` | wrong_reference | "Copper" (E18) is used where "Total" (E17) belongs. |
| 7:Fuel!G44 | `=SUM(G38:G43)` | wrong_function | "Supplier" calls for AVERAGE, but the formula uses SUM. |
| 7:Fuel!J50 | `=J46*(1+J47)/(1-J48)+J49` | wrong_reference | "Gross Receipts Tax" (J46) is used where "W.A. Base Price" (J45) belongs. |
| 8:Cost Estimate Summary!L14 | `=I14*28000*1.1*G14` | wrong_operator | The formula multiplies "Size (\")" (I14) by 28000 where an exponent is intended. |
| 9:MANUAL!W33 | `=SUM(E20,J20,O20:P20,T20,Y7,Y13,Y20,E42,J42)` | missing_term | "O42" (O42) should be added here but is left out. |
| 9:MANUAL!E42 | `=SUM(E29:E41)` | skipped_rows | The SUM range stops short: FIN 1, FIN 2 belong to the same block but are left out. |
| 9:MANUAL!J42 | `=SUM(J29:J41)` | skipped_rows | The SUM range stops short: HASKELL, LIBERAL belong to the same block but are left out. |
| 9:Apr01!AB5 | `=+F6` | wrong_reference | The PVR column should pull the PVR value from column E, but this version points one column over to F6, which is the BUSHTON PVR value that the next column (AC) already uses. |
| 9:May 01!AB5 | `=+F6` | wrong_reference | The PVR cell should pull the PVR value from column E, but it points one column over to F6, which is the BUSHTON PVR value that the next column AC5 already uses. |
| 9:May 01!H38 | `=SUM(H6:H36)+H37` | double_count | The VOLUME ADJ. row (H37) is already inside the summed range H6:H36, so adding it again counts the volume adjustment twice in the APR. CUMULATIVE total. |
| 9:June 01!AA5 | `=+F6` | wrong_reference | The HUGO TOTAL cell should pull the HUGO column (E), but it points one column over to F6, which is the BUSHTON PVR value that the PVR TOTAL cell already uses. |
| 9:June 01!AB5 | `=+F6` | wrong_reference | The PVR column should pull the PVR value from E6, but this version points one column over to F6, which is the BUSHTON PVR value that the MULL column already uses. |
| 9:June 01!T38 | `=SUM(T6:T36)+T37` | double_count | The VOLUME ADJ. row (T37) is already inside the summed range T6:T36, so adding it again counts the volume adjustment twice in the MAY CUMULATIVE total. |
| 9:July 01!V5 | `=SUM(D5:T5)` | extra_rows | The TOTAL DEVIATION range is stretched left into the 'TOTAL DEVIATION' subtotal cell D5 (=B5+C5), so the SUBLETTE and HOLCOMB beginning balances are counted a second time in the total. |
| 9:July 01!P38 | `=SUM(P6:P36)+P37` | double_count | The VOLUME ADJ. amount in P37 is already inside the summed range P6:P36, so adding it again counts it twice in the JULY CUMULATIVE total. |
| 9:July 01!T38 | `=SUM(T6:T36)+T37` | double_count | The VOLUME ADJ. row (T37) is already inside the summed range T6:T36, so adding it again counts it twice in the JULY CUMULATIVE total. |
| 9:AUGUST 01!V5 | `=SUM(D5:T5)` | extra_rows | The SUM range reaches into "TOTAL DEVIATION" (D5), which is not part of the block. |
| 9:AUGUST 01!J38 | `=SUM(J6:J36)+J37` | double_count | The VOLUME ADJ. amount in J37 is already inside the summed range J6:J36, so adding it again counts it twice in the AUGUST CUMULATIVE total. |
| 9:AUGUST 01!B39 | `=B5+B38` | wrong_sign | "AUGUST CUMULATIVE" (B38) is added here but should be subtracted. |
| 9:SEPT 01 !V5 | `=SUM(D5:T5)` | extra_rows | The TOTAL DEVIATION range is stretched left into the TOTAL DEVIATION subtotal in D5 (=B5+C5), so the SUBLETTE and HOLCOMB beginning balances are counted a second time. |
| 9:SEPT 01 !H38 | `=SUM(H6:H36)+H37` | double_count | The VOLUME ADJ. amount in H37 is already inside the summed range H6:H36, so adding it again counts it twice in the SEPTEMBER CUMULATIVE total. |
| 9:SEPT 01 !J38 | `=SUM(J6:J36)+J37` | double_count | The VOLUME ADJ. amount in J37 is already inside the summed range J6:J36, so adding it again counts it twice in the SEPTEMBER CUMULATIVE total. |
| 9:SEPT 01 !L38 | `=SUM(L6:L36)+L37` | double_count | The VOLUME ADJ. amount in L37 is already inside the summed range L6:L36, so adding it again counts it twice in the SEPTEMBER CUMULATIVE total. |
| 9:OCT 01!V5 | `=SUM(D5:T5)` | extra_rows | The TOTAL DEVIATION range is stretched left into the TOTAL DEVIATION subtotal in D5 (=B5+C5), so the SUBLETTE and HOLCOMB amounts are counted twice, and the result no longer matches the peer totals in V6 and V7. |
| 9:NOV 01!V5 | `=SUM(D5:T5)` | extra_rows | The TOTAL DEVIATION range is stretched left into the 'TOTAL DEVIATION' header cell D5, which holds the SUBLETTE+HOLCOMB subtotal (=B5+C5). That subtotal is then counted again alongside the field deviations, so the total is overstated. |
| 9:NOV 01!J38 | `=SUM(J6:J36)+J37` | double_count | The VOLUME ADJ. amount in J37 is already inside the summed range J6:J36, so adding it again counts it twice in the SEPTEMBER CUMULATIVE total. |
| 9:NOV 01!P38 | `=SUM(P6:P36)+P37` | double_count | The VOLUME ADJ. amount in P37 is already inside the summed range P6:P36, so adding it again counts it twice in the SEPTEMBER CUMULATIVE total. |
| 10:EPSunDevil!E16 | `=SUM(E14:E15)` | extra_rows | The 'Total Cost:' range is stretched up into the 'Miles Pipe' row (E14), which holds a raw mile count of 0, so the total no longer covers only 'Added Compression' as the peer total in F16 does. |
| 11:Data!D5 | `=D13-D11` | wrong_reference | "Exchange Fee $/MMBtu" (D11) is used where "Payables extension" (D12) belongs. |
| 11:Data!G17 | `=C17` | wrong_reference | "C17" (C17) is used where "B17" (B17) belongs. |
| 11:Data!C21 | `=C13/13` | wrong_operator | The formula divides by "tot volume" (13) where a product is expected. |
| 11:Data!D34 | `=C13/7` | wrong_reference | "tot volume" (C13) is used where "tot volume" (C12) belongs. |
| 11:Data!E36 | `=C5` | wrong_reference | "Swap amount" (C5) is used where "tot volume" (C36) belongs. |
| 11:Data!F51 | `=C5+D5` | wrong_sign | "Swap amount" (D5) is added here but should be subtracted. |
| 11:Data!F52 | `=D11` | wrong_reference | "Exchange Fee $/MMBtu" (D11) is used where "Exchange Fee $" (D12) belongs. |
| 11:Data!F54 | `=F51/D49` | wrong_reference | "Total delivered volume" (D49) is used where "Total delivered volume" (D50) belongs. |
| 12:Summary!F4 | `=-AVERAGE(Exposure!C7:C18)` | wrong_function | "IF NGPL MidContinent index > Forgan > Delivery Point > Existing Deals with Huber" calls for SUM, but the formula uses AVERAGE. |
| 12:Summary!F5 | `=-AVERAGE(Exposure!D7:D18)` | skipped_rows | The AVERAGE range stops short: D6 belong to the same block but are left out. |
| 12:Summary!F6 | `=-AVERAGE(Exposure!E12:E18)` | None | unparseable reply |
| 12:Summary!G6 | `=8299906+2298900` | wrong_sign | "IF NGPL MidContinent Index minus $0.01" (2298900) is added here but should be subtracted. |
| 12:Summary!F7 | `=F4+F5` | missing_term | The 'Total Payables as of Jan 25, 2002' row should sum all three contract-price payables (IF NGPL MidContinent index, IF NGPL MidContinent index, IF NGPL MidContinent Index minus $0.01), but the Gage term in F6 is left out. |
| 12:Summary!F13 | `=-AVERAGE(Exposure!F7:F12)` | skipped_rows | The AVERAGE range stops short: IF CIG Rocky Mtns. index minus $0.03 (Proposed), IF CIG Rocky Mtns. index minus $0.03 (Proposed), IF CIG Rocky Mtns. index minus $0.03 (Proposed), IF CIG Rocky Mtns. index minus $0.03 (Proposed), IF CIG Rocky Mtns. index minus $0.03 (Proposed), IF CIG Rocky Mtns. index minus $0.03 (Proposed) belong to the same block but are left out. |
| 12:Summary!F15 | `=-AVERAGE(Exposure!H7:H11)` | skipped_rows | The AVERAGE range stops short: H12 belong to the same block but are left out. |
| 12:Summary!F16 | `=-AVERAGE(Exposure!I7:I11)` | skipped_rows | The AVERAGE range stops short: I12, I13, I14, I15, I16, I17, I18 belong to the same block but are left out. |
| 12:Summary!F18 | `=F14` | wrong_reference | "Gas Daily PG&E Topock index minus $0.02" (F14) is used where "Total Payables as of Jan 25, 2002" (F17) belongs. |
| 12:Exposure!C6 | `=25*Volumes!B4*Curves!F5` | missing_factor | The product leaves out "IF NGPL MidContinent index (@ Forgan)" ($A6), which the neighbouring cells apply. |
| 12:Exposure!D6 | `=25*Volumes!C4*Curves!J5` | missing_factor | The product leaves out "Days in Month" ($A6), which the neighbouring cells apply. |
| 12:Exposure!H6 | `=25*Curves!Z5*Volumes!G4` | missing_factor | The product leaves out "Days in Month" (A6), which the neighbouring cells apply. |
| 12:Exposure!I6 | `=25*Curves!AD5*Volumes!H4` | missing_factor | The product leaves out "Days in Month" (A6), which the neighbouring cells apply. |
| 12:Exposure!L6 | `=J6/Volumes!I4/25` | wrong_operator | Parentheses are missing: "J6/(Volumes!I4/25)" must be computed before dividing. |
| 12:Exposure!C7 | `=$A6*Volumes!B4*Curves!F5+25*Volumes!B5*Curves!F6` | wrong_reference | "B4" (Volumes!B4) is used where "B5" (Volumes!B5) belongs. |
| 12:Exposure!H7 | `=A6*Volumes!G4*Curves!Z5+25*Curves!Z6*Volumes!G5` | missing_factor | The first term drops the 25-day multiplier, so it no longer matches the 25*Volumes*Curves pattern used in the peer cells and in the second term of the same formula. |
| 12:Exposure!L7 | `=J7/Volumes!I5/(25+A6)` | wrong_reference | "A6" (A6) is used where "A7" (A7) belongs. |
| 13:Sheet1!I22 | `=I5-H19` | wrong_reference | "Total after income credits" (H19) is used where "Total after income credits" (H20) belongs. |
| 13:Sheet1!I29 | `=I22-H28` | wrong_reference | "Total" (H28) is used where "Unusual loss from government ban of certain preservatives" (H26) belongs. |
| 16:Sheet1!B30 | `=SUM(B24:B29)` | extra_rows | The 'Total' of the charge components (Fuel - %, Transport., ACA, GRI, GPS) should start at row 25, but the range now begins at row 24 and pulls in the 'IF Index' price of 4.83, which is not a component. |
| 16:Sheet1!F30 | `=SUM(F24:F29)` | extra_rows | The SUM range reaches into "IF Index" (F24), which is not part of the block. |
| 16:Sheet1!J30 | `=SUM(J24:J29)` | extra_rows | The Sta. #45 total should add only the Fuel - %, Transport., ACA, GRI and GPS components, but the range now starts at row 24 and pulls in the IF Index of 2.25, which is not a component. |
| 16:Sheet1!L30 | `=SUM(L24:L29)` | extra_rows | The Total of the Fuel - %, Transport., ACA, GRI and GPS components should start at row 25, but the range now begins at row 24 and pulls in the IF Index price of 1.78, which is not a component. |
| 16:Sheet1!N30 | `=SUM(N24:N29)` | extra_rows | The total of the charge components (Fuel - %, Transport., ACA, GRI, GPS) should start at N25, but the range now begins at N24 and pulls in the IF Index price of 3.14, which is not a component. |
| 16:Sheet1!B42 | `=SUM(B36:B41)` | extra_rows | The 'Total' of the Fuel - %, Transport., ACA, GRI and GPS components should start at row 37, but the range now begins at row 36 and adds the 'IF Index' price of 4.88, which is not a component. |
| 16:Sheet1!D42 | `=SUM(D36:D41)` | extra_rows | The 'Total' of the Fuel - %, Transport., ACA, GRI and GPS components should start at row 37, but the range now begins at row 36 and pulls in the 'IF Index' price of 3.74, which is not a component. |
| 16:Sheet1!F42 | `=SUM(F36:F41)` | extra_rows | The total of the charge components (Fuel - %, Transport., ACA, GRI, GPS) should start at F37, but the range now begins at F36 and pulls in the IF Index price of 3.19, which is not a charge component. |
| 16:Sheet1!L42 | `=SUM(L36:L41)` | extra_rows | The Contract Price total should add only the component rates (Fuel - %, Transport., ACA, GRI, GPS), but the range now starts at row 36 and pulls in the IF Index price of 1.86, which is not a component rate. |
| 16:Sheet1!N42 | `=SUM(N36:N41)` | extra_rows | The Total should add only the charge components Fuel - %, Transport., ACA, GRI and GPS, but the range now starts at row 36 and pulls in the IF Index price of 3.18, which is not a charge. |
| 16:Sheet1!R19 | `=SUM(F14:F17)+N12` | wrong_sign | "IF Index" (N12) is added here but should be subtracted. |
| 16:Sheet1!R31 | `=SUM(F26:F29)+N24` | wrong_reference | "IF Index" (N24) is used where "Fuel - %" (N25) belongs. |
| 16:Sheet1!R43 | `=SUM(F38:F41)+N36` | wrong_reference | "IF Index" (N36) is used where "Sta. #65 - Dths / Day" (N35) belongs. |
| 16:Sheet1!B45 | `=(B35*31)*B44` | wrong_operator | The 'Amount Underbilled' should be the daily volume (Sta. #65 - Dths / Day) times the days in the month divided by the 'Difference' in price, but this version multiplies by the difference instead of dividing, unlike the peer formula in D45. |
| 16:Sheet1!P58 | `=+N58+P47` | wrong_sign | "Total Term Purchase" (P47) is added here but should be subtracted. |
| 16:Sheet1!N63 | `=2564*2.77` | missing_factor | The product leaves out "Days" (365), which the neighbouring cells apply. |
| 16:Sheet1!J80 | `=SUM(J77:J79)` | extra_rows | The Total Cash Out range is stretched up into the September 2001 row, which is a prior-period amount, so the total no longer covers only October and November 2001. |
| 16:Sheet1!L80 | `=SUM(L78:L79)` | skipped_rows | The SUM range stops short: September 2001 belong to the same block but are left out. |
| 16:Sheet1!N80 | `=SUM(N78:N79)` | skipped_rows | The SUM range stops short: September 2001 belong to the same block but are left out. |
| 19:MAY(2)!AF18 | `=SUM(Y18:AA18)` | skipped_rows | The SUM range stops short: DIRECT BILL, DIRECT BILL belong to the same block but are left out. |
| 19:MAY(1)!AG18 | `=SUM(C18:R18,W18:Y18)` | extra_rows | The NET PALO VERDE total should cover only the DIRECT BILL hours C:R and the EPMI DEAL #502431 hours W:X, but the range runs one column too far into Y18, which is a DIRECT BILL hour that belongs to the NET FOUR CORNERS block. |
| 21:Sheet1!E105 | `=+E103+E92` | missing_term | "Interest" (E102) should be added here but is left out. |
| 21:Sheet1 (2)!E103 | `=SUM(E94:E101)` | skipped_rows | The SUM range stops short: (blank) belong to the same block but are left out. |
| 21:Sheet1 (2)!E105 | `=+E103+E92` | wrong_reference | "(Retro billed March 20, 2001)" (E92) is used where "(Retro billed March 20, 2001)" (E93) belongs. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: C28 belong to the same block but are left out. |
| 24:Legacy!H25 | `=$G25*H$21*H$22` | missing_factor | The product leaves out "Factor" (H$23), which the neighbouring cells apply. |
| 25:external!F36 | `=(D36-E36)+F34` | wrong_reference | "F34" (F34) is used where "F35" (F35) belongs. |
| 26:Dec 2001!F18 | `=G45+G150+G165+G190+G201+G222+G244+G339` | missing_term | The 'Total for 2001' count of turbines that have operated > 90 days leaves out the last project block's 'Turbines Included' total in G345, even though the weighted-average availability formula in F19 still multiplies G345 by its availability. |
| 26:Dec 2001!G45 | `=SUM(G25:G44)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G150 | `=SUM(G50:G149)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J208 | `=COUNT(C206:C221)` | wrong_function | "December" calls for SUM, but the formula uses COUNT. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J229 | `=COUNT(C227:C243)` | wrong_function | "December" calls for SUM, but the formula uses COUNT. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!F2 | `=I29+I134+I149+I174+I185+I206+I228+I323` | missing_term | The total of 'Turbines Included' averages leaves out the last block's average in I328, even though the weighted-average formula in F3 still multiplies F329 by I328. |
| 26:Mar 2002!F2 | `=I29+I134+I149+I174+I185+I206+I228+I323` | missing_term | The total of 'Turbines Included' blocks leaves out the last block's count in I328, even though the weighted-average formula in F3 still multiplies F329 by I328. |
| 28:Sheet1!I8 | `=G8*H8` | missing_factor | The product leaves out "he 6" (0.7), which the neighbouring cells apply. |
| 30:Hotlist - Identified !T11 | `=+E11+I11+M11+Q11` | missing_term | "SUBTOTAL" (G11) should be added here but is left out. |
| 30:Hotlist - Identified !E37 | `=SUM(E30:E36)` | extra_rows | The Weather SUBTOTAL range starts two rows too early and picks up the SMUD deal value in E30, which belongs to the Emissions block above, so the Weather subtotal is inflated by 1000. |
| 30:Hotlist - Identified !E67 | `=+E11+E22+E28+E37+E43+E65+E50+E55+E60` | wrong_reference | "SUBTOTAL" (E60) is used where "SUBTOTAL" (E61) belongs. |
| 30:Hotlist - Identified !I67 | `=+I11+I22+I28+I37+I43+I65+I50+I55+I60` | wrong_reference | "SUBTOTAL" (I43) is used where "SUBTOTAL" (I44) belongs. |
| 30:Hotlist - Identified !M67 | `=+M11+M22+M28+M37+M43+M65+M50+M55+M60` | wrong_reference | "SUBTOTAL" (M65) is used where "SUBTOTAL" (M61) belongs. |
| 30:Hotlist - Identified !Q67 | `=+Q11+Q22+Q28+Q37+Q43+Q65+Q50+Q55+Q60` | wrong_reference | "SUBTOTAL" (Q60) is used where "Deal" (Q61) belongs. |
| 30:Hotlist - Identified !T67 | `=+T11+T22+T28+T37+T43+T65+T50+T55+T60` | missing_term | The TOTALS row should add every deal TOTAL, but the first deal's TOTAL in T6 is left out, while the peer totals in R67 and U67 still include row 6. |
