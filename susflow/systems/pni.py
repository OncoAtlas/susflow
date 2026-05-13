from .base import generic_load

def load(uf: str, year: int):
    # PNI geralmente é anual ou por doses, ajustamos conforme a tabela
    return generic_load(
        system="PNI", 
        sub_dir="DADOS", 
        table="DPNI", 
        uf=uf, 
        year=year
    )