# SUSFlow

> High-performance Python library to extract, convert, and standardize data from DATASUS — the Brazilian Ministry of Health's public data platform.

**🇧🇷 [Leia em Português](README-ptbr.md)**

---

## Overview

`susflow` automates the entire DATASUS pipeline: discovering files on legacy FTP servers, converting proprietary `.dbc` formats, deduplicating, and delivering clean, analysis-ready data in Parquet format — all with a single function call.

### Why susflow?

| Challenge | susflow Solution |
|-----------|-----------------|
| `.dbc` files don't open on Mac/Linux | Transparent DBC → Parquet conversion via `pyreaddbc` + DuckDB |
| Cryptic column names (`CAUSABAS`, `DTINTERNA`) | Auto-renamed to readable names (`causa_basica_obito`, `data_internacao`) |
| ISO-8859-1 encoding / Mojibake | Corrected to UTF-8 on every read |
| Duplicate rows in legacy files | Removed automatically during conversion |
| Repeated downloads waste time | Hive-partitioned local cache — re-runs are instant |
| Different FTP structures per system | Unified `load()` API across all systems |

---

## Repository Structure

```
.
├── README.md                        # This file (English)
├── README-ptbr.md                   # Portuguese translation
├── CONTRIBUTING.md                  # How to add systems and run tests
├── CONTEXT.md                       # Strategic and philosophical context
├── pyproject.toml                   # Build config and dependencies
├── setup.py                         # Legacy install compatibility
│
├── docs/
│   ├── CHANGELOG_REFACTOR.md        # Refactoring history
│   └── MIGRATION_RATIONALE.md       # Architectural decisions
│
├── susflow/
│   ├── __init__.py
│   ├── config.py                    # The "brain": FTP maps, column mappings, UF lists
│   ├── ftp.py                       # Network layer: resilient FTP downloads with retry/backoff
│   ├── cache.py                     # Local path management for downloaded files
│   ├── reader.py                    # Local file support (.zip, .dbf)
│   │
│   ├── core/
│   │   ├── cleaner.py               # Column renaming, municipality enrichment, CID descriptions, date parsing
│   │   ├── specialties.py           # Clinical domain filters (e.g. Oncology ICD C00–D48)
│   │   ├── synchronization.py       # BacktrackingEngine: finds the most recent consistent FTP month
│   │   └── validator.py             # Validates UF, year range, and granularity against config rules
│   │
│   ├── parsers/
│   │   └── converter.py             # DBC/DBF → Parquet via DuckDB + Polars (dedup + ZSTD)
│   │
│   ├── resources/
│   │   ├── territory.py             # IBGE municipality map (7-digit → 6-digit code, cached)
│   │   └── municipios_br.parquet    # Local geolocation cache
│   │
│   ├── storage/
│   │   └── local_lake.py            # Hive-partitioned path builder for the local data lake
│   │
│   └── systems/                     # User-facing entry points — one file per DATASUS system
│       ├── base.py                  # generic_load() and generic_bulk_load() — the universal engine
│       ├── sim.py                   # SIM: Mortality Information System
│       ├── sinasc.py                # SINASC: Live Births
│       ├── sinan.py                 # SINAN: Notifiable Diseases
│       ├── sih.py                   # SIHSUS: Hospital Information System (AIH)
│       ├── cnes.py                  # CNES: Health Establishment Registry
│       └── sia.py                   # SIASUS: Outpatient Information System
│
└── tests/                           # Unit and integration test suite
```

**Local Data Lake layout** (created automatically on first use):

```
data_lake/
├── SIM/DO/year=2022/uf=PB/data.parquet
├── SIHSUS/RD/year=2023/month=03/uf=SP/data.parquet
├── CNES/ST/year=2024/month=01/uf=RJ/data.parquet
└── _temp/                           # Temporary download workspace (auto-cleaned)
```

---

## Installation

```bash
pip install susflow
```

**Requirements:** Python 3.10+, DuckDB, Polars, pyreaddbc

---

## Get Started

### Mortality data (SIM)

```python
from susflow.systems import sim

# Load deaths for Paraíba in 2022
df = sim.load(uf="PB", year=2022)
print(df.head())
# Columns: causa_basica_obito, data_obito, municipio_residencia, sexo_paciente ...
```

### Hospitalizations (SIHSUS)

```python
from susflow.systems import sih

# Single month
df = sih.load(uf="SP", year=2023, month=3, table="RD")

# Full year in parallel (12 months, up to 5 concurrent downloads)
df_year = sih.load_year(uf="SP", year=2023)
```

### Notifiable diseases (SINAN)

```python
from susflow.systems import sinan

df_dengue = sinan.load(agravo="DENG", uf="CE", year=2023)
df_tb     = sinan.load(agravo="TUBE", uf="AM", year=2022)
```

### Live births (SINASC)

```python
from susflow.systems import sinasc

df = sinasc.load(uf="RJ", year=2021)
```

### CNES — always get the latest available month

```python
from susflow.systems import cnes

# BacktrackingEngine scans the FTP backwards to find the most recent
# month where the requested table is already published
df_estab = cnes.load_latest(table="ST", uf="MG")
```

### Bulk load — multiple states in parallel

```python
from susflow.systems import sim

nordeste = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
df_nordeste = sim.load_bulk(ufs=nordeste, year=2022)
```

### Oncology filter (ICD C00–D48)

```python
from susflow.systems import sim
from susflow.core import specialties

df = sim.load(uf="SP", year=2022)
df_cancer = specialties.filter_oncology(df, cid_column="causa_basica_obito")
```

### Lazy scan of the entire local lake (zero RAM until `.collect()`)

```python
from susflow.systems.base import scan_system
import polars as pl

lazy = scan_system("SIM", "DO")
result = lazy.filter(pl.col("year") == 2022).collect()
```

### Load an entire region

```python
from susflow.systems.base import load_region

df_sul = load_region("SIM", "DO", region_name="SUL", year=2022)
# region_name options: "NORTE", "NORDESTE", "CENTRO-OESTE", "SUDESTE", "SUL"
```

---

## Architecture at a Glance

```
User calls sim.load(uf, year)
        │
        ▼
validator.validate_params()       ← checks UF list, year range, granularity (config.py)
        │
        ▼
local_lake.get_path()             ← builds Hive-partitioned cache path
        │
   ┌────┴────┐
   │ cached? │
   └────┬────┘
    Yes │                    No
        ▼                    ▼
  converter.load_as_df()   ftp.baixar()              ← resilient download with retry/backoff
        │                  converter.to_parquet()    ← DBC → DBF → DuckDB → Polars (dedup + ZSTD)
        │                         │
        └──────────┬───────────────┘
                   ▼
        cleaner.apply_standard_clean()    ← rename + municipalities + CID descriptions + dates
                   │
                   ▼
             pl.DataFrame  ✓
```

---

## Configuration Reference

All system rules live in `config.py`. Key constants:

| Constant | Purpose |
|----------|---------|
| `UFS` | All 27 valid Brazilian state codes |
| `REGIOES` | State groupings by region (Norte, Nordeste, etc.) |
| `UF_PARA_REGIAO` | Reverse lookup: UF → region name |
| `COLUMN_MAPPINGS` | Cryptic DATASUS columns → readable snake_case names |
| `MAX_WORKERS` | Parallel download concurrency (default: 5) |
| `ALL_SYSTEMS` | Registry of all supported DATASUS systems and their FTP rules |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for a step-by-step guide on adding new systems and running the test suite.

---

## License

MIT
