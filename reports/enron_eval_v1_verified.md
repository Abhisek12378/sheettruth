# Held-out evaluation

| metric | value |
|---|---|
| errors | 32 |
| covered | 29 |
| found | 11 |
| missed | 18 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 2817 |
| flagged_windows | 235 |
| false_alarm_windows | 223 |
| recall_covered | 0.379 |
| recall_all | 0.344 |
| precision_windows | 0.051 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | sheet1 | F28, G28 | Range error | missed |  |  |  |
| 2 | 2 | sheet1 | I34 | Range error | found | skipped_rows | yes | The SUM range stops short: he 6 belong to the same block but are left out. |
| 3 | 3 | bmspt066 | W43 | Range error | found | skipped_rows |  | The SUM range stops short: Estimated, Estimated, Estimated, Estimated, Projected belong to the same block but are left out. |
| 4 | 3 | bmspt066 | C43, D43, E43, F43, G43, H43, I43, J43,  | Range error | missed |  |  |  |
| 5 | 4 | sheet1 | L16 | Range error | found | skipped_rows | yes | The AVERAGE range stops short: Transco Z5 belong to the same block but are left out. |
| 6 | 5 | jul01 | AL44 | Range error | missed |  |  |  |
| 7 | 6 | real time | V23 | Range error | missed |  |  |  |
| 8 | 7 | deals | AD142 | Range error | found | skipped_rows |  | The SUM range stops short: PV belong to the same block but are left out. |
| 9 | 8 | cost estimate summary | L23 | Range error | found | skipped_rows | yes | The SUM range stops short: Gallup CS Mods belong to the same block but are left out. |
| 10 | 9 | oct 01 | T39 | Wrong formula | missed |  |  |  |
| 11 | 10 | epsundevil | F10 | Wrong reference | missed |  |  |  |
| 12 | 11 | data | D13 | Wrong calculation | missed |  |  |  |
| 13 | 12 | curves | V10, V100, V101, V102, V103, V104, V105, | Wrong calculation | missed |  |  |  |
| 14 | 13 | sheet1 | H33 | Wrong calculation | missed |  |  |  |
| 15 | 13 | sheet1 | I35 | Wrong calculation | missed |  |  |  |
| 16 | 13 | sheet1 | I38 | Wrong calculation | found | wrong_sign |  | "Extraordinary loss due to tornado damage" (H36) is subtracted here but should be added. |
| 19 | 16 | sheet1 | B13, B25, B37, C13, C25, C37, D13, D25,  | Wrong calculation | missed |  |  |  |
| 22 | 18 | crack spread option | M10, M11, M12, M13, M14, M9 | Wrong calculation | not_covered |  |  |  |
| 23 | 19 | may(2) | AE18, AE19, AE20, AE21, AE22, AE23, AE24 | Range error | missed |  |  |  |
| 24 | 20 | sheet1 | D112 | Range error | missed |  |  |  |
| 25 | 21 | sheet1 (2) | F94 | Wrong calculation | found | wrong_sign |  | "in Dispute" (B95) is subtracted here but should be added. |
| 26 | 22 | sheet1 | C7 | File reference not working | missed |  |  |  |
| 27 | 23 | egs exp | W12 | Range error | found | skipped_rows | yes | The SUM range stops short: April, May, June, July, August belong to the same block but are left out. |
| 28 | 24 | new | C10, C11, C12, C13, C14, C25, C26, C27,  | Wrong calculation | missed |  |  |  |
| 29 | 25 | external | D11, D12, D13, D14, D15, D16, D17, D18,  | Wrong calculation | not_covered |  |  |  |
| 30 | 25 | external | E36, E37 | Wrong reference | missed |  |  |  |
| 31 | 26 | mar 2002 | I132 | Fixed Value | not_covered |  |  |  |
| 32 | 27 | jd-mal or cptjk trans | H12, H13, H14, H15, H16, H17, H34, H35 | Range error | found | skipped_rows |  | The SUM range stops short: NOT FOR TOM, ET AL belong to the same block but are left out. |
| 33 | 28 | sheet1 | I25, I26, I27, I28, I29, I30, I31 | Wrong reference | missed |  |  |  |
| 34 | 28 | sheet1 | G33, I34 | Range error | found | skipped_rows |  | The SUM range stops short: he 6 belong to the same block but are left out. |
| 35 | 29 | sheet1 | F8 | Formula: = SUM(D8*E8) | missed |  |  |  |
| 36 | 30 | hotlist - identified | M22, M37 | Range error | found | skipped_rows |  | The SUM range stops short: M&G - UK, Origination & Finance belong to the same block but are left out. |

