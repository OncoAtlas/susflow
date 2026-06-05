# SINASC — Live Births Information System

FTP base: `ftp.datasus.gov.br/dissemin/publicos/SINASC/NOV/`

---

## Available data types

| Type          | Function                   | Returns             | Description                                       |
| ------------- | -------------------------- | ------------------- | ------------------------------------------------- |
| By state (UF) | `read(uf, year, engine=..., parquet=...)` | `DataFrame` (or engine table) | Live births recorded in a state, by year          |
| By state (UF) | `download(uf, year)`       | `Path`              | Raw `.dbc` file for the state                     |
| National      | `read_national(year)`      | `DataFrame`         | National aggregate (incomplete series: 2014–2017) |
| National      | `download_national(year)`  | `Path`              | `.dbc` file of the national aggregate             |
| Exceptions    | `read_exception(year)`     | `DataFrame`         | Supplementary, one-off records                    |
| Exceptions    | `download_exception(year)` | `Path`              | `.dbc` exception file                             |
| Documentation | `download_docs(file?)`     | `Path / list[Path]` | Layouts, structure and legislation                |

---

> **Common parameters supported by all `read*()` functions (including national/exception variants):**
> - `engine="pandas" | "polars" | "pyarrow"` (default: `"pandas"`) — return native objects instead of pandas DataFrame. Requires the matching extra (`susflow[polars]` or `susflow[pyarrow]`).
> - `parquet=True` — enable fast local `.parquet` sidecar cache next to the source file (subsequent calls skip the slow DBC→DBF conversion). Requires `susflow[parquet]` or `susflow[pyarrow]`. Pass `force=True` to force rebuild.

## Data by state — `DNRES/`

**File pattern:** `DN{UF}{YYYY}.dbc`  
 **Coverage:** 1996–2022, all 27 states  
 **Granularity:** annual / by state

```python
from susflow.systems import sinasc

df = sinasc.read(uf="SP", year=2022)
path = sinasc.download(uf="RJ", year=2021)
files = sinasc.list_files(uf="MG")
```

### Main DataFrame variables

| Variable     | Type | Description                                     |
| ------------ | ---- | ----------------------------------------------- |
| `DTNASC`     | str  | Birth date (DDMMYYYY)                           |
| `SEXO`       | str  | Sex (1=Male, 2=Female, 0=Ignored)               |
| `PESO`       | str  | Birth weight (grams)                            |
| `GESTACAO`   | str  | Gestational age (coded)                         |
| `GRAVIDEZ`   | str  | Pregnancy type (1=Single, 2=Twins, 3=Triplets+) |
| `PARTO`      | str  | Delivery type (1=Vaginal, 2=Cesarean)           |
| `CONSULTAS`  | str  | Number of prenatal visits                       |
| `APGAR1`     | str  | Apgar score at 1 minute                         |
| `APGAR5`     | str  | Apgar score at 5 minutes                        |
| `RACACOR`    | str  | Newborn race/color                              |
| `IDADEMAE`   | str  | Mother's age                                    |
| `ESTCIVMAE`  | str  | Mother's marital status                         |
| `ESCMAE`     | str  | Mother's education                              |
| `CODMUNRES`  | str  | IBGE code of mother's residence municipality    |
| `CODMUNNASC` | str  | IBGE code of birth municipality                 |
| `CODESTAB`   | str  | Health establishment code                       |
| `LOCNASC`    | str  | Place of birth (hospital, home, etc.)           |
| `IDANOMAL`   | str  | Identified congenital anomaly                   |
| `KOTELCHUCK` | str  | Kotelchuck index (prenatal adequacy)            |

> For the full list of variables and codes, download the technical documentation with `sinasc.download_docs()`.

---

## National aggregate — `DNBR`

**File pattern:** `DNBR{YYYY}.dbc`  
 **Coverage:** 2014–2017 (incomplete series — only these years were confirmed on the FTP)  
 **Granularity:** annual / national

```python
df = sinasc.read_national(year=2015)
path = sinasc.download_national(year=2016)
files = sinasc.list_national()
```

> For national analyses outside this range, aggregate state data manually.

---

## Exception files — `DNEX`

**File pattern:** `DNEX{YYYY}.dbc`  
 **Nature:** one-off files with supplementary records — not a regular series  
 **Confirmed on FTP:** `DNEX2021.dbc` (only file identified)

```python
df = sinasc.read_exception(year=2021)
path = sinasc.download_exception(year=2021)
files = sinasc.list_exceptions()
```

---

## Technical documentation — `DOCS/`

> **Note:** the FTP path for this directory has not been fully confirmed by direct mapping. If download fails, run `python tools/mapear_ftp.py --alvo /dissemin/publicos/SINASC/NOV` to locate the correct directory.

| File                           | Description                           | When to use                    |
| ------------------------------ | ------------------------------------- | ------------------------------ |
| `Estrutura_SINASC_para_CD.pdf` | File structure (legacy CD-ROM format) | Old datasets distributed on CD |
| `Legislacao_PDF.pdf`           | Legislation related to SINASC         | Normative reference            |
| `NASC98.HLP`                   | Legacy help file (1998)               | For datasets from 1996–1998    |
| `Portaria.pdf`                 | Regulatory ordinance                  | Normative reference            |

```python
# see what's available
print(sinasc.list_docs())

# download a specific document
path = sinasc.download_docs("Estrutura_SINASC_para_CD.pdf")
path = sinasc.download_docs("NASC98.HLP")  # for 1996–1998 datasets

# download all at once
paths = sinasc.download_docs()

# save to a specific folder
path = sinasc.download_docs("Legislacao_PDF.pdf", destination="/my/data/sinasc")
```

---

## Recommended workflow

```
1. Explore what's available
   sinasc.list_files(uf="SP")
   sinasc.list_national()
   sinasc.list_exceptions()

2. Download data
   df = sinasc.read(uf="SP", year=2022)          ← microdata by state
   df = sinasc.read_national(year=2015)           ← national aggregate
   df = sinasc.read_exception(year=2021)          ← supplementary records

3. Download references to understand the fields
   sinasc.download_docs("Estrutura_SINASC_para_CD.pdf")
   sinasc.download_docs("NASC98.HLP")             ← for datasets from 1996–1998
```

---

## Notes

- `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
- The `GESTACAO` field uses a custom coding: 1=<22 weeks, 2=22–27, 3=28–31, 4=32–36, 5=37–41, 6=42+, 9=ignored.
- The `PESO` field is in grams. Values like `9999` indicate ignored/missing.
- Municipalities are identified by the 6-digit IBGE code. Use `CADMUN.DBF` from SIM to join to names.
