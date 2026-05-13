# susflow/parsers/converter.py
import tempfile
from pathlib import Path
import duckdb
import polars as pl
import pandas as pd
from pyreaddbc import dbc2dbf

def to_parquet(input_path: Path, output_path: Path) -> Path:
    """
    Converte DBC/DBF para Parquet via DuckDB, limpa duplicatas 
    e trata codificação Latin-1.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        dbf_path = Path(tmp_dir) / "temp.dbf"
        # Usamos um caminho temporário para o primeiro dump do DuckDB
        raw_parquet = Path(tmp_dir) / "raw.parquet"
        
        if input_path.suffix.lower() == ".dbc":
            dbc2dbf(str(input_path), str(dbf_path))
        else:
            dbf_path = input_path

        conn = duckdb.connect()
        conn.execute("INSTALL spatial;")
        conn.execute("LOAD spatial;")
        
        try:
            # 1. Extração via DuckDB (Tratando Encoding)
            query = f"""
                COPY (
                    SELECT * FROM st_read(
                        '{str(dbf_path)}', 
                        open_options=['ENCODING=ISO-8859-1']
                    )
                ) TO '{str(raw_parquet)}' (FORMAT PARQUET)
            """
            conn.execute(query)
            conn.close()

            # 2. Refinamento via Polars (Remoção de Duplicatas)
            df = pl.read_parquet(raw_parquet)
            initial_rows = df.height
            
            # Remove linhas 100% idênticas
            df = df.unique()
            
            final_rows = df.height
            if initial_rows > final_rows:
                print(f"🧹 {input_path.name}: {initial_rows - final_rows} duplicatas removidas.")

            # 3. Escrita final otimizada
            df.write_parquet(output_path, compression="zstd")

        except Exception as e:
            if 'conn' in locals(): conn.close()
            raise Exception(f"Falha na conversão/limpeza: {e}")
            
    return output_path

def load_as_df(parquet_path: Path, use_polars: bool = True):
    """Retorna o DataFrame a partir do Parquet de cache."""
    if use_polars:
        return pl.read_parquet(parquet_path)
    return pd.read_parquet(parquet_path)