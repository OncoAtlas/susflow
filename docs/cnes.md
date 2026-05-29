 # CNES — National Register of Health Establishments

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | By state | `read(uf, year, month)` | `DataFrame` | Registration data for a subtype and state |
 | By state | `download(uf, year, month)` | `Path` | Raw `.dbc` file |

 ---

 ## Available subtypes

 **File pattern:** `{TYPE}/{TYPE}{UF}{YY}{MM}.dbc`  
 **Granularity:** monthly / by state  

 > Files are stored inside a subdirectory named after the subtype:  
 > e.g. `ST/STSP2501.dbc` → establishments in SP, January 2025.

 ```python
 from susflow.systems import cnes

 # show all available subtypes
 print(cnes.subtypes())

 # Establishments — default subtype
 df = cnes.read(uf="SP", year=2025, month=1)
 df = cnes.read(uf="SP", year=2025, month=1, type_="ST")

 # other subtypes
 df = cnes.read(uf="SP", year=2025, month=1, type_="PF")   # professionals
 df = cnes.read(uf="RJ", year=2024, month=6, type_="LT")   # beds
 df = cnes.read(uf="MG", year=2023, month=3, type_="EQ")   # equipment

 # download only
 path = cnes.download(uf="SP", year=2025, month=1)
 path = cnes.download(uf="SP", year=2025, month=1, type_="PF")

 # list available files
 cnes.list_files()                          # all ST files
 cnes.list_files(uf="SP")                   # ST files for SP
 cnes.list_files(uf="SP", type_="PF")       # professionals for SP
 ```

 ### Active subtypes

 | Type | Example file | Content | Coverage |
 |------|---------------|---------|----------|
 | `ST` | `STSP2501.dbc` | **Establishments** — identification, location, type | 2005–2026 |
 | `PF` | `PFSP2501.dbc` | **Health professionals** — employment links and CBO | 2005–2026 |
 | `DC` | `DCSP2501.dbc` | Additional establishment data | 2005–2026 |
 | `EQ` | `EQSP2501.dbc` | Available equipment | 2005–2026 |
 | `SR` | `SRSP2501.dbc` | Specialized services offered | 2005–2026 |
 | `LT` | `LTSP0510.dbc` | Beds (SUS and non-SUS) | 2005–2026 |
 | `HB` | `HBSP0703.dbc` | Authorizations and certifications | 2007–2026 |
 | `EF` | `EFSP0703.dbc` | Surgical and obstetric centers | 2007–2026 |
 | `EP` | `EPSP0704.dbc` | Health teams (eSF, eAP, etc.) | 2007–2026 |
 | `RC` | `RCSP0703.dbc` | Contractual rules | 2007–2026 |
 | `IN` | `INSP0711.dbc` | Financial incentives | 2007–2026 |
 | `GM` | `GMSP1407.dbc` | Management and goals | 2014–2026 |

 ### Retired subtypes (still available on the FTP)

 | Type | Example file | Content | Coverage | Note |
 |------|--------------|---------|----------|------|
 | `EE` | `EESP0703.dbc` | Equipment and production | 2007–2019 | Retired in Dec/2019 |

 ---

 ## Main variables by subtype

 ### ST — Establishments

 | Variable | Type | Description |
 |----------|------|-------------|
 | `CNES` | str | CNES code (unique identifier) |
 | `CODUFMUN` | str | IBGE municipality code |
 | `REGSAUDE` | str | Health region |
 | `MICR_REG` | str | Health microregion |
 | `DISTRSAN` | str | Sanitary district |
 | `DISTRADM` | str | Administrative district |
 | `TPGESTAO` | str | Management type (M=municipal, E=state, D=both) |
 | `PF_PJ` | str | Individual or legal entity |
 | `CPF_CNPJ` | str | CPF or CNPJ |
 | `NIV_DEP` | str | Dependency level |
 | `CNPJ_MAN` | str | Maintainer's CNPJ |
 | `ESFERA_A` | str | Administrative sphere |
 | `ATIVIDAD` | str | Teaching/research activity |
 | `RETENCAO` | str | Retention type |
 | `NATUREZA` | str | Legal nature |
 | `CLIENTEL` | str | Served clientele |
 | `TP_UNID` | str | Unit type |
 | `TURNO_AT` | str | Service shift |
 | `NIV_HIER` | str | Hierarchy level |
 | `TERCEIRO` | str | Outsourcing indicator |
 | `COMPETEN` | str | Competence (YYYYMM) |

 ### PF — Professionals

 | Variable | Type | Description |
 |----------|------|-------------|
 | `CNES` | str | Establishment CNES code |
 | `CBO` | str | Occupation CBO code |
 | `NOMEPROF` | str | Professional's name |
 | `CNS_PROF` | str | Professional's CNS |
 | `CONSELHO` | str | Professional council |
 | `REGISTRO` | str | Council registration number |
 | `VINCULAC` | str | Employment link type |
 | `SUBVINCUL` | str | Employment subtype |
 | `TP_SUS` | str | Provides services to SUS |
 | `COMPETEN` | str | Competence (YYYYMM) |

 ### LT — Beds

 | Variable | Type | Description |
 |----------|------|-------------|
 | `CNES` | str | Establishment CNES code |
 | `TP_LEITO` | str | Bed type |
 | `CODLEITO` | str | Bed code |
 | `QT_EXIST` | str | Existing quantity |
 | `QT_CONTR` | str | Contracted quantity (SUS) |
 | `QT_SUS` | str | SUS quantity |
 | `COMPETEN` | str | Competence (YYYYMM) |

 ---

 ## Recommended workflow

 ```
 1. Explore available data
    print(cnes.subtypes())                 ← all subtypes and descriptions
    cnes.list_files(uf="SP")               ← ST files available for SP
    cnes.list_files(uf="SP", type_="PF")   ← professionals for SP

 2. Download data
    df = cnes.read(uf="SP", year=2025, month=1)               ← establishments
    df = cnes.read(uf="SP", year=2025, month=1, type_="PF")   ← professionals
    df = cnes.read(uf="SP", year=2025, month=1, type_="LT")   ← beds

 3. Combine months into a time series
    import pandas as pd
    dfs = [cnes.read(uf="SP", year=2024, month=m) for m in range(1, 13)]
    df_year = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The year uses **2 digits** and the month **2 digits with leading zero**: `STSP2501.dbc` = SP, January 2025.
 - Files are stored in a subdirectory with the same name as the subtype — this is handled automatically by the library.
 - Each subtype has its own temporal coverage. Attempting to download `EE` for 2022 will raise an error with the correct coverage (2007–2019).
 - `ST` and `PF` are the most used subtypes: `ST` for analyses of establishment distribution, `PF` for workforce analyses.
 - The `CNES` field is the key to join all subtypes — use it to enrich `ST` with `LT`, `EQ`, `PF`, etc.
 - To map municipality codes to names, use `CADMUN.DBF` available in SIM (`sim.download_tables("CADMUN.DBF")`).