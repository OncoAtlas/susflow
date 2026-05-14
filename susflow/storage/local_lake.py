# susflow/storage/local_lake.py
from pathlib import Path
import os

BASE_DIR = Path("data_lake")

def get_path(system: str, table: str, year: int, month: int, uf: str) -> Path:
    """
    Creates the structure: data_lake/SYSTEM/TABLE/year=YYYY/uf=XX/data.parquet
    """
    # 1. Base: data_lake/SIM/DO
    path = BASE_DIR / system.upper() / table.upper()
    
    # 2. Year partition: year=2023
    path = path / f"year={year}"
    
    # 3. Month partition (optional, for monthly systems like SIH/CNES)
    if month > 0:
        path = path / f"month={month:02d}"
        
    # 4. UF partition: uf=PB
    path = path / f"uf={uf.upper()}"
    
    # Create folders if they do not exist
    path.mkdir(parents=True, exist_ok=True)
    
    return path / "data.parquet"

def get_temp_path(filename: str) -> Path:
    temp_dir = BASE_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename

def get_temp_path(filename: str) -> Path:
    """Builds the path for temporary downloads."""
    temp_dir = BASE_DIR / "_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename