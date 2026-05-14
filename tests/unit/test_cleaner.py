import polars as pl
import pytest
from susflow.core import cleaner

def test_cleaner_integration_full_flow():
    """
    Testa o fluxo completo de limpeza: preservação de dados, 
    conversão de datas e tradução de CID via simple-icd-10.
    """
    # 1. Setup de dados de teste (usando padrões reais do DATASUS)
    df = pl.DataFrame({
        "DIAG_PRINC": ["C61", "C50", "XXXX"], # Câncer de Próstata, Mama e um Inválido
        "DT_INTER": ["20231201", "20230101", "99999999"], # Datas válidas e uma 'corrompida'
        "OUTRA_COL": [1, 2, 3] # Coluna que não deve ser tocada
    })

    # 2. Execução
    df_cleaned = cleaner.apply_standard_clean(df)

    # A. Verificação de nomes (O cleaner mapeia DIAG_PRINC -> diagnostico_principal)
    assert "diagnostico_principal" in df_cleaned.columns
    assert "diagnostico_principal_desc" in df_cleaned.columns
    assert "DT_INTER_dt" in df_cleaned.columns
    
    # B. Integridade: Coluna extra mantida e soma correta
    assert df_cleaned["OUTRA_COL"].sum() == 6

    # C. Datas: Verificação da conversão (Usando sufixo minúsculo _dt)
    assert df_cleaned["DT_INTER_dt"][0].year == 2023
    assert df_cleaned["DT_INTER_dt"][1].month == 1
    # Data inválida vira null
    assert df_cleaned["DT_INTER_dt"][2] is None

    # D. CID (simple-icd-10): Verificação da tradução
    # Buscamos a linha do C61 usando o NOVO nome da coluna
    desc_c61 = df_cleaned.filter(pl.col("diagnostico_principal") == "C61")["diagnostico_principal_desc"][0]
    
    assert "Malignant" in desc_c61
    assert "prostate" in desc_c61.lower()
    
    # O código 'XXXX' não deve ter tradução
    desc_invalid = df_cleaned.filter(pl.col("diagnostico_principal") == "XXXX")["diagnostico_principal_desc"][0]
    assert desc_invalid is None

def test_cleaner_no_cid_columns():
    """Garante que o cleaner funciona mesmo sem colunas de diagnóstico."""
    df = pl.DataFrame({"IDADE": [25, 30], "NOME": ["A", "B"]})
    df_cleaned = cleaner.apply_standard_clean(df)
    
    # Verifica o mapeamento IDADE -> idade_paciente
    assert "idade_paciente" in df_cleaned.columns
    # Garante que não criou colunas fantasmas
    assert "diagnostico_principal" not in df_cleaned.columns 