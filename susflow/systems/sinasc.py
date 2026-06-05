"""
susflow/systems/sinasc.py
=========================
SINASC — Live Births Information System.

Data subtypes:

    uf         → DN{UF}{YYYY}.dbc  in NOV/DNRES/   e.g. DNSP2022.dbc
                         by state, annual, 1996–2022

    national   → DNBR{YYYY}.dbc   in NOV/DNRES/   e.g. DNBR2015.dbc
                         national aggregate, incomplete series (2014–2017 confirmed)

    exceptions → DNEX{YYYY}.dbc   in NOV/DNRES/   e.g. DNEX2021.dbc
                         one-off files with supplementary records

Auxiliary files (download only, not read as DataFrame):

    docs       → system technical documentation (FTP path to confirm)
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SINASC as _CFG
from ..config import UFS
from ..reader import read as _read

_CFG_UF = _CFG["uf"]
_CFG_NATIONAL = _CFG["national"]
_CFG_EXCEPTIONS = _CFG["exceptions"]
_CFG_DOCS = _CFG["docs"]

_YEAR_MIN_UF, _YEAR_MAX_UF = _CFG_UF["year_range"]
_YEAR_MIN_NATIONAL, _YEAR_MAX_NATIONAL = _CFG_NATIONAL["year_range"]


def _validate_uf(uf: str, year: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (_YEAR_MIN_UF <= year <= _YEAR_MAX_UF):
        raise ValueError(
            f"Year out of range: {year} (available: {_YEAR_MIN_UF}–{_YEAR_MAX_UF})"
        )


def _validate_national(year: int) -> None:
    if not (_YEAR_MIN_NATIONAL <= year <= _YEAR_MAX_NATIONAL):
        raise ValueError(
            f"Year out of range for the national aggregate: {year} "
            f"(confirmed: {_YEAR_MIN_NATIONAL}–{_YEAR_MAX_NATIONAL})"
        )


def _download_file(
    ftp_dir: str, name: str, destination: Path | None, force: bool
) -> Path:
    path = f"{ftp_dir}/{name}"
    local = _cache.local_path(path, destination)
    if local.exists() and not force:
        return local
    return _ftp.download(path, local)


# ---------------------------------------------------------------------------
# By state (UF)
# ---------------------------------------------------------------------------


def list_files(uf: str | None = None) -> list[str]:
    """List files by state (UF) available on the FTP. Filters by UF if provided."""
    files = _ftp.list_files(_CFG_UF["ftp_dir"])
    files = [
        f
        for f in files
        if f.upper().startswith("DN") and not f.upper().startswith(("DNBR", "DNEX"))
    ]
    if uf:
        prefix = f"DN{uf.upper()}"
        files = [f for f in files if f.upper().startswith(prefix)]
    return files


def download(
    uf: str, year: int, destination: Path | None = None, force: bool = False
) -> Path:
    """Download `DN{UF}{YYYY}.dbc` to local cache."""
    _validate_uf(uf, year)
    return _download_file(
        _CFG_UF["ftp_dir"], f"DN{uf.upper()}{year}.dbc", destination, force
    )


def read(
    uf: str,
    year: int,
    destination: Path | None = None,
    force: bool = False,
    engine: str = "pandas",
    parquet: bool = False,
) -> Any:
    """Download (if needed) and return data by state (UF) as a DataFrame (or engine table)."""
    return _read(
        download(uf, year, destination=destination, force=force),
        engine=engine,
        parquet=parquet,
        force=force,
    )


# ---------------------------------------------------------------------------
# National aggregate (DNBR — incomplete series: 2014–2017)
# ---------------------------------------------------------------------------


def list_national() -> list[str]:
    """List national aggregate files available on the FTP."""
    files = _ftp.list_files(_CFG_NATIONAL["ftp_dir"])
    return [f for f in files if f.upper().startswith("DNBR")]


def download_national(
    year: int, destination: Path | None = None, force: bool = False
) -> Path:
    """Download `DNBR{YYYY}.dbc` to local cache."""
    _validate_national(year)
    return _download_file(
        _CFG_NATIONAL["ftp_dir"], f"DNBR{year}.dbc", destination, force
    )


def read_national(
    year: int,
    destination: Path | None = None,
    force: bool = False,
    engine: str = "pandas",
    parquet: bool = False,
) -> Any:
    """Download (if needed) and return the national aggregate as a DataFrame (or engine table)."""
    return _read(
        download_national(year, destination=destination, force=force),
        engine=engine,
        parquet=parquet,
        force=force,
    )


# ---------------------------------------------------------------------------
# Exception / supplementary files (DNEX)
# ---------------------------------------------------------------------------


def list_exceptions() -> list[str]:
    """List exception files available on the FTP."""
    files = _ftp.list_files(_CFG_EXCEPTIONS["ftp_dir"])
    return [f for f in files if f.upper().startswith("DNEX")]


def download_exception(
    year: int, destination: Path | None = None, force: bool = False
) -> Path:
    """Download `DNEX{YYYY}.dbc` to local cache."""
    return _download_file(
        _CFG_EXCEPTIONS["ftp_dir"], f"DNEX{year}.dbc", destination, force
    )


def read_exception(
    year: int,
    destination: Path | None = None,
    force: bool = False,
    engine: str = "pandas",
    parquet: bool = False,
) -> Any:
    """Download (if needed) and return the exception file as a DataFrame (or engine table)."""
    return _read(
        download_exception(year, destination=destination, force=force),
        engine=engine,
        parquet=parquet,
        force=force,
    )


# ---------------------------------------------------------------------------
# Technical documentation — download only
# ---------------------------------------------------------------------------


def list_docs() -> dict[str, str]:
    """Return technical documents available for download: {name: description}."""
    return dict(_CFG_DOCS["files"])


def download_docs(
    file: str | None = None,
    destination: Path | None = None,
    force: bool = False,
) -> "Path | list[Path]":
    """Download SINASC technical documents.

    Note: the FTP path for this directory has not been fully confirmed.
    If download fails, use `mapear_ftp.py` to locate the correct directory.

    - If `file` is provided, download only that file.
    - If omitted, download all available files.
    """
    available = _CFG_DOCS["files"]
    ftp_dir = _CFG_DOCS["ftp_dir"]

    if file:
        if file not in available:
            raise ValueError(
                f"Document not available: '{file}'. Available: {list(available)}"
            )
        return _download_file(ftp_dir, file, destination, force)

    return [_download_file(ftp_dir, name, destination, force) for name in available]
