import ftplib
from pathlib import Path

import pytest

from susflow import ftp as _ftp


class FakeFTPGood:
    def __init__(self):
        self.closed = False

    def connect(self, *a, **k):
        pass

    def login(self):
        pass

    def set_pasv(self, b: bool):
        pass

    def retrlines(self, cmd, cb):
        cb("-rw-r--r-- 1 user group 123 Jan 01 00:00 file1.dbc")
        cb("<DIR> somefolder")

    def cwd(self, p):
        pass

    def retrbinary(self, cmd, writefn):
        writefn(b"hello")

    def quit(self):
        self.closed = True


def test__retry_retries_then_fails(monkeypatch):
    calls = {"n": 0}

    def bad():
        calls["n"] += 1
        raise ftplib.error_temp("421 Service not available")

    monkeypatch.setattr(_ftp, "time", type("T", (), {"sleep": lambda *_: None}))

    with pytest.raises(_ftp.FTPError):
        _ftp._retry(bad)
    assert calls["n"] == _ftp._RETRIES


def test_download_success(monkeypatch, tmp_path: Path):
    fake = FakeFTPGood()

    monkeypatch.setattr(_ftp, "_connect", lambda: fake)

    destination = tmp_path / "out.dbc"
    res = _ftp.download("/some/file.dbc", destination)
    assert res.exists()
    assert res.read_bytes() == b"hello"
