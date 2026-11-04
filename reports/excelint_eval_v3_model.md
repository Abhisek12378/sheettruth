# Held-out evaluation

| metric | value |
|---|---|
| errors | 317 |
| covered | 314 |
| found | 20 |
| missed | 294 |
| unsupported | 0 |
| not_covered | 3 |
| windows | 6210 |
| flagged_windows | 30 |
| false_alarm_windows | 10 |
| recall_covered | 0.064 |
| recall_all | 0.063 |
| precision_windows | 0.667 |

## Documented errors

| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 | pb | K35 | ExceLint audit: formula error | missed |  |  |  |
| 2 | 2 | pb | B42 | ExceLint audit: formula error | not_covered |  |  |  |
| 3 | 2 | pm2.5 | J30 | ExceLint audit: formula error | found | skipped_rows |  | The AVERAGE range stops short: POWDERSVILLE* belong to the same block but are left out. |
| 4 | 2 | rain | L7 | ExceLint audit: formula error | missed |  |  |  |
| 5 | 2 | rain | L12, L13 | ExceLint audit: formula error | missed |  |  |  |
| 6 | 2 | tsp | H35 | ExceLint audit: formula error | missed |  |  |  |
| 7 | 3 | fy 2002 | I17, J17, K17, L17, M17 | ExceLint audit: formula error | missed |  |  |  |
| 8 | 3 | fy 2002 | H17 | ExceLint audit: formula error | missed |  |  |  |
| 9 | 3 | fy 2002 | N17, O17 | ExceLint audit: formula error | missed |  |  |  |
| 10 | 5 | general ptsa budget | J22 | ExceLint audit: formula error | missed |  |  |  |
| 11 | 5 | general ptsa budget | H113 | ExceLint audit: formula error | missed |  |  |  |
| 12 | 6 | general exp page 4 | A4 | ExceLint audit: formula error | missed |  |  |  |
| 13 | 6 | general exp page 4 | I17 | ExceLint audit: formula error | missed |  |  |  |
| 14 | 6 | general exp page 4 | K17 | ExceLint audit: formula error | missed |  |  |  |
| 15 | 6 | general exp page 4 | G17 | ExceLint audit: formula error | missed |  |  |  |
| 16 | 6 | capital projects page 6 | F20 | ExceLint audit: formula error | missed |  |  |  |
| 17 | 6 | capital projects page 6 | J20 | ExceLint audit: formula error | missed |  |  |  |
| 18 | 6 | capital projects page 6 | F28 | ExceLint audit: formula error | missed |  |  |  |
| 19 | 6 | capital projects page 6 | H28 | ExceLint audit: formula error | missed |  |  |  |
| 20 | 6 | capital projects page 6 | J28 | ExceLint audit: formula error | missed |  |  |  |
| 21 | 6 | capital projects page 6 | F75 | ExceLint audit: formula error | missed |  |  |  |
| 22 | 6 | capital projects page 6 | H75 | ExceLint audit: formula error | missed |  |  |  |
| 23 | 6 | capital projects page 6 | F35 | ExceLint audit: formula error | missed |  |  |  |
| 24 | 6 | capital projects page 6 | H35 | ExceLint audit: formula error | missed |  |  |  |
| 25 | 6 | capital projects page 6 | J35 | ExceLint audit: formula error | missed |  |  |  |
| 26 | 6 | capital projects page 6 | F41 | ExceLint audit: formula error | missed |  |  |  |
| 27 | 6 | capital projects page 6 | H41 | ExceLint audit: formula error | missed |  |  |  |
| 28 | 6 | capital projects page 6 | J41 | ExceLint audit: formula error | missed |  |  |  |
| 29 | 6 | capital projects page 6 | J48 | ExceLint audit: formula error | missed |  |  |  |
| 30 | 6 | capital projects page 6 | F68 | ExceLint audit: formula error | missed |  |  |  |
| 31 | 6 | capital projects page 6 | H68 | ExceLint audit: formula error | missed |  |  |  |
| 32 | 6 | capital projects page 6 | J68 | ExceLint audit: formula error | missed |  |  |  |
| 33 | 6 | capital projects page 6 | H20 | ExceLint audit: formula error | missed |  |  |  |
| 34 | 6 | food service page 7 | A4 | ExceLint audit: formula error | missed |  |  |  |
| 35 | 6 | food service page 7 | I47 | ExceLint audit: formula error | missed |  |  |  |
| 36 | 6 | internal service page 9 | J28 | ExceLint audit: formula error | missed |  |  |  |
| 37 | 6 | combined bal sheet page 1 | D54, E54, F54, G54, H54, I54 | ExceLint audit: formula error | missed |  |  |  |
| 38 | 6 | general rev 3 | A4 | ExceLint audit: formula error | missed |  |  |  |
| 39 | 6 | general rev 3 | G55 | ExceLint audit: formula error | missed |  |  |  |
| 40 | 6 | general rev 3 | I55 | ExceLint audit: formula error | missed |  |  |  |
| 41 | 6 | general rev 3 | K55 | ExceLint audit: formula error | missed |  |  |  |
| 42 | 6 | general rev 3 | G66 | ExceLint audit: formula error | missed |  |  |  |
| 43 | 6 | general rev 3 | I66 | ExceLint audit: formula error | missed |  |  |  |
| 44 | 6 | general rev 3 | K66 | ExceLint audit: formula error | missed |  |  |  |
| 45 | 6 | general rev 3 | K75 | ExceLint audit: formula error | missed |  |  |  |
| 46 | 6 | general rev 3 | G75 | ExceLint audit: formula error | missed |  |  |  |
| 47 | 6 | general rev 3 | I75 | ExceLint audit: formula error | missed |  |  |  |
| 48 | 6 | debt service page 5 | A4 | ExceLint audit: formula error | missed |  |  |  |
| 49 | 6 | debt service page 5 | G18 | ExceLint audit: formula error | missed |  |  |  |
| 50 | 6 | debt service page 5 | I18 | ExceLint audit: formula error | missed |  |  |  |
| 51 | 6 | debt service page 5 | K18 | ExceLint audit: formula error | missed |  |  |  |
| 52 | 6 | debt service page 5 | G39 | ExceLint audit: formula error | missed |  |  |  |
| 53 | 6 | debt service page 5 | I39 | ExceLint audit: formula error | missed |  |  |  |
| 54 | 6 | debt service page 5 | K39 | ExceLint audit: formula error | missed |  |  |  |
| 55 | 6 | debt service page 5 | K44 | ExceLint audit: formula error | missed |  |  |  |
| 56 | 6 | debt service page 5 | G50 | ExceLint audit: formula error | missed |  |  |  |
| 57 | 6 | debt service page 5 | I50 | ExceLint audit: formula error | missed |  |  |  |
| 58 | 6 | federal projects page 8 | A4 | ExceLint audit: formula error | missed |  |  |  |
| 59 | 6 | federal projects page 8 | H29 | ExceLint audit: formula error | missed |  |  |  |
| 60 | 6 | federal projects page 8 | J29 | ExceLint audit: formula error | missed |  |  |  |
| 61 | 6 | federal projects page 8 | F29 | ExceLint audit: formula error | missed |  |  |  |
| 62 | 6 | federal projects page 8 | F46 | ExceLint audit: formula error | missed |  |  |  |
| 63 | 8 | q3 fy04 | B218, C218, D218 | ExceLint audit: formula error | missed |  |  |  |
| 64 | 8 | q3 fy04 | F218 | ExceLint audit: formula error | missed |  |  |  |
| 65 | 8 | q3 fy04 | B68 | ExceLint audit: formula error | missed |  |  |  |
| 66 | 8 | q3 fy04 | C68, D68 | ExceLint audit: formula error | missed |  |  |  |
| 67 | 8 | q3 fy04 | F68 | ExceLint audit: formula error | missed |  |  |  |
| 68 | 8 | q3 fy04 | E218 | ExceLint audit: formula error | missed |  |  |  |
| 70 | 12 | notes to fs | C60 | ExceLint audit: formula error | missed |  |  |  |
| 71 | 12 | notes to fs | G346 | ExceLint audit: formula error | missed |  |  |  |
| 72 | 12 | annexure 3 | H11 | ExceLint audit: formula error | missed |  |  |  |
| 73 | 12 | annexure 3 | H17 | ExceLint audit: formula error | missed |  |  |  |
| 74 | 12 | annexure 3 | H12 | ExceLint audit: formula error | missed |  |  |  |
| 75 | 12 | annexure 3 | H15 | ExceLint audit: formula error | missed |  |  |  |
| 76 | 12 | annexure 3 | H13, H14 | ExceLint audit: formula error | missed |  |  |  |
| 77 | 12 | annexure 3 | H16 | ExceLint audit: formula error | missed |  |  |  |
| 78 | 12 | annexure 3 | H21 | ExceLint audit: formula error | missed |  |  |  |
| 79 | 12 | annexure 3 | H18, H19 | ExceLint audit: formula error | missed |  |  |  |
| 80 | 12 | annexure 3 | H20 | ExceLint audit: formula error | missed |  |  |  |
| 81 | 12 | annexure 3 | H28 | ExceLint audit: formula error | missed |  |  |  |
| 82 | 12 | annexure 4 | G9 | ExceLint audit: formula error | missed |  |  |  |
| 83 | 12 | annexure 4 | G12, G13, G14 | ExceLint audit: formula error | missed |  |  |  |
| 84 | 12 | annexure 4 | G22 | ExceLint audit: formula error | missed |  |  |  |
| 85 | 12 | annexure 4 | G25, G26, G27 | ExceLint audit: formula error | missed |  |  |  |
| 86 | 12 | annexure 4 | G8 | ExceLint audit: formula error | missed |  |  |  |
| 87 | 12 | appropriation statement | C127, D127, E127, F127, G127 | ExceLint audit: formula error | missed |  |  |  |
| 88 | 12 | appropriation statement | I127, J127 | ExceLint audit: formula error | missed |  |  |  |
| 89 | 12 | appropriation statement | C139, D139, E139, F139, G139 | ExceLint audit: formula error | missed |  |  |  |
| 90 | 12 | appropriation statement | I139, J139 | ExceLint audit: formula error | missed |  |  |  |
| 91 | 12 | appropriation statement | C185, D185, E185, F185 | ExceLint audit: formula error | missed |  |  |  |
| 92 | 12 | appropriation statement | I185, J185 | ExceLint audit: formula error | missed |  |  |  |
| 93 | 12 | appropriation statement | C239, D239, E239, F239 | ExceLint audit: formula error | missed |  |  |  |
| 94 | 12 | appropriation statement | I239, J239 | ExceLint audit: formula error | missed |  |  |  |
| 95 | 12 | appropriation statement | C296, D296, E296, F296, G296 | ExceLint audit: formula error | missed |  |  |  |
| 96 | 12 | appropriation statement | I296, J296 | ExceLint audit: formula error | missed |  |  |  |
| 97 | 12 | appropriation statement | C398, D398, E398, F398, G398 | ExceLint audit: formula error | missed |  |  |  |
| 98 | 12 | appropriation statement | I398, J398 | ExceLint audit: formula error | missed |  |  |  |
| 99 | 12 | appropriation statement | C173, D173, E173, F173 | ExceLint audit: formula error | missed |  |  |  |
| 100 | 12 | appropriation statement | I173, J173 | ExceLint audit: formula error | missed |  |  |  |
| 101 | 12 | appropriation statement | C227, D227, E227, F227 | ExceLint audit: formula error | missed |  |  |  |
| 102 | 12 | appropriation statement | I227, J227 | ExceLint audit: formula error | missed |  |  |  |
| 103 | 12 | appropriation statement | C30 | ExceLint audit: formula error | missed |  |  |  |
| 104 | 12 | appropriation statement | E30, F30, G30 | ExceLint audit: formula error | missed |  |  |  |
| 105 | 12 | appropriation statement | I30, J30 | ExceLint audit: formula error | missed |  |  |  |
| 106 | 12 | appropriation statement | C284 | ExceLint audit: formula error | missed |  |  |  |
| 107 | 12 | appropriation statement | I284, J284 | ExceLint audit: formula error | missed |  |  |  |
| 108 | 12 | appropriation statement | C344, D344, E344, F344, G344 | ExceLint audit: formula error | missed |  |  |  |
| 109 | 12 | appropriation statement | I344, J344 | ExceLint audit: formula error | missed |  |  |  |
| 110 | 12 | appropriation statement | C45 | ExceLint audit: formula error | missed |  |  |  |
| 111 | 12 | appropriation statement | E45, F45, G45 | ExceLint audit: formula error | missed |  |  |  |
| 112 | 12 | appropriation statement | I45, J45 | ExceLint audit: formula error | missed |  |  |  |
| 113 | 12 | appropriation statement | C357, D357, E357, F357, G357 | ExceLint audit: formula error | missed |  |  |  |
| 114 | 12 | appropriation statement | I357, J357 | ExceLint audit: formula error | missed |  |  |  |
| 115 | 12 | appropriation statement | C386, D386, E386, F386, G386 | ExceLint audit: formula error | missed |  |  |  |
| 116 | 12 | appropriation statement | I386, J386 | ExceLint audit: formula error | missed |  |  |  |
| 117 | 12 | appropriation statement | C78, D78, E78, F78 | ExceLint audit: formula error | missed |  |  |  |
| 118 | 12 | appropriation statement | I78, J78 | ExceLint audit: formula error | missed |  |  |  |
| 119 | 12 | appropriation statement | C89, D89, E89, F89 | ExceLint audit: formula error | missed |  |  |  |
| 120 | 12 | appropriation statement | I89, J89 | ExceLint audit: formula error | missed |  |  |  |
| 121 | 12 | appropriation statement | D284, E284, F284, G284 | ExceLint audit: formula error | missed |  |  |  |
| 122 | 12 | appropriation statement | E100 | ExceLint audit: formula error | missed |  |  |  |
| 123 | 12 | appropriation statement | E151 | ExceLint audit: formula error | missed |  |  |  |
| 124 | 12 | appropriation statement | E193, E194 | ExceLint audit: formula error | missed |  |  |  |
| 125 | 12 | appropriation statement | E251 | ExceLint audit: formula error | missed |  |  |  |
| 126 | 12 | appropriation statement | E306 | ExceLint audit: formula error | missed |  |  |  |
| 127 | 12 | appropriation statement | E135 | ExceLint audit: formula error | missed |  |  |  |
| 128 | 12 | appropriation statement | G306 | ExceLint audit: formula error | missed |  |  |  |
| 129 | 12 | appropriation statement | G410 | ExceLint audit: formula error | missed |  |  |  |
| 130 | 12 | appropriation statement | E150 | ExceLint audit: formula error | missed |  |  |  |
| 131 | 12 | appropriation statement | E355 | ExceLint audit: formula error | missed |  |  |  |
| 132 | 12 | appropriation statement | E410 | ExceLint audit: formula error | missed |  |  |  |
| 133 | 12 | appropriation statement | E191, E192 | ExceLint audit: formula error | missed |  |  |  |
| 134 | 13 | revenue assumptions | P28 | ExceLint audit: formula error | missed |  |  |  |
| 139 | 15 | cash flow | D57 | ExceLint audit: formula error | missed |  |  |  |
| 140 | 15 | cash flow | D58 | ExceLint audit: formula error | missed |  |  |  |
| 141 | 16 | c-5.5 | G40 | ExceLint audit: formula error | missed |  |  |  |
| 142 | 16 | c-5.6 wrkld by discrete categor | E47 | ExceLint audit: formula error | missed |  |  |  |
| 143 | 16 | c-5.9 | E7 | ExceLint audit: formula error | missed |  |  |  |
| 144 | 16 | c-5.9 | E16 | ExceLint audit: formula error | missed |  |  |  |
| 145 | 18 | finresrep 02-01-00 | C32, D32, E32, F32 | ExceLint audit: formula error | missed |  |  |  |
| 146 | 18 | finresrep 02-01-00 | C50, D50, E50, F50 | ExceLint audit: formula error | missed |  |  |  |
| 147 | 20 | sheet1 | C125 | ExceLint audit: formula error | missed |  |  |  |
| 148 | 20 | sheet1 | C147 | ExceLint audit: formula error | missed |  |  |  |
| 149 | 20 | sheet1 | C161 | ExceLint audit: formula error | missed |  |  |  |
| 150 | 20 | sheet1 | C37 | ExceLint audit: formula error | missed |  |  |  |
| 151 | 20 | sheet1 | C79 | ExceLint audit: formula error | missed |  |  |  |
| 152 | 20 | sheet1 | E25 | ExceLint audit: formula error | missed |  |  |  |
| 153 | 20 | placed online | C141, D141 | ExceLint audit: formula error | missed |  |  |  |
| 154 | 20 | placed online | C155 | ExceLint audit: formula error | missed |  |  |  |
| 155 | 20 | placed online | D37 | ExceLint audit: formula error | missed |  |  |  |
| 156 | 20 | placed online | D119 | ExceLint audit: formula error | missed |  |  |  |
| 157 | 20 | placed online | D155 | ExceLint audit: formula error | missed |  |  |  |
| 158 | 20 | placed online | D77 | ExceLint audit: formula error | missed |  |  |  |
| 159 | 21 | sheet1 | C39 | ExceLint audit: formula error | missed |  |  |  |
| 160 | 21 | sheet1 | G39 | ExceLint audit: formula error | missed |  |  |  |
| 161 | 21 | sheet1 | E39 | ExceLint audit: formula error | missed |  |  |  |
| 162 | 22 | no. 3 | E32, F32 | ExceLint audit: formula error | missed |  |  |  |
| 163 | 22 | no. 3 | J32 | ExceLint audit: formula error | missed |  |  |  |
| 164 | 22 | no. 4 | D34, E34, F34, G34, H34, I34, J34, K34 | ExceLint audit: formula error | missed |  |  |  |
| 165 | 22 | no. 4 | D20 | ExceLint audit: formula error | missed |  |  |  |
| 166 | 23 | reporting | AA14 | ExceLint audit: formula error | found | wrong_reference |  | "Class" (G15) is used where "Homework" (G14) belongs. |
| 167 | 23 | reporting | AA15 | ExceLint audit: formula error | missed |  |  |  |
| 168 | 23 | reporting | AA5 | ExceLint audit: formula error | missed |  |  |  |
| 169 | 23 | reporting | C16 | ExceLint audit: formula error | found | wrong_reference |  | The Elective total should sum the Elective block rows 17-19 (Reading/Preparing, Homework, Class), but the range points four rows up into the Requirements block, which the Requirements total in C12 already sums. |
| 170 | 23 | reporting | C20 | ExceLint audit: formula error | missed |  |  |  |
| 171 | 24 | salaries | B13, C13 | ExceLint audit: formula error | missed |  |  |  |
| 172 | 24 | salaries | B20 | ExceLint audit: formula error | missed |  |  |  |
| 173 | 24 | salaries | B32 | ExceLint audit: formula error | missed |  |  |  |
| 174 | 24 | salaries | F8 | ExceLint audit: formula error | missed |  |  |  |
| 175 | 24 | salaries | B36 | ExceLint audit: formula error | missed |  |  |  |
| 176 | 24 | salaries | C20 | ExceLint audit: formula error | missed |  |  |  |
| 177 | 24 | salaries | C32 | ExceLint audit: formula error | missed |  |  |  |
| 178 | 24 | salaries | C36 | ExceLint audit: formula error | missed |  |  |  |
| 179 | 24 | fy04 | F15, F16 | ExceLint audit: formula error | missed |  |  |  |
| 180 | 24 | fy04 | F19 | ExceLint audit: formula error | missed |  |  |  |
| 181 | 24 | fy04 | F17, F18 | ExceLint audit: formula error | missed |  |  |  |
| 182 | 24 | fy04 | F26, F27 | ExceLint audit: formula error | missed |  |  |  |
| 183 | 24 | fy04 | F32 | ExceLint audit: formula error | missed |  |  |  |
| 184 | 24 | fy05 | B27 | ExceLint audit: formula error | missed |  |  |  |
| 185 | 24 | fy05 | C19 | ExceLint audit: formula error | missed |  |  |  |
| 186 | 24 | fy05 | F23, F24, F25 | ExceLint audit: formula error | missed |  |  |  |
| 187 | 24 | fy05 | F26 | ExceLint audit: formula error | missed |  |  |  |
| 188 | 24 | fy05 | F31 | ExceLint audit: formula error | missed |  |  |  |
| 189 | 24 | fy06 | D12 | ExceLint audit: formula error | missed |  |  |  |
| 190 | 24 | fy06 | B32 | ExceLint audit: formula error | missed |  |  |  |
| 191 | 24 | fy07 | F27 | ExceLint audit: formula error | missed |  |  |  |
| 192 | 24 | fy08 | E27 | ExceLint audit: formula error | missed |  |  |  |
| 196 | 27 | final | D11 | ExceLint audit: formula error | missed |  |  |  |
| 197 | 27 | final | E11, F11, G11 | ExceLint audit: formula error | missed |  |  |  |
| 198 | 27 | 1st& 2nd iteration | D15, E15, F15, G15 | ExceLint audit: formula error | missed |  |  |  |
| 199 | 27 | 1st& 2nd iteration | I15 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: I7 belong to the same block but are left out. |
| 200 | 27 | 1st& 2nd iteration | K15 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: K7 belong to the same block but are left out. |
| 201 | 27 | 1st& 2nd iteration | M15 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: M7 belong to the same block but are left out. |
| 202 | 27 | 1st& 2nd iteration | O15 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: O7 belong to the same block but are left out. |
| 203 | 27 | 1st& 2nd iteration | D31, E31, F31, G31 | ExceLint audit: formula error | missed |  |  |  |
| 204 | 27 | 1st& 2nd iteration | I31 | ExceLint audit: formula error | missed |  |  |  |
| 205 | 27 | 1st& 2nd iteration | K31 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: K23 belong to the same block but are left out. |
| 206 | 27 | 1st& 2nd iteration | M31 | ExceLint audit: formula error | missed |  |  |  |
| 207 | 27 | 1st& 2nd iteration | O31 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: O23 belong to the same block but are left out. |
| 208 | 27 | 1st& 2nd iteration | H15 | ExceLint audit: formula error | found | extra_rows |  | The Hectares total for Period 2 should sum only the age-class rows H8:H14, but the range starts one row early and pulls in H7, which is the Period 1 total (=SUM(F7:F14)), so the result is 30 instead of 21.5. |
| 209 | 27 | 1st& 2nd iteration | L15 | ExceLint audit: formula error | found | extra_rows |  | The Hectares total for Period 3 should sum only the age-class rows L8:L14, but the range starts one row early and pulls in L7, which is the Period 2 total (=SUM(J7:J14)), so the result is 30 instead of 21.5. |
| 210 | 27 | 1st& 2nd iteration | H31 | ExceLint audit: formula error | found | extra_rows |  | The Hectares total for Period 2 should sum only the age rows H24:H30, but the range starts one row early and pulls in H23, the Period 1 Hectares subtotal (=SUM(F23:F30)), so the total becomes 30 instead of 20.1. |
| 211 | 27 | 1st& 2nd iteration | L31 | ExceLint audit: formula error | found | extra_rows |  | The Hectares total for Period 3 should sum only the age rows 24-30, but the range starts one row early and pulls in L23, the Period 2 total (=SUM(J23:J30)), so it adds another period's total to this one. |
| 212 | 27 | 1st& 2nd iteration | P15 | ExceLint audit: formula error | found | extra_rows |  | The Area total should sum only the age rows P7:P14, but the range now starts at P6, which is the separate Volume subtotal (=SUM(N7:N14)), so Volume is added into the Area total. |
| 213 | 27 | 1st& 2nd iteration | P31 | ExceLint audit: formula error | found | extra_rows |  | The Area total should sum only the age rows 24-30, but the range starts at row 22 and pulls in the separate N23:N30 subtotal in P22, so that subtotal is counted again. |
| 214 | 28 | general ledger | B12 | ExceLint audit: formula error | missed |  |  |  |
| 215 | 28 | general ledger | G11 | ExceLint audit: formula error | missed |  |  |  |
| 216 | 29 | total loe | B70 | ExceLint audit: formula error | missed |  |  |  |
| 217 | 30 | summary inst | B14, C14, D14, E14 | ExceLint audit: formula error | missed |  |  |  |
| 218 | 30 | summary inst | G14 | ExceLint audit: formula error | missed |  |  |  |
| 219 | 30 | summary inst | F14 | ExceLint audit: formula error | missed |  |  |  |
| 220 | 30 | summary urban | B12, C12, D12, E12, F12 | ExceLint audit: formula error | missed |  |  |  |
| 221 | 30 | summary urban | G12, H12 | ExceLint audit: formula error | missed |  |  |  |
| 227 | 34 | sheet1 | C21, D21, E21, F21 | ExceLint audit: formula error | missed |  |  |  |
| 228 | 34 | sheet1 | H21 | ExceLint audit: formula error | missed |  |  |  |
| 229 | 34 | sheet1 | J21, K21 | ExceLint audit: formula error | missed |  |  |  |
| 230 | 36 | sheet1 | F10, F11, F7, F8, F9 | ExceLint audit: formula error | missed |  |  |  |
| 231 | 36 | sheet1 | F6 | ExceLint audit: formula error | missed |  |  |  |
| 232 | 36 | sheet1 | G6, G7, G8 | ExceLint audit: formula error | missed |  |  |  |
| 233 | 38 | sheet1 | H93, I93, J93, K93 | ExceLint audit: formula error | missed |  |  |  |
| 234 | 38 | sheet1 | D93, E93, F93, G93 | ExceLint audit: formula error | missed |  |  |  |
| 235 | 41 | bts par section | J105, J106, J107, J108 | ExceLint audit: formula error | missed |  |  |  |
| 236 | 41 | bts par section | J109 | ExceLint audit: formula error | found | wrong_reference |  | "Force de vente" (G108) is used where "Etablissement" (G109) belongs. |
| 237 | 43 | annex d - app. of funds | C17, D17, E17 | ExceLint audit: formula error | missed |  |  |  |
| 238 | 43 | annex d - app. of funds | C27 | ExceLint audit: formula error | missed |  |  |  |
| 239 | 43 | annex d - app. of funds | D27, E27 | ExceLint audit: formula error | missed |  |  |  |
| 312 | 45 | tsfhours | J184, J185 | ExceLint audit: formula error | missed |  |  |  |
| 313 | 45 | tsfhours | J84, J85 | ExceLint audit: formula error | missed |  |  |  |
| 314 | 45 | tsfhours | M184, M185 | ExceLint audit: formula error | missed |  |  |  |
| 315 | 45 | tsfhours | M84, M85 | ExceLint audit: formula error | missed |  |  |  |
| 316 | 45 | tsfhours | P184, P185 | ExceLint audit: formula error | missed |  |  |  |
| 317 | 45 | tsfhours | P84, P85 | ExceLint audit: formula error | missed |  |  |  |
| 318 | 45 | tsfhours | S184, S185 | ExceLint audit: formula error | missed |  |  |  |
| 319 | 45 | tsfhours | S84, S85 | ExceLint audit: formula error | missed |  |  |  |
| 320 | 45 | tsfhours | D184, D185 | ExceLint audit: formula error | missed |  |  |  |
| 321 | 45 | tsfhours | D84, D85 | ExceLint audit: formula error | missed |  |  |  |
| 322 | 45 | tsfhours | G184, G185 | ExceLint audit: formula error | missed |  |  |  |
| 323 | 45 | tsfhours | G84, G85 | ExceLint audit: formula error | missed |  |  |  |
| 335 | 46 | aial | F35, G35, H35, I35, J35, K35, L35, M35 | ExceLint audit: formula error | missed |  |  |  |
| 336 | 46 | aial | B49, C49, D49, E49, F49, G49 | ExceLint audit: formula error | missed |  |  |  |
| 337 | 46 | aial | J49, K49, L49, M49 | ExceLint audit: formula error | missed |  |  |  |
| 338 | 46 | aial | D74, E74, F74, G74, H74, I74, J74, K74,  | ExceLint audit: formula error | missed |  |  |  |
| 339 | 46 | aial | D86, E86, F86, G86, H86, I86, J86, K86,  | ExceLint audit: formula error | missed |  |  |  |
| 340 | 46 | aial | B97, C97, D97 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: Taxation Receivable belong to the same block but are left out. |
| 341 | 46 | aial | F97, G97, H97, I97, J97, K97, L97, M97 | ExceLint audit: formula error | missed |  |  |  |
| 342 | 46 | aial | B148 | ExceLint audit: formula error | found | wrong_reference |  | "CASH AT END OF THE YEAR" (C149) is used where "NET INCREASE (DECREASE) IN CASH HELD" (C147) belongs. |
| 343 | 46 | aial | B35, C35, D35 | ExceLint audit: formula error | missed |  |  |  |
| 344 | 46 | aial | B74, C74 | ExceLint audit: formula error | missed |  |  |  |
| 345 | 46 | aial | B86, C86 | ExceLint audit: formula error | missed |  |  |  |
| 346 | 46 | aial | E35 | ExceLint audit: formula error | missed |  |  |  |
| 347 | 46 | aial | E97 | ExceLint audit: formula error | missed |  |  |  |
| 348 | 46 | aial | I49 | ExceLint audit: formula error | missed |  |  |  |
| 365 | 46 | wial | G76, H76, I76, J76, K76 | ExceLint audit: formula error | found | skipped_rows |  | The SUM range stops short: Bank Overdraft/Advance belong to the same block but are left out. |
| 366 | 46 | wial | B144 | ExceLint audit: formula error | found | wrong_reference |  | "CASH AT END OF THE YEAR" (C145) is used where "NET INCREASE (DECREASE) IN CASH HELD" (C143) belongs. |
| 367 | 46 | wial | B42 | ExceLint audit: formula error | missed |  |  |  |
| 368 | 46 | wial | B76, C76, D76, E76, F76 | ExceLint audit: formula error | missed |  |  |  |
| 369 | 46 | cial | B14, C14, D14, E14, F14, G14 | ExceLint audit: formula error | missed |  |  |  |
| 370 | 46 | cial | I14, J14, K14, L14, M14 | ExceLint audit: formula error | missed |  |  |  |
| 371 | 46 | cial | F43, G43, H43, I43, J43, K43, L43, M43 | ExceLint audit: formula error | missed |  |  |  |
| 372 | 46 | cial | H14 | ExceLint audit: formula error | missed |  |  |  |
| 373 | 47 | note 14-16 | I13 | ExceLint audit: formula error | missed |  |  |  |
| 374 | 47 | note 14-16 | K13 | ExceLint audit: formula error | missed |  |  |  |
| 375 | 47 | note 14-16 | M13 | ExceLint audit: formula error | missed |  |  |  |
| 376 | 47 | note 14-16 | O13 | ExceLint audit: formula error | missed |  |  |  |
| 377 | 47 | note 17-18 | L40 | ExceLint audit: formula error | missed |  |  |  |
| 378 | 47 | note 20 | L48 | ExceLint audit: formula error | missed |  |  |  |
| 379 | 47 | note 20 | N48 | ExceLint audit: formula error | missed |  |  |  |
| 380 | 48 | sheet1 | D31 | ExceLint audit: formula error | missed |  |  |  |
| 381 | 49 | sheet1 | D13 | ExceLint audit: formula error | missed |  |  |  |
| 382 | 49 | sheet1 | D17 | ExceLint audit: formula error | missed |  |  |  |
| 383 | 49 | sheet1 | D43, D44, D45, D46, D47 | ExceLint audit: formula error | missed |  |  |  |
| 384 | 49 | sheet1 | D48 | ExceLint audit: formula error | missed |  |  |  |
| 385 | 50 | current funds | F18 | ExceLint audit: formula error | missed |  |  |  |
| 386 | 50 | current funds | H18 | ExceLint audit: formula error | missed |  |  |  |
| 387 | 53 | summary | B12 | ExceLint audit: formula error | missed |  |  |  |
| 388 | 53 | summary | D12, E12 | ExceLint audit: formula error | missed |  |  |  |
| 389 | 53 | summary | C12 | ExceLint audit: formula error | missed |  |  |  |
| 390 | 56 | fall | E24 | ExceLint audit: formula error | missed |  |  |  |
| 391 | 56 | fall | K24 | ExceLint audit: formula error | missed |  |  |  |
| 392 | 56 | fall | H24 | ExceLint audit: formula error | missed |  |  |  |
| 394 | 56 | c | H16 | ExceLint audit: formula error | missed |  |  |  |
| 395 | 56 | c | I26, I27, I28, I29, I30, I31 | ExceLint audit: formula error | not_covered |  |  |  |
| 396 | 56 | c | I33, I34, I35, I36, I37 | ExceLint audit: formula error | not_covered |  |  |  |
| 397 | 56 | d | L24, L25 | ExceLint audit: formula error | missed |  |  |  |
| 398 | 56 | d | C24, C25 | ExceLint audit: formula error | missed |  |  |  |
| 399 | 56 | d | F24, F25 | ExceLint audit: formula error | missed |  |  |  |
| 400 | 56 | d | I24, I25 | ExceLint audit: formula error | missed |  |  |  |
| 401 | 56 | d | H16 | ExceLint audit: formula error | missed |  |  |  |
| 402 | 56 | d (2) | L24, L25 | ExceLint audit: formula error | missed |  |  |  |
| 403 | 56 | d (2) | C24, C25 | ExceLint audit: formula error | missed |  |  |  |
| 404 | 56 | d (2) | F24, F25 | ExceLint audit: formula error | missed |  |  |  |
| 405 | 56 | d (2) | I24, I25 | ExceLint audit: formula error | missed |  |  |  |
| 406 | 56 | d (2) | H16 | ExceLint audit: formula error | missed |  |  |  |
| 407 | 57 | crime | L16 | ExceLint audit: formula error | missed |  |  |  |
| 408 | 57 | ete | L22 | ExceLint audit: formula error | missed |  |  |  |
| 409 | 57 | cross panel | K6, L6 | ExceLint audit: formula error | missed |  |  |  |
| 410 | 57 | cross panel | K9, L9 | ExceLint audit: formula error | missed |  |  |  |
| 411 | 57 | cross panel | L8 | ExceLint audit: formula error | missed |  |  |  |
| 412 | 57 | envt | J17 | ExceLint audit: formula error | missed |  |  |  |
| 413 | 57 | envt | L20 | ExceLint audit: formula error | missed |  |  |  |
| 414 | 61 | lem demand calibration | D162 | ExceLint audit: formula error | missed |  |  |  |
| 415 | 61 | lem demand calibration | D178 | ExceLint audit: formula error | missed |  |  |  |
| 416 | 61 | lem demand calibration | D193 | ExceLint audit: formula error | missed |  |  |  |
| 417 | 61 | c&p calc | D169 | ExceLint audit: formula error | missed |  |  |  |
| 418 | 61 | c&p calc | D171 | ExceLint audit: formula error | missed |  |  |  |
| 419 | 61 | c&p calc | E169, F169, G169, H169, I169 | ExceLint audit: formula error | missed |  |  |  |
| 420 | 61 | c&p calc | E171, F171, G171, H171, I171 | ExceLint audit: formula error | missed |  |  |  |
| 421 | 63 | summary1201 | B21, C21 | ExceLint audit: formula error | missed |  |  |  |
| 422 | 63 | summary1201 | E21 | ExceLint audit: formula error | missed |  |  |  |
| 423 | 63 | summary1201 | G21 | ExceLint audit: formula error | missed |  |  |  |
| 424 | 70 | revenues by source | B15, C15 | ExceLint audit: formula error | missed |  |  |  |
| 425 | 70 | expenditures by function | B19, C19 | ExceLint audit: formula error | missed |  |  |  |
| 426 | 70 | expenditures by category | B15, C15 | ExceLint audit: formula error | missed |  |  |  |
| 427 | 70 | ftee calculation | B27, C27 | ExceLint audit: formula error | missed |  |  |  |
| 428 | 70 | ftee calculation | F27 | ExceLint audit: formula error | missed |  |  |  |
| 429 | 70 | ftee calculation | H27, I27 | ExceLint audit: formula error | missed |  |  |  |
| 430 | 70 | ftee calculation | E27 | ExceLint audit: formula error | missed |  |  |  |

