 # SIASUS — Ambulatory Information System (SUS)

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | By state | `read(uf, year, month)` | `DataFrame` | Ambulatory microdata for a state |
 | By state | `download(uf, year, month)` | `Path` | Raw `.dbc` file |

 ---

 ## Available prefixes

 **File pattern:** `{PREFIX}{UF}{YY}{MM}.dbc`  
 **Granularity:** monthly / by state

 ```python
 from susflow.systems import siasus

 # show all available prefixes
 print(siasus.prefixes())

 # Ambulatory production — default prefix
 df = siasus.read(uf="SP", year=2023, month=1)
 df = siasus.read(uf="SP", year=2023, month=1, prefix="PA")

 # other prefixes
 df = siasus.read(uf="SP", year=2023, month=1, prefix="AQ")   # chemotherapy
 df = siasus.read(uf="RJ", year=2023, month=6, prefix="ATD")  # dialysis

 # download only
 path = siasus.download(uf="SP", year=2023, month=1)
 path = siasus.download(uf="MG", year=2023, month=3, prefix="AM")

 # list available files
 siasus.list_files()                          # all PA files
 siasus.list_files(uf="SP")                   # PA files for SP
 siasus.list_files(uf="SP", prefix="AQ")      # chemotherapy for SP
 ```

 ### Active prefixes

 | Prefix | Example file | Content | Coverage |
 |--------|---------------|---------|----------|
 | `PA` | `PASP2301.dbc` | **Ambulatory Production (BPA)** — main dataset | 2008–2026 |
 | `BI` | `BISP2301.dbc` | Individualized BPA | 2008–2026 |
 | `AD` | `ADSP2301.dbc` | APAC for Miscellaneous Reports | 2008–2026 |
 | `AM` | `AMSP2301.dbc` | APAC for Medications | 2008–2026 |
 | `AMP` | `AMPSP2301.dbc` | APAC for Standardized Medications | 2020–2026 |
 | `AQ` | `AQSP2301.dbc` | APAC for Chemotherapy | 2008–2026 |
 | `AR` | `ARSP2301.dbc` | APAC for Radiotherapy | 2008–2026 |
 | `ACF` | `ACFSP1408.dbc` | APAC for AV fistula creation | 2014–2026 |
 | `ATD` | `ATDSP1408.dbc` | APAC for Dialysis Treatment | 2014–2026 |
 | `PS` | `PSSP1305.dbc` | Psychosocial RAAS | 2013–2026 |
 | `AB` | `ABSP2501.dbc` | APAC for Post-Bariatric Surgery Follow-up (new) | 2025–2026 |

 ### Retired prefixes (still available on the FTP)

 | Prefix | Example file | Content | Coverage | Note |
 |--------|--------------|---------|----------|------|
 | `ABO` | `ABOSP1502.dbc` | Legacy post-bariatric APAC | 2015–2018 | Replaced by `AB` |
 | `AN` | `ANSP0801.dbc` | Nephrology APAC | 2008–2014 | Replaced by `ATD` |
 | `SAD` | `SADSP1307.dbc` | Home care RAAS | 2013–2015 | Retired |

 > Year validation respects each prefix coverage. Attempting to download `AN` for 2020 will raise an error.

 ---

 ## Difference between PA and BI

 - `PA` (Consolidated BPA) — each row represents the total procedures performed by an establishment in a month. Aggregated data.
 - `BI` (Individualized BPA) — each row represents a single attendance. Microdata with patient identifiers.

 For individual-level analyses (patient profiles, care trajectories) use `BI`. For production-by-establishment analyses use `PA`.

 ---

 ## Difference between AM and AMP

 - `AM` — APAC for Medications (all medications in the specialized component)
 - `AMP` — APAC for Standardized Medications (specific subset, available from 2020)

 ---

 ## Main DataFrame variables (PA — Ambulatory Production)

 | Variable | Type | Description |
 |----------|------|-------------|
 | `PA_CODUNI` | str | Establishment CNES code |
 | `PA_GESTAO` | str | Management code |
 | `PA_CONDIC` | str | Attendance condition |
 | `PA_UFMUN` | str | Municipality IBGE code |
 | `PA_REGCT` | str | Contractual registration |
 | `PA_INCOUT` | str | Other increment |
 | `PA_INCURG` | str | Emergency increment |
 | `PA_TPUPS` | str | UPS type |
 | `PA_TIPPRE` | str | Provider type |
 | `PA_MN_IND` | str | Modality/nature |
 | `PA_CNPJCPF` | str | Establishment CNPJ/CPF |
 | `PA_CNPJMNT` | str | Maintainer CNPJ |
 | `PA_CNPJ_CC` | str | Contract CNPJ |
 | `PA_MVM` | str | Movement month/year (YYYYMM) |
 | `PA_CMP` | str | Competence month/year (YYYYMM) |
 | `PA_PROC_ID` | str | Procedure code (SIGTAP) |
 | `PA_TPFIN` | str | Funding type |
 | `PA_SUBFIN` | str | Funding subsource |
 | `PA_NIVCPL` | str | Complexity level |
 | `PA_DOCORIG` | str | Originating document |
 | `PA_AUTORIZ` | str | Authorization number |
 | `PA_CNSMED` | str | Professional CNS |
 | `PA_CBOCOD` | str | Professional CBO |
 | `PA_MOTSAI` | str | Discharge reason |
 | `PA_OBITO` | str | Death indicator |
 | `PA_ENCERR` | str | Closing indicator |
 | `PA_PERMAN` | str | Permanence indicator |
 | `PA_ALTA` | str | Discharge indicator |
 | `PA_TRANSF` | str | Transfer indicator |
 | `PA_QTDPRO` | str | Produced quantity |
 | `PA_QTDAPR` | str | Approved quantity |
 | `PA_VALPRO` | float | Produced value (BRL) |
 | `PA_VALAPR` | float | Approved value (BRL) |

 > For a complete variable dictionary per prefix, consult DATASUS official documentation (SIGTAP).

 ---

 ## Recommended workflow

 ```
 1. Explore what's available
    print(siasus.prefixes())               ← all prefixes and descriptions
    siasus.list_files(uf="SP")             ← PA files available for SP
    siasus.list_files(uf="SP", prefix="AQ") ← chemotherapy for SP

 2. Download the data
    df = siasus.read(uf="SP", year=2023, month=1)               ← ambulatory production
    df = siasus.read(uf="SP", year=2023, month=1, prefix="AQ")  ← chemotherapy

 3. Combine months into a time series
    import pandas as pd
    dfs = [siasus.read(uf="SP", year=2023, month=m) for m in range(1, 13)]
    df_year = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The year uses **2 digits** and the month **2 digits with leading zero**: `PASP2301.dbc` = SP, January 2023.
 - Each prefix has its own temporal coverage. Year validation is prefix-specific — attempting to download `AN` for 2020 will raise an error with the correct coverage.
 - `PA` is the largest file — large states (SP, RJ, MG) may have hundreds of MB per month.
 - Procedures are identified by SIGTAP code (`PA_PROC_ID`). Consult the SIGTAP table for descriptions.
 - To map municipalities to names, use `CADMUN.DBF` available in SIM (`sim.download_tables("CADMUN.DBF")`).
