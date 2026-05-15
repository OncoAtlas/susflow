# susflow/systems/base.py
import time
from pathlib import Path
from typing import List, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import polars as pl
from .. import ftp as _ftp
from ..parsers import converter as _converter
from ..storage import local_lake as _lake
from ..core import cleaner  
from ..core import validator as _validator
from .. import config as _cfg
from susflow.core import validator as _validator
from susflow.core import cleaner as _cleaner

def scan_system(system: str, table: str):
    """
    Scans the entire partitioned structure for the system.
    This is extremely fast and uses no RAM until you call .collect().
    """
    root_path = _lake.BASE_DIR / system.upper() / table.upper()
    
    return pl.scan_parquet(f"{root_path}/*/*/*/*.parquet", hive_partitioning=True)

def load_region(system: str, table: str, region_name: str, year: int):
    """
    Reads an entire region without loading unnecessary files.
    """
    from ..config import REGIOES
    
    ufs_da_regiao = REGIOES.get(region_name.upper())
    if not ufs_da_regiao:
        raise ValueError(f"Região {region_name} não encontrada.")

    # Root path for the system/table
    root_path = _lake.BASE_DIR / system.upper() / table.upper()
    
    # Polars scans the folders and filters by the 'uf' and 'year' partitions
    return (
        pl.scan_parquet(f"{root_path}/*/*/*/*.parquet", hive_partitioning=True)
        .filter(
            (pl.col("year") == year) & 
            (pl.col("uf").is_in(ufs_da_regiao))
        )
        .collect() # Executes the optimized read
    )

def generic_load(
    system: str, 
    sub_dir: str, 
    table: str, 
    uf: str, 
    year: int, 
    month: int = 0, 
    use_polars: bool = True,
    columns: Optional[List[str]] = None  
):
    """
    Universal DATASUS data loading engine.
    Handles validation, cache, download, conversion, logs, and enrichment.
    """
    # 1. Parameter validation
    uf, year, month = _validator.validate_params(system, uf, year, month)
    parquet_path = _lake.get_path(system, table, year, month, uf)
    
    # 2. Cache management
    if parquet_path.exists():
        if parquet_path.stat().st_size == 0:
            parquet_path.unlink()
        else:
            # If the file exists and has content, load it directly
            df = _converter.load_as_df(parquet_path, use_polars=use_polars)
            return _post_process(df, use_polars, columns)

    # 3. Download and conversion
    start_total = time.perf_counter()
    
    # File name formatting (e.g. RDPB2301.dbc)
    yy = str(year)[-2:]
    mm = str(month).zfill(2)
    date_suffix = f"{yy}{mm}" if month > 0 else str(year)
    nome_arquivo = f"{table.upper()}{uf.upper()}{date_suffix}.dbc"
    
    # --- FTP PATH FIX (avoids duplication) ---
    base_path = f"/dissemin/publicos/{system}/"
    # If sub_dir already contains the base path, do not concatenate
    if sub_dir.startswith("/dissemin"):
        caminho_ftp = f"{sub_dir}/{nome_arquivo}".replace("//", "/")
    else:
        caminho_ftp = f"{base_path}/{sub_dir}/{nome_arquivo}".replace("//", "/")
    
    temp_dbc = _lake.get_temp_path(nome_arquivo)
    
    try:
        # Download
        start_down = time.perf_counter()
        _ftp.baixar(caminho_ftp, temp_dbc)
        end_down = time.perf_counter()
        
        # Conversion
        start_conv = time.perf_counter()
        _converter.to_parquet(temp_dbc, parquet_path)
        end_conv = time.perf_counter()
        
        # Metadata write
        _write_metadata(parquet_path, caminho_ftp, system)

        total_time = time.perf_counter() - start_total
        print(f"⏱️  [{system}] {uf} {year}/{month} processado em {total_time:.2f}s "
              f"(Down: {end_down-start_down:.2f}s | Conv: {end_conv-start_conv:.2f}s)")
            
    except Exception as e:
        if parquet_path.exists(): parquet_path.unlink()
        raise Exception(f"❌ Erro ao processar {nome_arquivo}: {e}")
    finally:
        if temp_dbc.exists(): temp_dbc.unlink()

    # 4. Load and post-processing
    df = _converter.load_as_df(parquet_path, use_polars=use_polars)
    return _post_process(df, use_polars, columns)

def _post_process(df: pl.DataFrame, use_polars: bool, columns: Optional[List[str]]) -> pl.DataFrame:
    """Applies column filters and cleanup after loading."""
    if use_polars:
        df = cleaner.apply_standard_clean(df)
        if columns:
            df = df.select([c for c in columns if c in df.columns])
    return df

def _write_metadata(parquet_path: Path, ftp_url: str, system: str):
    """Ensures data provenance by saving a .meta manifest."""
    meta_path = parquet_path.with_suffix('.meta')
    with open(meta_path, 'w') as f:
        f.write(f"provenance: {ftp_url}\n")
        f.write(f"system: {system}\n")
        f.write(f"download_date: {time.ctime()}\n")

# BULK LOAD to speed up annual or multi-state loads

def generic_bulk_load(
    system: str, 
    sub_dir: str, 
    table: str, 
    ufs: List[str], 
    year: int, 
    months: Optional[List[int]] = None, 
    max_workers: int = None,
    **kwargs
):
    """
    Downloads and consolidates multiple states/months in parallel.
    """
    max_workers = max_workers or _cfg.MAX_WORKERS
    if months is None:
        months = [0] # For annual systems

    print(f"[BULK] Starting load of {len(ufs)} state(s) for {system} ({year})")
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(generic_load, system, sub_dir, table, uf, year, m, **kwargs): (uf, m)
            for uf in ufs for m in months
        }
        
        for future in as_completed(futures):
            uf, m = futures[future]
            try:
                df = future.result()
                if df is not None and not df.is_empty():
                    results.append(df)
            except Exception as e:
                    print(f"⚠️  [BULK] Failed to process {uf} (Month {m}): {e}")

    if not results:
        return pl.DataFrame()

    print(f"[BULK] Consolidating {len(results)} files into a single DataFrame...")
    return pl.concat(results, how="vertical")