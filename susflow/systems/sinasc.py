"""
susflow/systems/sinasc.py
=========================
SINASC — Live Births Information System.

Data subtypes:

    uf       → DN{UF}{YYYY}.dbc  in NOV/DNRES/   e.g. DNSP2022.dbc
                         by state, annual, 1996–2022

    national → DNBR{YYYY}.dbc   in NOV/DNRES/   e.g. DNBR2015.dbc
                         national aggregate, incomplete series (2014–2017 confirmed)

    exceptions → DNEX{YYYY}.dbc   in NOV/DNRES/   e.g. DNEX2021.dbc
                         one-off files with supplementary records

Auxiliary files (download only, not read as DataFrame):

    docs     → system technical documentation (FTP path to confirm)
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SINASC as _CFG
from ..config import UFS
from ..reader import ler as _ler

_CFG_UF = _CFG["uf"]
_CFG_NAC = _CFG["nacional"]
_CFG_EXC = _CFG["excecoes"]
_CFG_DOC = _CFG["docs"]

_ANO_MIN_UF, _ANO_MAX_UF = _CFG_UF["year_range"]
_ANO_MIN_NAC, _ANO_MAX_NAC = _CFG_NAC["year_range"]


def _validar_uf(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (_ANO_MIN_UF <= ano <= _ANO_MAX_UF):
        raise ValueError(
            f"Year out of range: {ano} (available: {_ANO_MIN_UF}–{_ANO_MAX_UF})"
        )


def _validar_nacional(ano: int) -> None:
    if not (_ANO_MIN_NAC <= ano <= _ANO_MAX_NAC):
        raise ValueError(
            f"Year out of range for the national aggregate: {ano} "
            f"(confirmed: {_ANO_MIN_NAC}–{_ANO_MAX_NAC})"
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
# Por UF
# ---------------------------------------------------------------------------


def listar(uf: str | None = None) -> list[str]:
    """List files by state (UF) available on the FTP. Filters by UF if provided."""
    arquivos = _ftp.listar(_CFG_UF["ftp_dir"])
    arquivos = [
        a
        for a in arquivos
        if a.upper().startswith("DN") and not a.upper().startswith(("DNBR", "DNEX"))
    ]
    if uf:
        prefixo = f"DN{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar(
    uf: str, ano: int, destino: Path | None = None, forcar: bool = False
) -> Path:
    """Download `DN{UF}{YYYY}.dbc` to local cache."""
    _validar_uf(uf, ano)
    return _baixar_arquivo(
        _CFG_UF["ftp_dir"], f"DN{uf.upper()}{ano}.dbc", destino, forcar
    )


def ler(
    uf: str, ano: int, destino: Path | None = None, forcar: bool = False
) -> pd.DataFrame:
    """Download (if needed) and return data by state (UF) as a DataFrame."""
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Agregado nacional (DNBR — série incompleta: 2014–2017)
# ---------------------------------------------------------------------------


def listar_nacional() -> list[str]:
    """List national aggregate files available on the FTP."""
    arquivos = _ftp.listar(_CFG_NAC["ftp_dir"])
    return [a for a in arquivos if a.upper().startswith("DNBR")]


def baixar_nacional(
    ano: int, destino: Path | None = None, forcar: bool = False
) -> Path:
    """Download `DNBR{YYYY}.dbc` to local cache."""
    _validar_nacional(ano)
    return _baixar_arquivo(_CFG_NAC["ftp_dir"], f"DNBR{ano}.dbc", destino, forcar)


def ler_nacional(
    ano: int, destino: Path | None = None, forcar: bool = False
) -> pd.DataFrame:
    """Download (if needed) and return the national aggregate as a DataFrame."""
    return _ler(baixar_nacional(ano, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Arquivos de exceção/suplementares (DNEX)
# ---------------------------------------------------------------------------


def listar_excecoes() -> list[str]:
    """List exception files available on the FTP."""
    arquivos = _ftp.listar(_CFG_EXC["ftp_dir"])
    return [a for a in arquivos if a.upper().startswith("DNEX")]


def baixar_excecao(ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Download `DNEX{YYYY}.dbc` to local cache."""
    return _baixar_arquivo(_CFG_EXC["ftp_dir"], f"DNEX{ano}.dbc", destino, forcar)


def ler_excecao(
    ano: int, destino: Path | None = None, forcar: bool = False
) -> pd.DataFrame:
    """Download (if needed) and return the exception file as a DataFrame."""
    return _ler(baixar_excecao(ano, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Documentação técnica — apenas download
# ---------------------------------------------------------------------------


def listar_docs() -> dict[str, str]:
    """Return technical documents available for download: {name: description}."""
    return dict(_CFG_DOC["arquivos"])


def baixar_docs(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> "Path | list[Path]":
    """Download SINASC technical documents.

    Note: the FTP path for this directory has not been fully confirmed.
    If download fails, use `mapear_ftp.py` to locate the correct directory.

    - If `arquivo` is provided, download only that file.
    - If omitted, download all available files.
    """
    disponiveis = _CFG_DOC["arquivos"]
    ftp_dir = _CFG_DOC["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(
                f"Document not available: '{arquivo}'. Available: {list(disponiveis)}"
            )
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]
