# tests/integration/test_enrichment.py
import polars as pl
from susflow.systems import sim

def test_sim_load_has_enrichment():
    """Valida se o carregamento do SIM traz as colunas traduzidas dinamicamente."""
    df = sim.load(uf="PB", year=2023)
    
    # No SIM, esperamos encontrar CAUSABAS e DTOBITO
    # O cleaner deve ter criado CAUSABAS_DESC e DTOBITO_DT
    assert "causa_basica_obito_desc" in df.columns
    assert "data_obito_dt" in df.columns
    
    # Verifica se a tipagem da data convertida está correta
    assert df["data_obito_dt"].dtype == pl.Date
    
    # Verifica integridade: o número de linhas não pode ter mudado com o join
    # (O erro do SIM anterior tinha 28.773 linhas)
    assert df.height == 28773