# susflow/systems/sih.py
from .base import generic_load, generic_bulk_load
from typing import List, Optional

def load(uf: str, year: int, month: int, table: str = "RD", columns: Optional[List[str]] = None):
    """
    Loads SIHSUS data (hospitalizations).
    Default: table 'RD' (Reduced), which contains diagnosis and value.
    """
    return generic_load(
        system="SIHSUS", 
        sub_dir="200801_/Dados", 
        table=table, 
        uf=uf, 
        year=year, 
        month=month,
        columns=columns
    )

# Additional function to load the whole year in parallel (12 months)
# SIH files are huge, so this significantly speeds up annual loading
def load_year(uf: str, year: int, table: str = "RD", **kwargs):
    """Loads the 12 months of a year in parallel."""
    months = list(range(1, 13))
    return generic_bulk_load(
        system="SIHSUS",
        sub_dir="200801_/Dados",
        table=table,
        uf=uf,
        year=year,
        months=months,
        **kwargs
    )