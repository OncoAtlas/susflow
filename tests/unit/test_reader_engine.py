from pathlib import Path

import pandas as pd
import pytest

from susflow import reader


def _make_df():
    return pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})


def test_read_invalid_engine(tmp_path: Path, monkeypatch):
    f = tmp_path / "f.dbf"
    f.write_text("x")
    monkeypatch.setattr(reader, "_read_source", lambda p: _make_df())
    with pytest.raises(ValueError, match="Unknown engine"):
        reader.read(f, engine="csv")


def test_read_pandas_engine(tmp_path: Path, monkeypatch):
    f = tmp_path / "f.dbf"
    f.write_text("x")
    expected = _make_df()
    monkeypatch.setattr(reader, "_read_source", lambda p: expected)
    result = reader.read(f, engine="pandas")
    assert isinstance(result, pd.DataFrame)
    assert result.equals(expected)


def test_read_polars_engine(tmp_path: Path, monkeypatch):
    pl = pytest.importorskip("polars")
    f = tmp_path / "f.dbf"
    f.write_text("x")
    monkeypatch.setattr(reader, "_read_source", lambda p: _make_df())
    result = reader.read(f, engine="polars")
    assert isinstance(result, pl.DataFrame)


def test_read_pyarrow_engine(tmp_path: Path, monkeypatch):
    pa = pytest.importorskip("pyarrow")
    f = tmp_path / "f.dbf"
    f.write_text("x")
    monkeypatch.setattr(reader, "_read_source", lambda p: _make_df())
    result = reader.read(f, engine="pyarrow")
    assert isinstance(result, pa.Table)


def test_read_polars_missing_dep(tmp_path: Path, monkeypatch):
    f = tmp_path / "f.dbf"
    f.write_text("x")
    monkeypatch.setattr(reader, "_read_source", lambda p: _make_df())

    import builtins
    real_import = builtins.__import__

    def block_polars(name, *args, **kwargs):
        if name == "polars":
            raise ImportError("no polars")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", block_polars)
    with pytest.raises(ImportError, match="susflow\\[polars\\]"):
        reader.read(f, engine="polars")


def test_read_pyarrow_missing_dep(tmp_path: Path, monkeypatch):
    f = tmp_path / "f.dbf"
    f.write_text("x")
    monkeypatch.setattr(reader, "_read_source", lambda p: _make_df())

    import builtins
    real_import = builtins.__import__

    def block_pyarrow(name, *args, **kwargs):
        if name == "pyarrow":
            raise ImportError("no pyarrow")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", block_pyarrow)
    with pytest.raises(ImportError, match="susflow\\[pyarrow\\]"):
        reader.read(f, engine="pyarrow")


def test_convert_pandas_returns_same_object():
    df = _make_df()
    assert reader._convert(df, "pandas") is df
