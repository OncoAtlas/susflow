 # DATASUS File Patterns Summary (FTP)

 Base: `ftp.datasus.gov.br`

 ## 1. SIM – Mortality Information System

 **Base path:** `/dissemin/publicos/SIM/CID10/`

 | Subfolder | Pattern | Description | Example |
 | --------- | ------- | ----------- | ------- |
 | `DOFET` | `DOEXT<AA>.DBC` | Adult deaths – extended format (AA = year, 2 digits) | `DOEXT00.DBC`, `DOEXT23.DBC` |
 | `DOFET` | `DOFET<AA>.DBC` | Fetal deaths – reduced format | `DOFET00.dbc`, `DOFET23.dbc` |
 | `DOFET` | `DOINF<AA>.DBC` | Infant deaths (0‑1 year) | `DOINF00.DBC`, `DOINF23.dbc` |
 | `DOFET` | `DOMAT<AA>.DBC` | Maternal deaths | `DOMAT00.DBC`, `DOMAT23.dbc` |
 | `DOFET` | `DOREXT<AA>.DBC` | Deaths of residents in other states (small files) | `DOREXT13.dbc`, `DOREXT23.dbc` |
 | `DORES` | `DO<UF><AAAA>.DBC` | Deaths by state + full year (4 digits) | `DOAC2000.dbc`, `DOBR2024.dbc` |
 | `DORES` | `DO<UF><AA>.DBC` | Deaths by state + year (2 digits – early years) | `DOAC1996.dbc` |
 | `DOCS` | `Docs_Tabs_CID10.zip`, `Estrutura_do_SIM_2025.pdf` | Documentation, layouts and manuals | |
 | `TAB` | `OBITOS_CID10_TAB.zip`, `CNVS_CID10_v2019.rar` | Aggregated data and auxiliary tables | |
 | `TABELAS` | `CID10.DBF`, `TABUF.DBF`, `CADMUN.DBF` | Support tables (CID10, UF, municipalities) | |

 ## 2. SINASC – Live Births Information System

 **Base path:** `/dissemin/publicos/SINASC/NOV/DNRES/`

 | Pattern | Description | Example |
 | ------- | ----------- | ------- |
 | `DN<UF><AAAA>.DBC` | Live births by state + year (4 digits) | `DNAC1996.DBC`, `DNRJ2022.dbc` |
 | `DN<UF><AA>.DBC` | Live births by state + year (2 digits) | `DNAC96.DBC` (may not appear in mapping but common) |
 | `DNBR<AAAA>.DBC` | Live births – Brazil (national aggregate) | `DNBR2014.dbc` |
 | `DNEX<AAAA>.dbc` | Exceptions / supplementary records (small files) | `DNEX2021.dbc` |

 _Note: early years used two-digit years; from 2000 onward four digits are common._

 ## 3. SINAN – Notifiable Diseases Information System

 **Base path:** `/dissemin/publicos/SINAN/DADOS/` (subfolders `FINAIS/` and `PRELIM/`)

 ### General pattern:

 - Final data: `FINAIS/<DISEASE><UF><AA>.DBC` or `<DISEASE>BR<AA>.DBC`
 - Preliminary data: `PRELIM/<DISEASE><UF><AA>.DBC` (same structure)

 ### Main diseases (prefixes):

 | Prefix | Disease | Example |
 | ------ | ------- | ------- |
 | `ACBI` | Occupational accident with link | `ACBIBR07.dbc` |
 | `ACGR` | Severe occupational accident | `ACGRBR07.dbc` |
 | `ANIM` | Venomous animal accidents | `ANIMBR07.dbc` |
 | `ANTR` | Anthrax | `ANTRBR07.dbc` |
 | `BOTU` | Botulism | `BOTUBR07.dbc` |
 | `CANC` | Cancer (notification) | `CANCBR07.dbc` |
 | `CHAG` | Chagas disease | `CHAGBR00.dbc` |
 | `CHIK` | Chikungunya | `CHIKBR15.dbc` |
 | `COQU` | Pertussis | `COQUBR07.dbc` |
 | `DENG` | Dengue | `DENGBR00.dbc` |
 | `DERM` | Occupational dermatoses | `DERMBR06.dbc` |
 | `DIFT` | Diphtheria | `DIFTBR07.dbc` |
 | `ESQU` | Schistosomiasis | `ESQUBR07.dbc` |
 | `FMAC` | Spotted fever | `FMACBR07.dbc` |
 | `FTIF` | Typhoid fever | `FTIFBR07.dbc` |
 | `HANS` | Leprosy | `HANSBR01.dbc` |
 | `HANT` | Hantavirus | `HANTBR00.dbc` |
 | `IEXO` | Exogenous intoxication (other) | `IEXOBR06.dbc` |
 | `LEIV` | Visceral leishmaniasis | `LEIVBR00.dbc` |
 | `LEPT` | Leptospirosis | `LEPTBR00.dbc` |
 | `LTA` | American cutaneous leishmaniasis | `LTANBR00.dbc` |
 | `MALA` | Malaria | `MALABR04.dbc` |
 | `MENI` | Meningitis | `MENIBR07.dbc` |
 | `MENT` | (other) mental disorders | `MENTBR06.dbc` |
 | `NTRA` | NTRA – possible pesticide intoxication | `NTRABR10.dbc` |
 | `PAIR` | Acute flaccid paralysis | `PAIRBR06.dbc` |
 | `PEST` | Plague | `PESTBR07.dbc` |
 | `PFAN` | Yellow fever (PFAN) | `PFANBR07.dbc` |
 | `PNEU` | Pneumonia (SAR) | `PNEUBR06.dbc` |
 | `RAIV` | Human rabies | `RAIVBR07.dbc` |
 | `ROTA` | Rotavirus | `ROTABR09.dbc` |
 | `SDTA` | Toxemia of pregnancy syndrome (other) | `SDTABR07.dbc` |
 | `TETA` | Accidental tetanus | `TETABR07.dbc` |
 | `TOXC` | Specific intoxication (TOXC) | `TOXCBR19.dbc` |
 | `TRAC` | Trachoma | `TRACBR09.dbc` |
 | `TUBE` | Tuberculosis | `TUBEBR01.dbc` |
 | `VIOL` | Domestic and other violence | `VIOLBR09.dbc` |
 | `ZIKA` | Zika virus | `ZIKABR16.dbc` |

 _Note: `UF` can be `BR` (Brazil) or the state code (e.g. `SP`, `RJ`)._

 ## 4. SIH/SIHSUS – Hospital Information System

 **Base path:** `/dissemin/publicos/SIHSUS/200801_/Dados/`

 ### Common naming patterns:

 | Pattern | Description | Example |
 | ------- | ----------- | ------- |
 | `RD<UF><AA><MM>.dbc` | **Hospitalization summary** – main admissions file | `RDSP0801.dbc` (2008/jan) |
 | `ER<UF><AA><MM>.dbc` | Professional services complement (ER) | `ERSP0801.dbc` |
 | `SP<UF><AA><MM>.dbc` | Complement (professional services – old) | `SPAC0801.dbc` |
 | `RJ<UF><AA><MM>.dbc` | Complement – appears for multiple states | `RJSP0801.dbc` |
 | `CHBR<AA><MM>.dbc` | Header? (small files) | `CHBR1901.dbc` |
 | `CMBR<AA><MM>.dbc` | Complement? (small files) | `CMBR1901.dbc` |

 **Note:** `<AA>` = two-digit year; `<MM>` = month (01 to 12).

 ## 5. SIA/SIASUS – Outpatient Information System

 **Base path:** `/dissemin/publicos/SIASUS/200801_/Dados/`

 | Pattern | Description | Example |
 | ------- | ----------- | ------- |
 | `AB<UF><AA><MM>.dbc` | **Outpatient production** (APAC, BPA, etc.) – main file | `ABSP0801.dbc`, `ABAC2501.dbc` |
 | `ACF<UF><AA><MM>.dbc` | Authorization for high-cost / complex procedures | `ACFAL1408.dbc` |
 | `PA<UF><AA><MM>.dbc` | Another outpatient production format (common) | `PASPB0801.dbc` |

 **Name structure:**

 - `AB`, `PA`, `ACF` = file type
 - `UF` = state code (e.g. `SP`, `RJ`, `BR`)
 - `AA` = year (two digits)
 - `MM` = month

 ## 6. Additional complementary patterns

 ### Documentation and layout files

 - Usually located in `DOCS/` or `TABELAS/` subfolders within each system.
 - Extensions: `.pdf`, `.zip`, `.rar`, `.DBF`.

 ### Support tables

 - **UF:** `TABUF.DBF`
 - **Municipalities:** `CADMUN.DBF` or `Tabela-de-Municipios-informacoes.pdf`
 - **CID10:** `CID10.DBF`
 - **CID10 chapters:** `CIDCAP10.DBF`
 - **CBO (occupations):** `TABOCUP.DBF`
 - **Countries:** `TABPAIS.DBF`

 ## 7. Query and usage tips

 - **Prefix is the key**: identify the system by the file prefix (e.g. `DO` = SIM, `DN` = SINASC, `RD`/`ER` = SIH, `AB` = SIA).
 - **Year**: most use two digits until 1999, then four digits or two+two (year+month).
 - **UF**: `BR` = Brazil; two-character state codes for states.
 - **`.dbc` extension** → compressed file (DBF + proprietary compression). Use `dbc2dbf` or libraries like `pysus`.
 - **Preliminary files**: in `SINAN/DADOS/PRELIM/` – data not yet consolidated.
 - **Final files**: in `FINAIS/` (SINAN) or in each system's root directories.

 ## 8. Query examples by system

 | Goal | Pattern to look for | Typical path |
 | ---- | ------------------- | ------------ |
 | Deaths in Rio de Janeiro in 2023 | `DORJ2023.DBC` | `/dissemin/publicos/SIM/CID10/DORES/` |
 | Live births in São Paulo, 2022 | `DNSP2022.dbc` | `/dissemin/publicos/SINASC/NOV/DNRES/` |
 | Dengue in Brazil, 2020 (final) | `DENGBR20.dbc` (or `DENGBR2020.dbc`) | `/dissemin/publicos/SINAN/DADOS/FINAIS/` |
 | Hospital admissions in Minas Gerais, Jan 2019 | `RDMG1901.dbc` | `/dissemin/publicos/SIHSUS/200801_/Dados/` |
 | Outpatient production in Ceará, Dec 2021 | `ABCE2112.dbc` | `/dissemin/publicos/SIASUS/200801_/Dados/` |

 ---

 _Last updated: 2026-05-13 (based on the provided mapping)._  
 _For new systems or changes, consult the FTP directory directly or the official DATASUS documentation._
