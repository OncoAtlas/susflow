"""
susflow/ftp.py
==============
Transport layer: all communication with the DATASUS FTP happens here.
"""

import time
from ftplib import FTP, all_errors
from pathlib import Path

from .config import FTP_HOST

_TIMEOUT = 30  # seconds
_RETRIES = 3
_BACKOFF = 2  # seconds between attempts


class FTPError(Exception):
    """Communication error with the DATASUS FTP."""


class FileNotFoundOnFTPError(FTPError):
    """File does not exist on the FTP."""


def _connect() -> FTP:
    """Open a fresh FTP connection. Reconnecting per operation avoids '200 Type set to A' bug."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21, timeout=_TIMEOUT)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def _retry(fn, *args, **kwargs):
    """Run `fn` with retries and backoff."""
    last_error = None
    for attempt in range(_RETRIES):
        try:
            return fn(*args, **kwargs)

        except all_errors as e:
            last_error = e
            if attempt < _RETRIES - 1:
                time.sleep(_BACKOFF)

    raise FTPError(f"Failed after {_RETRIES} attempts: {last_error}") from last_error


def list_files(path: str) -> list[str]:
    """
    List file names in an FTP directory.
    Returns files only (no subdirectories).
    """

    def _list():
        ftp = _connect()

        try:
            entries: list[str] = []
            ftp.retrlines("LIST", entries.append)
            ftp.cwd(path)
            entries.clear()
            ftp.retrlines("LIST", entries.append)

            files = []
            for line in entries:
                if "<DIR>" in line:
                    continue
                name = line.split()[-1]
                files.append(name)

            return files

        finally:
            ftp.quit()

    return _retry(_list)


def download(ftp_path: str, destination: Path) -> Path:
    """
    Download a file from the FTP to local path `destination`.
    Creates necessary directories. Returns the saved file path.
    Raises FileNotFoundOnFTPError if the file does not exist on the FTP.
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    def _download():
        ftp = _connect()

        try:
            with open(destination, "wb") as f:
                ftp.retrbinary(f"RETR {ftp_path}", f.write)

        except all_errors as e:
            if destination.exists():
                destination.unlink()

            if "550" in str(e):
                raise FileNotFoundOnFTPError(
                    f"File not found on FTP: {ftp_path}"
                ) from e
            raise

        finally:
            ftp.quit()

        return destination

    return _retry(_download)
