import polars as pl
import requests
from pathlib import Path

# Path where the file will be stored inside the library structure
RESOURCE_PATH = Path(__file__).parent / "municipios_br.parquet"

def get_municipality_map() -> pl.DataFrame:
    """
    Returns the municipality map.
    If it is not on disk, downloads and saves it.
    """
    if RESOURCE_PATH.exists():
        return pl.read_parquet(RESOURCE_PATH)
    
    df = _fetch_from_ibge()
    
    # Save for future runs (offline-first)
    df.write_parquet(RESOURCE_PATH)
    print(f"Dicionário de municípios salvo em: {RESOURCE_PATH}")
    
    return df

def _fetch_from_ibge() -> pl.DataFrame:
    """Fetches raw data from the IBGE API and formats it to the DATASUS standard."""
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    print("🌐 Baixando dicionário de municípios via API do IBGE...")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        municipios = []
        for m in data:
            # Safely fetch the UF abbreviation
            microrregiao = m.get("microrregiao") or {}
            mesorregiao = microrregiao.get("mesorregiao") or {}
            uf_sigla = mesorregiao.get("UF", {}).get("sigla", "N/A")
            
            municipios.append({
                "codigo_municipio": str(m["id"])[:6],
                "municipio_nome": m["nome"],
                "uf_sigla": uf_sigla,
                "regiao_saude": m.get("regiao-imediata", {}).get("nome", "N/A")
            })
        return pl.DataFrame(municipios)
    except Exception as e:
        raise Exception(f"❌ Falha ao obter dados do IBGE: {e}")