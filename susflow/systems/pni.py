from .base import generic_load

def load(uf: str, year: int):
    # PNI is usually annual or dose-based; we adjust according to the table
    return generic_load(
        system="PNI", 
        sub_dir="DADOS", 
        table="DPNI", 
        uf=uf, 
        year=year
    )