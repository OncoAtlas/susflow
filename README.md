# SUSFlow

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Output: pandas.DataFrame](https://img.shields.io/badge/output-pandas.DataFrame-orange.svg)](#)
[![PyPI](https://img.shields.io/pypi/v/susflow.svg)](https://pypi.org/project/susflow)
![CI Status](https://github.com/SEU_USUARIO/oncology-atlas-sus/actions/workflows/ci.yml/badge.svg)

Modern Python library for downloading, parsing and engineering DATASUS public health datasets. SUSFlow provides:

- resilient FTP access to DATASUS
- a local cache that mirrors the FTP tree
- transparent decompression of proprietary `.dbc` files to tabular data
- helpers to load datasets as pandas DataFrame ready for analysis

This repository focuses on practical reproducibility and safe access to legacy public data systems.

Contents
-
- Documentation for each system: `docs/` (layouts, variable dictionaries, notes)
- Library code: `susflow/`
- Utilities: `tools/` (FTP mapping and inspection)

Quick links
- [CNES](./docs/cnes.md) — health establishments
- [PNI](./docs/pni.md) — immunizations
- [SIM](./docs/sim.md) — mortality
- [SINAN](./docs/sinan.md) — notifiable diseases
- [SINASC](./docs/sinasc.md) — live births

Installation
-
Install in editable mode during development:

```bash
git clone https://github.com/OncoAtlas/susflow.git
cd susflow
python -m venv .venv
. ./.venv/bin/activate
pip install -U pip
pip install -e .
```

Install from PyPI (recommended for most users):

```bash
pip install susflow
```

To install a specific released version:

```bash
pip install susflow==0.1.1
```

Core runtime dependencies are declared in `pyproject.toml`. Typical extras for performance:

- `pyarrow` or `fastparquet` (Parquet cache)
- `pandas` (DataFrame API)

Basic usage
-
Each DATASUS system is available under `susflow.systems`. APIs are lightweight: `listar`, `baixar` and `ler` helpers manage discovery, download and conversion.

Example: SINASC (Live Births)

```python
from susflow.systems import sinasc

# list files for a state
sinasc.listar(uf="SP")

# download and return a pandas.DataFrame
df = sinasc.ler(uf="SP", ano=2020)
```

Example: PNI (Vaccinations)

```python
from susflow.systems import pni
df = pni.ler(uf="RJ", ano=2015)
```

Caching behavior
-
By default downloads are stored under `~/.susflow/cache/` mirroring FTP paths. If a requested file is present locally the library skips the download and reads directly from cache. To force re-download set `forcar=True` on download/reader helpers.

Performance guidance
-
- Downcast numeric types and convert repeated strings to `category` to reduce memory.
- Convert commonly used datasets to Parquet once and reuse local Parquet caches.
- For very large datasets prefer processing in chunks or using DuckDB/Polars to avoid excessive RAM.

Developer tools and linters
-
We recommend the following dev tools for contributors:

```bash
. ./.venv/bin/activate
pip install -U ruff black isort pytest pytest-mock coverage
ruff .
black --check .
isort --check-only .
pytest -q
```

Testing strategy
-
- Unit tests should mock FTP and file IO; see `tests/unit/` for examples.
- Integration tests that access live FTP data should be opt-in and run manually (network-dependent).

Utilities
-
`tools/mapear_ftp.py` helps locate and audit DATASUS FTP directory structures when paths change. It can save structured maps to `tools/mapas/` for offline analysis.

Contributing
-
See `CONTRIBUTING.md` for guidelines: coding style, tests, and PR workflow.

License
-
This project is released under the MIT License — see `LICENSE`.

Contact
-
Open issues and pull requests are welcome. For larger changes please open an issue to discuss scope before implementing.
