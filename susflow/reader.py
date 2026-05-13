"""
susflow/reader.py
=================
Camada de leitura: converte arquivos locais (.dbc, .dbf, .zip) em DataFrame.
"""

import tempfile
import zipfile
from pathlib import Path

import pandas as pd


class LeituraError(Exception):
    """Falha ao converter arquivo para DataFrame."""


def ler(arquivo: Path) -> pd.DataFrame:
    """
    Lê um arquivo local e retorna um DataFrame.
    Suporta .dbc, .dbf e .zip (que contenha .dbc ou .dbf).
    Colunas sempre em maiúsculo, strings decodificadas em latin-1.
    """
    arquivo = Path(arquivo)
    sufixo  = arquivo.suffix.lower()

    if sufixo == ".dbc":
        return _ler_dbc(arquivo)
    if sufixo == ".dbf":
        return _ler_dbf(arquivo)
    if sufixo == ".zip":
        return _ler_zip(arquivo)

    raise LeituraError(f"Formato não suportado: {sufixo}")


def _ler_dbc(arquivo: Path) -> pd.DataFrame:
    try:
        import tempfile
        from pyreaddbc import dbc2dbf
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
        raise LeituraError(f"Falha ao ler .dbc: {arquivo}") from e


def _ler_dbf(arquivo: Path) -> pd.DataFrame:
    try:
        from dbfread import DBF
        tabela = DBF(str(arquivo), encoding="latin-1", load=True)
        df = pd.DataFrame(iter(tabela))
        df.columns = df.columns.str.upper()
        return df
    except Exception as e:
        raise LeituraError(f"Falha ao ler .dbf: {arquivo}") from e


def _ler_zip(arquivo: Path) -> pd.DataFrame:
    try:
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(arquivo) as zf:
                nomes = [n for n in zf.namelist() if not n.endswith("/")]
                if not nomes:
                    raise LeituraError(f"ZIP vazio: {arquivo}")
                zf.extractall(tmp)

            # lê o primeiro arquivo reconhecível dentro do zip
            for nome in nomes:
                extraido = Path(tmp) / nome
                sufixo   = extraido.suffix.lower()
                if sufixo in (".dbc", ".dbf"):
                    return ler(extraido)

        raise LeituraError(f"Nenhum .dbc ou .dbf encontrado dentro de {arquivo}")
    
    except LeituraError:
        raise

    except Exception as e:
        raise LeituraError(f"Falha ao ler .zip: {arquivo}") from e
