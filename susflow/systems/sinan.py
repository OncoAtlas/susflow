"""
susflow/systems/sinan.py
========================
SINAN — Notifiable Diseases Information System.

Disease data:

    final        → {DISEASE}BR{YY}.dbc  in DADOS/FINAIS/   e.g. DENGBR23.dbc
    preliminary  → {DISEASE}BR{YY}.dbc  in DADOS/PRELIM/   (use flag `preliminary=True`)

Auxiliary files (download only, not read as DataFrame):

    docs         → layouts, variable dictionary and technical notes per disease
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SINAN as _CFG
from ..reader import read as _read

_DIR_FINAL = _CFG["ftp_dir"]
_DIR_PRELIM = _CFG["ftp_dir_prelim"]
_CFG_DOCS = _CFG["docs"]
_DISEASES = {k.upper(): v for k, v in _CFG["diseases"].items()}
_YEAR_MIN = 2000
_YEAR_MAX = 2024


def _validate(disease: str, year: int) -> str:
    disease = disease.upper()
    if disease not in _DISEASES:
        available = ", ".join(sorted(_DISEASES))
        raise ValueError(f"Invalid disease code: '{disease}'.\nAvailable: {available}")

    if not (_YEAR_MIN <= year <= _YEAR_MAX):
        raise ValueError(f"Year out of range: {year} (available: {_YEAR_MIN}–{_YEAR_MAX})")

    return disease


def _file_name(disease: str, year: int) -> str:
    return f"{disease}BR{str(year)[-2:]}.dbc"


def _download_file(
    ftp_dir: str, name: str, destination: Path | None, force: bool
) -> Path:
    path = f"{ftp_dir}/{name}"
    local = _cache.local_path(path, destination)
    if local.exists() and not force:
        return local
    return _ftp.download(path, local)


def diseases() -> dict[str, str]:
    """Return the dictionary {code: description} of all available diseases."""
    return dict(_DISEASES)


def list_files(disease: str | None = None, preliminary: bool = False) -> list[str]:
    """
    List files available on the FTP.
    If `disease` is provided, filter by disease code.
    Use `preliminary=True` to list preliminary data.
    """
    directory = _DIR_PRELIM if preliminary else _DIR_FINAL
    files = _ftp.list_files(directory)

    if disease:
        prefix = disease.upper()
        files = [f for f in files if f.upper().startswith(prefix)]

    return files


def download(
    disease: str,
    year: int,
    destination: Path | None = None,
    force: bool = False,
    preliminary: bool = False,
) -> Path:
    """
    Download `{DISEASE}BR{YY}.dbc` to local cache.
    Use `preliminary=True` to download preliminary data.
    """
    disease = _validate(disease, year)
    ftp_dir = _DIR_PRELIM if preliminary else _DIR_FINAL
    path = f"{ftp_dir}/{_file_name(disease, year)}"
    local = _cache.local_path(path, destination)

    if local.exists() and not force:
        return local

    return _ftp.download(path, local)


def read(
    disease: str,
    year: int,
    destination: Path | None = None,
    force: bool = False,
    preliminary: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return the data as a DataFrame."""
    return _read(
        download(disease, year, destination=destination, force=force, preliminary=preliminary)
    )


# ---------------------------------------------------------------------------
# Technical documentation — download only
# ---------------------------------------------------------------------------


def list_docs() -> dict[str, str]:
    """Return available technical documents for download: {name: description}."""
    return dict(_CFG_DOCS["files"])


def download_docs(
    file: str | None = None,
    destination: Path | None = None,
    force: bool = False,
) -> "Path | list[Path]":
    """Download SINAN technical documents (layouts, variable dictionary, technical notes).

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
                f"Document not available: '{file}'.\nAvailable: {list(available)}"
            )
        return _download_file(ftp_dir, file, destination, force)

    return [_download_file(ftp_dir, name, destination, force) for name in available]
