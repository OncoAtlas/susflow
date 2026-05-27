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
from ..reader import ler as _ler

_BASE = _CFG["ftp_base"]
_SUBTIPOS = _CFG["subtypes"]  # {tipo: (descricao, ano_min, ano_max)}


def _validar_subtipo(tipo: str) -> str:
    tipo = tipo.upper()
    if tipo not in _SUBTIPOS:
        raise ValueError(
            f"Invalid subtype: '{tipo}'. " f"Available: {sorted(_SUBTIPOS)}"
        )
    return tipo


def _validar(tipo: str, uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")
    if not (1 <= mes <= 12):
        raise ValueError(f"Invalid month: {mes}. Use 1–12.")
    _, ano_min, ano_max = _SUBTIPOS[tipo]
    if not (ano_min <= ano <= ano_max):
        raise ValueError(
            f"Year {ano} out of range for subtype '{tipo}' "
            f"(available: {ano_min}–{ano_max})"
        )


def _ftp_dir(tipo: str) -> str:
    return f"{_BASE}/{tipo}"


def _nome(tipo: str, uf: str, ano: int, mes: int) -> str:
    return f"{tipo}{uf}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(tipo: str, nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_ftp_dir(tipo)}/{nome}"
    local = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


def subtipos() -> dict[str, str]:
    """Return available subtypes: {type: description}."""
    return {k: v[0] for k, v in _SUBTIPOS.items()}


def listar(uf: str | None = None, tipo: str = "ST") -> list[str]:
    """List files available on the FTP for the given subtype.

    Filters by state (UF) if provided. Default subtype: `ST` (Establishments).
    """
    tipo = _validar_subtipo(tipo)
    arquivos = _ftp.listar(_ftp_dir(tipo))
    if uf:
        filtro = f"{tipo}{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(filtro)]
    return arquivos


def baixar(
    uf: str,
    ano: int,
    mes: int,
    tipo: str = "ST",
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Download `{TYPE}{UF}{YY}{MM}.dbc` to local cache.

    Default subtype: `ST` (Establishments).
    """
    tipo = _validar_subtipo(tipo)
    _validar(tipo, uf, ano, mes)
    return _baixar_arquivo(tipo, _nome(tipo, uf.upper(), ano, mes), destino, forcar)


def ler(
    uf: str,
    ano: int,
    mes: int,
    tipo: str = "ST",
    destino: Path | None = None,
    forcar: bool = False,
) -> pd.DataFrame:
    """Download (if needed) and return the data as a DataFrame."""
    return _ler(baixar(uf, ano, mes, tipo=tipo, destino=destino, forcar=forcar))
