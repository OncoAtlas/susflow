"""
susflow/ftp.py
==============
Transport layer: all communication with the DATASUS FTP lives here.
"""

from ftplib import FTP, all_errors
from pathlib import Path

from .config import FTP_HOST

_TIMEOUT    = 30   # segundos
_TENTATIVAS = 3
_BACKOFF    = 2    # segundos entre tentativas


class FTPError(Exception):
    """DATASUS FTP communication error."""


class ArquivoNaoEncontradoError(FTPError):
    """File does not exist on the FTP."""


def _conectar() -> FTP:
    """Opens a clean FTP connection. Reconnecting per operation avoids the '200 Type set to A' bug."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21, timeout=_TIMEOUT)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def _tentar(fn, *args, **kwargs):
    """Executes fn with retries and backoff."""
    import time
    ultimo_erro = None
    for tentativa in range(_TENTATIVAS):
        try:
            return fn(*args, **kwargs)
        except all_errors as e:
            ultimo_erro = e
            if tentativa < _TENTATIVAS - 1:
                time.sleep(_BACKOFF)
    raise FTPError(f"Falha após {_TENTATIVAS} tentativas: {ultimo_erro}") from ultimo_erro


def listar(caminho: str) -> list[str]:
    """
    Lists file names in an FTP directory.
    Returns files only, not subdirectories.
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

def existe(caminho_ftp: str) -> bool:
    """
    Checks whether a file exists on the FTP using the SIZE command.
    It is much faster than trying to download or list the directory.
    """
    def _checar():
        ftp = _conectar()
        try:
            # SIZE returns the file size if it exists
            # If it does not exist, the server returns error 550
            ftp.voidcmd(f"SIZE {caminho_ftp}")
            return True
        except all_errors as e:
            if "550" in str(e):
                return False
            raise
        finally:
            ftp.quit()

    return _tentar(_checar)


def baixar(caminho_ftp: str, destino: Path) -> Path:
    """
    Downloads a file from the FTP to the local path `destino`.
    Creates the necessary directories. Returns the saved file path.
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
                    f"Arquivo não encontrado no FTP: {caminho_ftp}"
                ) from e
            raise
        finally:
            ftp.quit()
        return destino

    return _tentar(_baixar)