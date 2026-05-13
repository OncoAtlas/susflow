# susflow/storage/local_lake.py
from pathlib import Path
import os

# Raiz do Lake na home do usuário
BASE_DIR = Path.home() / ".susflow" / "data"

def get_path(system: str, table: str, year: int, month: int, uf: str) -> Path:
    """Calcula o caminho do arquivo Parquet final."""
    comp = f"{year}{str(month).zfill(2)}"
    path = BASE_DIR / system.lower() / table.upper() / comp / f"{uf.upper()}.parquet"
    return path

def get_temp_path(filename: str) -> Path:
    """Calcula caminho para downloads temporários."""
    temp_dir = BASE_DIR / "_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename