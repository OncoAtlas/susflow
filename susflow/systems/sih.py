from .base import generic_load

def load(table: str, uf: str, year: int, month: int):
    return generic_load(
        system="SIHSUS", 
        sub_dir="200801_/Dados", 
        table=table, 
        uf=uf, 
        year=year, 
        month=month
    )