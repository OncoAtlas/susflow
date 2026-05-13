import polars as pl
import pytest
from susflow.core import cleaner

def test_cleaner_preserves_original_data():
    df = pl.DataFrame({
        "DIAG_PRINC": ["C61", "C50", "XXXX"],
        "DT_INTER": ["20231201", "20230101", "99999999"] # Data inválida para testar segurança
    })
    
    df_cleaned = cleaner.apply_standard_clean(df)
    
    # 1. Verifica se as colunas originais ainda existem e são idênticas
    assert "DIAG_PRINC" in df_cleaned.columns
    assert "DT_INTER" in df_cleaned.columns
    assert df_cleaned["DIAG_PRINC"].to_list() == ["C61", "C50", "XXXX"]
    
    # 2. Verifica se as novas colunas foram criadas
    assert "DIAG_PRINC_DESC" in df_cleaned.columns
    assert "DT_INTER_DT" in df_cleaned.columns
    
    # 3. Verifica a integridade da tradução
    assert df_cleaned.filter(pl.col("DIAG_PRINC") == "C61")["DIAG_PRINC_DESC"][0] == "Neoplasia Maligna da Próstata"
    assert df_cleaned.filter(pl.col("DIAG_PRINC") == "XXXX")["DIAG_PRINC_DESC"][0] is None # Left join garante isso
    
    # 4. Verifica a integridade da data (strict=False)
    assert df_cleaned["DT_INTER_DT"][0] is not None
    assert df_cleaned["DT_INTER_DT"][2] is None # Data 99999999 deve virar null, não dar erro