from .base import generic_load

def load(agravo: str, uf: str, year: int, use_polars: bool = True):
    """
    Carrega dados do SINAN. 
    Exemplos de 'agravo': 'DENG' (Dengue), 'TUBE' (Tuberculose), 'HANS' (Hanseníase).
    """
    # O SINAN armazena os arquivos em subpastas com o nome do agravo
    return generic_load(
        system="SINAN",
        sub_dir="2007_/Dados",
        table=agravo.upper(),
        uf=uf,
        year=year,
        month=0,
        use_polars=use_polars
    )