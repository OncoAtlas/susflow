# susflow/systems/sinasc.py
from .base import generic_load

def load(uf: str, year: int, use_polars: bool = True):
    return generic_load(
        system="SINASC",
        sub_dir="1994_/Dados", # Pasta correta para o SINASC
        table="DN",
        uf=uf,
        year=year,
        month=0, 
        use_polars=use_polars
    )