## By category

| category | found | missed | unsupported | not covered |
|---|---|---|---|---|
| ExceLint audit: formula error | 20 | 294 | 0 | 3 |

## False alarms (10)

| id | formula | type | reason |
|---|---|---|---|
| 21:Sheet1!X16 | `=B16*B$2+K16*K$2+L16*L$2+V16*V$2+W16*W$2+5` | extra_rows | The weighted total in the Pts > Tot column adds a stray +5, so it no longer matches the peer formulas in X14, X15 and X17, which are pure weighted sums of Article, Two, Exam, Best and Perf. |
| 22:No. 3!F55 | `=F49/F54` | wrong_reference | "Sec. Ratio 1 to" (F49) is used where "XXXXXXX" (F47) belongs. |
| 28:General Ledger!G25 | `=SUM(G21:G23)` | skipped_rows | The SUM range stops short: FOH belong to the same block but are left out. |
| 28:General Ledger!J25 | `=SUM(J21:J23)` | skipped_rows | The SUM range stops short: FOH belong to the same block but are left out. |
| 28:General Ledger!M25 | `=SUM(M21:M23)` | skipped_rows | The SUM range stops short: FOH belong to the same block but are left out. |
| 28:General Ledger!G34 | `=SUM(G30:G32)` | skipped_rows | The SUM range stops short: FOH belong to the same block but are left out. |
| 28:General Ledger!M34 | `=SUM(M30:M32)` | skipped_rows | The SUM range stops short: FOH belong to the same block but are left out. |
| 36:Sheet1!E7 | `=AVERAGE(B7:D7)` | wrong_function | "Smith" calls for SUM, but the formula uses AVERAGE. |
| 61:c&P calc!D31 | `=+SUM(D18:D27)` | skipped_rows | The SUM range stops short: D28, D29, D30 belong to the same block but are left out. |
| 61:c&P calc!I152 | `=+I141*'LEM Demand Calibration'!H59` | missing_factor | The product leaves out "Assumed cost A&T/yielded chip" ('LEM Demand Calibration'!$D$46), which the neighbouring cells apply. |
