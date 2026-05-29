from pathlib import Path

import pandas as pd
import pytest

from susflow import reader
from susflow.reader import ReadError


def test__read_dbc_uses_dbc2dbf_and_calls_read_dbf(tmp_path: Path, monkeypatch):
    dbc_file = tmp_path / "sample.dbc"
    dbc_file.write_text("dummy")

    called = {}

    def fake_dbc2dbf(src, dst):
        called["src"] = src
        called["dst"] = dst

    expected = pd.DataFrame({"A": [1]})

    monkeypatch.setattr(reader, "dbc2dbf", fake_dbc2dbf)
    monkeypatch.setattr(reader, "_read_dbf", lambda p: expected)

    df = reader._read_dbc(dbc_file)
    assert df.equals(expected)
    assert called["src"].endswith("sample.dbc")
    assert called["dst"].endswith(".dbf")


def test__read_dbf_returns_dataframe_and_uppercases_columns(monkeypatch, tmp_path: Path):
    class FakeDBF:
        def __init__(self, path, encoding=None, load=False):
            self._rows = [{"col": "x", "num": 1}]

        def __iter__(self):
            return iter(self._rows)

    monkeypatch.setattr(reader, "DBF", FakeDBF)

    p = tmp_path / "dummy.dbf"
    p.write_text("x")

    df = reader._read_dbf(p)
    assert list(df.columns) == ["COL", "NUM"]
    assert df.iloc[0]["COL"] == "x"


def test__read_dbf_raises_readerror_on_failure(monkeypatch, tmp_path: Path):
    def bad_dbf(path, encoding=None, load=False):
        raise RuntimeError("boom")

    monkeypatch.setattr(reader, "DBF", bad_dbf)
    with pytest.raises(ReadError):
        reader._read_dbf(tmp_path / "nope.dbf")
