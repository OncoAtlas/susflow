"""
susflow/systems/cnes.py
=======================
CNES — National Registry of Health Establishments.

File pattern: {TYPE}/{TYPE}{UF}{YY}{MM}.dbc
Granularity: monthly / by state (UF)
Overall coverage: 2005–2026

Files are located two levels inside `Dados/`:
    e.g. /dissemin/publicos/CNES/200508_/Dados/ST/STSP2501.dbc

Active subtypes:
    ST  — Establishments (main data)               2005–2026
    PF  — Health professionals                      2005–2026
    DC  — Complementary data                        2005–2026
    EQ  — Equipment                                 2005–2026
    SR  — Specialized services                      2005–2026
    LT  — Beds                                      2005–2026
    HB  — Authorizations                             2007–2026
    EF  — Surgical and obstetric centers            2007–2026
    EP  — Health teams                              2007–2026
    RC  — Contract rules                            2007–2026
    IN  — Incentives                                2007–2026
    GM  — Management and targets                    2014–2026

Retired subtypes (still available on FTP):
    EE  — Equipment and production                 2007–2019
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import CNES as _CFG
from ..config import UFS
from ..reader import read as _read

_BASE = _CFG["ftp_base"]
_SUBTYPES = _CFG["subtypes"]  # {type: (description, year_min, year_max)}


def _validate_subtype(type_: str) -> str:
    type_ = type_.upper()
    if type_ not in _SUBTYPES:
        raise ValueError(
            f"Invalid subtype: '{type_}'. Available: {sorted(_SUBTYPES)}"
        )
    return type_


def _validate(type_: str, uf: str, year: int, month: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Use 1–12.")
    _, year_min, year_max = _SUBTYPES[type_]
    if not (year_min <= year <= year_max):
        raise ValueError(
            f"Year {year} out of range for subtype '{type_}' "
            f"(available: {year_min}–{year_max})"
        )


def _ftp_dir(type_: str) -> str:
    return f"{_BASE}/{type_}"


def _file_name(type_: str, uf: str, year: int, month: int) -> str:
    return f"{type_}{uf}{str(year)[-2:]}{month:02d}.dbc"


def _download_file(type_: str, name: str, destination: Path | None, force: bool) -> Path:
    path = f"{_ftp_dir(type_)}/{name}"
    local = _cache.local_path(path, destination)
    if local.exists() and not force:
        return local
    return _ftp.download(path, local)


def subtypes() -> dict[str, str]:
    """Return available subtypes: {type: description}."""
    return {k: v[0] for k, v in _SUBTYPES.items()}


def list_files(uf: str | None = None, type_: str = "ST") -> list[str]:
    """List files available on the FTP for the given subtype.

    Filters by state (UF) if provided. Default subtype: `ST` (Establishments).
    """
    type_ = _validate_subtype(type_)
    files = _ftp.list_files(_ftp_dir(type_))
    if uf:
        filter_ = f"{type_}{uf.upper()}"
        files = [f for f in files if f.upper().startswith(filter_)]
    return files


def download(
    uf: str,
    year: int,
    month: int,
    type_: str = "ST",
    destination: Path | None = None,
    force: bool = False,
) -> Path:
    """Download `{TYPE}{UF}{YY}{MM}.dbc` to local cache.

    Default subtype: `ST` (Establishments).
    """
    type_ = _validate_subtype(type_)
    _validate(type_, uf, year, month)
    return _download_file(type_, _file_name(type_, uf.upper(), year, month), destination, force)


def read(
    uf: str,
    year: int,
    month: int,
    type_: str = "ST",
    destination: Path | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return the data as a DataFrame."""
    return _read(download(uf, year, month, type_=type_, destination=destination, force=force))
