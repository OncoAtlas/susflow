# susflow/systems/sih.py
from .base import generic_load, generic_bulk_load
from typing import List, Optional

def load(uf: str, year: int, month: int, table: str = "RD", columns: Optional[List[str]] = None):
    """
    Carrega dados do SIHSUS (Internações).
    Padrão: Tabela 'RD' (Reduzido), que contém o diagnóstico e valor.
    """
    return generic_load(
        system="SIHSUS", 
        sub_dir="200801_/Dados", 
        table=table, 
        uf=uf, 
        year=year, 
        month=month,
        columns=columns
    )

# Função adicional para carregar o ano inteiro em paralelo (12 meses)
# arquivos do SIH são enormes, então isso acelera a carga anual significativamente
def load_year(uf: str, year: int, table: str = "RD", **kwargs):
    """Carrega os 12 meses de um ano em paralelo."""
    months = list(range(1, 13))
    return generic_bulk_load(
        system="SIHSUS",
        sub_dir="200801_/Dados",
        table=table,
        uf=uf,
        year=year,
        months=months,
        **kwargs
    )