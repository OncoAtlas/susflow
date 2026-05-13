"""
susflow/systems/sinan.py
========================
SINAN — Sistema de Informações de Agravos de Notificação.

Padrão de arquivo: {DOENÇA}BR{YY}.dbc   ex: DENGBR23.dbc
Granularidade:     anual / nacional (BR)
Dados finais:      /dissemin/publicos/SINAN/DADOS/FINAIS/
Dados preliminares:/dissemin/publicos/SINAN/DADOS/PRELIM/
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import SINAN as _CFG
from ..reader import ler as _ler

_DIR_FINAL  = _CFG["ftp_dir"]
_DIR_PRELIM = _CFG["ftp_dir_prelim"]
_DOENCAS    = {k.upper(): v for k, v in _CFG["diseases"].items()}
_ANO_MIN    = 2001   # menor ano observado nos arquivos do FTP
_ANO_MAX    = 2024

def _validar(doenca: str, ano: int) -> str:
    doenca = doenca.upper()
    if doenca not in _DOENCAS:
        disponiveis = ", ".join(sorted(_DOENCAS))
        raise ValueError(f"Doença inválida: '{doenca}'.\nDisponíveis: {disponiveis}")
    
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(f"Ano fora do intervalo: {ano} (disponível: {_ANO_MIN}–{_ANO_MAX})")
    
    return doenca


def _nome_arquivo(doenca: str, ano: int) -> str:
    return f"{doenca}BR{str(ano)[-2:]}.dbc"

def doencas() -> dict[str, str]:
    """Retorna o dicionário {código: descrição} de todas as doenças disponíveis."""
    return dict(_DOENCAS)

def listar(doenca: str | None = None, preliminar: bool = False) -> list[str]:
    """
    Lista arquivos disponíveis no FTP.
    Se `doenca` for informada, filtra pelo código.
    Use `preliminar=True` para listar dados preliminares.
    """
    diretorio = _DIR_PRELIM if preliminar else _DIR_FINAL
    arquivos  = _ftp.listar(diretorio)
    
    if doenca:
        prefixo = doenca.upper()
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]

    return arquivos


def baixar(doenca: str, ano: int, destino: Path | None = None,
           forcar: bool = False, preliminar: bool = False) -> Path:
    """
    Baixa {DOENÇA}BR{YY}.dbc para o cache local.
    Use `preliminar=True` para baixar dados preliminares.
    """
    doenca  = _validar(doenca, ano)
    dirftp  = _DIR_PRELIM if preliminar else _DIR_FINAL
    caminho = f"{dirftp}/{_nome_arquivo(doenca, ano)}"
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def ler(doenca: str, ano: int, destino: Path | None = None,
        forcar: bool = False, preliminar: bool = False) -> pd.DataFrame:
    """
    Baixa (se necessário) e retorna os dados como DataFrame.
    """
    return _ler(baixar(doenca, ano, destino=destino, forcar=forcar, preliminar=preliminar))
