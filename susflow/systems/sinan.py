from .base import generic_load
"""
Loads SINAN data.
Examples of 'agravo': 'DENG' (Dengue), 'TUBE' (Tuberculosis), 'HANS' (Leprosy).
"""

def load(agravo: str, uf: str, year: int, use_polars: bool = True):
    # SINAN stores files in subfolders named after the condition
    return generic_load(
        system="SINAN",
        sub_dir="2007_/Dados",
        table=agravo.upper(),
        uf=uf,
        year=year,
        month=0,
        use_polars=use_polars
    )