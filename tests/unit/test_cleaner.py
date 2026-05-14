import polars as pl
import pytest
from susflow.core import cleaner

def test_cleaner_integration_full_flow():
    """
    Tests the full cleaning flow: data preservation,
    date conversion, and CID translation via simple-icd-10.
    """
    # 1. Test data setup (using real DATASUS patterns)
    df = pl.DataFrame({
        "DIAG_PRINC": ["C61", "C50", "XXXX"], # Prostate, breast, and one invalid code
        "DT_INTER": ["20231201", "20230101", "99999999"], # Valid dates and one corrupted value
        "OUTRA_COL": [1, 2, 3] # Column that should not be touched
    })

    # 2. Execution
    df_cleaned = cleaner.apply_standard_clean(df)

    # A. Name checks (the cleaner maps DIAG_PRINC -> diagnostico_principal)
    assert "diagnostico_principal" in df_cleaned.columns
    assert "diagnostico_principal_desc" in df_cleaned.columns
    assert "DT_INTER_dt" in df_cleaned.columns
    
    # B. Integrity: extra column preserved and sum is correct
    assert df_cleaned["OUTRA_COL"].sum() == 6

    # C. Dates: conversion check (using lowercase _dt suffix)
    assert df_cleaned["DT_INTER_dt"][0].year == 2023
    assert df_cleaned["DT_INTER_dt"][1].month == 1
    # Invalid date becomes null
    assert df_cleaned["DT_INTER_dt"][2] is None

    # D. CID (simple-icd-10): translation check
    # We look up the C61 row using the NEW column name
    desc_c61 = df_cleaned.filter(pl.col("diagnostico_principal") == "C61")["diagnostico_principal_desc"][0]
    
    assert "Malignant" in desc_c61
    assert "prostate" in desc_c61.lower()
    
    # The 'XXXX' code should not have a translation
    desc_invalid = df_cleaned.filter(pl.col("diagnostico_principal") == "XXXX")["diagnostico_principal_desc"][0]
    assert desc_invalid is None

def test_cleaner_no_cid_columns():
    """Ensures the cleaner works even without diagnosis columns."""
    df = pl.DataFrame({"IDADE": [25, 30], "NOME": ["A", "B"]})
    df_cleaned = cleaner.apply_standard_clean(df)
    
    # Check the IDADE -> idade_paciente mapping
    assert "idade_paciente" in df_cleaned.columns
    # Ensure no phantom columns were created
    assert "diagnostico_principal" not in df_cleaned.columns 