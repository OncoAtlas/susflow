import pytest
import polars as pl
from susflow.systems import sim, cnes

def test_cross_system_integrity():
    """Valida se os dados do SIM e CNES podem ser relacionados."""
    # 1. Carrega óbitos (SIM)
    df_sim = sim.load(uf="PB", year=2023)
    
    # No SIM, o código do estabelecimento é 'CODESTAB'
    col_estabelecimento_sim = "CODESTAB"
    
    # Garantir que a coluna seja String e remover nulos/vazios
    lista_cnes_sim = (
        df_sim.filter(pl.col(col_estabelecimento_sim).is_not_null())
        .select(pl.col(col_estabelecimento_sim).cast(pl.Utf8))
        .unique()[col_estabelecimento_sim]
        .to_list()
    )
    
    assert len(lista_cnes_sim) > 0, "Deveria haver óbitos com estabelecimento informado"
    
    # 2. Carrega Cadastro de Estabelecimentos (CNES - ST)
    # No CNES, a coluna é de fato 'CNES'
    df_cnes = cnes.load(table="ST", uf="PB", year=2023, month=6)
    
    lista_cnes_oficial = (
        df_cnes.select(pl.col("CNES").cast(pl.Utf8))
        .unique()["CNES"]
        .to_list()
    )
    
    # 3. Cruzamento
    matches = set(lista_cnes_sim).intersection(set(lista_cnes_oficial))
    
    print(f"\n[DEBUG] Estabelecimentos no SIM: {len(lista_cnes_sim)}")
    print(f"[DEBUG] Estabelecimentos no CNES: {len(lista_cnes_oficial)}")
    print(f"[DEBUG] Coincidências encontradas: {len(matches)}")
    
    assert len(matches) > 0, "Os códigos de estabelecimento deveriam coincidir entre SIM e CNES"