import polars as pl

def filter_oncology(df: pl.DataFrame, cid_column: str = "causa_basica_obito") -> pl.DataFrame:
    """
    Filters the DataFrame for neoplasm records (C00-D48).
    Works for both SIM (causa_basica_obito) and SIH (diagnostico_principal).
    """
    # Regex to capture C00 through D48
    # C00-C97 (malignant), D00-D09 (in situ), D10-D36 (benign), D37-D48 (uncertain)
    regex_onco = r"^(C[0-9][0-9]|D[0-3][0-9]|D4[0-8])"
    
    return df.filter(pl.col(cid_column).str.contains(regex_onco))

def analyze_cost_at_end_of_life(df_sim_onco: pl.DataFrame, df_sih_onco: pl.DataFrame):
    """
    Tries to cross deaths with hospitalizations to estimate average cost.
    Note: In public data, the cross-match is statistical (by municipality/age/sex)
    since we do not have CPF/CNS due to LGPD constraints.
    """
    # Grouping costs by municipality and diagnosis in SIH
    costs = df_sih_onco.group_by(["municipio_residencia", "diagnostico_principal"]).agg(
        pl.col("valor_total_pago").mean().alias("custo_medio_internacao"),
        pl.col("valor_total_pago").count().alias("total_internacoes")
    )
    
    return costs