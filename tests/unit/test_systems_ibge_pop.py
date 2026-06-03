import pandas as pd
import pytest

from susflow import cache as _cache
from susflow import config
from susflow.systems import ibge_pop


def test_file_name_correct():
    assert ibge_pop._file_name(1995) == "POPBR95.zip"
    assert ibge_pop._file_name(2000) == "POPBR00.zip"
    assert ibge_pop._file_name(2012) == "POPBR12.zip"
    assert ibge_pop._file_name(1980) == "POPBR80.zip"


def test_validate_rejects_out_of_range():
    with pytest.raises(ValueError, match="out of range"):
        ibge_pop._validate(1979)
    with pytest.raises(ValueError, match="out of range"):
        ibge_pop._validate(2013)


def test_validate_accepts_bounds():
    ibge_pop._validate(1980)
    ibge_pop._validate(2012)


def test_download_uses_cache_when_file_exists(tmp_path, monkeypatch):
    local = tmp_path / "POPBR95.zip"
    local.write_bytes(b"dummy")
    monkeypatch.setattr(_cache, "local_path", lambda *a, **k: local)

    result = ibge_pop.download(1995, destination=tmp_path)
    assert result == local


def test_download_forces_download_when_force(tmp_path, monkeypatch):
    local = tmp_path / "POPBR95.zip"
    local.write_bytes(b"dummy")
    downloaded = {}

    monkeypatch.setattr(_cache, "local_path", lambda *a, **k: local)
    monkeypatch.setattr(
        ibge_pop._ftp,
        "download",
        lambda *a, **k: downloaded.update({"called": True}) or local,
    )

    ibge_pop.download(1995, destination=tmp_path, force=True)
    assert downloaded.get("called")


def test_read_returns_dataframe(tmp_path, monkeypatch):
    fake_path = tmp_path / "POPBR95.zip"
    fake_path.write_bytes(b"dummy")
    expected = pd.DataFrame({"POPULATION": [1000]})

    monkeypatch.setattr(ibge_pop, "download", lambda *a, **k: fake_path)
    monkeypatch.setattr(ibge_pop, "_read", lambda p: expected)

    result = ibge_pop.read(1995)
    assert result.equals(expected)


def test_config_ibge_pop_intact():
    assert config.IBGE_POP["ftp_dir"] == "/dissemin/publicos/IBGE/POP"
    assert config.IBGE_POP["format"] == "zip"
    assert config.IBGE_POP["scope"] == "national"
    assert "IBGE_POP" in config.ALL_SYSTEMS
