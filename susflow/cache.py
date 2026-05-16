"""
susflow/cache.py
================
Resolução de cache local. Compartilhado por todos os sistemas.
Pasta padrão: ~/.susflow/cache/, espelhando a estrutura do FTP.
"""

from pathlib import Path

_CACHE_PADRAO = Path.home() / ".susflow" / "cache"


def caminho_local(caminho_ftp: str, raiz: Path | None = None) -> Path:
    """
    Retorna o path local correspondente a um caminho FTP.
    Ex: /dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
     →  ~/.susflow/cache/dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
    """
    raiz = Path(raiz) if raiz else _CACHE_PADRAO
    # remove a barra inicial para não criar path absoluto ao fazer /
    relativo = caminho_ftp.lstrip("/")
    return raiz / relativo


def existe(caminho_ftp: str, raiz: Path | None = None) -> bool:
    return caminho_local(caminho_ftp, raiz).exists()
