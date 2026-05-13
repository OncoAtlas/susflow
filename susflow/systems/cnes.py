from .base import generic_load
from ..core.synchronization import BacktrackingEngine

def load(table: str, uf: str, year: int, month: int, use_polars: bool = True):
    return generic_load(
        system="CNES",
        sub_dir=f"200508_/Dados/{table.upper()}",
        table=table,
        uf=uf,
        year=year,
        month=month,
        use_polars=use_polars
    )

def load_latest(table: str, uf: str, use_polars: bool = True):
    engine = BacktrackingEngine(system="CNES")
    year, month = engine.find_latest_consistent(tables=[table.upper()], uf=uf.upper())
    return load(table, uf, year, month, use_polars=use_polars)