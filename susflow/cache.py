"""
susflow/cache.py
================
Local cache resolution. Shared by all systems.
Default folder: ~/.susflow/cache/, mirroring the FTP structure.
"""

from pathlib import Path

_DEFAULT_CACHE = Path.home() / ".susflow" / "cache"


def local_path(ftp_path: str, root: Path | None = None) -> Path:
    """
    Return the local path corresponding to an FTP path.
    Example: /dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
     →  ~/.susflow/cache/dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc
    """
    root = Path(root) if root else _DEFAULT_CACHE
    # strip leading slash to avoid creating an absolute path when joining
    relative = ftp_path.lstrip("/")
    return root / relative


def exists(ftp_path: str, root: Path | None = None) -> bool:
    return local_path(ftp_path, root).exists()