## By category

| category | found | missed | unsupported | not covered |
|---|---|---|---|---|
| File reference not working | 0 | 1 | 0 | 0 |
| Fixed Value | 0 | 0 | 0 | 1 |
| Formula: = SUM(D8*E8) | 0 | 1 | 0 | 0 |
| Range error | 9 | 6 | 0 | 0 |
| Wrong calculation | 2 | 6 | 0 | 2 |
| Wrong formula | 0 | 1 | 0 | 0 |
| Wrong reference | 0 | 3 | 0 | 0 |

## False alarms (223)

| id | formula | type | reason |
|---|---|---|---|
| 3:BMSPT066!Q6 | `=+'[2]BAM-EGS'!$BC$9+'[3]BAM-EGS'!$BC$9` | wrong_sign | "BAM-EGS" ('[3]BAM-EGS'!$BC$9) is added here but should be subtracted. |
| 5:jul01!AS44 | `=AL44+AN44-AQ44` | wrong_sign | "TOTAL" (AQ44) is subtracted here but should be added. |
| 6:Real Time!J26 | `=J23+J15` | wrong_sign | "Sr. Specialist" (J15) is added here but should be subtracted. |
| 6:Real Time!J27 | `=+J26*E27` | wrong_sign | "Jan" (J26) is subtracted here but should be added. |
| 6:Real Time!J28 | `=+J26*E28` | wrong_sign | "Jan" (J26) is subtracted here but should be added. |
| 6:Real Time!J29 | `=SUM(J26:J28)` | skipped_rows | The SUM range stops short: Jan belong to the same block but are left out. |
| 6:Real Time!N29 | `=+(N26*1.0425)*11` | wrong_sign | "Jan" ((N26*1.0425)) is added here but should be subtracted. |
| 6:Real Time!V29 | `=+(V26*1.0425)*11` | wrong_sign | "Jan" ((V26*1.0425)) is added here but should be subtracted. |
| 6:Real Time!H40 | `=+[1]YTD!M4-28000` | wrong_sign | "28000" ('28000') is subtracted here but should be added. |
| 6:Real Time!J71 | `=+H71*2` | wrong_sign | "Recruiting Expenses" (H71) is subtracted here but should be added. |
| 6:Real Time!J76 | `=+H76*2` | wrong_sign | "Outside Services - Legal" (H76) is subtracted here but should be added. |
| 6:Real Time!J88 | `=+H88*2` | wrong_sign | "Subscriptions & Periodicals" (H88) is subtracted here but should be added. |
| 6:Real Time!H43 | `=+[1]YTD!M5-5418` | wrong_sign | "5418" (M5) is subtracted here but should be added. |
| 6:Real Time!P43 | `=164412+279889` | wrong_sign | "Estimated" (279889) is added here but should be subtracted. |
| 6:Real Time!H44 | `=+[1]YTD!M6-2520` | wrong_sign | "Total Payroll Taxes" (2520) is subtracted here but should be added. |
| 6:Real Time!L45 | `=SUM(L43:L44)` | skipped_rows | The SUM range stops short: Total Salaries & Compensation belong to the same block but are left out. |
| 6:Real Time!H56 | `=+[1]YTD!M51` | wrong_sign | The subtraction of 5418 is required here but the formula adds it. |
| 6:Real Time!S56 | `=126+43435` | wrong_sign | "Benefits/Payroll Taxes (excludes contract labor)" (43435) is added here but should be subtracted. |
| 6:Real Time!L60 | `=[1]Plan!M14` | wrong_sign | "Benefits/Payroll Taxes (excludes contract labor)" ([1]Plan!M14) is subtracted here but should be added. |
| 6:Real Time!J68 | `=+J67+J66+J65` | wrong_sign | "Client Entertainment" (J66) and "Total Travel" (J65) are added here but should be subtracted. |
| 6:Real Time!N68 | `=+N67+N66+N65` | wrong_sign | "Customer Meetings" (N67) is added here but should be subtracted. |
| 7:Preschedule!Z4 | `=SUM(B4:Y4)` | skipped_rows | The SUM range stops short: x belong to the same block but are left out. |
| 7:Preschedule!Z58 | `=SUM(Z41:Z55)+Z41+Z42+Z43+Z48+Z49+Z50+Z51+Z52` | double_count | "NEWMAN 1 (30-70)" (Z41), "NEWMAN 2 (25-78)" (Z42), "NEWMAN 3 (31-103)" (Z43), "NEWMAN 4 (115-190)" (Z48), "COPPER" (Z49), "RIO GRANDE 6 (20-48)" (Z50), "RIO GRANDE 7 (14-44)" (Z51), "RIO GRANDE 8 (65-130)" (Z52) are already inside the summed range and are added again. |
| 7:Preschedule!Z97 | `=Z95-Z96` | wrong_sign | "Total Costs:" (Z95) is subtracted here but should be added. |
| 7:Preschedule!Z100 | `=Z98-Z99` | wrong_sign | "Total Costs:" (Z98) is subtracted here but should be added. |
| 7:Preschedule!M89 | `=M57` | wrong_sign | "4 CORNERS UNIT 5" (M56) is subtracted here but should be added. |
| 7:Preschedule!M92 | `=#REF!` | wrong_sign | "x" (M57) is subtracted here but should be added. |
| 7:Preschedule!Z108 | `=Z105-Z107` | wrong_sign | "Total Costs:" (Z105) is subtracted here but should be added. |
| 7:Preschedule!Z113 | `=Z110-Z112` | wrong_sign | "Total Costs:" (Z110) is subtracted here but should be added. |
| 7:Preschedule!Z118 | `=Z115-Z117` | wrong_sign | "Total Costs:" (Z115) is subtracted here but should be added. |
| 7:Preschedule!Z123 | `=Z120-Z122` | wrong_sign | "Total Costs:" (Z120) is subtracted here but should be added. |
| 7:Preschedule!Z133 | `=Z130-Z132` | wrong_sign | "Total Costs:" (Z130) is subtracted here but should be added. |
| 7:Preschedule!Z143 | `=Z140-Z142` | wrong_sign | "Total Costs:" (Z140) is subtracted here but should be added. |
| 7:Preschedule!Z153 | `=Z150-Z152` | wrong_sign | "Total Costs:" (Z150) is subtracted here but should be added. |
| 7:Preschedule!Z158 | `=Z155-Z157` | wrong_sign | "Total Costs:" (Z155) is subtracted here but should be added. |
| 7:Preschedule!Z163 | `=Z160-Z162` | wrong_sign | "Total Costs:" (Z160) is added here but should be subtracted. |
| 7:Deals!AD141 | `=SUM(AD22:AD120)` | skipped_rows | The SUM range stops short: PV, PV, PV, PV, PV belong to the same block but are left out. |
| 7:Deals!AE142 | `=SUM(AE121:AE131)` | skipped_rows | The SUM range stops short: PV, 4C, 4C belong to the same block but are left out. |
| 7:Deals!AD146 | `=SUM(AD132:AD133)` | skipped_rows | The SUM range stops short: PV belong to the same block but are left out. |
| 7:Economics!B3 | `=(F3+0.7)*E3` | wrong_sign | "SPS Avg. Cost Est." (0.7) is added here but should be subtracted. |
| 7:Economics!B28 | `=-F28*E28` | wrong_sign | "4 Corners Unit 4" (F28) is subtracted here but should be added. |
| 8:Cost Estimate Summary!R42 | `=R23+R34+R40` | wrong_sign | "---" (R40) is added here but should be subtracted. |
| 9:MANUAL!Y13 | `=SUM(Y12)` | skipped_rows | The SUM range stops short: EDWARD 3 belong to the same block but are left out. |
| 9:Jan01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:Feb01!T34 | `=+H36` | wrong_sign | "BUSHTON PVR" (H36) is subtracted here but should be added. |
| 9:Feb01!W34 | `=+N36` | wrong_sign | "TOTAL DEVIATION" (N36) is subtracted here but should be added. |
| 9:Feb01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:Mar01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (B37) is added here but should be subtracted. |
| 9:Mar01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:Apr01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:Apr01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:May 01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:May 01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:June 01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:June 01!D83 | `=+D80-D81` | wrong_sign | "TOTAL DEVIATION" (D81) is subtracted here but should be added. |
| 9:July 01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:AUGUST 01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:AUGUST 01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:SEPT 01 !D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:SEPT 01 !D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 9:OCT 01!AA35 | `=+F38` | wrong_sign | "VOLUME ADJ." (F38) is subtracted here but should be added. |
| 9:OCT 01!D82 | `=+D79-D80` | wrong_sign | "TOTAL DEVIATION" (D80) is subtracted here but should be added. |
| 9:NOV 01!D37 | `=+B37+C37` | wrong_sign | "VOLUME ADJ." (C37) is added here but should be subtracted. |
| 9:NOV 01!D81 | `=+D78-D79` | wrong_sign | "TOTAL DEVIATION" (D79) is subtracted here but should be added. |
| 11:Data!C5 | `=C6-C4` | wrong_sign | "Payables extension" (C4) is subtracted here but should be added. |
| 11:Data!B52 | `=B51-B36` | wrong_sign | "tot volume" (B36) is subtracted here but should be added. |
| 11:Data!F52 | `=D11` | missing_factor | The product leaves out "Exchange Fee $/MMBtu" (E11), which the neighbouring cells apply. |
| 12:Summary!F7 | `=F4+F5` | wrong_sign | "IF NGPL MidContinent index" (F5) is added here but should be subtracted. |
| 12:Summary!F18 | `=F14` | skipped_rows | The SUM range stops short: IF CIG Rocky Mtns. index minus $0.03 belong to the same block but are left out. |
| 13:Sheet1!H17 | `=SUM(H8:H16)` | skipped_rows | The SUM range stops short: Incurred between measurement date and end of fiscal year belong to the same block but are left out. |
| 13:Sheet1!I22 | `=I5-H19` | wrong_sign | "Total after income credits" (H19) is subtracted here but should be added. |
| 19:MAY(2)!C46 | `=SUM(C18:C41)` | wrong_sign | "PDT TOTAL" calls for SUM, but the formula uses SUM. |
| 19:MAY(2)!R46 | `=SUM(C46:Q46)` | skipped_rows | The SUM range stops short: EPMI DEAL #502431, EPMI DEAL #502431 belong to the same block but are left out. |
| 19:MAY(2)!AB46 | `=SUM(S46:AA46)` | skipped_rows | The SUM range stops short: TOTAL SALES belong to the same block but are left out. |
| 19:MAY(1)!AG18 | `=SUM(C18:R18,W18:Y18)` | skipped_rows | The SUM range stops short: DIRECT BILL, DIRECT BILL, DIRECT BILL belong to the same block but are left out. |
| 19:MAY(1)!V46 | `=SUM(C46:U46)` | skipped_rows | The SUM range stops short: EPMI DEAL #502431, EPMI DEAL #502431, DIRECT BILL, DIRECT BILL belong to the same block but are left out. |
| 19:MAY(1)!AE46 | `=SUM(W46:AD46)` | skipped_rows | The SUM range stops short: TOTAL SALES belong to the same block but are left out. |
| 20:Sheet1!J5 | `=C5*E5` | missing_factor | The product leaves out "Municipal Money Market" (F5), which the neighbouring cells apply. |
| 20:Sheet1!J24 | `=C24*E24` | wrong_sign | "ORCL" (F24) is added here but should be subtracted. |
| 20:Sheet1!J41 | `=C41*E41` | wrong_sign | "Stable Asset" (F41) is added here but should be subtracted. |
| 20:Sheet1!J48 | `=C48*E48` | wrong_sign | "ENE savings" (F48) is added here but should be subtracted. |
| 20:Sheet1!J62 | `=C62*E62` | missing_factor | The product leaves out "ENE (100%) 106974 97ECT" (F62), which the neighbouring cells apply. |
| 20:Sheet1!J88 | `=C88*E88` | missing_factor | The product leaves out "Legg Mason Value Trust" (F88), which the neighbouring cells apply. |
| 20:Sheet1!J69 | `=G69` | wrong_sign | "ENE jan 02 35 calls" (G69) is added here but should be subtracted. |
| 20:Sheet1!M16 | `=C16*E16*-1` | wrong_sign | "ENE jan 02 35 calls" (E16) is subtracted here but should be added. |
| 20:unvested!E4 | `=SUM(C25:C25)+C33` | wrong_sign | "restricted stock" (C33) is added here but should be subtracted. |
| 20:unvested!E5 | `=SUM(E3:E4)` | skipped_rows | The SUM range stops short: pre tax belong to the same block but are left out. |
| 20:unvested!G14 | `=C14*(Sheet1!$E$32-D14)` | wrong_sign | "options" (D14) is subtracted here but should be added. |
| 20:unvested!B103 | `=-333000*0.28` | wrong_sign | "est. tax 2001" (333000) is subtracted here but should be added. |
| 21:Sheet1!C5 | `=+B5+B4` | wrong_sign | "in Dispute" (B4) is added here but should be subtracted. |
| 21:Sheet1!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short: & No Interest belong to the same block but are left out. |
| 21:Sheet1!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 21:Sheet1 (2)!C5 | `=+B5+B4` | wrong_sign | "in Dispute" (B4) is added here but should be subtracted. |
| 21:Sheet1 (2)!E105 | `=+E103+E92` | wrong_sign | "(Retro billed March 20, 2001)" (E92) is added here but should be subtracted. |
| 21:Sheet1 (2)!G114 | `=SUM(B86:B91)` | skipped_rows | The SUM range stops short: & No Interest belong to the same block but are left out. |
| 21:Sheet1 (2)!H114 | `=D114-G114` | wrong_sign | "Nov, 1996 - Jan, 2001 Revenue" (G114) is subtracted here but should be added. |
| 21:Sheet1 (2)!E127 | `=H92` | wrong_sign | "(Retro billed March 20, 2001)" (H92) is subtracted here but should be divided. |
| 22:Sheet1!D5 | `=D4-D3` | wrong_sign | "LTD Liquidations as of 11/30" (D3) is subtracted here but should be added. |
| 23:INCOME STATEMENT!C29 | `=SUM(C7:C27)` | skipped_rows | The SUM range stops short: 'ENA IS'!C21 belong to the same block but are left out. |
| 23:EES IS!C30 | `=SUM(C22:C28)` | skipped_rows | The SUM range stops short: Other Income (Loss) belong to the same block but are left out. |
| 23:Europe Burn!E33 | `=E26+E28+E29+E30` | wrong_sign | "Plus: Capital Expenditures" (E28) is added here but should be subtracted. |
| 23:Europe Burn!G33 | `=+G26+G28+G31` | skipped_rows | The SUM range stops short: Other Cash Payments, Less: DD&A belong to the same block but are left out. |
| 23:Europe Burn!I33 | `=+I26+I28+I31` | wrong_sign | "November" (I31) is added here but should be subtracted. |
| 23:Europe Burn!K33 | `=+K26+K28+K31` | wrong_sign | "December" (K31) is added here but should be subtracted. |
| 23:Europe Burn!M33 | `=+M26+M28+M31` | wrong_sign | "Plus: Capital Expenditures" (M28) is added here but should be subtracted. |
| 23:Europe Burn!O33 | `=+O26+O28+O31` | wrong_sign | "Plus: Capital Expenditures" (O28) is added here but should be subtracted. |
| 23:ENA Burn!Q20 | `=SUM(Q17:Q19)` | skipped_rows | The SUM range stops short: Total belong to the same block but are left out. |
| 23:ENA Burn!I24 | `=-I18` | wrong_sign | "Depreciation & Amortization" (I18) is subtracted here but should be added. |
| 23:ENA Burn!E27 | `=E20+E22+E23+E24` | wrong_sign | "Plus: Capital Expenditures" (E22) is added here but should be subtracted. |
| 23:ENA Burn!G27 | `=+G20+G22+G25` | wrong_sign | "October" (G25) is added here but should be subtracted. |
| 23:ENA Burn!I27 | `=+I20+I22+I25` | wrong_sign | "November" (I25) is added here but should be subtracted. |
| 23:ENA Burn!K27 | `=+K20+K22+K25` | wrong_sign | "December" (K25) is added here but should be subtracted. |
| 23:ENA Burn!M27 | `=+M20+M22+M25` | wrong_sign | "Plus: Capital Expenditures" (M22) is added here but should be subtracted. |
| 23:ENA Burn!O27 | `=+O20+O22+O25` | wrong_sign | "Plus: Capital Expenditures" (O22) is added here but should be subtracted. |
| 23:EGM Burn!E25 | `=E18+E20+E21+E22` | wrong_sign | "Plus: Capital Expenditures" (E20) is added here but should be subtracted. |
| 23:EGM Burn!G25 | `=+G18+G20+G23` | skipped_rows | The SUM range stops short: Other Cash Payments, Less: DD&A belong to the same block but are left out. |
| 23:EGM Burn!I25 | `=+I18+I20+I23` | wrong_sign | "November" (I23) is added here but should be subtracted. |
| 23:EGM Burn!K25 | `=+K18+K20+K23` | wrong_sign | "Plus: Capital Expenditures" (K20) is added here but should be subtracted. |
| 23:EGM Burn!M25 | `=+M18+M20+M23` | wrong_sign | "Plus: Capital Expenditures" (M20) is added here but should be subtracted. |
| 23:EGM Burn!O25 | `=+O18+O20+O23` | wrong_sign | "Plus: Capital Expenditures" (O20) is added here but should be subtracted. |
| 23:EGM Burn!Q25 | `=+Q18+Q20+Q23` | wrong_sign | "Plus: Capital Expenditures" (Q20) is added here but should be subtracted. |
| 23:EGS Burn!E4 | `=110.4-14.3-19.8-26.2-7.1` | wrong_sign | "14.3" (14.3) is subtracted here but should be added. |
| 23:EGS Burn!O15 | `=SUM(O12:O14)` | skipped_rows | The SUM range stops short: Total belong to the same block but are left out. |
| 23:EIM Burn!E22 | `=E15+E17+E18+E19` | wrong_sign | "Less: DD&A" (E19) is added here but should be subtracted. |
| 23:EIM Burn!G22 | `=+G15+G17+G20` | wrong_sign | "Plus: Capital Expenditures" (G17) is added here but should be subtracted. |
| 23:EIM Burn!I22 | `=+I15+I17+I20` | wrong_sign | "November" (I20) is added here but should be subtracted. |
| 23:EIM Burn!K22 | `=+K15+K17+K20` | wrong_sign | "Plus: Capital Expenditures" (K17) is added here but should be subtracted. |
| 23:EIM Burn!M22 | `=+M15+M17+M20` | wrong_sign | "Plus: Capital Expenditures" (M17) is added here but should be subtracted. |
| 23:EBS Burn!I7 | `=SUM(I3:I6)` | skipped_rows | The SUM range stops short: Depreciation & Amortization, Taxes Other Than Income belong to the same block but are left out. |
| 23:EBS Burn!E17 | `=E10+E12+E13+E14` | wrong_sign | "Less: DD&A" (E14) is added here but should be subtracted. |
| 23:EBS Burn!G17 | `=+G10+G12+G15` | wrong_sign | "October" (G15) is added here but should be subtracted. |
| 23:EBS Burn!I17 | `=+I10+I12+I15` | wrong_sign | "November" (I15) is added here but should be subtracted. |
| 23:EBS Burn!K17 | `=+K10+K12+K15` | wrong_sign | "December" (K15) is added here but should be subtracted. |
| 23:EBS Burn!M17 | `=+M10+M12+M15` | wrong_sign | "Plus: Capital Expenditures" (M12) is added here but should be subtracted. |
| 23:ENW Burn!M10 | `=SUM(M3:M9)` | skipped_rows | The SUM range stops short: Total belong to the same block but are left out. |
| 23:ENW Burn!I17 | `=-I11` | wrong_sign | "Depreciation & Amortization" (I11) is subtracted here but should be added. |
| 23:ENW Burn!E20 | `=E13+E15+E16+E17` | wrong_sign | "Plus: Capital Expenditures" (E15) is added here but should be subtracted. |
| 23:ENW Burn!G20 | `=+G13+G15+G18` | wrong_sign | "Plus: Capital Expenditures" (G15) is added here but should be subtracted. |
| 23:ENW Burn!I20 | `=+I13+I15+I18` | wrong_sign | "Total Expenses net of Capitalized Expense" (I13) is added here but should be subtracted. |
| 23:ENW Burn!K20 | `=+K13+K15+K18` | wrong_sign | "Plus: Capital Expenditures" (K15) is added here but should be subtracted. |
| 23:ENW Burn!M20 | `=+M13+M15+M18` | wrong_sign | "Plus: Capital Expenditures" (M15) is added here but should be subtracted. |
| 23:ENW Burn!Q20 | `=+Q13+Q15+Q18` | wrong_sign | "Plus: Capital Expenditures" (Q15) is added here but should be subtracted. |
| 23:EES Burn!E27 | `=E20+E22+E23+E24` | wrong_sign | "Plus: Capital Expenditures" (E22) is added here but should be subtracted. |
| 23:EES Burn!G27 | `=+G20+G22+G25` | wrong_sign | "Plus: Capital Expenditures" (G22) is added here but should be subtracted. |
| 23:EES Burn!I27 | `=+I20+I22+I25` | wrong_sign | "November" (I25) is added here but should be subtracted. |
| 23:EES Burn!K27 | `=+K20+K22+K25` | wrong_sign | "Plus: Capital Expenditures" (K22) is added here but should be subtracted. |
| 23:EES Burn!M27 | `=+M20+M22+M25` | wrong_sign | "Plus: Capital Expenditures" (M22) is added here but should be subtracted. |
| 23:EPI Burn!E15 | `=E8+E10+E11+E12` | wrong_sign | "Plus: Capital Expenditures" (E10) is added here but should be subtracted. |
| 23:EPI Burn!G15 | `=+G8+G10+G13` | skipped_rows | The SUM range stops short: Other Cash Payments, Less: DD&A belong to the same block but are left out. |
| 23:EPI Burn!I15 | `=+I8+I10+I13` | wrong_sign | "Total Expenses net of Capitalized Expense" (I8) is added here but should be subtracted. |
| 23:EPI Burn!K15 | `=+K8+K10+K13` | wrong_sign | "Plus: Capital Expenditures" (K10) is added here but should be subtracted. |
| 23:EPI Burn!M15 | `=+M8+M10+M13` | wrong_sign | "Plus: Capital Expenditures" (M10) is added here but should be subtracted. |
| 23:ENA EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Other belong to the same block but are left out. |
| 23:EGM EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:EIM EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:Europe EXP!G23 | `=SUM(G16:G22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:Europe EXP!I23 | `=SUM(I16:I22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:Europe EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: 2001 Forecast Expense belong to the same block but are left out. |
| 23:EBS EXP!N5 | `=SUM(C5:M5)` | skipped_rows | The SUM range stops short: October belong to the same block but are left out. |
| 23:EBS EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:ENW EXP!G23 | `=SUM(G16:G22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:ENW EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:EES EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:EPI EXP!M23 | `=SUM(M16:M22)` | skipped_rows | The SUM range stops short: Subtotal belong to the same block but are left out. |
| 23:ENA BS!E8 | `=SUM(E5:E7)` | skipped_rows | The SUM range stops short: Current Liabilities belong to the same block but are left out. |
| 23:ENA BS!E15 | `=SUM(E8:E14)` | skipped_rows | The SUM range stops short: Notes and Accounts Payable (including interco.), Other Current Liabilities, PRML belong to the same block but are left out. |
| 23:ENA BS!B21 | `=+B19+B20+B18+B17+B13+B12` | wrong_sign | "Total Assets" calls for addition, but the formula subtracts "Total Current Assets" (B12). |
| 23:ENA BS!E21 | `=+E20+E15` | wrong_sign | "Total Liabilities" (E15) is added here but should be subtracted. |
| 23:ENA OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:ENA OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EGM OFF BS !B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EGM OFF BS !F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EGS OFF BS!G18 | `=G17+B10` | wrong_sign | "Recall of debt by Hong Kong bank" (B10) is added here but should be subtracted. |
| 23:EIM OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EIM OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EuropeOFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EuropeOFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EBS OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EBS OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:ENW OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:ENW OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EES OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EES OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EPI OFF BS!B16 | `=B15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 23:EPI OFF BS!F16 | `=F15+B8` | wrong_sign | "Sub total" (B8) is added here but should be subtracted. |
| 25:external!F38 | `=(D38-E38)+F37` | wrong_sign | "BURN" (E38) is subtracted here but should be added. |
| 25:external!E12 | `=3025+1472` | wrong_sign | "BURN" (1472) is added here but should be subtracted. |
| 26:Nov 2001!L13 | `=SUM(L10:L12)` | skipped_rows | The SUM range stops short: Remaining belong to the same block but are left out. |
| 26:Nov 2001!I30 | `=SUM(I10:I29)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!L183 | `=L180+L181+L182` | wrong_sign | "November" (L182) is added here but should be subtracted. |
| 26:Nov 2001!I186 | `=SUM(I180:I185)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I207 | `=SUM(I191:I206)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I229 | `=SUM(I212:I228)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Nov 2001!I324 | `=SUM(I234:I323)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J16 | `=J54+J157+J171+J197+J207+J228+J250` | wrong_sign | "November" (J157) is added here but should be subtracted. |
| 26:Dec 2001!G190 | `=SUM(G170:G189)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!J55 | `=J50+J51+J52+J53+J54` | skipped_rows | The SUM range stops short: December belong to the same block but are left out. |
| 26:Dec 2001!J198 | `=J195+J196+J197` | wrong_sign | "November" (J197) is added here but should be subtracted. |
| 26:Dec 2001!F165 | `=AVERAGE(F155:F164)` | wrong_function | "Average" calls for SUM, but the formula uses AVERAGE. |
| 26:Dec 2001!G165 | `=SUM(G155:G164)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G201 | `=SUM(G195:G200)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G222 | `=SUM(G206:G221)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G244 | `=SUM(G227:G243)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Dec 2001!G339 | `=SUM(G249:G338)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I30 | `=SUM(I10:I29)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I175 | `=SUM(I155:I174)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!L183 | `=L180+L181+L182` | wrong_sign | "November" (L182) is added here but should be subtracted. |
| 26:Jan 2002!I186 | `=SUM(I180:I185)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I207 | `=SUM(I191:I206)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I229 | `=SUM(I212:I228)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Jan 2002!I324 | `=SUM(I234:I323)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!I174 | `=SUM(I154:I173)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!I185 | `=SUM(I179:I184)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!I206 | `=SUM(I190:I205)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Feb 2002!I228 | `=SUM(I211:I227)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Mar 2002!I29 | `=SUM(I9:I28)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 26:Mar 2002!I174 | `=SUM(I154:I173)` | wrong_function | "Average" calls for AVERAGE, but the formula uses SUM. |
| 29:Sheet1!G8 | `=SUM(D8-F8)` | wrong_sign | "011220" (F8) is subtracted here but should be added. |
| 30:Hotlist - Identified !T11 | `=+E11+I11+M11+Q11` | wrong_sign | "SUBTOTAL" (Q11) is added here but should be subtracted. |
| 30:Hotlist - Identified !I50 | `=SUM(I45:I49)` | skipped_rows | The SUM range stops short: Hoegh Galleon, LNG, LNG belong to the same block but are left out. |
| 30:Hotlist - Completed!I6 | `=+'Hotlist - Identified '!B29` | wrong_sign | "Emissions" ('Hotlist - Identified '!B29) is subtracted here but should be added. |
| 30:Hotlist - Completed!K29 | `=+E10+E20+E26+K11+K20+K26` | wrong_sign | "SUBTOTAL" (K11, K20, K26) is added here but should be subtracted. |
