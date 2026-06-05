 # SIM — Mortality Information System

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | By state | `read(uf, year)` | `DataFrame` | Registered deaths in a state, by year |
 | By state | `download(uf, year)` | `Path` | Raw `.dbc` file for the state |
 | Special | `read_special(type_, year)` | `DataFrame` | National deaths by category (EXT/FET/INF/MAT) |
 | Special | `download_special(type_, year)` | `Path` | Raw `.dbc` file for the category |
 | Documentation | `download_docs(file?)` | `Path / list[Path]` | Layouts, structure and variable dictionary |
 | Support tables | `download_tables(file?)` | `Path / list[Path]` | CID-10, municipalities, occupations, countries, UFs |
 | Tabulated data | `download_tab(file?)` | `Path / list[Path]` | Aggregated deaths by CID-10 (time series) |

 ---

> **Common parameters supported by all `read*()` functions (including special variants):**
> - `engine="pandas" | "polars" | "pyarrow"` (default: `"pandas"`) — return native objects. Requires matching extra.
> - `parquet=True` — enable local Parquet sidecar cache for speed. Requires `susflow[parquet]`/`[pyarrow]`. Use `force=True` to rebuild.

## Data by state — `DORES/`

 **File pattern:** `DO{UF}{YYYY}.dbc`  
 **Coverage:** 1996–2024, all 27 states  
 **Granularity:** annual / by state

 ```python
 from susflow.systems import sim

 df = sim.read(uf="SP", year=2023)
 path = sim.download(uf="RJ", year=2022)
 files = sim.list_files(uf="MG")
 ```

 ### Main DataFrame variables

 | Variable | Type | Description |
 |----------|------|-------------|
 | `DTOBITO` | str | Date of death (DDMMYYYY) |
 | `CAUSABAS` | str | Underlying cause of death (ICD-10) |
 | `SEXO` | str | Sex (1=Male, 2=Female, 9=Ignored) |
 | `IDADE` | str | Encoded age (see dictionary) |
 | `CODMUNRES` | str | IBGE code of municipality of residence |
 | `CODMUNOCI` | str | IBGE code of municipality of occurrence |
 | `ESTCIV` | str | Marital status |
 | `ESC` | str | Education level |
 | `OCUP` | str | Occupation (CBO) |
 | `RACACOR` | str | Race/color |
 | `LOCOCOR` | str | Place of occurrence (hospital, home, etc.) |
 | `ASSISTMED` | str | Medical assistance received |
 | `ATESTANTE` | str | Type of certifier |
 | `CIRCOBITO` | str | Circumstance of death |
 | `ACIDTRAB` | str | Work accident |
 | `FONTE` | str | Information source |
 | `TPMORTEOCO` | str | Type of death |
 | `CAUSABAS_O` | str | Original underlying cause (before correction) |
 | `UFINFORM` | str | Reporting UF |

 > For a complete list of variables and codes, download `Estrutura_do_SIM_2025.pdf` or `Docs_Tabs_CID10.zip`.

 ---

 ## Special data — `DOFET/`

 **File pattern:** `DO{TIPO}{YY}.dbc`  
 **Coverage:** 1996–2024, national scope  
 **Granularity:** annual / national

 | Type | Example file | Content |
 |------|--------------|---------|
 | `EXT` | `DOEXT24.dbc` | Deaths due to external causes (accidents, homicides, suicides) |
 | `FET` | `DOFET24.dbc` | Fetal deaths |
 | `INF` | `DOINF24.dbc` | Infant deaths (0–1 year) |
 | `MAT` | `DOMAT24.dbc` | Maternal deaths |

 ```python
 df = sim.read_special(type_="EXT", year=2023)
 df = sim.read_special(type_="MAT", year=2022)

 path = sim.download_special(type_="INF", year=2024)
 files = sim.list_special(type_="FET")
 ```

 ---

 ## Technical documentation — `DOCS/`

 Files available for download (not read as DataFrame):

 | File | Description | When to use |
 |------|-------------|-------------|
 | `Docs_Tabs_CID10.zip` | Full layouts, tables and variable dictionary | Main reference to understand fields |
 | `Estrutura_do_SIM_2025.pdf` | Current file structure | Bases from 2010 onwards |
 | `Estrutura_SIM_Anterior.pdf` | Previous file structure | **Needed for legacy data (before 2010)** |

 ```python
 # see what's available
 print(sim.list_docs())

 # download a specific document
 path = sim.download_docs("Estrutura_do_SIM_2025.pdf")
 path = sim.download_docs("Estrutura_SIM_Anterior.pdf")  # for older bases

 # download all at once
 paths = sim.download_docs()

 # save to a specific folder
 path = sim.download_docs("Docs_Tabs_CID10.zip", destination="/my/data/sim")
 ```

 ---

 ## Support tables — `TABELAS/`

 Reference tables used to decode DataFrame fields:

 | File | Format | Content |
 |------|--------|---------|
 | `CID10.DBF` | DBF | International Classification of Diseases — ICD-10 (codes and descriptions) |
 | `CIDCAP10.DBF` | DBF | ICD-10 chapters |
 | `CADMUN.DBF` | DBF | Brazilian municipalities registry (IBGE code, name, UF) |
 | `CADMUN.xls` | Excel | Municipality registry (Excel format) |
 | `TABOCUP.DBF` | DBF | Occupations table — CBO |
 | `TABPAIS.DBF` | DBF | Countries table |
 | `TABUF.DBF` | DBF | Federative units table |

 ```python
 # see what's available
 print(sim.list_tables())

 # download a specific table
 path = sim.download_tables("CID10.DBF")
 path = sim.download_tables("CADMUN.DBF")

 # download all at once
 paths = sim.download_tables()
 ```

 ---

 ## Tabulated data — `TAB/`

 Pre-aggregated data, useful for analysis without processing microdata:

 | File | Content |
 |------|---------|
 | `OBITOS_CID10_TAB.zip` | Time series of deaths aggregated by ICD-10 |

 ```python
 print(sim.list_tab())

 path = sim.download_tab("OBITOS_CID10_TAB.zip")
 paths = sim.download_tab()  # download all
 ```

 ---

 ## Recommended workflow

 ```
 1. Explore what's available
    sim.list_files(uf="SP")
    sim.list_special()

 2. Download the data
    df = sim.read(uf="SP", year=2023)                    ← microdata by state
    df = sim.read_special(type_="MAT", year=2022)        ← national special data

 3. Download reference tables to decode fields
    sim.download_tables("CID10.DBF")
    sim.download_tables("CADMUN.DBF")

 4. Inspect field structure (if needed)
    sim.download_docs("Estrutura_do_SIM_2025.pdf")
    sim.download_docs("Estrutura_SIM_Anterior.pdf")      ← for years prior to 2010
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The `IDADE` field uses DATASUS encoding: the first digit indicates the unit (1=hours, 2=days, 3=months, 4=years) and the next two digits the value.
 - Municipalities are identified by the 6-digit IBGE code (`CODMUNRES`, `CODMUNOCI`). Use `CADMUN.DBF` to join with names.
 - Causes of death follow ICD-10. Use `CID10.DBF` to obtain code descriptions.
 - For pre-2010 bases, field structure may differ — consult `Estrutura_SIM_Anterior.pdf`.
 ```
