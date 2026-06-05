"""
susflow/systems/sim.py
======================
SIM — Mortality Information System.

Data subtypes:

    uf       → DO{UF}{YYYY}.dbc  in CID10/DORES/   e.g. DOSP2023.dbc
    special  → DO{TYPE}{YY}.dbc  in CID10/DOFET/   e.g. DOEXT24.dbc
                         types: EXT (external causes), FET (fetal), INF (infant), MAT (maternal)

Auxiliary files (download only, not read as DataFrame):

    docs     → layouts, variable dictionary and file structure
    tab      → aggregated tabulated data by CID-10
    tables   → support tables: CID-10, municipalities, occupations, countries, UFs
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SIM as _CFG
from ..config import UFS
from ..reader import read as _read

_DIR_UF = _CFG["uf"]["ftp_dir"]
_DIR_SPECIAL = _CFG["special"]["ftp_dir"]
_SPECIAL_TYPES = set(_CFG["special"]["types"].keys())
_YEAR_MIN_UF, _YEAR_MAX_UF = _CFG["uf"]["year_range"]
_YEAR_MIN_SPECIAL, _YEAR_MAX_SPECIAL = _CFG["special"]["year_range"]


def _validate_uf(uf: str, year: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    if not (_YEAR_MIN_UF <= year <= _YEAR_MAX_UF):
        raise ValueError(
            f"Year out of range: {year} (available: {_YEAR_MIN_UF}–{_YEAR_MAX_UF})"
        )


def _validate_special(type_: str, year: int) -> None:
    if type_.upper() not in _SPECIAL_TYPES:
        raise ValueError(
            f"Invalid type: '{type_}'. Accepted values: {sorted(_SPECIAL_TYPES)}"
        )
    if not (_YEAR_MIN_SPECIAL <= year <= _YEAR_MAX_SPECIAL):
        raise ValueError(
            f"Year out of range: {year} (available: {_YEAR_MIN_SPECIAL}–{_YEAR_MAX_SPECIAL})"
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
    files = _ftp.list_files(_DIR_UF)
    if uf:
        prefix = f"DO{uf.upper()}"
        files = [f for f in files if f.upper().startswith(prefix)]
    return files


def download(
    uf: str, year: int, destination: Path | None = None, force: bool = False
) -> Path:
    """Download `DO{UF}{YYYY}.dbc` to local cache."""
    _validate_uf(uf, year)
    return _download_file(_DIR_UF, f"DO{uf.upper()}{year}.dbc", destination, force)


def read(
    uf: str, year: int, destination: Path | None = None, force: bool = False, engine: str = "pandas"
) -> Any:
    """Download (if needed) and return data by state (UF) as a DataFrame."""
    return _read(download(uf, year, destination=destination, force=force), engine=engine)


# ---------------------------------------------------------------------------
# Special (DOFET — national data by category)
# ---------------------------------------------------------------------------


def list_special(type_: str | None = None) -> list[str]:
    """List special files (EXT/FET/INF/MAT). Filters by type if provided."""
    files = _ftp.list_files(_DIR_SPECIAL)
    if type_:
        prefix = f"DO{type_.upper()}"
        files = [f for f in files if f.upper().startswith(prefix)]
    return files


def download_special(
    type_: str, year: int, destination: Path | None = None, force: bool = False
) -> Path:
    """Download `DO{TYPE}{YY}.dbc` (e.g. `DOEXT24.dbc`) to local cache."""
    _validate_special(type_, year)
    name = f"DO{type_.upper()}{str(year)[-2:]}.dbc"
    return _download_file(_DIR_SPECIAL, name, destination, force)


def read_special(
    type_: str, year: int, destination: Path | None = None, force: bool = False, engine: str = "pandas"
) -> Any:
    """Download (if needed) and return special data as a DataFrame."""
    return _read(download_special(type_, year, destination=destination, force=force), engine=engine)


# ---------------------------------------------------------------------------
# Auxiliary files — download only
# ---------------------------------------------------------------------------


def list_docs() -> dict[str, str]:
    """Return the technical documents available for download: {name: description}."""
    return dict(_CFG["docs"]["files"])


def list_tables() -> dict[str, str]:
    """Return support tables available for download: {name: description}."""
    return dict(_CFG["tables"]["files"])


def list_tab() -> dict[str, str]:
    """Return aggregated tabulated data available for download: {name: description}."""
    return dict(_CFG["tab"]["files"])


def download_docs(
    file: str | None = None,
    destination: Path | None = None,
    force: bool = False,
) -> Path | list[Path]:
    """Download SIM technical documents (layouts, structure, dictionary).

    - If `file` is provided, download only that file.
    - If omitted, download all available documents.

    Returns the Path of the file (or list of Paths if downloading all).
    """
    available = _CFG["docs"]["files"]
    ftp_dir = _CFG["docs"]["ftp_dir"]

    if file:
        if file not in available:
            raise ValueError(
                f"Document not available: '{file}'. Available: {list(available)}"
            )
        return _download_file(ftp_dir, file, destination, force)

    return [_download_file(ftp_dir, name, destination, force) for name in available]


def download_tables(
    file: str | None = None,
    destination: Path | None = None,
    force: bool = False,
) -> Path | list[Path]:
    """Download SIM support tables (CID-10, municipalities, occupations, countries, UFs).

    - If `file` is provided, download only that file.
    - If omitted, download all available tables.
    """
    available = _CFG["tables"]["files"]
    ftp_dir = _CFG["tables"]["ftp_dir"]

    if file:
        if file not in available:
            raise ValueError(
                f"Table not available: '{file}'. Available: {list(available)}"
            )
        return _download_file(ftp_dir, file, destination, force)

    return [_download_file(ftp_dir, name, destination, force) for name in available]


def download_tab(
    file: str | None = None,
    destination: Path | None = None,
    force: bool = False,
) -> Path | list[Path]:
    """Download aggregated tabulated data by CID-10.

    - If `file` is provided, download only that file.
    - If omitted, download all available files.
    """
    available = _CFG["tab"]["files"]
    ftp_dir = _CFG["tab"]["ftp_dir"]

    if file:
        if file not in available:
            raise ValueError(
                f"File not available: '{file}'. Available: {list(available)}"
            )
        return _download_file(ftp_dir, file, destination, force)

    return [_download_file(ftp_dir, name, destination, force) for name in available]
