# susflow/core/cleaner.py
import polars as pl

def apply_standard_clean(df: pl.DataFrame, custom_cid_map: dict = None) -> pl.DataFrame:
    # 1. Identifica colunas de CID (contém DIAG, CAUSA ou CID)
    cols_cid = [c for c in df.columns if any(p in c.upper() for p in ["DIAG", "CAUSA", "CID"])]
    
    # 2. Identifica colunas de Data (começa com DT ou contém DATA)
    # Isso pegará DTOBITO, DT_INTER, DTNASC, etc.
    cols_data = [c for c in df.columns if c.upper().startswith("DT") or "DATA" in c.upper()]
    
    if cols_cid:
        df = translate_codes(df, cols_cid, custom_cid_map)
        
    if cols_data:
        df = format_dates_safely(df, cols_data)
        
    return df

def translate_codes(df: pl.DataFrame, columns: list, mapping: dict = None) -> pl.DataFrame:
    # Mapeamento padrão (pode ser expandido ou movido para um recurso externo)
    default_map = {
        "C61": "Neoplasia Maligna da Próstata",
        "C50": "Neoplasia Maligna da Mama",
        # Adicione outros aqui...
    }
    active_map = mapping if mapping else default_map

    for col in columns:
        map_df = pl.DataFrame({
            col: list(active_map.keys()),
            f"{col}_DESC": list(active_map.values())
        })
        df = df.join(map_df, on=col, how="left")
    return df

def format_dates_safely(df: pl.DataFrame, columns: list) -> pl.DataFrame:
    for col in columns:
        # O pl.coalesce tenta converter nos dois formatos comuns do DATASUS
        # Se um falhar (null), ele tenta o próximo.
        df = df.with_columns([
            pl.coalesce([
                pl.col(col).str.to_date(format="%Y%m%d", strict=False), # Padrão SIH/SIA
                pl.col(col).str.to_date(format="%d%m%Y", strict=False)  # Padrão SIM/SINASC
            ]).alias(f"{col}_DT")
        ])
    return df