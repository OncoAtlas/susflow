# susflow/core/cleaner.py
import polars as pl
import simple_icd_10 as icd
from .. import config as _cfg
from ..resources import territory

def enrich_municipality_names(df: pl.DataFrame, muni_cols: list) -> pl.DataFrame:
    muni_map = territory.get_municipality_map()
    # 1. Garanta que o mapa só tem o que interessa
    muni_map = muni_map.select(["codigo_municipio", "municipio_nome"])

    for col in muni_cols:
        if col not in df.columns:
            continue
            
        # 2. Renomeie a coluna NO MAPA antes do join para evitar conflito
        temp_map = muni_map.rename({"municipio_nome": f"{col}_nome"})
        
        # 3. Join direto - já vem com o nome correto
        df = df.join(
            temp_map,
            left_on=col,
            right_on="codigo_municipio",
            how="left"
        )
    return df

def apply_standard_clean(df: pl.DataFrame) -> pl.DataFrame:
    """
    Pipeline de limpeza: Renomeia -> Enriquece Municípios -> Traduz CIDs -> Formata Datas.
    """
    # 1. Renomeação para Legibilidade
    rename_dict = {old: new for old, new in _cfg.COLUMN_MAPPINGS.items() if old in df.columns}
    if rename_dict:
        df = df.rename(rename_dict)

    # 2. Identificação de colunas para enriquecimento territorial (Case Insensitive)
    muni_cols = [c for c in df.columns if "municipio" in c.lower()]
    if muni_cols:
        df = enrich_municipality_names(df, muni_cols)

    # 3. Identificação Dinâmica de Colunas (CID e Datas)
    cols_cid = [c for c in df.columns if any(p in c.lower() for p in ["diagnostico", "causa_basica", "cid"])]
    cols_data = [c for c in df.columns if any(p in c.lower() for p in ["data", "dt_"])]
    
    if cols_cid:
        df = enrich_cid_descriptions(df, cols_cid)
    
    if cols_data:
        df = format_dates_safely(df, cols_data)
    
    # REMOVIDA A CHAMADA DUPLICADA QUE ESTAVA AQUI NO FINAL
        
    return df

def enrich_cid_descriptions(df: pl.DataFrame, columns: list) -> pl.DataFrame:
    """Adiciona a descrição oficial da OMS para cada código CID encontrado."""
    for col in columns:
        unique_codes = df.select(pl.col(col)).unique().drop_nulls()[col].to_list()
        
        mapping = {
            code: icd.get_description(code) 
            for code in unique_codes if icd.is_valid_item(code)
        }
        
        if mapping:
            map_df = pl.DataFrame({
                col: list(mapping.keys()),
                f"{col}_desc": list(mapping.values())
            })
            df = df.join(map_df, on=col, how="left")
            
    return df

def format_dates_safely(df: pl.DataFrame, columns: list) -> pl.DataFrame:
    """Converte strings de data em objetos de data reais."""
    for col in columns:
        df = df.with_columns([
            pl.coalesce([
                pl.col(col).cast(pl.String).str.to_date(format="%Y%m%d", strict=False),
                pl.col(col).cast(pl.String).str.to_date(format="%d%m%Y", strict=False)
            ]).alias(f"{col}_dt")
        ])
    return df