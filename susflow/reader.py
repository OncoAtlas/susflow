"""
susflow/reader.py
=================
Read layer: convert local files (.dbc, .dbf, .zip) to DataFrame.
"""

import tempfile
import zipfile

from pyreaddbc import dbc2dbf
from pathlib import Path
from dbfread import DBF

import pandas as pd


class LeituraError(Exception):
    """Failed to convert file to DataFrame."""

def ler(arquivo: Path) -> pd.DataFrame:
    """
    Read a local file and return a DataFrame.
    Supports .dbc, .dbf and .zip (containing .dbc or .dbf).
    Columns always uppercased, strings decoded using latin-1.
    """
    arquivo = Path(arquivo)
    sufixo  = arquivo.suffix.lower()

    if sufixo == ".dbc":
        return _ler_dbc(arquivo)
    
    if sufixo == ".dbf":
        return _ler_dbf(arquivo)
    
    if sufixo == ".zip":
        return _ler_zip(arquivo)

    raise LeituraError(f"Unsupported format: {sufixo}")


def _ler_dbc(arquivo: Path) -> pd.DataFrame:
    try:
        with tempfile.NamedTemporaryFile(suffix=".dbf", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            dbc2dbf(str(arquivo), str(tmp_path))
            return _ler_dbf(tmp_path)
        
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    except LeituraError:
        raise

    except Exception as e:
        raise LeituraError(f"Failed to read .dbc: {arquivo}") from e


def _ler_dbf(arquivo: Path) -> pd.DataFrame:
    try:
        tabela = DBF(str(arquivo), encoding="latin-1", load=True)
        df = pd.DataFrame(iter(tabela))
        df.columns = df.columns.str.upper()
        return df
    
    except Exception as e:
        raise LeituraError(f"Failed to read .dbf: {arquivo}") from e


def _ler_zip(arquivo: Path) -> pd.DataFrame:
    try:
        with tempfile.TemporaryDirectory() as tmp:
            
            with zipfile.ZipFile(arquivo) as zf:
                nomes = [n for n in zf.namelist() if not n.endswith("/")]
                
                if not nomes:
                    raise LeituraError(f"Empty ZIP: {arquivo}")
                
                zf.extractall(tmp)

            # read the first recognizable file inside the zip
            for nome in nomes:
                extraido = Path(tmp) / nome
                sufixo   = extraido.suffix.lower()
                if sufixo in (".dbc", ".dbf"):
                    return ler(extraido)

        raise LeituraError(f"No .dbc or .dbf found inside {arquivo}")
    
    except LeituraError:
        raise

    except Exception as e:
        raise LeituraError(f"Failed to read .zip: {arquivo}") from e