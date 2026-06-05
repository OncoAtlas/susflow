# SUSFlow

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Output: pandas.DataFrame](https://img.shields.io/badge/output-pandas.DataFrame-orange.svg)](#)
[![PyPI](https://img.shields.io/pypi/v/susflow.svg)](https://pypi.org/project/susflow)

Modern Python library for downloading, parsing and engineering DATASUS public health datasets. SUSFlow provides:

- resilient FTP access to DATASUS
- a local cache that mirrors the FTP tree
- transparent decompression of proprietary `.dbc` files to tabular data
- helpers to load datasets as pandas DataFrame ready for analysis

This repository focuses on practical reproducibility and safe access to legacy public data systems.

Portuguese (Brazil) documentation and module index: [Português do Brasil](./docs/pt-br/README.md)

## Contents

- Module documentation in `docs/en/` (layouts, variable dictionaries, notes)
- Library code: `susflow/`
- Utilities: `tools/` (FTP mapping and inspection)

Quick links

- [CNES](./docs/en/cnes.md) — health establishments
- [PNI](./docs/en/pni.md) — immunizations
- [SIM](./docs/en/sim.md) — mortality
- [SINAN](./docs/en/sinan.md) — notifiable diseases
- [SINASC](./docs/en/sinasc.md) — live births
- [SIASUS](./docs/en/siasus.md) — ambulatory information system (SUS)
- [SIHSUS](./docs/en/sihsus.md) — hospital information system (SUS)
- IBGE — population estimates (see `susflow.systems.ibge_pop`)
- [FTP file patterns summary](./docs/en/summary.md)

## Installation

Install in editable mode during development (includes dev/lint/test tools via the `dev` extra):

```bash
git clone https://github.com/OncoAtlas/susflow.git
cd susflow
python -m venv .venv
. ./.venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

Install from PyPI (recommended for most users):

```bash
pip install susflow
```

To install a specific released version:

```bash
pip install susflow==0.1.1
```

Core runtime dependencies are declared in `pyproject.toml`. Optional extras:

- `susflow[dev]` — development tools (ruff, black, isort, pytest, coverage, etc.)
- `susflow[polars]` — Polars output support via `engine="polars"`
- `susflow[pyarrow]` — PyArrow output + Parquet sidecar cache support
- `susflow[parquet]` — Parquet sidecar cache (pyarrow)
- `susflow[polars,pyarrow]` — for full `engine=` and cache flexibility

## Basic usage

Each DATASUS system is available under `susflow.systems` (including the newer `ibge_pop`). APIs are lightweight: `list_files`, `download` and `read` helpers manage discovery, download and conversion.

The `read()` functions now support additional options:
- `engine="pandas" | "polars" | "pyarrow"` — return native objects instead of pandas DataFrame.
- `parquet=True` — enable local `.parquet` sidecar cache for faster repeated reads.

Example: SINASC (Live Births)

```python
from susflow.systems import sinasc

# list files for a state
sinasc.list_files(uf="SP")

# download and return a pandas.DataFrame
df = sinasc.read(uf="SP", year=2020)
```

Example: PNI (Vaccinations)

```python
from susflow.systems import pni
df = pni.read(uf="RJ", year=2015)
```

Example: Using new `engine` and `parquet` options + batch downloads

```python
from susflow import download_batch
from susflow.systems import sinasc

# Read with Polars (requires susflow[polars])
df = sinasc.read(uf="SP", year=2020, engine="polars")

# Enable Parquet sidecar cache (requires susflow[pyarrow] or [parquet])
df = sinasc.read(uf="SP", year=2020, parquet=True)

# Concurrent downloads
paths = download_batch([
    ("sinasc", {"uf": "SP", "year": 2020}),
    ("sinasc", {"uf": "RJ", "year": 2021}),
])
```

## Command-line interface

SUSFlow also provides a `susflow` CLI (installed via the package or `pip install susflow`):

```bash
susflow --help
susflow sinasc list --uf SP
susflow cnes download SP 2023 --type ST
```

The CLI supports `list` and `download` for the main systems. For full control (including `engine=` and `parquet` cache), use the Python API.

New in recent releases: `ibge_pop` module for population estimates.

## Caching behavior

By default downloads are stored under `~/.susflow/cache/` mirroring FTP paths. If a requested file is present locally the library skips the download and reads directly from cache. To force re-download set `force=True` on download/reader helpers.

## Performance guidance

- Downcast numeric types and convert repeated strings to `category` to reduce memory.
- Convert commonly used datasets to Parquet once and reuse local Parquet caches.
- For very large datasets prefer processing in chunks or using DuckDB/Polars to avoid excessive RAM.

## Developer tools and linters

After `pip install -e ".[dev]"` (see Installation above), the tools are available. Run the checks locally:

```bash
. ./.venv/bin/activate
ruff check .
black --check .
isort --check-only .
pytest -q
```

## Testing strategy

- Unit tests should mock FTP and file IO; see `tests/unit/` for examples.
- Integration tests that access live FTP data should be opt-in and run manually (network-dependent).

## Utilities

`tools/mapear_ftp.py` helps locate and audit DATASUS FTP directory structures when paths change. It can save structured maps to `tools/mapas/` for offline analysis.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines: coding style, tests, and PR workflow.
See [docs/en/coverage.md](./docs/en/coverage.md) for coverage instructions.

## License

This project is released under the MIT License — see `LICENSE`.

## Contact

Open issues and pull requests are welcome. For larger changes please open an issue to discuss scope before implementing.
