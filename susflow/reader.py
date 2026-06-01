"""
susflow/reader.py
=================
Read layer: convert local files (.dbc, .dbf, .zip) to DataFrame.
"""

import tempfile
import zipfile
from pathlib import Path

import pandas as pd
from dbfread import DBF
from pyreaddbc import dbc2dbf


class ReadError(Exception):
    """Failed to convert file to DataFrame."""


def read(file: Path) -> pd.DataFrame:
    """
    Read a local file and return a DataFrame.
    Supports .dbc, .dbf and .zip (containing .dbc or .dbf).
    Columns always uppercased, strings decoded using latin-1.
    """
    file = Path(file)
    suffix = file.suffix.lower()

    if suffix == ".dbc":
        return _read_dbc(file)

    if suffix == ".dbf":
        return _read_dbf(file)

    if suffix == ".zip":
        return _read_zip(file)

    raise ReadError(f"Unsupported format: {suffix}")


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
                    return read(extracted)

        raise ReadError(f"No .dbc or .dbf found inside {file}")

    except ReadError:
        raise

    except Exception as e:
        raise ReadError(f"Failed to read .zip: {file}") from e
