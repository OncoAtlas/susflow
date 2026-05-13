"""
susflow/ftp.py
==============
Camada de transporte: toda comunicação com o FTP do DATASUS fica aqui.
"""

from ftplib import FTP, all_errors
from pathlib import Path

from .config import FTP_HOST

_TIMEOUT    = 30   # segundos
_TENTATIVAS = 3
_BACKOFF    = 2    # segundos entre tentativas


class FTPError(Exception):
    """Erro de comunicação com o FTP do DATASUS."""


class ArquivoNaoEncontradoError(FTPError):
    """Arquivo não existe no FTP."""


def _conectar() -> FTP:
    """Abre uma conexão FTP limpa. Reconectar por operação evita o bug '200 Type set to A'."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21, timeout=_TIMEOUT)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def _tentar(fn, *args, **kwargs):
    """Executa fn com retentativas e backoff."""
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
    Lista os nomes de arquivo em um diretório FTP.
    Retorna apenas arquivos (não subdiretórios).
    """
    def _listar():
        ftp = _conectar()
        try:
            itens: list[str] = []
            ftp.retrlines("LIST", itens.append)  # LIST no cwd após cwd()
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
    Baixa um arquivo do FTP para o caminho local `destino`.
    Cria os diretórios necessários. Retorna o path do arquivo salvo.
    Levanta ArquivoNaoEncontradoError se o arquivo não existir no FTP.
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
