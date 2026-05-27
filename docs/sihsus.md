 # SIHSUS — Hospital Information System (SUS)

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | By state | `ler(uf, ano, mes)` | `DataFrame` | Hospitalization microdata for a state |
 | By state | `baixar(uf, ano, mes)` | `Path` | Raw `.dbc` file per state |
 | National | `ler_nacional(ano, mes)` | `DataFrame` | Aggregated national data (CH or CM) |
 | National | `baixar_nacional(ano, mes)` | `Path` | National `.dbc` file |

 ---

 ## Data by state

 **File pattern:** `{PREFIX}{UF}{YY}{MM}.dbc`  
 **Coverage:** 2008–2026, all 27 states  
 **Granularity:** monthly

 ```python
 from susflow.systems import sihsus

 # show available prefixes
 print(sihsus.prefixos())

 # Reduced AIH — main dataset (default prefix: RD)
 df = sihsus.ler(uf="SP", ano=2023, mes=1)
 df = sihsus.ler(uf="RJ", ano=2022, mes=12)

 # other prefixes
 df = sihsus.ler(uf="MG", ano=2023, mes=6, prefixo="SP")  # professional services
 df = sihsus.ler(uf="BA", ano=2023, mes=3, prefixo="RJ")  # rejected AIH

 # download only
 path = sihsus.baixar(uf="SP", ano=2023, mes=1)
 path = sihsus.baixar(uf="SP", ano=2023, mes=1, prefixo="ER")

 # list available files
 sihsus.listar()                        # all RD files
 sihsus.listar(uf="SP")               # RD files for SP
 sihsus.listar(uf="SP", prefixo="SP")   # professional services for SP
 ```

 ### Prefixes by state

 | Prefix | Example file | Content |
 |--------|---------------|---------|
 | `RD` | `RDSP2301.dbc` | **Reduced AIH — main dataset** (hospitalization record) |
 | `SP` | `SPSP2301.dbc` | Complementary professional services |
 | `RJ` | `RJSP2301.dbc` | Rejected AIH (not approved for payment) |
 | `ER` | `ERSP2301.dbc` | AIH with data entry errors |

 ---

 ## National data (CH and CM)

 **File pattern:** `{PREFIX}BR{YY}{MM}.dbc`  
 **Scope:** national (BR fixed — no state-level version)

 ```python
 # show national prefixes
 print(sihsus.prefixos_nacionais())

 # national header (default prefix: CH)
 df = sihsus.ler_nacional(ano=2023, mes=1)
 path = sihsus.baixar_nacional(ano=2023, mes=1)

 # movement communication
 df = sihsus.ler_nacional(ano=2023, mes=1, prefixo="CM")

 # list available
 sihsus.listar_nacional()               # CH (default)
 sihsus.listar_nacional(prefixo="CM")   # CM
 ```

 ### National prefixes

 | Prefix | Example file | Content |
 |--------|---------------|---------|
 | `CH` | `CHBR2301.dbc` | National header — aggregated reference data |
 | `CM` | `CMBR2301.dbc` | Hospital movement communication |

 ---

 ## Main DataFrame variables (Reduced AIH — RD)

 | Variable | Type | Description |
 |----------|------|-------------|
 | `N_AIH` | str | AIH number |
 | `DT_INTER` | str | Admission date (YYYYMMDD) |
 | `DT_SAIDA` | str | Discharge date |
 | `DIAG_PRINC` | str | Primary diagnosis (ICD-10) |
 | `DIAG_SECUN` | str | Secondary diagnosis (ICD-10) |
 | `PROC_REA` | str | Performed procedure |
 | `PROC_SOLIC` | str | Requested procedure |
 | `VAL_TOT` | float | Total AIH value (BRL) |
 | `VAL_UTI` | float | ICU value |
 | `QT_DIARIAS` | str | Number of days |
 | `MORTE` | str | Death indicator (0=no, 1=yes) |
 | `SEXO` | str | Patient sex |
 | `IDADE` | str | Patient age |
 | `MUNIC_RES` | str | IBGE code of residence municipality |
 | `MUNIC_MOV` | str | IBGE code of treatment municipality |
 | `CNES` | str | Establishment CNES code |
 | `GESTAO` | str | Management type (municipal/state) |
 | `COMPLEX` | str | Complexity of care |
 | `INSTRU` | str | Patient education level |
 | `CID_ASSO` | str | Associated ICD |
 | `CID_MORTE` | str | Death cause ICD |
 | `NATUREZA` | str | Legal nature of the establishment |
 | `RUBRICA` | str | Budget rubric |

 > For the full variable dictionary, consult DATASUS official documentation.

 ---

 ## Recommended workflow

 ```
 1. Explore what's available
    sihsus.listar(uf="SP")              ← RD files available for SP
    sihsus.listar_nacional()            ← national CH files

 2. Download the data
    df = sihsus.ler(uf="SP", ano=2023, mes=1)       ← hospitalizations SP Jan/2023
    df = sihsus.ler_nacional(ano=2023, mes=1)        ← national header

 3. Combine months into a time series
    import pandas as pd
    dfs = [sihsus.ler(uf="SP", ano=2023, mes=m) for m in range(1, 13)]
    df_ano = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The year in the filename uses **2 digits** and the month uses **2 digits with leading zero**: `RDSP2301.dbc` = SP, January 2023.
 - `RD` files are the main microdata — each row is a hospitalization (AIH).
 - `SP`, `RJ` and `ER` are complementary to `RD` and share the `N_AIH` field for joins.
 - `CH` and `CM` have national scope (`BR`) and do not exist per state.
 - Large files: `RD` from populous states (SP, RJ, MG) can be tens of MB per month.
 - To map municipalities to names, use `CADMUN.DBF` available in SIM (`sim.baixar_tabelas("CADMUN.DBF")`).
 - To join establishments with registration data, use CNES.
