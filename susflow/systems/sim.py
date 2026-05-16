"""
susflow/systems/sim.py
======================
SIM — Sistema de Informações sobre Mortalidade.

Subtipos de dados:

  uf       → DO{UF}{YYYY}.dbc  em CID10/DORES/   ex: DOSP2023.dbc
  especial → DO{TIPO}{YY}.dbc  em CID10/DOFET/   ex: DOEXT24.dbc
             tipos: EXT (causas externas), FET (fetal), INF (infantil), MAT (materno)

Arquivos auxiliares (apenas download, sem leitura como DataFrame):

  docs     → layouts, dicionário de variáveis e estrutura dos arquivos
  tab      → dados agregados tabulados por CID-10
  tabelas  → tabelas de apoio: CID-10, municípios, ocupações, países, UFs
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SIM as _CFG, UFS
from ..reader import ler as _ler

_DIR_UF      = _CFG["uf"]["ftp_dir"]
_DIR_ESP     = _CFG["special"]["ftp_dir"]
_TIPOS_ESP   = set(_CFG["special"]["types"].keys())
_ANO_MIN_UF,  _ANO_MAX_UF  = _CFG["uf"]["year_range"]
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
    arquivos = _ftp.listar(_DIR_UF)
    if uf:
        prefixo = f"DO{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """Baixa DO{UF}{YYYY}.dbc para o cache local."""
    _validar_uf(uf, ano)
    return _baixar_arquivo(_DIR_UF, f"DO{uf.upper()}{ano}.dbc", destino, forcar)


def ler(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados por UF como DataFrame."""
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
    nome = f"DO{tipo.upper()}{str(ano)[-2:]}.dbc"
    return _baixar_arquivo(_DIR_ESP, nome, destino, forcar)


def ler_especial(tipo: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """Baixa (se necessário) e retorna dados especiais como DataFrame."""
    return _ler(baixar_especial(tipo, ano, destino=destino, forcar=forcar))


# ---------------------------------------------------------------------------
# Arquivos auxiliares — apenas download
# ---------------------------------------------------------------------------

def listar_docs() -> dict[str, str]:
    """Retorna os documentos técnicos disponíveis para download: {nome: descrição}."""
    return dict(_CFG["docs"]["arquivos"])


def listar_tabelas() -> dict[str, str]:
    """Retorna as tabelas de apoio disponíveis para download: {nome: descrição}."""
    return dict(_CFG["tabelas"]["arquivos"])


def listar_tab() -> dict[str, str]:
    """Retorna os dados agregados tabulados disponíveis para download: {nome: descrição}."""
    return dict(_CFG["tab"]["arquivos"])


def baixar_docs(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """
    Baixa documentos técnicos do SIM (layouts, estrutura, dicionário).

    - Se `arquivo` for informado, baixa apenas aquele arquivo.
    - Se omitido, baixa todos os documentos disponíveis.

    Retorna o Path do arquivo (ou lista de Paths se baixar todos).
    """
    disponiveis = _CFG["docs"]["arquivos"]
    ftp_dir     = _CFG["docs"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(f"Documento não disponível: '{arquivo}'. Disponíveis: {list(disponiveis)}")
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]


def baixar_tabelas(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """
    Baixa tabelas de apoio do SIM (CID-10, municípios, ocupações, países, UFs).

    - Se `arquivo` for informado, baixa apenas aquele arquivo.
    - Se omitido, baixa todas as tabelas disponíveis.
    """
    disponiveis = _CFG["tabelas"]["arquivos"]
    ftp_dir     = _CFG["tabelas"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(f"Tabela não disponível: '{arquivo}'. Disponíveis: {list(disponiveis)}")
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]


def baixar_tab(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path | list[Path]:
    """
    Baixa dados agregados tabulados por CID-10.

    - Se `arquivo` for informado, baixa apenas aquele arquivo.
    - Se omitido, baixa todos os disponíveis.
    """
    disponiveis = _CFG["tab"]["arquivos"]
    ftp_dir     = _CFG["tab"]["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(f"Arquivo não disponível: '{arquivo}'. Disponíveis: {list(disponiveis)}")
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]
