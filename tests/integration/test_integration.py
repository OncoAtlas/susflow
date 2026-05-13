import pytest
import polars as pl
from susflow.systems import cnes, sim, sinasc

def test_cnes_load_integration():
    """Valida carga do CNES (Sistema com Meses)"""
    # Usando Paraíba, Março de 2026 (que já sabemos que funciona)
    df = cnes.load(table="ST", uf="PB", year=2026, month=3)
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "CNES" in df.columns

def test_sim_load_integration():
    """Valida carga do SIM (Sistema Anual)"""
    # Nota: Ajuste o ano para um que você saiba que existe no FTP (ex: 2022 ou 2023)
    df = sim.load(uf="PB", year=2023)
    assert isinstance(df, pl.DataFrame)
    assert "DTOBITO" in df.columns or "DT_OBITO" in df.columns

def test_sinasc_load_integration():
    """Valida carga do SINASC"""
    df = sinasc.load(uf="PB", year=2020)
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()

@pytest.mark.parametrize("system_module, table, uf, year, month", [
    (cnes, "EQ", "PB", 2026, 3),
    # Adicione outros aqui
])
def test_generic_loader_behavior(system_module, table, uf, year, month):
    df = system_module.load(table=table, uf=uf, year=year, month=month)
    assert df.shape[0] > 0