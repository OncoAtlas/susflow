"""
susflow/systems/sihsus.py
=========================
SIHSUS — Sistema de Informações Hospitalares do SUS.

Dados por UF (prefixo + UF):

  RD{UF}{YY}{MM}.dbc  — AIH Reduzida (internações — dado principal)
  SP{UF}{YY}{MM}.dbc  — Serviços profissionais
  RJ{UF}{YY}{MM}.dbc  — AIH rejeitada
  ER{UF}{YY}{MM}.dbc  — AIH com erro

Dados nacionais (prefixo + BR fixo):

  CH BR{YY}{MM}.dbc   — Cabeçalho nacional (dados agregados)
  CM BR{YY}{MM}.dbc   — Comunicação de movimento

Granularidade: mensal / ano com 2 dígitos
Cobertura:     2008–2026
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SIHSUS as _CFG, UFS
from ..reader import ler as _ler

_DIR        = _CFG["ftp_dir"]
_PREFIXOS   = set(_CFG["prefixes"].keys())           # RD, SP, RJ, ER
_PREFIXOS_N = set(_CFG["prefixes_nacionais"].keys())  # CH, CM
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar_uf(uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    _validar_periodo(ano, mes)


def _validar_periodo(ano: int, mes: int) -> None:
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(f"Ano fora do intervalo: {ano} (disponível: {_ANO_MIN}–{_ANO_MAX})")
    if not (1 <= mes <= 12):
        raise ValueError(f"Mês inválido: {mes}. Use 1–12.")


def _validar_prefixo(prefixo: str, nacional: bool = False) -> str:
    prefixo = prefixo.upper()
    pool = _PREFIXOS_N if nacional else _PREFIXOS
    if prefixo not in pool:
        raise ValueError(
            f"Prefixo inválido: '{prefixo}'. "
            f"Disponíveis: {sorted(pool)}"
        )
    return prefixo


def _nome(prefixo: str, uf_ou_br: str, ano: int, mes: int) -> str:
    return f"{prefixo}{uf_ou_br}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_DIR}/{nome}"
    local   = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


# ---------------------------------------------------------------------------
# Por UF
# ---------------------------------------------------------------------------

def prefixos() -> dict[str, str]:
    """Retorna os prefixos disponíveis para dados por UF: {prefixo: descrição}."""
    return dict(_CFG["prefixes"])


def listar(uf: str | None = None, prefixo: str = "RD") -> list[str]:
    """
    Lista arquivos disponíveis no FTP.
    Filtra por prefixo (padrão: RD) e opcionalmente por UF.
    """
    prefixo  = prefixo.upper()
    arquivos = _ftp.listar(_DIR)
    arquivos = [a for a in arquivos if a.upper().startswith(prefixo)
                and not a.upper().startswith(f"{prefixo}BR")]
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
    """
    Baixa {PREFIX}{UF}{YY}{MM}.dbc para o cache local.
    Prefixo padrão: RD (AIH Reduzida — internações).
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
) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados por UF como DataFrame."""
    return _ler(baixar(uf, ano, mes, prefixo=prefixo, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Nacionais (CH e CM — usam BR fixo)
# ---------------------------------------------------------------------------

def prefixos_nacionais() -> dict[str, str]:
    """Retorna os prefixos nacionais disponíveis: {prefixo: descrição}."""
    return dict(_CFG["prefixes_nacionais"])


def listar_nacional(prefixo: str = "CH") -> list[str]:
    """
    Lista arquivos nacionais disponíveis no FTP.
    Prefixo padrão: CH (cabeçalho nacional).
    """
    prefixo  = prefixo.upper()
    arquivos = _ftp.listar(_DIR)
    return [a for a in arquivos if a.upper().startswith(f"{prefixo}BR")]


def baixar_nacional(
    ano: int,
    mes: int,
    prefixo: str = "CH",
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """Baixa {PREFIX}BR{YY}{MM}.dbc (escopo nacional) para o cache local."""
    prefixo = _validar_prefixo(prefixo, nacional=True)
    _validar_periodo(ano, mes)
    return _baixar_arquivo(_nome(prefixo, "BR", ano, mes), destino, forcar)


def ler_nacional(
    ano: int,
    mes: int,
    prefixo: str = "CH",
    destino: Path | None = None,
    forcar: bool = False,
) -> pd.DataFrame:
    """Baixa (se necessário) e retorna dados nacionais como DataFrame."""
    return _ler(baixar_nacional(ano, mes, prefixo=prefixo, destino=destino, forcar=forcar))
