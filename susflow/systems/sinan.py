"""
susflow/systems/sinan.py
========================
SINAN — Notifiable Diseases Information System.

Disease data:

    final        → {DISEASE}BR{YY}.dbc  in DADOS/FINAIS/   e.g. DENGBR23.dbc
    preliminary  → {DISEASE}BR{YY}.dbc  in DADOS/PRELIM/   (use flag `preliminar=True`)

Auxiliary files (download only, not read as DataFrame):

    docs         → layouts, variable dictionary and technical notes per disease
"""

from pathlib import Path
from typing import Any

from .. import cache as _cache
from .. import ftp as _ftp
from ..config import SINAN as _CFG
from ..reader import ler as _ler

_DIR_FINAL = _CFG["ftp_dir"]
_DIR_PRELIM = _CFG["ftp_dir_prelim"]
_CFG_DOC = _CFG["docs"]
_DOENCAS = {k.upper(): v for k, v in _CFG["diseases"].items()}
_ANO_MIN = 2000  # menor ano observado nos arquivos do FTP
_ANO_MAX = 2024


def _validar(doenca: str, ano: int) -> str:
    doenca = doenca.upper()
    if doenca not in _DOENCAS:
        disponiveis = ", ".join(sorted(_DOENCAS))
        raise ValueError(f"Invalid disease code: '{doenca}'.\nAvailable: {disponiveis}")

    if not (_ANO_MIN <= ano <= _ANO_MAX):
        raise ValueError(f"Year out of range: {ano} (available: {_ANO_MIN}–{_ANO_MAX})")

    return doenca


def _nome_arquivo(doenca: str, ano: int) -> str:
    return f"{doenca}BR{str(ano)[-2:]}.dbc"


def _baixar_arquivo(
    ftp_dir: str, nome: str, destino: Path | None, forcar: bool
) -> Path:
    caminho = f"{ftp_dir}/{nome}"
    local = _cache.caminho_local(caminho, destino)
    if local.exists() and not forcar:
        return local
    return _ftp.baixar(caminho, local)


def doencas() -> dict[str, str]:
    """Return the dictionary {code: description} of all available diseases."""
    return dict(_DOENCAS)


def listar(doenca: str | None = None, preliminar: bool = False) -> list[str]:
    """
    List files available on the FTP.
    If `doenca` is provided, filter by disease code.
    Use `preliminar=True` to list preliminary data.
    """
    diretorio = _DIR_PRELIM if preliminar else _DIR_FINAL
    arquivos = _ftp.listar(diretorio)

    if doenca:
        prefixo = doenca.upper()
        arquivos = [a for a in arquivos if a.upper().startswith(prefixo)]

    return arquivos


def baixar(
    doenca: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
    preliminar: bool = False,
) -> Path:
    """
    Download `{DISEASE}BR{YY}.dbc` to local cache.
    Use `preliminar=True` to download preliminary data.
    """
    doenca = _validar(doenca, ano)
    dirftp = _DIR_PRELIM if preliminar else _DIR_FINAL
    caminho = f"{dirftp}/{_nome_arquivo(doenca, ano)}"
    local = _cache.caminho_local(caminho, destino)

    if local.exists() and not forcar:
        return local

    return _ftp.baixar(caminho, local)


def ler(
    doenca: str,
    ano: int,
    destino: Path | None = None,
    forcar: bool = False,
    preliminar: bool = False,
    engine: str = "pandas",
) -> Any:
    """
    Download (if needed) and return the data as a DataFrame.
    """
    return _ler(
        baixar(doenca, ano, destino=destino, forcar=forcar, preliminar=preliminar),
        engine=engine,
    )


# ---------------------------------------------------------------------------
# Technical documentation — download only
# ---------------------------------------------------------------------------


def listar_docs() -> dict[str, str]:
    """Return available technical documents for download: {name: description}."""
    return dict(_CFG_DOC["arquivos"])


def baixar_docs(
    arquivo: str | None = None,
    destino: Path | None = None,
    forcar: bool = False,
) -> "Path | list[Path]":
    """Download SINAN technical documents (layouts, variable dictionary, technical notes).

    Note: the FTP path for this directory has not been fully confirmed.
    If download fails, use `mapear_ftp.py` to locate the correct directory.

    - If `arquivo` is provided, download only that file.
    - If omitted, download all available files.
    """
    disponiveis = _CFG_DOC["arquivos"]
    ftp_dir = _CFG_DOC["ftp_dir"]

    if arquivo:
        if arquivo not in disponiveis:
            raise ValueError(
                f"Document not available: '{arquivo}'.\nAvailable: {list(disponiveis)}"
            )
        return _baixar_arquivo(ftp_dir, arquivo, destino, forcar)

    return [_baixar_arquivo(ftp_dir, nome, destino, forcar) for nome in disponiveis]
