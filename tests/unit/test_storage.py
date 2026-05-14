from susflow.storage import local_lake
from pathlib import Path

def test_hive_path_generation():
    # Se a ordem for (system, table, year, month, uf)
    # Use 0 para o mês em sistemas anuais como o SIM
    path = local_lake.get_path("SIM", "DO", 2023, 0, "PB")
    assert "SIM/DO/year=2023/uf=PB" in str(path)

def test_temp_path_creation():
    """Garante que arquivos temporários vão para a pasta correta."""
    temp_path = local_lake.get_temp_path("test.dbc")
    assert "temp" in str(temp_path)
    assert temp_path.suffix == ".dbc"