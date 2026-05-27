"""
susflow/ftp.py
==============
Transport layer: all communication with the DATASUS FTP happens here.
"""

import time
from ftplib import FTP, all_errors
from pathlib import Path

from .config import FTP_HOST

_TIMEOUT = 30  # segundos
_TENTATIVAS = 3
_BACKOFF = 2  # segundos entre tentativas


class FTPError(Exception):
    """Communication error with the DATASUS FTP."""


class ArquivoNaoEncontradoError(FTPError):
    """File does not exist on the FTP."""


def _conectar() -> FTP:
    """Open a fresh FTP connection. Reconnecting per operation avoids '200 Type set to A' bug."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21, timeout=_TIMEOUT)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def _tentar(fn, *args, **kwargs):
    """Run `fn` with retries and backoff."""
    ultimo_erro = None
    for tentativa in range(_TENTATIVAS):
        try:
            return fn(*args, **kwargs)

        except all_errors as e:
            ultimo_erro = e
            if tentativa < _TENTATIVAS - 1:
                time.sleep(_BACKOFF)

    raise FTPError(
        f"Failed after {_TENTATIVAS} attempts: {ultimo_erro}"
    ) from ultimo_erro


def listar(caminho: str) -> list[str]:
    """
    List file names in an FTP directory.
    Returns files only (no subdirectories).
    """

    def _listar():
        ftp = _conectar()

        try:
            itens: list[str] = []
            ftp.retrlines("LIST", itens.append)  # LIST in cwd after cwd()
            ftp.cwd(caminho)
            itens.clear()
            ftp.retrlines("LIST", itens.append)

            arquivos = []
            for linha in itens:
                if "<DIR>" in linha:
                    continue

                nome = linha.split()[-1]
                arquivos.append(nome)

            return arquivos

        finally:
            ftp.quit()

    return _tentar(_listar)


def baixar(caminho_ftp: str, destino: Path) -> Path:
    """
    Download a file from the FTP to local path `destino`.
    Creates necessary directories. Returns the saved file path.
    Raises ArquivoNaoEncontradoError if the file does not exist on the FTP.
    """
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    def _baixar():
        ftp = _conectar()

        try:
            with open(destino, "wb") as f:
                ftp.retrbinary(f"RETR {caminho_ftp}", f.write)

        except all_errors as e:
            if destino.exists():
                destino.unlink()

            if "550" in str(e):
                raise ArquivoNaoEncontradoError(
                    f"File not found on FTP: {caminho_ftp}"
                ) from e
            raise

        finally:
            ftp.quit()

        return destino

    return _tentar(_baixar)
