"""
susflow/systems/pni.py
======================
PNI — National Immunization Program.

File pattern: DPNI{UF}{YY}.DBF
Granularity: annual / by state (UF)
Coverage:    1994–2019

Files are located directly in `DADOS/` (no nested folder):
    e.g. /dissemin/publicos/PNI/DADOS/DPNISP02.DBF

Notes:
    - Pure .DBF format (no blast); read with `dbfread` via `reader.py`.
    - Year suffix uses 2 digits (94–19); years 2000–2009 appear as
        00–09, so normalization is done with `(ano % 100)`.
    - UF encoded as 2 uppercase letters (e.g. SP, RJ, AM).
    - Coverage ends in 2019; there are no preliminary files.
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import PNI as _CFG
from ..config import UFS
from ..reader import ler as _ler

_BASE = _CFG["ftp_dir"]
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(
            f"Year {ano} out of range for PNI " f"(available: {_ANO_MIN}–{_ANO_MAX})"
        )


def _nome(uf: str, ano: int) -> str:
    return f"DPNI{uf.upper()}{ano % 100:02d}.DBF"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_BASE}/{nome}"
    local = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def listar(uf: str | None = None) -> list[str]:
    """List files available on the FTP for PNI.

    Filters by state (UF) if provided.
    """
    arquivos = _ftp.listar(_BASE)
    if uf:
        filtro = f"DPNI{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(filtro)]
    return arquivos


def baixar(
    uf: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Download `DPNI{UF}{YY}.DBF` to local cache and return the path.

    Parameters
    ----------
    uf      : state code (e.g. 'SP')
    ano     : year with 4 digits (e.g. 2010)
    destino : destination folder; uses default cache if None
    forcar  : if True, download even if file exists in cache
    """
    _validar(uf, ano)
    return _baixar_arquivo(_nome(uf, ano), destino, forcar)


def ler(
    uf: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
    engine: str = "pandas",
) -> Any:
    """Download (if needed) and return the data as a DataFrame."""
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar), engine=engine)
