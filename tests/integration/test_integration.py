import pytest
import polars as pl
from susflow.systems import cnes, sim, sinasc, base

def test_cnes_load_integration():
    """Valida carga do CNES (Sistema com Meses)"""
    # Usando Paraíba, Março de 2026 (que já sabemos que funciona)
    df = cnes.load(table="ST", uf="PB", year=2026, month=3)
    # CNES foi mapeado para codigo_cnes no seu config.py
    assert "codigo_cnes" in df.columns

def test_sim_load_integration():
    """Valida carga do SIM (Sistema Anual)"""
    # Nota: Ajuste o ano para um que você saiba que existe no FTP (ex: 2022 ou 2023)
    df = sim.load(uf="PB", year=2023)
    # DTOBITO foi mapeado para data_obito
    assert "data_obito" in df.columns

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

def test_sim_data_integrity_sentinel():
    """Valida se a tradução dos códigos CID faz sentido clínico."""
    df = sim.load(uf="PB", year=2023)
    
    # Correção do filtro: causa_basica_obito (conforme config.py)
    prostate_cancer = df.filter(pl.col("causa_basica_obito") == "C61")
    
    if not prostate_cancer.is_empty():
        # Verificação da descrição enriquecida
        desc = prostate_cancer["causa_basica_obito_desc"][0].lower()
        assert "próstata" in desc or "prostate" in desc
    
    import datetime
    hoje = datetime.date.today()
    # Verifica o sufixo minúsculo _dt
    assert df["data_obito_dt"].max() <= hoje