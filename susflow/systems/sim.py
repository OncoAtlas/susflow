"""
susflow/systems/sim.py
======================
SIM — Sistema de Informações sobre Mortalidade.

Dois subtipos:

  uf       → DO{UF}{YYYY}.dbc  em CID10/DORES/   ex: DOSP2023.dbc
  especial → DO{TIPO}{YY}.dbc  em CID10/DOFET/   ex: DOEXT24.dbc
             tipos: EXT (causas externas), FET (fetal), INF (infantil), MAT (materno)
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SIM as _CFG, UFS

_DIR_UF      = _CFG["uf"]["ftp_dir"]
_DIR_ESP     = _CFG["special"]["ftp_dir"]
_TIPOS_ESP   = set(_CFG["special"]["types"].keys())          # EXT, FET, INF, MAT
_ANO_MIN_UF, _ANO_MAX_UF   = _CFG["uf"]["year_range"]
_ANO_MIN_ESP, _ANO_MAX_ESP = _CFG["special"]["year_range"]


def _validar_uf(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    if not (_ANO_MIN_UF <= ano <= _ANO_MAX_UF):
        raise ValueError(f"Ano fora do intervalo: {ano} (disponível: {_ANO_MIN_UF}–{_ANO_MAX_UF})")


def _validar_especial(tipo: str, ano: int) -> None:
    if tipo.upper() not in _TIPOS_ESP:
        raise ValueError(f"Tipo inválido: '{tipo}'. Valores aceitos: {sorted(_TIPOS_ESP)}")
    if not (_ANO_MIN_ESP <= ano <= _ANO_MAX_ESP):
        raise ValueError(f"Ano fora do intervalo: {ano} (disponível: {_ANO_MIN_ESP}–{_ANO_MAX_ESP})")


# ---------------------------------------------------------------------------
# Por UF
# ---------------------------------------------------------------------------

def listar(uf: str | None = None) -> list[str]:
    """Lista arquivos por UF disponíveis no FTP. Filtra por UF se informada."""
    arquivos = _ftp.listar(_DIR_UF)
    if uf:
        prefixo = f"DO{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DO{UF}{YYYY}.dbc para o cache local."""
    _validar_uf(uf, ano)
    caminho = f"{_DIR_UF}/DO{uf.upper()}{ano}.dbc"
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def ler(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados por UF como DataFrame."""
    from ..reader import ler as _ler
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Especial (DOFET — dados nacionais por categoria)
# ---------------------------------------------------------------------------

def listar_especial(tipo: str | None = None) -> list[str]:
    """Lista arquivos especiais (EXT/FET/INF/MAT). Filtra por tipo se informado."""
    arquivos = _ftp.listar(_DIR_ESP)
    if tipo:
        prefixo = f"DO{tipo.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar_especial(tipo: str, ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DO{TIPO}{YY}.dbc (ex: DOEXT24.dbc) para o cache local."""
    _validar_especial(tipo, ano)
    nome    = f"DO{tipo.upper()}{str(ano)[-2:]}.dbc"
    caminho = f"{_DIR_ESP}/{nome}"
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def ler_especial(tipo: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna dados especiais como DataFrame."""
    from ..reader import ler as _ler
    return _ler(baixar_especial(tipo, ano, destino=destino, forcar=forcar))
