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
from ..reader import ler as _ler

_DIR = _CFG["ftp_dir"]
_PREFIXOS = set(_CFG["prefixes"].keys())  # RD, SP, RJ, ER
_PREFIXOS_N = set(_CFG["prefixes_nacionais"].keys())  # CH, CM
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar_uf(uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    _validar_periodo(ano, mes)


def _validar_periodo(ano: int, mes: int) -> None:
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(f"Year out of range: {ano} (available: {_ANO_MIN}–{_ANO_MAX})")
    if not (1 <= mes <= 12):
        raise ValueError(f"Invalid month: {mes}. Use 1–12.")


def _validar_prefixo(prefixo: str, nacional: bool = False) -> str:
    prefixo = prefixo.upper()
    pool = _PREFIXOS_N if nacional else _PREFIXOS
    if prefixo not in pool:
        raise ValueError(f"Invalid prefix: '{prefixo}'. " f"Available: {sorted(pool)}")
    return prefixo


def _nome(prefixo: str, uf_ou_br: str, ano: int, mes: int) -> str:
    return f"{prefixo}{uf_ou_br}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_DIR}/{nome}"
    local = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


# ---------------------------------------------------------------------------
# By state (UF)
# ---------------------------------------------------------------------------


def prefixos() -> dict[str, str]:
    """Return available prefixes for data by state (UF): {prefix: description}."""
    return dict(_CFG["prefixes"])


def listar(uf: str | None = None, prefixo: str = "RD") -> list[str]:
    """List files available on the FTP.

    Filters by prefix (default: `RD`) and optionally by state (UF).
    """
    prefixo = prefixo.upper()
    arquivos = _ftp.listar(_DIR)
    arquivos = [
        a
        for a in arquivos
        if a.upper().startswith(prefixo) and not a.upper().startswith(f"{prefixo}BR")
    ]
    if uf:
        filtro = f"{prefixo}{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(filtro)]
    return arquivos


def baixar(
    uf: str,
    ano: int,
    mes: int,
    prefixo: str = "RD",
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Download `{PREFIX}{UF}{YY}{MM}.dbc` to local cache.

    Default prefix: `RD` (Reduced AIH — admissions).
    """
    prefixo = _validar_prefixo(prefixo)
    _validar_uf(uf, ano, mes)
    return _baixar_arquivo(_nome(prefixo, uf.upper(), ano, mes), destino, forcar)


def ler(
    uf: str,
    ano: int,
    mes: int,
    prefixo: str = "RD",
    destino: Path | None = None,
    forcar: bool = False,
    parquet: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return data by state (UF) as a DataFrame."""
    return _ler(
        baixar(uf, ano, mes, prefixo=prefixo, destino=destino, forcar=forcar),
        parquet=parquet,
        forcar=forcar,
    )


# ---------------------------------------------------------------------------
# National (CH and CM — use fixed BR)
# ---------------------------------------------------------------------------


def prefixos_nacionais() -> dict[str, str]:
    """Return available national prefixes: {prefix: description}."""
    return dict(_CFG["prefixes_nacionais"])


def listar_nacional(prefixo: str = "CH") -> list[str]:
    """List national files available on the FTP.

    Default prefix: `CH` (national header).
    """
    prefixo = prefixo.upper()
    arquivos = _ftp.listar(_DIR)
    return [a for a in arquivos if a.upper().startswith(f"{prefixo}BR")]


def baixar_nacional(
    ano: int,
    mes: int,
    prefixo: str = "CH",
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Download `{PREFIX}BR{YY}{MM}.dbc` (national scope) to local cache."""
    prefixo = _validar_prefixo(prefixo, nacional=True)
    _validar_periodo(ano, mes)
    return _baixar_arquivo(_nome(prefixo, "BR", ano, mes), destino, forcar)


def ler_nacional(
    ano: int,
    mes: int,
    prefixo: str = "CH",
    destino: Path | None = None,
    forcar: bool = False,
    parquet: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return national data as a DataFrame."""
    return _ler(
        baixar_nacional(ano, mes, prefixo=prefixo, destino=destino, forcar=forcar),
        parquet=parquet,
        forcar=forcar,
    )
