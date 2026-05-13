# susflow/systems/sim.py
from .base import generic_load

def load(uf: str, year: int, use_polars: bool = True):
    return generic_load(
        system="SIM",
        sub_dir="CID10/DORES", # Caminho completo até o arquivo
        table="DO",
        uf=uf,
        year=year,
        month=0,
        use_polars=use_polars
    )