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

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SIM as _CFG
from ..config import UFS
from ..reader import ler as _ler

_DIR_UF = _CFG["uf"]["ftp_dir"]
_DIR_ESP = _CFG["special"]["ftp_dir"]
_TIPOS_ESP = set(_CFG["special"]["types"].keys())
_ANO_MIN_UF, _ANO_MAX_UF = _CFG["uf"]["year_range"]
_ANO_MIN_ESP, _ANO_MAX_ESP = _CFG["special"]["year_range"]


def _validar_uf(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    if not (_ANO_MIN_UF <= ano <= _ANO_MAX_UF):
        raise ValueError(
            f"Year out of range: {ano} (available: {_ANO_MIN_UF}–{_ANO_MAX_UF})"
        )


def _validar_especial(tipo: str, ano: int) -> None:
    if tipo.upper() not in _TIPOS_ESP:
        raise ValueError(
            f"Invalid type: '{tipo}'. Accepted values: {sorted(_TIPOS_ESP)}"
        )
    if not (_ANO_MIN_ESP <= ano <= _ANO_MAX_ESP):
        raise ValueError(
            f"Year out of range: {ano} (available: {_ANO_MIN_ESP}–{_ANO_MAX_ESP})"
        )


def _baixar_arquivo(
    ftp_dir: str, nome: str, destino: Path | None, forcar: bool
) -> Path:
    caminho = f"{ftp_dir}/{nome}"
    local = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


# ---------------------------------------------------------------------------
# By state (UF)
# ---------------------------------------------------------------------------


def listar(uf: str | None = None) -> list[str]:
    """List files by state (UF) available on the FTP. Filters by UF if provided."""
    arquivos = _ftp.listar(_DIR_UF)
    if uf:
        prefixo = f"DO{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar(
    uf: str, ano: int, destino: Path | None = None, forcar: bool = False
) -> Path:
    """Download `DO{UF}{YYYY}.dbc` to local cache."""
    _validar_uf(uf, ano)
    return _baixar_arquivo(_DIR_UF, f"DO{uf.upper()}{ano}.dbc", destino, forcar)


def ler(
    uf: str, ano: int, destino: Path | None = None, forcar: bool = False, parquet: bool = False
) -> pd.DataFrame:
    """Download (if needed) and return data by state (UF) as a DataFrame."""
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar), parquet=parquet, forcar=forcar)


# ---------------------------------------------------------------------------
# Special (DOFET — national data by category)
# ---------------------------------------------------------------------------


def listar_especial(tipo: str | None = None) -> list[str]:
    """List special files (EXT/FET/INF/MAT). Filters by type if provided."""
    arquivos = _ftp.listar(_DIR_ESP)
    if tipo:
        prefixo = f"DO{tipo.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar_especial(
    tipo: str, ano: int, destino: Path | None = None, forcar: bool = False
) -> Path:
    """Download `DO{TYPE}{YY}.dbc` (e.g. `DOEXT24.dbc`) to local cache."""
    _validar_especial(tipo, ano)
    nome = f"DO{tipo.upper()}{str(ano)[-2:]}.dbc"
    return _baixar_arquivo(_DIR_ESP, nome, destino, forcar)


def ler_especial(
    tipo: str, ano: int, destino: Path | None = None, forcar: bool = False, parquet: bool = False
) -> pd.DataFrame:
    """Download (if needed) and return special data as a DataFrame."""
    return _ler(
        baixar_especial(tipo, ano, destino=destino, forcar=forcar), parquet=parquet, forcar=forcar
    )


# ---------------------------------------------------------------------------
# Arquivos auxiliares — apenas download
# ---------------------------------------------------------------------------


def listar_docs() -> dict[str, str]:
    """Return the technical documents available for download: {name: description}."""
    return dict(_CFG["docs"]["arquivos"])


def listar_tabelas() -> dict[str, str]:
    """Return support tables available for download: {name: description}."""
    return dict(_CFG["tabelas"]["arquivos"])


def listar_tab() -> dict[str, str]:
    """Return aggregated tabulated data available for download: {name: description}."""
    return dict(_CFG["tab"]["arquivos"])


def baixar_docs(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """Download SIM technical documents (layouts, structure, dictionary).

    - If `arquivo` is provided, download only that file.
    - If omitted, download all available documents.

    Returns the Path of the file (or list of Paths if downloading all).
    """
    disponiveis = _CFG["docs"]["arquivos"]
    ftp_dir = _CFG["docs"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(
                f"Document not available: '{arquivo}'. Available: {list(disponiveis)}"
            )
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]


def baixar_tabelas(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """Download SIM support tables (CID-10, municipalities, occupations, countries, UFs).

    - If `arquivo` is provided, download only that file.
    - If omitted, download all available tables.
    """
    disponiveis = _CFG["tabelas"]["arquivos"]
    ftp_dir = _CFG["tabelas"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(
                f"Table not available: '{arquivo}'. Available: {list(disponiveis)}"
            )
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]


def baixar_tab(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """Download aggregated tabulated data by CID-10.

    - If `arquivo` is provided, download only that file.
    - If omitted, download all available files.
    """
    disponiveis = _CFG["tab"]["arquivos"]
    ftp_dir = _CFG["tab"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(
                f"File not available: '{arquivo}'. Available: {list(disponiveis)}"
            )
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]
