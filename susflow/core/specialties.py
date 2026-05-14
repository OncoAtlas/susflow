import polars as pl

def filter_oncology(df: pl.DataFrame, cid_column: str = "causa_basica_obito") -> pl.DataFrame:
    """
    Filtra o DataFrame para registros de Neoplasias (C00-D48).
    Funciona tanto para SIM (causa_basica_obito) quanto para SIH (diagnostico_principal).
    """
    # Regex para capturar de C00 a D48
    # C00-C97 (Malignas), D00-D09 (In situ), D10-D36 (Benignas), D37-D48 (Incertas)
    regex_onco = r"^(C[0-9][0-9]|D[0-3][0-9]|D4[0-8])"
    
    return df.filter(pl.col(cid_column).str.contains(regex_onco))

def analyze_cost_at_end_of_life(df_sim_onco: pl.DataFrame, df_sih_onco: pl.DataFrame):
    """
    Tenta cruzar óbitos com internações para ver custo médio.
    Nota: Em dados públicos, o cruzamento é estatístico (por município/idade/sexo)
    já que não temos o CPF/CNS por questões de LGPD.
    """
    # Agrupando custos por município e diagnóstico no SIH
    costs = df_sih_onco.group_by(["municipio_residencia", "diagnostico_principal"]).agg(
        pl.col("valor_total_pago").mean().alias("custo_medio_internacao"),
        pl.col("valor_total_pago").count().alias("total_internacoes")
    )
    
    return costs