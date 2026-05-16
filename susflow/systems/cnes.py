"""
susflow/systems/cnes.py
=======================
CNES — Cadastro Nacional de Estabelecimentos de Saúde.

Padrão de arquivo: {TYPE}/{TYPE}{UF}{YY}{MM}.dbc
Granularidade:     mensal / por UF
Cobertura geral:   2005–2026

O arquivo fica 2 níveis dentro de Dados/:
  ex: /dissemin/publicos/CNES/200508_/Dados/ST/STSP2501.dbc

Subtipos ativos:
  ST  — Estabelecimentos (dado principal)       2005–2026
  PF  — Profissionais de saúde                  2005–2026
  DC  — Dados complementares                    2005–2026
  EQ  — Equipamentos                            2005–2026
  SR  — Serviços especializados                 2005–2026
  LT  — Leitos                                  2005–2026
  HB  — Habilitações                            2007–2026
  EF  — Centros cirúrgicos e obstétricos        2007–2026
  EP  — Equipes de saúde                        2007–2026
  RC  — Regras contratuais                      2007–2026
  IN  — Incentivos                              2007–2026
  GM  — Gestão e metas                          2014–2026

Subtipos encerrados (ainda disponíveis no FTP):
  EE  — Equipamentos e produções                2007–2019
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import CNES as _CFG, UFS
from ..reader import ler as _ler

_BASE     = _CFG["ftp_base"]
_SUBTIPOS = _CFG["subtypes"]   # {tipo: (descricao, ano_min, ano_max)}


def _validar_subtipo(tipo: str) -> str:
    tipo = tipo.upper()
    if tipo not in _SUBTIPOS:
        raise ValueError(
            f"Subtipo inválido: '{tipo}'. "
            f"Disponíveis: {sorted(_SUBTIPOS)}"
        )
    return tipo


def _validar(tipo: str, uf: str, ano: int, mes: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    if not (1 <= mes <= 12):
        raise ValueError(f"Mês inválido: {mes}. Use 1–12.")
    _, ano_min, ano_max = _SUBTIPOS[tipo]
    if not (ano_min <= ano <= ano_max):
        raise ValueError(
            f"Ano {ano} fora do intervalo para o subtipo '{tipo}' "
            f"(disponível: {ano_min}–{ano_max})"
        )


def _ftp_dir(tipo: str) -> str:
    return f"{_BASE}/{tipo}"


def _nome(tipo: str, uf: str, ano: int, mes: int) -> str:
    return f"{tipo}{uf}{str(ano)[-2:]}{mes:02d}.dbc"


def _baixar_arquivo(tipo: str, nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_ftp_dir(tipo)}/{nome}"
    local   = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


def subtipos() -> dict[str, str]:
    """Retorna os subtipos disponíveis: {tipo: descrição}."""
    return {k: v[0] for k, v in _SUBTIPOS.items()}


def listar(uf: str | None = None, tipo: str = "ST") -> list[str]:
    """
    Lista arquivos disponíveis no FTP para o subtipo informado.
    Filtra por UF se informada. Subtipo padrão: ST (Estabelecimentos).
    """
    tipo     = _validar_subtipo(tipo)
    arquivos = _ftp.listar(_ftp_dir(tipo))
    if uf:
        filtro   = f"{tipo}{uf.upper()}"
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
    """
    Baixa {TYPE}{UF}{YY}{MM}.dbc para o cache local.
    Subtipo padrão: ST (Estabelecimentos).
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
    """Baixa (se necessário) e retorna os dados como DataFrame."""
    return _ler(baixar(uf, ano, mes, tipo=tipo, destino=destino, forcar=forcar))
