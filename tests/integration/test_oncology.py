import pytest
import polars as pl
from susflow.systems import sim, cnes

def test_cross_system_integrity():
    """Valida se os dados do SIM e CNES podem ser relacionados."""
    df_sim = sim.load(uf="PB", year=2023)
    
    # Se CODESTAB não está no config.py, ele mantém o nome original.
    # Mas CNES vira codigo_cnes.
    col_estabelecimento_sim = "CODESTAB" 
    
    lista_cnes_sim = (
        df_sim.filter(pl.col(col_estabelecimento_sim).is_not_null())
        .select(pl.col(col_estabelecimento_sim).cast(pl.Utf8))
        .unique()[col_estabelecimento_sim]
        .to_list()
    )
    
    df_cnes = cnes.load(table="ST", uf="PB", year=2023, month=6)
    
    # ATENÇÃO: Aqui mudamos de "CNES" para "codigo_cnes"
    lista_cnes_oficial = (
        df_cnes.select(pl.col("codigo_cnes").cast(pl.Utf8))
        .unique()["codigo_cnes"]
        .to_list()
    )
    
    matches = set(lista_cnes_sim).intersection(set(lista_cnes_oficial))
    assert len(matches) > 0