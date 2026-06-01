"""
susflow/systems/sihsus.py
=========================
SIHSUS — SUS Hospital Admissions Information System.

Files by state (prefix + state code):

    RD{UF}{YY}{MM}.dbc  — Reduced AIH (admissions — main data)
    SP{UF}{YY}{MM}.dbc  — Professional services
    RJ{UF}{YY}{MM}.dbc  — Rejected AIH
    ER{UF}{YY}{MM}.dbc  — AIH with error

National files (prefix + fixed BR):

    CHBR{YY}{MM}.dbc   — National header (aggregated data)
    CMBR{YY}{MM}.dbc   — Movement communication

Granularity: monthly / year with 2 digits
Coverage:    2008–2026
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SIHSUS as _CFG
from ..config import UFS
from ..reader import read as _read

_DIR = _CFG["ftp_dir"]
_PREFIXES = set(_CFG["prefixes"].keys())  # RD, SP, RJ, ER
_NATIONAL_PREFIXES = set(_CFG["national_prefixes"].keys())  # CH, CM
_YEAR_MIN, _YEAR_MAX = _CFG["year_range"]


def _validate_uf(uf: str, year: int, month: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    _validate_period(year, month)


def _validate_period(year: int, month: int) -> None:
    if not (_YEAR_MIN <= year <= _YEAR_MAX):
        raise ValueError(
            f"Year out of range: {year} (available: {_YEAR_MIN}–{_YEAR_MAX})"
        )
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Use 1–12.")


def _validate_prefix(prefix: str, national: bool = False) -> str:
    prefix = prefix.upper()
    pool = _NATIONAL_PREFIXES if national else _PREFIXES
    if prefix not in pool:
        raise ValueError(f"Invalid prefix: '{prefix}'. Available: {sorted(pool)}")
    return prefix


def _file_name(prefix: str, uf_or_br: str, year: int, month: int) -> str:
    return f"{prefix}{uf_or_br}{str(year)[-2:]}{month:02d}.dbc"


def _download_file(name: str, destination: Path | None, force: bool) -> Path:
    path = f"{_DIR}/{name}"
    local = _cache.local_path(path, destination)
    if local.exists() and not force:
        return local
    return _ftp.download(path, local)


# ---------------------------------------------------------------------------
# By state (UF)
# ---------------------------------------------------------------------------


def prefixes() -> dict[str, str]:
    """Return available prefixes for data by state (UF): {prefix: description}."""
    return dict(_CFG["prefixes"])


def list_files(uf: str | None = None, prefix: str = "RD") -> list[str]:
    """List files available on the FTP.

    Filters by prefix (default: `RD`) and optionally by state (UF).
    """
    prefix = prefix.upper()
    files = _ftp.list_files(_DIR)
    files = [
        f
        for f in files
        if f.upper().startswith(prefix) and not f.upper().startswith(f"{prefix}BR")
    ]
    if uf:
        filter_ = f"{prefix}{uf.upper()}"
        files = [f for f in files if f.upper().startswith(filter_)]
    return files


def download(
    uf: str,
    year: int,
    month: int,
    prefix: str = "RD",
    destination: Path | None = None,
    force: bool = False,
) -> Path:
    """Download `{PREFIX}{UF}{YY}{MM}.dbc` to local cache.

    Default prefix: `RD` (Reduced AIH — admissions).
    """
    prefix = _validate_prefix(prefix)
    _validate_uf(uf, year, month)
    return _download_file(
        _file_name(prefix, uf.upper(), year, month), destination, force
    )


def read(
    uf: str,
    year: int,
    month: int,
    prefix: str = "RD",
    destination: Path | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return data by state (UF) as a DataFrame."""
    return _read(
        download(uf, year, month, prefix=prefix, destination=destination, force=force)
    )


# ---------------------------------------------------------------------------
# National (CH and CM — use fixed BR)
# ---------------------------------------------------------------------------


def national_prefixes() -> dict[str, str]:
    """Return available national prefixes: {prefix: description}."""
    return dict(_CFG["national_prefixes"])


def list_national(prefix: str = "CH") -> list[str]:
    """List national files available on the FTP.

    Default prefix: `CH` (national header).
    """
    prefix = prefix.upper()
    files = _ftp.list_files(_DIR)
    return [f for f in files if f.upper().startswith(f"{prefix}BR")]


def download_national(
    year: int,
    month: int,
    prefix: str = "CH",
    destination: Path | None = None,
    force: bool = False,
) -> Path:
    """Download `{PREFIX}BR{YY}{MM}.dbc` (national scope) to local cache."""
    prefix = _validate_prefix(prefix, national=True)
    _validate_period(year, month)
    return _download_file(_file_name(prefix, "BR", year, month), destination, force)


def read_national(
    year: int,
    month: int,
    prefix: str = "CH",
    destination: Path | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return national data as a DataFrame."""
    return _read(
        download_national(
            year, month, prefix=prefix, destination=destination, force=force
        )
    )
