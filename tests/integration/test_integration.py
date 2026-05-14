import pytest
import polars as pl
from susflow.systems import cnes, sim, sinasc, base

def test_cnes_load_integration():
    """Validates CNES loading (monthly system)."""
    # Using Paraiba, March 2026 (which we already know works)
    df = cnes.load(table="ST", uf="PB", year=2026, month=3)
    # CNES was mapped to codigo_cnes in config.py
    assert "codigo_cnes" in df.columns

def test_sim_load_integration():
    """Validates SIM loading (annual system)."""
    # Note: adjust the year to one you know exists on the FTP (e.g. 2022 or 2023)
    df = sim.load(uf="PB", year=2023)
    # DTOBITO was mapped to data_obito
    assert "data_obito" in df.columns

def test_sinasc_load_integration():
    """Validates SINASC loading."""
    df = sinasc.load(uf="PB", year=2020)
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()

@pytest.mark.parametrize("system_module, table, uf, year, month", [
    (cnes, "EQ", "PB", 2026, 3),
    # Add others here
])
def test_generic_loader_behavior(system_module, table, uf, year, month):
    df = system_module.load(table=table, uf=uf, year=year, month=month)
    assert df.shape[0] > 0

def test_sim_data_integrity_sentinel():
    """Validates whether CID code translation makes clinical sense."""
    df = sim.load(uf="PB", year=2023)
    
    # Filter correction: causa_basica_obito (as defined in config.py)
    prostate_cancer = df.filter(pl.col("causa_basica_obito") == "C61")
    
    if not prostate_cancer.is_empty():
        # Enriched description check
        desc = prostate_cancer["causa_basica_obito_desc"][0].lower()
        assert "próstata" in desc or "prostate" in desc
    
    import datetime
    hoje = datetime.date.today()
    # Checks the lowercase _dt suffix
    assert df["data_obito_dt"].max() <= hoje