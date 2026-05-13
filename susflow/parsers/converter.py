# susflow/parsers/converter.py
import tempfile
from pathlib import Path
import duckdb
import polars as pl
import pandas as pd
from pyreaddbc import dbc2dbf

def to_parquet(input_path: Path, output_path: Path) -> Path:
    """Converte DBC/DBF para Parquet via DuckDB tratando codificação Latin-1."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        dbf_path = Path(tmp_dir) / "temp.dbf"
        
        if input_path.suffix.lower() == ".dbc":
            dbc2dbf(str(input_path), str(dbf_path))
        else:
            dbf_path = input_path

        conn = duckdb.connect()
        
        conn.execute("INSTALL spatial;")
        conn.execute("LOAD spatial;")
        
        try:
            # O DuckDB agora exige que o encoding seja passado via open_options para arquivos DBF/SHP
            query = f"""
                COPY (
                    SELECT * FROM st_read(
                        '{str(dbf_path)}', 
                        open_options=['ENCODING=ISO-8859-1']
                    )
                ) TO '{str(output_path)}' (FORMAT PARQUET)
            """
            conn.execute(query)
        except Exception as e:
            conn.close()
            raise Exception(f"Falha na conversão DuckDB: {e}")
            
        conn.close()
    return output_path

def load_as_df(parquet_path: Path, use_polars: bool = True):
    """Retorna o DataFrame a partir do Parquet de cache."""
    if use_polars:
        return pl.read_parquet(parquet_path)
    return pd.read_parquet(parquet_path)