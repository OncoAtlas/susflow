# susflow/systems/sinasc.py
from .base import generic_load, generic_bulk_load

def load(uf: str, year: int, table: str = "DN", **kwargs):
    return generic_load(
        system="SINASC",
        sub_dir="NOV/DNRES", # O caminho que seu amigo descobriu!
        table=table,
        uf=uf,
        year=year,
        **kwargs
    )

def load_year(uf: str, year: int, **kwargs):
    # SINASC é anual, então load_year apenas chama o load normal 
    # ou pode baixar uma série histórica se passarmos uma lista de anos.
    return load(uf, year, **kwargs)