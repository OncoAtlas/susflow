"""
susflow/systems/sinasc.py
=========================
SINASC — Sistema de Informações sobre Nascidos Vivos.

Padrão de arquivo: DN{UF}{YYYY}.dbc   ex: DNSP2022.dbc
Granularidade:     anual / por UF
Cobertura:         1996 → 2022
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SINASC as _CFG, UFS

_DIR        = _CFG["ftp_dir"]
_ANO_MIN, _ANO_MAX = _CFG["year_range"]


def _validar(uf: str, ano: int) -> None:
    uf = uf.upper()
    if uf not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(f"Ano fora do intervalo disponível: {ano} (disponível: {_ANO_MIN}–{_ANO_MAX})")


def _nome_arquivo(uf: str, ano: int) -> str:
    return f"DN{uf.upper()}{ano}.dbc"


def _caminho_ftp(uf: str, ano: int) -> str:
    return f"{_DIR}/{_nome_arquivo(uf, ano)}"


def listar(uf: str | None = None) -> list[str]:
    """
    Lista arquivos disponíveis no FTP.
    Se `uf` for informada, filtra pelo prefixo da UF.
    """
    arquivos = _ftp.listar(_DIR)
    if uf:
        prefixo = f"DN{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]
    return arquivos


def baixar(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> Path:
    """
    Baixa o arquivo .dbc para o cache local (ou `destino` se informado).
    Usa cache se o arquivo já existir, a menos que `forcar=True`.
    """
    _validar(uf, ano)
    caminho = _caminho_ftp(uf, ano)
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def ler(uf: str, ano: int, destino: Path | None = None, forcar: bool = False) -> pd.DataFrame:
    """
    Baixa (se necessário) e retorna os dados como DataFrame.
    """
    from ..reader import ler as _ler
    arquivo = baixar(uf, ano, destino=destino, forcar=forcar)
    return _ler(arquivo)
