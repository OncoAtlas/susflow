"""
susflow/reader.py
=================
Read layer: convert local files (.dbc, .dbf, .zip) to DataFrame.
"""

import tempfile
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd
from dbfread import DBF
from pyreaddbc import dbc2dbf

_ENGINES = frozenset({"pandas", "polars", "pyarrow"})


class ReadError(Exception):
    """Failed to convert file to DataFrame."""


def read(
    file: Path, engine: str = "pandas", parquet: bool = False, force: bool = False
) -> Any:
    """
    Read a local file and return a DataFrame (or engine-specific table).
    Supports .dbc, .dbf and .zip (containing .dbc or .dbf).
    Columns always uppercased, strings decoded using latin-1.

    Args:
        engine: output type — "pandas" (default), "polars", or "pyarrow".
                Requires polars:  pip install susflow[polars]
                Requires pyarrow: pip install susflow[pyarrow]
        parquet: If True, a .parquet sidecar is written next to the source file on
                 first read and returned directly on subsequent calls (skipping
                 slow dbc2dbf). Pass force=True to rebuild the sidecar.
                 Requires pyarrow or fastparquet: pip install susflow[parquet]
                 (the sidecar is stored as pandas and converted to engine on load if needed).
    """
    if engine not in _ENGINES:
        raise ValueError(
            f"Unknown engine: '{engine}'. Valid options: {sorted(_ENGINES)}"
        )

    file = Path(file)

    if parquet:
        parquet_path = file.with_suffix(".parquet")
        if parquet_path.exists() and not force:
            df = pd.read_parquet(parquet_path)
            return _convert(df, engine)
        df = _read_source(file)
        df.to_parquet(parquet_path, index=False)
        return _convert(df, engine)

    return _convert(_read_source(file), engine)


def _read_source(file: Path) -> pd.DataFrame:
    suffix = file.suffix.lower()
    if suffix == ".dbc":
        return _read_dbc(file)
    if suffix == ".dbf":
        return _read_dbf(file)
    if suffix == ".zip":
        return _read_zip(file)
    raise ReadError(f"Unsupported format: {suffix}")


def _convert(df: pd.DataFrame, engine: str) -> Any:
    if engine == "pandas":
        return df
    if engine == "polars":
        try:
            import polars as pl
        except ImportError:
            raise ImportError(
                "engine='polars' requires polars. Install with: pip install susflow[polars]"
            ) from None
        return pl.from_pandas(df)
    if engine == "pyarrow":
        try:
            import pyarrow as pa
        except ImportError:
            raise ImportError(
                "engine='pyarrow' requires pyarrow. Install with: pip install susflow[pyarrow]"
            ) from None
        return pa.Table.from_pandas(df)


def _read_dbc(file: Path) -> pd.DataFrame:
    try:
        with tempfile.NamedTemporaryFile(suffix=".dbf", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            dbc2dbf(str(file), str(tmp_path))
            return _read_dbf(tmp_path)

        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    except ReadError:
        raise

    except Exception as e:
        raise ReadError(f"Failed to read .dbc: {file}") from e


def _read_dbf(file: Path) -> pd.DataFrame:
    try:
        table = DBF(str(file), encoding="latin-1", load=True)
        df = pd.DataFrame(iter(table))
        df.columns = df.columns.str.upper()
        return df

    except Exception as e:
        raise ReadError(f"Failed to read .dbf: {file}") from e


def _read_zip(file: Path) -> pd.DataFrame:
    try:
        with tempfile.TemporaryDirectory() as tmp:

            with zipfile.ZipFile(file) as zf:
                names = [n for n in zf.namelist() if not n.endswith("/")]

                if not names:
                    raise ReadError(f"Empty ZIP: {file}")

                zf.extractall(tmp)

            # read the first recognizable file inside the zip
            for name in names:
                extracted = Path(tmp) / name
                suffix = extracted.suffix.lower()
                if suffix in (".dbc", ".dbf"):
                    return _read_source(extracted)

        raise ReadError(f"No .dbc or .dbf found inside {file}")

    except ReadError:
        raise

    except Exception as e:
        raise ReadError(f"Failed to read .zip: {file}") from e
