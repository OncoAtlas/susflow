# susflow/storage/local_lake.py
from pathlib import Path
import os

BASE_DIR = Path("data_lake")

def get_path(system: str, table: str, year: int, month: int, uf: str) -> Path:
    """
    Cria a estrutura: data_lake/SISTEMA/TABELA/year=YYYY/uf=XX/data.parquet
    """
    # 1. Base: data_lake/SIM/DO
    path = BASE_DIR / system.upper() / table.upper()
    
    # 2. Partição de Ano: year=2023
    path = path / f"year={year}"
    
    # 3. Partição de Mês (opcional, para sistemas mensais como SIH/CNES)
    if month > 0:
        path = path / f"month={month:02d}"
        
    # 4. Partição de UF: uf=PB
    path = path / f"uf={uf.upper()}"
    
    # Cria as pastas se não existirem
    path.mkdir(parents=True, exist_ok=True)
    
    return path / "data.parquet"

def get_temp_path(filename: str) -> Path:
    temp_dir = BASE_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename

def get_temp_path(filename: str) -> Path:
    """Calcula caminho para downloads temporários."""
    temp_dir = BASE_DIR / "_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / filename