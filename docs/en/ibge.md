# IBGE — Population Estimates

**FTP base:** `/dissemin/publicos/IBGE/POP/`

---

## Available data types

| Type     | Function             | Returns     | Description                                      |
| -------- | -------------------- | ----------- | ------------------------------------------------ |
| national | `read(year, engine=..., parquet=...)` | `DataFrame` (or engine table) | Population estimates for Brazil by year          |
| national | `download(year)`     | `Path`      | Raw `.zip` file containing the estimates         |

---

> **Common parameters for `read()`:**
> - `engine="pandas" | "polars" | "pyarrow"`
> - `parquet=True` — Parquet sidecar cache

## National annual data

**File pattern:** `POPBR{YY}.zip` (2-digit year suffix)

**Coverage:** 1980–2012

**Granularity:** annual / national only (no breakdown by state or municipality)

```python
from susflow.systems import ibge_pop

# Download (if needed) and return a pandas DataFrame (or other engine)
df = ibge_pop.read(2000)

# Download only the raw ZIP file
path = ibge_pop.download(1995)

# List available files
files = ibge_pop.list_files()
```

The ZIP files contain a single `.DBC` (or `.DBF`) with population counts, typically broken down by age groups, sex, and other demographics for the reference year.

For detailed variable descriptions, consult the original IBGE metadata or inspect the columns of the returned DataFrame.

**Note:** This system only provides national-level data. For state or municipal population data, other IBGE sources or DATASUS systems may be used.
