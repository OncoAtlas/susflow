# tests/integration/test_enrichment.py
import polars as pl
from susflow.systems import sim

def test_sim_load_has_enrichment():
    """Validates that SIM loading brings the dynamically translated columns."""
    df = sim.load(uf="PB", year=2023)
    
    # In SIM, we expect CAUSABAS and DTOBITO
    # The cleaner should have created CAUSABAS_DESC and DTOBITO_DT
    assert "causa_basica_obito_desc" in df.columns
    assert "data_obito_dt" in df.columns
    
    # Checks that the converted date type is correct
    assert df["data_obito_dt"].dtype == pl.Date
    
    # Checks integrity: the number of rows must not change after the join
    # (The previous SIM issue had 28,773 rows)
    assert df.height == 28773