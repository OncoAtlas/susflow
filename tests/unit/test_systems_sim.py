from pathlib import Path

import pytest

from susflow.systems import sim


def test_validar_uf_invalid():
    with pytest.raises(ValueError):
        sim._validar_uf("XX", 2020)


def test_validar_uf_year_out_of_range():
    min_year, max_year = sim._ANO_MIN_UF, sim._ANO_MAX_UF
    with pytest.raises(ValueError):
        sim._validar_uf("SP", min_year - 1)
    with pytest.raises(ValueError):
        sim._validar_uf("SP", max_year + 1)


def test_listar_filters(monkeypatch):
    sample = ["DOSP2020.dbc", "DOBA2021.dbc", "README.txt"]

    monkeypatch.setattr(sim._ftp, "listar", lambda d: sample)

    all_files = sim.listar()
    assert all_files == sample

    sp_files = sim.listar("SP")
    assert sp_files == ["DOSP2020.dbc"]


def test_listar_especial_filters(monkeypatch):
    sample = ["DOEXT24.dbc", "DOFET24.dbc", "OTHER.txt"]
    monkeypatch.setattr(sim._ftp, "listar", lambda d: sample)

    all_files = sim.listar_especial()
    assert all_files == sample

    ext_files = sim.listar_especial("EXT")
    assert ext_files == ["DOEXT24.dbc"]


def test_baixar_docs_invalid():
    with pytest.raises(ValueError):
        sim.baixar_docs("not-a-file")


def test_baixar_docs_all(monkeypatch, tmp_path):
    # Patch _baixar_arquivo to return a Path so function returns list
    dummy = tmp_path / "doc.zip"
    monkeypatch.setattr(
        sim, "_baixar_arquivo", lambda ftp_dir, nome, dest, forcar: dummy
    )

    result = sim.baixar_docs()
    assert isinstance(result, list)
    assert all(isinstance(p, Path) for p in result)
