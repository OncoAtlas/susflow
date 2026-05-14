# susflow/systems/sinasc.py
from .base import generic_load, generic_bulk_load

def load(uf: str, year: int, table: str = "DN", **kwargs):
    return generic_load(
        system="SINASC",
        sub_dir="NOV/DNRES", # The path your friend discovered!
        table=table,
        uf=uf,
        year=year,
        **kwargs
    )

def load_year(uf: str, year: int, **kwargs):
    # SINASC is annual, so load_year just calls the normal load
    # or can download a historical series if we pass a list of years.
    return load(uf, year, **kwargs)