import tempfile
from pathlib import Path

from susflow.cache import caminho_local, existe


def test_caminho_local_with_custom_root(tmp_path: Path):
    ftp_path = "/dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc"
    local = caminho_local(ftp_path, raiz=tmp_path)
    assert str(local).startswith(str(tmp_path))
    assert local.name == "DNSP2022.dbc"


def test_existe_false_for_nonexistent(tmp_path: Path):
    ftp_path = "/no/such/file.dbc"
    assert existe(ftp_path, raiz=tmp_path) is False
