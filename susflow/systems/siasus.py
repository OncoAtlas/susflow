"""
susflow/systems/siasus.py
=========================
SIASUS — Outpatient Information System (SUS).

File pattern: {PREFIX}{UF}{YY}{MM}.dbc
Granularity: monthly / by state (UF)
Overall coverage: 2008–2026

Active prefixes:
    PA   — Outpatient production (BPA)              2008–2026
    BI   — Individualized BPA                       2008–2026
    AD   — APAC various reports                     2008–2026
    AM   — APAC medications                         2008–2026
    AMP  — APAC standardized medications            2020–2026
    AQ   — APAC chemotherapy                         2008–2026
    AR   — APAC radiotherapy                         2008–2026
    ACF  — APAC creation of arteriovenous fistula   2014–2026
    ATD  — APAC dialysis treatment                  2014–2026
    PS   — RAAS Psychosocial                        2013–2026
    AB   — APAC Post-bariatric surgery (new)        2025–2026

Retired prefixes (still available on FTP):
    ABO  — APAC Post-bariatric surgery (legacy)    2015–2018
    AN   — APAC nephrology (replaced by ATD)       2008–2014
    SAD  — RAAS Home Care                           2013–2015
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SIASUS as _CFG
from ..config import UFS
from ..reader import ler as _ler

_DIR = _CFG["ftp_dir"]
_PREFIXOS = _CFG["prefixes"]  # {prefixo: (descricao, ano_min, ano_max)}
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar_prefixo(prefixo: str) -> str:
    prefixo = prefixo.upper()
    if prefixo not in _PREFIXOS:
        raise ValueError(
            f"Invalid prefix: '{prefixo}'. " f"Available: {sorted(_PREFIXOS)}"
        )
    return prefixo


def _validar(prefixo: str, uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"Invalid UF: '{uf}'. Accepted values: {UFS}")

    if not (1 <= mes <= 12):
        raise ValueError(f"Invalid month: {mes}. Use 1–12.")
    _, ano_min, ano_max = _PREFIXOS[prefixo]

    if not (ano_min <= ano <= ano_max):
        raise ValueError(
            f"Year {ano} out of range for prefix '{prefixo}' "
            f"(available: {ano_min}–{ano_max})"
        )


def _nome(prefixo: str, uf: str, ano: int, mes: int) -> str:
    return f"{prefixo}{uf}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_DIR}/{nome}"
    local = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def prefixos() -> dict[str, str]:
    """Return available prefixes: {prefix: description}."""
    return {k: v[0] for k, v in _PREFIXOS.items()}


def listar(uf: str | None = None, prefixo: str = "PA") -> list[str]:
    """List files available on the FTP.

    Filters by prefix (default: `PA`) and optionally by state (UF).
    """
    prefixo = _validar_prefixo(prefixo)
    arquivos = _ftp.listar(_DIR)
    arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]

    if uf:
        filtro = f"{prefixo}{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(filtro)]
    return arquivos


def baixar(
    uf: str,
    ano: int,
    mes: int,
    prefixo: str = "PA",
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Download `{PREFIX}{UF}{YY}{MM}.dbc` to local cache.

    Default prefix: `PA` (Outpatient production).
    """
    prefixo = _validar_prefixo(prefixo)
    _validar(prefixo, uf, ano, mes)
    return _baixar_arquivo(_nome(prefixo, uf.upper(), ano, mes), destino, forcar)


def ler(
    uf: str,
    ano: int,
    mes: int,
    prefixo: str = "PA",
    destino: Path | None = None,
    forcar: bool = False,
    engine: str = "pandas",
) -> Any:
    """Download (if needed) and return the data as a DataFrame."""
    return _ler(baixar(uf, ano, mes, prefixo=prefixo, destino=destino, forcar=forcar), engine=engine)
