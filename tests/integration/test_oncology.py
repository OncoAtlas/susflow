import pytest
import polars as pl
from susflow.systems import sim, cnes

def test_cross_system_integrity():
    """Validates whether SIM and CNES data can be linked."""
    df_sim = sim.load(uf="PB", year=2023)
    
    # If CODESTAB is not in config.py, it keeps the original name.
    # But CNES becomes codigo_cnes.
    col_estabelecimento_sim = "CODESTAB" 
    
    lista_cnes_sim = (
        df_sim.filter(pl.col(col_estabelecimento_sim).is_not_null())
        .select(pl.col(col_estabelecimento_sim).cast(pl.Utf8))
        .unique()[col_estabelecimento_sim]
        .to_list()
    )
    
    df_cnes = cnes.load(table="ST", uf="PB", year=2023, month=6)
    
    # WARNING: Here we switch from "CNES" to "codigo_cnes"
    lista_cnes_oficial = (
        df_cnes.select(pl.col("codigo_cnes").cast(pl.Utf8))
        .unique()["codigo_cnes"]
        .to_list()
    )
    
    matches = set(lista_cnes_sim).intersection(set(lista_cnes_oficial))
    assert len(matches) > 0