"""
susflow/systems/siasus.py
=========================
SIASUS — Outpatient Information System (SUS).

File pattern: {PREFIX}{UF}{YY}{MM}.dbc
Granularity: monthly / by state (UF)
Overall coverage: 2008–2026

Active prefixes:
    PA   — Outpatient production (BPA)              2008–2026
    BI   — Individualized BPA                       2008–2026
    AD   — APAC various reports                     2008–2026
    AM   — APAC medications                         2008–2026
    AMP  — APAC standardized medications            2020–2026
    AQ   — APAC chemotherapy                        2008–2026
    AR   — APAC radiotherapy                        2008–2026
    ACF  — APAC creation of arteriovenous fistula   2014–2026
    ATD  — APAC dialysis treatment                  2014–2026
    PS   — RAAS Psychosocial                        2013–2026
    AB   — APAC Post-bariatric surgery (new)        2025–2026

Retired prefixes (still available on FTP):
    ABO  — APAC Post-bariatric surgery (legacy)    2015–2018
    AN   — APAC nephrology (replaced by ATD)       2008–2014
    SAD  — RAAS Home Care                           2013–2015
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SIASUS as _CFG
from ..config import UFS
from ..reader import read as _read

_DIR = _CFG["ftp_dir"]
_PREFIXES = _CFG["prefixes"]  # {prefix: (description, year_min, year_max)}
_YEAR_MIN, _YEAR_MAX = _CFG["year_range"]


def _validate_prefix(prefix: str) -> str:
    prefix = prefix.upper()
    if prefix not in _PREFIXES:
        raise ValueError(f"Invalid prefix: '{prefix}'. Available: {sorted(_PREFIXES)}")
    return prefix


def _validate(prefix: str, uf: str, year: int, month: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Use 1–12.")
    _, year_min, year_max = _PREFIXES[prefix]

    if not (year_min <= year <= year_max):
        raise ValueError(
            f"Year {year} out of range for prefix '{prefix}' "
            f"(available: {year_min}–{year_max})"
        )


def _file_name(prefix: str, uf: str, year: int, month: int) -> str:
    return f"{prefix}{uf}{str(year)[-2:]}{month:02d}.dbc"


def _download_file(name: str, destination: Path | None, force: bool) -> Path:
    path = f"{_DIR}/{name}"
    local = _cache.local_path(path, destination)

    if local.exists() and not force:
        return local

    return _ftp.download(path, local)


def prefixes() -> dict[str, str]:
    """Return available prefixes: {prefix: description}."""
    return {k: v[0] for k, v in _PREFIXES.items()}


def list_files(uf: str | None = None, prefix: str = "PA") -> list[str]:
    """List files available on the FTP.

    Filters by prefix (default: `PA`) and optionally by state (UF).
    """
    prefix = _validate_prefix(prefix)
    files = _ftp.list_files(_DIR)
    files = [f for f in files if f.upper().startswith(prefix)]

    if uf:
        filter_ = f"{prefix}{uf.upper()}"
        files = [f for f in files if f.upper().startswith(filter_)]
    return files


def download(
    uf: str,
    year: int,
    month: int,
    prefix: str = "PA",
    destination: Path | None = None,
    force: bool = False,
) -> Path:
    """Download `{PREFIX}{UF}{YY}{MM}.dbc` to local cache.

    Default prefix: `PA` (Outpatient production).
    """
    prefix = _validate_prefix(prefix)
    _validate(prefix, uf, year, month)
    return _download_file(
        _file_name(prefix, uf.upper(), year, month), destination, force
    )


def read(
    uf: str,
    year: int,
    month: int,
    prefix: str = "PA",
    destination: Path | None = None,
    force: bool = False,
    parquet: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return the data as a DataFrame."""
    return _read(
        download(uf, year, month, prefix=prefix, destination=destination, force=force),
        parquet=parquet,
        force=force,
    )
