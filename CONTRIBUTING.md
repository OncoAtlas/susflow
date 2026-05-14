# Contributing to susflow

Thank you for your interest in contributing! This guide covers the two most common contributions: **adding a new DATASUS system** and **running the test suite**.

---

## Table of Contents

1. [Project Conventions](#project-conventions)
2. [Adding a New System](#adding-a-new-system)
   - [Step 1 — Register the system in `config.py`](#step-1--register-the-system-in-configpy)
   - [Step 2 — Create the system wrapper](#step-2--create-the-system-wrapper)
   - [Step 3 — Add column mappings](#step-3--add-column-mappings)
   - [Step 4 — Validate and test](#step-4--validate-and-test)
3. [Running the Tests](#running-the-tests)
4. [Code Style](#code-style)
5. [Submitting a Pull Request](#submitting-a-pull-request)

---

## Project Conventions

| Convention | Rule |
|-----------|------|
| Language | English for all code, docstrings, and commit messages |
| DataFrames | Polars as primary; Pandas only for compatibility shims |
| Compression | Always ZSTD when writing Parquet |
| Encoding | Always read raw files with `ISO-8859-1`; output is UTF-8 |
| Secrets | Never commit FTP credentials or API keys |
| Column names | `snake_case`, in Portuguese, descriptive (e.g. `causa_basica_obito`) |

---

## Adding a New System

Adding a new DATASUS system (e.g. **SIOPS**, **RNDS**, **GAL**) requires exactly four steps.

### Step 1 — Register the system in `config.py`

Open `susflow/config.py` and add a new dictionary following the established schema. Every key is required unless explicitly marked optional.

```python
# susflow/config.py

MY_SYSTEM = {
    "description": "Human-readable name of the system",   # str
    "ftp_dir":     "/dissemin/publicos/MY_SYSTEM/DADOS",  # FTP base path (no trailing slash)
    "pattern":     "{PREFIX}{UF}{YY}{MM}.dbc",            # filename pattern with placeholders
    "granularity": "month",          # "year" | "month"
    "year_digits": 2,                # 2 (YY) | 4 (YYYY) — must match the FTP filenames
    "format":      "dbc",            # "dbc" | "dbf" | "zip"
    "scope":       "uf",             # "uf" | "national"
    "year_range":  (2010, 2025),     # inclusive (min_year, max_year)

    # Optional — only for systems with named sub-tables (like CNES or SIHSUS)
    "prefixes": {
        "XX": "Descriptive label",
    },
}
```

**Pattern placeholders reference:**

| Placeholder | Expands to | Example |
|-------------|-----------|---------|
| `{UF}` | State code | `PB` |
| `{YY}` | 2-digit year | `23` |
| `{YYYY}` | 4-digit year | `2023` |
| `{MM}` | Zero-padded month | `07` |
| `{PREFIX}` | Sub-table prefix | `RD` |
| `{DISEASE}` | Disease code (SINAN only) | `DENG` |

Then register it in the global index at the bottom of the same file:

```python
ALL_SYSTEMS = {
    # ... existing systems ...
    "MY_SYSTEM": MY_SYSTEM,   # ← add here
}
```

This single addition makes the system visible to `validator.py`, which will automatically enforce its `year_range` and `granularity` rules.

---

### Step 2 — Create the system wrapper

Create `susflow/systems/my_system.py`. Keep it thin — all heavy lifting happens in `base.generic_load()`.

**Minimal wrapper (annual, national scope):**

```python
# susflow/systems/my_system.py
from .base import generic_load

def load(uf: str, year: int, **kwargs):
    """Loads MY_SYSTEM data for a given state and year."""
    return generic_load(
        system="MY_SYSTEM",
        sub_dir="DADOS",          # relative to /dissemin/publicos/MY_SYSTEM/
        table="MY_TABLE",         # filename prefix on the FTP
        uf=uf,
        year=year,
        month=0,                  # 0 = annual
        **kwargs
    )
```

**Monthly wrapper with bulk support:**

```python
# susflow/systems/my_system.py
from .base import generic_load, generic_bulk_load
from typing import List, Optional
from .. import config as _cfg

def load(uf: str, year: int, month: int, table: str = "XX", **kwargs):
    """Loads MY_SYSTEM data for a given state, year, and month."""
    return generic_load(
        system="MY_SYSTEM",
        sub_dir="200801_/Dados",
        table=table,
        uf=uf,
        year=year,
        month=month,
        **kwargs
    )

def load_year(uf: str, year: int, table: str = "XX", **kwargs):
    """Loads all 12 months of a year in parallel."""
    return generic_bulk_load(
        system="MY_SYSTEM",
        sub_dir="200801_/Dados",
        table=table,
        ufs=[uf],
        year=year,
        months=list(range(1, 13)),
        max_workers=_cfg.MAX_WORKERS,
        **kwargs
    )
```

> **Do not** put validation logic, FTP logic, or Polars transformations directly in a system wrapper. That responsibility belongs to `base.py`, `validator.py`, and `cleaner.py` respectively.

---

### Step 3 — Add column mappings

If the new system introduces columns not yet in `COLUMN_MAPPINGS`, add them to `config.py`:

```python
# susflow/config.py — COLUMN_MAPPINGS dict

COLUMN_MAPPINGS = {
    # ... existing mappings ...

    # MY_SYSTEM additions
    "MY_CRYPTIC_COL":  "my_readable_name",
    "ANOTHER_COL":     "another_readable_name",
}
```

`cleaner.apply_standard_clean()` picks these up automatically on the next load — no further changes needed.

If your system has ICD-10 columns (diagnoses), name them so they contain `diagnostico`, `causa_basica`, or `cid` — the cleaner's dynamic detection will enrich them with WHO descriptions automatically.

---

### Step 4 — Validate and test

**Quick smoke test (no real FTP needed):**

```python
# In a Python shell or notebook
from susflow.core import validator

# Should pass without raising
uf, year, month = validator.validate_params("MY_SYSTEM", "PB", 2022, 1)
print(uf, year, month)

# Should raise ValueError (year before range)
validator.validate_params("MY_SYSTEM", "PB", 1800, 1)
```

**Write a unit test in `tests/`:**

```python
# tests/test_my_system.py
import pytest
from susflow.core.validator import validate_params

def test_valid_params():
    uf, year, month = validate_params("MY_SYSTEM", "sp", 2022, 3)
    assert uf == "SP"
    assert year == 2022
    assert month == 3

def test_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        validate_params("MY_SYSTEM", "XX", 2022, 3)

def test_year_too_old():
    with pytest.raises(ValueError, match="2010"):
        validate_params("MY_SYSTEM", "PB", 2005, 1)
```

---

## Running the Tests

### Prerequisites

```bash
pip install susflow[dev]
# or manually:
pip install pytest pytest-cov polars duckdb pyreaddbc
```

### Run the full suite

```bash
pytest tests/ -v
```

### Run with coverage report

```bash
pytest tests/ --cov=susflow --cov-report=term-missing
```

### Run only unit tests (no FTP, fast)

```bash
pytest tests/unit/ -v
```

### Run only integration tests (requires network)

```bash
pytest tests/integration/ -v -m "integration"
```

### Test a specific file

```bash
pytest tests/test_validator.py -v
```

---

### Test Structure Convention

```
tests/
├── unit/
│   ├── test_validator.py       # validate_params() logic
│   ├── test_cleaner.py         # column renaming, date parsing, CID enrichment
│   ├── test_local_lake.py      # Hive path construction
│   └── test_config.py          # ALL_SYSTEMS completeness checks
├── integration/
│   ├── test_sim_load.py        # Real FTP + conversion (marked @pytest.mark.integration)
│   └── test_sih_bulk.py        # Parallel bulk load
└── conftest.py                 # Shared fixtures (mock FTP, sample DataFrames)
```

Use `pytest.mark.integration` on any test that requires network access, so CI can skip them when no FTP is available:

```python
import pytest

@pytest.mark.integration
def test_real_download():
    from susflow.systems import sim
    df = sim.load(uf="PB", year=2010)
    assert df.height > 0
```

---

## Code Style

- Formatter: `black` (line length 100)
- Linter: `ruff`
- Type hints: required on all public functions

```bash
black susflow/ tests/
ruff check susflow/ tests/
```

---

## Submitting a Pull Request

1. Fork the repository and create a branch: `git checkout -b feat/add-my-system`
2. Follow the four steps above for new systems, or write a focused fix for bugs
3. Ensure `pytest tests/unit/` passes with zero failures
4. Run `black` and `ruff` before committing
5. Open a PR with a description that includes:
   - What system/feature/fix is added
   - The FTP path where you verified the files exist
   - Sample output (a `df.head()` screenshot or paste)

Questions? Open an issue — we're happy to help.