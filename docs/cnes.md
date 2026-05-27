 # CNES — National Register of Health Establishments

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | By state | `ler(uf, ano, mes)` | `DataFrame` | Registration data for a subtype and state |
 | By state | `baixar(uf, ano, mes)` | `Path` | Raw `.dbc` file |

 ---

 ## Available subtypes

 **File pattern:** `{TYPE}/{TYPE}{UF}{YY}{MM}.dbc`  
 **Granularity:** monthly / by state  

 > Files are stored inside a subdirectory named after the subtype:  
 > e.g. `ST/STSP2501.dbc` → establishments in SP, January 2025.

 ```python
 from susflow.systems import cnes

 # show all available subtypes
 print(cnes.subtipos())

 # Establishments — default subtype
 df = cnes.ler(uf="SP", ano=2025, mes=1)
 df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="ST")

 # other subtypes
 df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="PF")   # professionals
 df = cnes.ler(uf="RJ", ano=2024, mes=6, tipo="LT")   # beds
 df = cnes.ler(uf="MG", ano=2023, mes=3, tipo="EQ")   # equipment

 # download only
 path = cnes.baixar(uf="SP", ano=2025, mes=1)
 path = cnes.baixar(uf="SP", ano=2025, mes=1, tipo="PF")

 # list available files
 cnes.listar()                       # all ST files
 cnes.listar(uf="SP")                # ST files for SP
 cnes.listar(uf="SP", tipo="PF")     # professionals for SP
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
    print(cnes.subtipos())              ← all subtypes and descriptions
    cnes.listar(uf="SP")                ← ST files available for SP
    cnes.listar(uf="SP", tipo="PF")     ← professionals for SP

 2. Download data
    df = cnes.ler(uf="SP", ano=2025, mes=1)              ← establishments
    df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="PF")   ← professionals
    df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="LT")   ← beds

 3. Combine months into a time series
    import pandas as pd
    dfs = [cnes.ler(uf="SP", ano=2024, mes=m) for m in range(1, 13)]
    df_ano = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The year uses **2 digits** and the month **2 digits with leading zero**: `STSP2501.dbc` = SP, January 2025.
 - Files are stored in a subdirectory with the same name as the subtype — this is handled automatically by the library.
 - Each subtype has its own temporal coverage. Attempting to download `EE` for 2022 will raise an error with the correct coverage (2007–2019).
 - `ST` and `PF` are the most used subtypes: `ST` for analyses of establishment distribution, `PF` for workforce analyses.
 - The `CNES` field is the key to join all subtypes — use it to enrich `ST` with `LT`, `EQ`, `PF`, etc.
 - To map municipality codes to names, use `CADMUN.DBF` available in SIM (`sim.baixar_tabelas("CADMUN.DBF")`).
