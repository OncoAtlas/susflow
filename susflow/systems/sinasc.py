"""
susflow/systems/sinasc.py
=========================
SINASC — Sistema de Informações sobre Nascidos Vivos.

Subtipos de dados:

  uf       → DN{UF}{YYYY}.dbc  em NOV/DNRES/   ex: DNSP2022.dbc
             por UF, anual, 1996–2022

  nacional → DNBR{YYYY}.dbc   em NOV/DNRES/   ex: DNBR2015.dbc
             agregado nacional, série incompleta (2014–2017 confirmados)

  excecoes → DNEX{YYYY}.dbc   em NOV/DNRES/   ex: DNEX2021.dbc
             arquivos pontuais com registros suplementares

Arquivos auxiliares (apenas download, sem leitura como DataFrame):

  docs     → documentação técnica do sistema (caminho FTP a confirmar)
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SINASC as _CFG, UFS
from ..reader import ler as _ler

_CFG_UF  = _CFG["uf"]
_CFG_NAC = _CFG["nacional"]
_CFG_EXC = _CFG["excecoes"]
_CFG_DOC = _CFG["docs"]

_ANO_MIN_UF,  _ANO_MAX_UF  = _CFG_UF["year_range"]
_ANO_MIN_NAC, _ANO_MAX_NAC = _CFG_NAC["year_range"]


def _validar_uf(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    if not (_ANO_MIN_UF <= ano <= _ANO_MAX_UF):
        raise ValueError(f"Ano fora do intervalo: {ano} (disponível: {_ANO_MIN_UF}–{_ANO_MAX_UF})")

def _validar_nacional(ano: int) -> None:
    if not (_ANO_MIN_NAC <= ano <= _ANO_MAX_NAC):
        raise ValueError(
            f"Ano fora do intervalo disponível para o agregado nacional: {ano} "
            f"(confirmado: {_ANO_MIN_NAC}–{_ANO_MAX_NAC})"
        )

def _baixar_arquivo(ftp_dir: str, nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{ftp_dir}/{nome}"
    local   = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)

# ---------------------------------------------------------------------------
# Por UF
# ---------------------------------------------------------------------------

def listar(uf: str | None = None) -> list[str]:
    """Lista arquivos por UF disponíveis no FTP. Filtra por UF se informada."""
    arquivos = _ftp.listar(_CFG_UF["ftp_dir"])
    arquivos = [a for a in arquivos if a.upper().startswith("DN") and not a.upper().startswith(("DNBR", "DNEX"))]
    if uf:
        prefixo = f"DN{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos

def baixar(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DN{UF}{YYYY}.dbc para o cache local."""
    _validar_uf(uf, ano)
    return _baixar_arquivo(_CFG_UF["ftp_dir"], f"DN{uf.upper()}{ano}.dbc", destino, forcar)

def ler(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados por UF como DataFrame."""
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar))

# ---------------------------------------------------------------------------
# Agregado nacional (DNBR — série incompleta: 2014–2017)
# ---------------------------------------------------------------------------

def listar_nacional() -> list[str]:
    """Lista os arquivos do agregado nacional disponíveis no FTP."""
    arquivos = _ftp.listar(_CFG_NAC["ftp_dir"])
    return [a for a in arquivos if a.upper().startswith("DNBR")]

def baixar_nacional(ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DNBR{YYYY}.dbc para o cache local."""
    _validar_nacional(ano)
    return _baixar_arquivo(_CFG_NAC["ftp_dir"], f"DNBR{ano}.dbc", destino, forcar)

def ler_nacional(ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna o agregado nacional como DataFrame."""
    return _ler(baixar_nacional(ano, destino=destino, forcar=forcar))

# ---------------------------------------------------------------------------
# Arquivos de exceção/suplementares (DNEX)
# ---------------------------------------------------------------------------

def listar_excecoes() -> list[str]:
    """Lista os arquivos de exceção disponíveis no FTP."""
    arquivos = _ftp.listar(_CFG_EXC["ftp_dir"])
    return [a for a in arquivos if a.upper().startswith("DNEX")]


def baixar_excecao(ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DNEX{YYYY}.dbc para o cache local."""
    return _baixar_arquivo(_CFG_EXC["ftp_dir"], f"DNEX{ano}.dbc", destino, forcar)


def ler_excecao(ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna o arquivo de exceção como DataFrame."""
    return _ler(baixar_excecao(ano, destino=destino, forcar=forcar))

# ---------------------------------------------------------------------------
# Documentação técnica — apenas download
# ---------------------------------------------------------------------------

def listar_docs() -> dict[str, str]:
    """Retorna os documentos técnicos disponíveis para download: {nome: descrição}."""
    return dict(_CFG_DOC["arquivos"])

def baixar_docs(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> "Path | list[Path]":
    """
    Baixa documentos técnicos do SINASC.

    Atenção: o caminho FTP deste diretório ainda não foi confirmado.
    Se o download falhar, use mapear_ftp.py para localizar o diretório correto.

    - Se `arquivo` for informado, baixa apenas aquele arquivo.
    - Se omitido, baixa todos os disponíveis.
    """
    disponiveis = _CFG_DOC["arquivos"]
    ftp_dir     = _CFG_DOC["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(f"Documento não disponível: '{arquivo}'. Disponíveis: {list(disponiveis)}")
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]
