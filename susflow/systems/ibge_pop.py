"""
susflow/systems/ibge_pop.py
===========================
IBGE/POP — Population estimates (IBGE).

File pattern: POPBR{YY}.zip
Granularity: annual / national
Coverage:    1980–2012

Files are located directly in /dissemin/publicos/IBGE/POP/:
    e.g. /dissemin/publicos/IBGE/POP/POPBR95.zip

Notes:
    - National scope only (no UF breakdown).
    - ZIP archive; reader.py extracts and reads the first .dbc or .dbf inside.
    - Year suffix uses 2 digits: 1980 → 80, 2000 → 00, 2012 → 12.
"""

from pathlib import Path

import pandas as pd

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import IBGE_POP as _CFG
from ..reader import ler as _ler

_BASE = _CFG["ftp_dir"]
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar(ano: int) -> None:
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(
            f"Year {ano} out of range for IBGE/POP (available: {_ANO_MIN}–{_ANO_MAX})"
        )


def _nome(ano: int) -> str:
    return f"POPBR{ano % 100:02d}.zip"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_BASE}/{nome}"
    local = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


def listar() -> list[str]:
    """List population estimate files available on the FTP."""
    return _ftp.listar(_BASE)


def baixar(ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Download `POPBR{YY}.zip` to local cache and return the path.

    Parameters
    ----------
    ano     : year with 4 digits (e.g. 1995)
    destino : destination folder; uses default cache if None
    forcar  : if True, download even if file exists in cache
    """
    _validar(ano)
    return _baixar_arquivo(_nome(ano), destino, forcar)


def ler(ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Download (if needed) and return the population estimates as a DataFrame."""
    return _ler(baixar(ano, destino=destino, forcar=forcar))
