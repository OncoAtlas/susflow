"""
susflow/systems/pni.py
======================
PNI — Programa Nacional de Imunizações.

Padrão de arquivo: DPNI{UF}{YY}.DBF
Granularidade:     anual / por UF
Cobertura:         1994–2019

O arquivo fica diretamente em DADOS/ (sem subdiretório):
  ex: /dissemin/publicos/PNI/DADOS/DPNISP02.DBF

Observações:
  - Formato .DBF puro (sem blast); lido com dbfread via reader.py.
  - O sufixo de ano usa 2 dígitos (94–19); anos 2000–2009 ficam
    como 00–09, portanto a normalização é feita com (ano % 100).
  - UF codificada com 2 letras maiúsculas (ex: SP, RJ, AM).
  - Cobertura termina em 2019; não há dados preliminares.
"""

from pathlib import Path

import pandas as pd

from .. import ftp as _ftp
from .. import cache as _cache
from ..config import PNI as _CFG, UFS
from ..reader import ler as _ler

_BASE       = _CFG["ftp_dir"]
_ANO_MIN, _ANO_MAX = _CFG["year_range"]

def _validar(uf: str, ano: int) -> None:
    if uf.upper() not in UFS:
        raise ValueError(f"UF inválida: '{uf}'. Valores aceitos: {UFS}")
    
    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(
            f"Ano {ano} fora do intervalo do PNI "
            f"(disponível: {_ANO_MIN}–{_ANO_MAX})"
        )

def _nome(uf: str, ano: int) -> str:
    return f"DPNI{uf.upper()}{ano % 100:02d}.DBF"

def _baixar_arquivo(nome: str, destino: Path | None, forcar: bool) -> Path:
    caminho = f"{_BASE}/{nome}"
    local   = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local
    
    return _ftp.baixar(caminho, local)

def listar(uf: str | None = None) -> list[str]:
    """
    Lista arquivos disponíveis no FTP para o PNI.
    Filtra por UF se informada.
    """
    arquivos = _ftp.listar(_BASE)
    if uf:
        filtro   = f"DPNI{uf.upper()}"
        arquivos = [a for a in arquivos if a.upper().startswith(filtro)]
    return arquivos

def baixar(
    uf: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
) -> Path:
    """
    Baixa DPNI{UF}{YY}.DBF para o cache local e retorna o path.

    Parâmetros
    ----------
    uf      : sigla da UF (ex: 'SP')
    ano     : ano com 4 dígitos (ex: 2010)
    destino : pasta de destino; usa o cache padrão se None
    forcar  : se True, baixa mesmo que o arquivo já exista no cache
    """
    _validar(uf, ano)
    return _baixar_arquivo(_nome(uf, ano), destino, forcar)

def ler(uf: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
) -> pd.DataFrame:
    """Baixa (se necessário) e retorna os dados como DataFrame."""
    return _ler(baixar(uf, ano, destino=destino, forcar=forcar))