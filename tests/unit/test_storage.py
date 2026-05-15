from susflow.storage import local_lake
from pathlib import Path

def test_hive_path_generation():
    # If the order is (system, table, year, month, uf)
    # Use 0 for the month in annual systems like SIM
    path = local_lake.get_path("SIM", "DO", 2023, 0, "PB")
    assert "SIM/DO/year=2023/uf=PB" in str(path)

def test_temp_path_creation():
    """Ensures temporary files go to the correct folder."""
    temp_path = local_lake.get_temp_path("test.dbc")
    assert "temp" in str(temp_path)
    assert temp_path.suffix == ".dbc"