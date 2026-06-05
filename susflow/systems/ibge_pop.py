"""
susflow/systems/ibge_pop.py
===========================
IBGE/POP — Population estimates (IBGE).

File pattern: POPBR{YY}.zip
Granularity: annual / national
Coverage:    1980–2012

Files are located directly in /dissemin/publicos/IBGE/POP/:
    e.g. /dissemin/publicos/IBGE/POP/POPBR95.zip

Notes:
    - National scope only (no UF breakdown).
    - ZIP archive; reader.py extracts and reads the first .dbc or .dbf inside.
    - Year suffix uses 2 digits: 1980 → 80, 2000 → 00, 2012 → 12.
"""

from pathlib import Path
from typing import Any

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import IBGE_POP as _CFG
from ..reader import read as _read

_BASE = _CFG["ftp_dir"]
_YEAR_MIN, _YEAR_MAX = _CFG["year_range"]


def _validate(year: int) -> None:
    if not (_YEAR_MIN <= year <= _YEAR_MAX):
        raise ValueError(
            f"Year {year} out of range for IBGE/POP (available: {_YEAR_MIN}–{_YEAR_MAX})"
        )


def _file_name(year: int) -> str:
    return f"POPBR{year % 100:02d}.zip"


def _download_file(name: str, destination: Path | None, force: bool) -> Path:
    path = f"{_BASE}/{name}"
    local = _cache.local_path(path, destination)
    if local.exists() and not force:
        return local
    return _ftp.download(path, local)


def list_files() -> list[str]:
    """List population estimate files available on the FTP."""
    return _ftp.list_files(_BASE)


def download(year: int, destination: Path | None = None, force: bool = False) -> Path:
    """Download `POPBR{YY}.zip` to local cache and return the path.

    Parameters
    ----------
    year        : year with 4 digits (e.g. 1995)
    destination : destination folder; uses default cache if None
    force       : if True, download even if file exists in cache
    """
    _validate(year)
    return _download_file(_file_name(year), destination, force)


def read(
    year: int, destination: Path | None = None, force: bool = False,
    engine: str = "pandas", parquet: bool = False
) -> Any:
    """Download (if needed) and return the population estimates as a DataFrame (or engine table)."""
    return _read(
        download(year, destination=destination, force=force),
        engine=engine,
        parquet=parquet,
        force=force,
    )
