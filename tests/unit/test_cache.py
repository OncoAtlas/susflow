from pathlib import Path

from susflow.cache import local_path, exists


def test_local_path_with_custom_root(tmp_path: Path):
    ftp_path = "/dissemin/publicos/SINASC/NOV/DNRES/DNSP2022.dbc"
    local = local_path(ftp_path, root=tmp_path)
    assert str(local).startswith(str(tmp_path))
    assert local.name == "DNSP2022.dbc"


def test_exists_false_for_nonexistent(tmp_path: Path):
    ftp_path = "/no/such/file.dbc"
    assert exists(ftp_path, root=tmp_path) is False
