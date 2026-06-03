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


def test__read_dbf_returns_dataframe_and_uppercases_columns(
    monkeypatch, tmp_path: Path
):
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


# ---------------------------------------------------------------------------
# Parquet cache
# ---------------------------------------------------------------------------

_SAMPLE = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})


def _make_dbf(tmp_path: Path) -> Path:
    p = tmp_path / "sample.dbf"
    p.write_text("dummy")
    return p


def test_read_parquet_writes_sidecar_on_first_call(monkeypatch, tmp_path: Path):
    src = _make_dbf(tmp_path)
    monkeypatch.setattr(reader, "_read_source", lambda _: _SAMPLE)

    result = reader.read(src, parquet=True)
    parquet_path = src.with_suffix(".parquet")

    assert result.equals(_SAMPLE)
    assert parquet_path.exists()


def test_read_parquet_reads_sidecar_on_second_call(monkeypatch, tmp_path: Path):
    src = _make_dbf(tmp_path)
    call_count = {"n": 0}

    def counting_source(_):
        call_count["n"] += 1
        return _SAMPLE

    monkeypatch.setattr(reader, "_read_source", counting_source)

    reader.read(src, parquet=True)
    reader.read(src, parquet=True)

    assert call_count["n"] == 1


def test_read_parquet_force_rebuilds_sidecar(monkeypatch, tmp_path: Path):
    src = _make_dbf(tmp_path)
    call_count = {"n": 0}

    def counting_source(_):
        call_count["n"] += 1
        return _SAMPLE

    monkeypatch.setattr(reader, "_read_source", counting_source)

    reader.read(src, parquet=True)
    reader.read(src, parquet=True, force=True)

    assert call_count["n"] == 2


def test_read_without_parquet_does_not_create_sidecar(monkeypatch, tmp_path: Path):
    src = _make_dbf(tmp_path)
    monkeypatch.setattr(reader, "_read_source", lambda _: _SAMPLE)

    reader.read(src)

    assert not src.with_suffix(".parquet").exists()
