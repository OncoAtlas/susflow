import pytest
from pathlib import Path

from susflow.systems import sinan


def test_validar_invalid_disease():
    with pytest.raises(ValueError):
        sinan._validar("UNKNOWN", 2020)


def test_validar_year_out_of_range():
    with pytest.raises(ValueError):
        sinan._validar("DENG", 1990)


def test_nome_arquivo():
    assert sinan._nome_arquivo("DENG", 2023) == "DENGBR23.dbc"


def test_listar_filters(monkeypatch):
    sample = ["DENGBR23.dbc", "CHIKBR23.dbc", "README.txt"]
    monkeypatch.setattr(sinan._ftp, "listar", lambda d: sample)

    all_files = sinan.listar()
    assert all_files == sample

    deng_files = sinan.listar("DENG")
    assert deng_files == ["DENGBR23.dbc"]


def test_baixar_uses_cache_if_exists(monkeypatch, tmp_path):
    local = tmp_path / "DENGBR23.dbc"
    local.write_text("x")

    # Simulate cache returning a local path that exists
    monkeypatch.setattr(sinan._cache, "caminho_local", lambda caminho, destino: local)

    # _ftp.baixar should not be called; monkeypatch to raise if called
    monkeypatch.setattr(sinan._ftp, "baixar", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("ftp called")))

    result = sinan.baixar("DENG", 2023)
    assert result == local


def test_baixar_invalid_doenca(monkeypatch):
    with pytest.raises(ValueError):
        sinan.baixar("XXXX", 2023)
