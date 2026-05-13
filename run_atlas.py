# run_atlas.py
from susflow.systems import cnes
import polars as pl

print("🚀 Iniciando busca de dados consistentes no CNES...")

try:
    # Testando com a Paraíba (PB) para Março de 2024
    # A lib vai: 
    # 1. Olhar o cache 
    # 2. Se não tiver, baixar o DBC 
    # 3. Converter para Parquet via DuckDB
    # 4. Retornar o DataFrame
    df_st = cnes.load(table="ST", uf="PB", year=2024, month=3)
    
    print("\n✅ Sucesso! Tabela de Estabelecimentos (ST) carregada.")
    print(f"Shape do DataFrame: {df_st.shape}")
    print("\nPrimeiras linhas:")
    print(df_st.head())

except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")