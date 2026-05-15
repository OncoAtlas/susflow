"""
susflow/cache.py
================
Local cache resolution. Shared by all systems.
Default folder: ~/.susflow/cache/, mirroring the FTP structure.
"""

from pathlib import Path

_CACHE_PADRAO = Path.home() / ".susflow" / "cache"


def caminho_local(caminho_ftp: str, raiz: Path | None = None) -> Path:
    """
    Returns the local path corresponding to an FTP path.
    Ex: /dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
     →  ~/.susflow/cache/dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
    """
    raiz = Path(raiz) if raiz else _CACHE_PADRAO
    # remove the leading slash to avoid creating an absolute path when joining
    relativo = caminho_ftp.lstrip("/")
    return raiz / relativo


def existe(caminho_ftp: str, raiz: Path | None = None) -> bool:
    return caminho_local(caminho_ftp, raiz).exists()
