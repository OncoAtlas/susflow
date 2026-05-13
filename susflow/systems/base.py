# susflow/systems/base.py
from pathlib import Path
import polars as pl
from .. import ftp as _ftp
from ..parsers import converter as _converter
from ..storage import local_lake as _lake
from ..core import cleaner  # <--- Novo import

def generic_load(
    system: str, 
    sub_dir: str, 
    table: str, 
    uf: str, 
    year: int, 
    month: int = 0, 
    use_polars: bool = True
):
    """
    Motor universal de carga de dados do DATASUS com enriquecimento automático.
    """
    parquet_path = _lake.get_path(system, table, year, month, uf)
    
    if not parquet_path.exists():
        # ... (Mantemos toda a lógica de download e conversão igual) ...
        yy = str(year)[-2:]
        mm = str(month).zfill(2)
        date_suffix = f"{yy}{mm}" if month > 0 else str(year)
        nome_arquivo = f"{table.upper()}{uf.upper()}{date_suffix}.dbc"
        
        caminho_ftp = f"/dissemin/publicos/{system}/{sub_dir}/{nome_arquivo}"
        if system in ["SIM", "SINASC"]:
            caminho_ftp = f"/dissemin/publicos/{system}/{sub_dir}/{nome_arquivo}"

        temp_dbc = _lake.get_temp_path(nome_arquivo)
        
        try:
            print(f"📥 [{system}] Baixando {nome_arquivo}...")
            _ftp.baixar(caminho_ftp, temp_dbc)
            _converter.to_parquet(temp_dbc, parquet_path)
        except Exception as e:
            if parquet_path.exists(): parquet_path.unlink()
            raise Exception(f"Falha ao processar {system} {table}: {e}")
        finally:
            if temp_dbc.exists(): temp_dbc.unlink()

    # 4. Carrega o dado
    df = _converter.load_as_df(parquet_path, use_polars=use_polars)

    # 5. Enriquecimento (Apenas se usar Polars)
    if use_polars:
        # Aplicamos as melhorias sem tocar nos dados originais
        df = cleaner.apply_standard_clean(df)

    return df