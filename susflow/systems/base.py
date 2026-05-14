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
    Faz um scan de toda a estrutura particionada do sistema.
    Isso é extremamente rápido e não consome RAM até você dar o .collect()
    """
    root_path = _lake.BASE_DIR / system.upper() / table.upper()
    
    return pl.scan_parquet(f"{root_path}/*/*/*/*.parquet", hive_partitioning=True)

def load_region(system: str, table: str, region_name: str, year: int):
    """
    Lê uma região inteira sem carregar arquivos desnecessários.
    """
    from ..config import REGIOES
    
    ufs_da_regiao = REGIOES.get(region_name.upper())
    if not ufs_da_regiao:
        raise ValueError(f"Região {region_name} não encontrada.")

    # Caminho raiz do sistema/tabela
    root_path = _lake.BASE_DIR / system.upper() / table.upper()
    
    # Mágica: O Polars varre as pastas e já filtra pela partição 'uf' e 'year'
    return (
        pl.scan_parquet(f"{root_path}/*/*/*/*.parquet", hive_partitioning=True)
        .filter(
            (pl.col("year") == year) & 
            (pl.col("uf").is_in(ufs_da_regiao))
        )
        .collect() # Executa a leitura otimizada
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
    Engine universal de carga de dados do DATASUS.
    Lida com: Validação, Cache, Download, Conversão, Logs e Enriquecimento.
    """
    # 1. Validação de Parâmetros
    uf, year, month = _validator.validate_params(system, uf, year, month)
    parquet_path = _lake.get_path(system, table, year, month, uf)
    
    # 2. Gestão de Cache
    if parquet_path.exists():
        if parquet_path.stat().st_size == 0:
            parquet_path.unlink()
        else:
            # Se o arquivo existe e tem tamanho, carregamos direto
            df = _converter.load_as_df(parquet_path, use_polars=use_polars)
            return _post_process(df, use_polars, columns)

    # 3. Download e Conversão
    start_total = time.perf_counter()
    
    # Formatação do nome do arquivo (ex: RDPB2301.dbc)
    yy = str(year)[-2:]
    mm = str(month).zfill(2)
    date_suffix = f"{yy}{mm}" if month > 0 else str(year)
    nome_arquivo = f"{table.upper()}{uf.upper()}{date_suffix}.dbc"
    
    # --- CORREÇÃO DE CAMINHO FTP (Evita duplicação) ---
    base_path = f"/dissemin/publicos/{system}/"
    # Se o sub_dir já contém o caminho base, não concatenamos
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
        
        # Conversão
        start_conv = time.perf_counter()
        _converter.to_parquet(temp_dbc, parquet_path)
        end_conv = time.perf_counter()
        
        # Escrita de Metadados
        _write_metadata(parquet_path, caminho_ftp, system)

        total_time = time.perf_counter() - start_total
        print(f"⏱️  [{system}] {uf} {year}/{month} processado em {total_time:.2f}s "
              f"(Down: {end_down-start_down:.2f}s | Conv: {end_conv-start_conv:.2f}s)")
            
    except Exception as e:
        if parquet_path.exists(): parquet_path.unlink()
        raise Exception(f"❌ Erro ao processar {nome_arquivo}: {e}")
    finally:
        if temp_dbc.exists(): temp_dbc.unlink()

    # 4. Carga e Pós-processamento
    df = _converter.load_as_df(parquet_path, use_polars=use_polars)
    return _post_process(df, use_polars, columns)

def _post_process(df: pl.DataFrame, use_polars: bool, columns: Optional[List[str]]) -> pl.DataFrame:
    """Aplica filtros de coluna e limpeza após a carga."""
    if use_polars:
        df = cleaner.apply_standard_clean(df)
        if columns:
            df = df.select([c for c in columns if c in df.columns])
    return df

def _write_metadata(parquet_path: Path, ftp_url: str, system: str):
    """Garante a proveniência dos dados salvando um manifesto .meta."""
    meta_path = parquet_path.with_suffix('.meta')
    with open(meta_path, 'w') as f:
        f.write(f"provenance: {ftp_url}\n")
        f.write(f"system: {system}\n")
        f.write(f"download_date: {time.ctime()}\n")

# BULK LOAD para acelerar cargas anuais ou multi-estado

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
    Baixa e consolida múltiplos estados/meses em paralelo.
    """
    max_workers = max_workers or _cfg.MAX_WORKERS
    if months is None:
        months = [0] # Caso sistemas anuais

    print(f"[BULK] Iniciando carga de {len(ufs)} estado(s) para {system} ({year})")
    
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
                print(f"⚠️  [BULK] Falha ao processar {uf} (Mês {m}): {e}")

    if not results:
        return pl.DataFrame()

    print(f"[BULK] Consolidando {len(results)} arquivos em um único DataFrame...")
    return pl.concat(results, how="vertical")