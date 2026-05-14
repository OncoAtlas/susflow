import pytest
from unittest.mock import patch, MagicMock
from susflow.systems import base, sim
from pathlib import Path

def test_corrupted_dbc_file(tmp_path):
    with patch('susflow.storage.local_lake.BASE_DIR', tmp_path):
        corrupted_file = tmp_path / "DOPB2023.dbc"
        corrupted_file.write_text("CONTEUDO_CORROMPIDO")
        
        # O truque está aqui: retornar o path absoluto como string
        with patch('susflow.ftp.baixar', return_value=str(corrupted_file.absolute())):
            with pytest.raises(Exception):
                # Chame o load que vai tentar processar esse lixo
                sim.load(uf="PB", year=2023)