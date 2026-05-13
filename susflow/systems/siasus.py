"""
susflow/systems/siasus.py
=========================
SIASUS — Sistema de Informações Ambulatoriais do SUS.

Padrão de arquivo: {PREFIX}{UF}{YY}{MM}.dbc
Granularidade:     mensal / por UF
Cobertura geral:   2008–2026

Prefixos ativos:
  PA   — Produção Ambulatorial (BPA)              2008–2026
  BI   — BPA Individualizado                      2008–2026
  AD   — APAC de Laudos Diversos                  2008–2026
  AM   — APAC de Medicamentos                     2008–2026
  AMP  — APAC de Medicamentos Padronizados        2020–2026
  AQ   — APAC de Quimioterapia                    2008–2026
  AR   — APAC de Radioterapia                     2008–2026
  ACF  — APAC Confecção de Fístula Arteriovenosa  2014–2026
  ATD  — APAC Tratamento Dialítico                2014–2026
  PS   — RAAS Psicossocial                        2013–2026
  AB   — APAC Pós Cirurgia Bariátrica (novo)      2025–2026

Prefixos encerrados (ainda disponíveis no FTP):
  ABO  — APAC Pós Cirurgia Bariátrica (legado)    2015–2018
  AN   — APAC de Nefrologia (substituído por ATD) 2008–2014
  SAD  — RAAS Atenção Domiciliar                  2013–2015
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SIASUS as _CFG, UFS
from ..reader import ler as _ler

_DIR      = _CFG["ftp_dir"]
_PREFIXOS = _CFG["prefixes"]   # {prefixo: (descricao, ano_min, ano_max)}
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar_prefixo(prefixo: str) -> str:
    prefixo = prefixo.upper()
    if prefixo not in _PREFIXOS:
        raise ValueError(
            f"Prefixo inválido: '{prefixo}'. "
            f"Disponíveis: {sorted(_PREFIXOS)}"
        )
    return prefixo


def _validar(prefixo: str, uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    
    if not (1 <= mes <= 12):
        raise ValueError(f"Mês inválido: {mes}. Use 1–12.")
    _, ano_min, ano_max = _PREFIXOS[prefixo]

    if not (ano_min <= ano <= ano_max):
        raise ValueError(
            f"Ano {ano} fora do intervalo para o prefixo '{prefixo}' "
            f"(disponível: {ano_min}–{ano_max})"
        )


def _nome(prefixo: str, uf: str, ano: int, mes: int) -> str:
    return f"{prefixo}{uf}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_DIR}/{nome}"
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local
    
    return _ftp.baixar(caminho, local)


def prefixos() -> dict[str, str]:
    """Retorna os prefixos disponíveis: {prefixo: descrição}."""
    return {k: v[0] for k, v in _PREFIXOS.items()}


def listar(uf: str | None = None, prefixo: str = "PA") -> list[str]:
    """
    Lista arquivos disponíveis no FTP.
    Filtra por prefixo (padrão: PA) e opcionalmente por UF.
    """
    prefixo  = _validar_prefixo(prefixo)
    arquivos = _ftp.listar(_DIR)
    arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    
    if uf:
        filtro   = f"{prefixo}{uf.upper()}"
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
    """
    Baixa {PREFIX}{UF}{YY}{MM}.dbc para o cache local.
    Prefixo padrão: PA (Produção Ambulatorial).
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
) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados como DataFrame."""
    return _ler(baixar(uf, ano, mes, prefixo=prefixo, destino=destino, forcar=forcar))
