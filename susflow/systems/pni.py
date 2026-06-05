"""
susflow/systems/pni.py
======================
PNI — National Immunization Program.

File pattern: DPNI{UF}{YY}.DBF
Granularity: annual / by state (UF)
Coverage:    1994–2019

Files are located directly in `DADOS/` (no nested folder):
    e.g. /dissemin/publicos/PNI/DADOS/DPNISP02.DBF

Notes:
    - Pure .DBF format (no blast); read with `dbfread` via `reader.py`.
    - Year suffix uses 2 digits (94–19); years 2000–2009 appear as
        00–09, so normalization is done with `(year % 100)`.
    - UF encoded as 2 uppercase letters (e.g. SP, RJ, AM).
    - Coverage ends in 2019; there are no preliminary files.
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import PNI as _CFG
from ..config import UFS
from ..reader import read as _read

_BASE = _CFG["ftp_dir"]
_YEAR_MIN, _YEAR_MAX = _CFG["year_range"]


def _validate(uf: str, year: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (_YEAR_MIN <= year <= _YEAR_MAX):
        raise ValueError(
            f"Year {year} out of range for PNI (available: {_YEAR_MIN}–{_YEAR_MAX})"
        )


def _file_name(uf: str, year: int) -> str:
    return f"DPNI{uf.upper()}{year % 100:02d}.DBF"


def _download_file(name: str, destination: Path | None, force: bool) -> Path:
    path = f"{_BASE}/{name}"
    local = _cache.local_path(path, destination)

    if local.exists() and not force:
        return local

    return _ftp.download(path, local)


def list_files(uf: str | None = None) -> list[str]:
    """List files available on the FTP for PNI.

    Filters by state (UF) if provided.
    """
    files = _ftp.list_files(_BASE)
    if uf:
        filter_ = f"DPNI{uf.upper()}"
        files = [f for f in files if f.upper().startswith(filter_)]
    return files


def download(
    uf: str,
    year: int,
    destination: Path | None = None,
    force: bool = False,
) -> Path:
    """Download `DPNI{UF}{YY}.DBF` to local cache and return the path.

    Parameters
    ----------
    uf          : state code (e.g. 'SP')
    year        : 4-digit year (e.g. 2010)
    destination : destination folder; uses default cache if None
    force       : if True, download even if file exists in cache
    """
    _validate(uf, year)
    return _download_file(_file_name(uf, year), destination, force)


def read(
    uf: str,
    year: int,
    destination: Path | None = None,
    force: bool = False,
    engine: str = "pandas",
    parquet: bool = False,
) -> Any:
    """Download (if needed) and return the data as a DataFrame (or engine table)."""
    return _read(
        download(uf, year, destination=destination, force=force),
        engine=engine,
        parquet=parquet,
        force=force,
    )
