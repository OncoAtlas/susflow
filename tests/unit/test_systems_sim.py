from pathlib import Path

import pytest

from susflow.systems import sim


def test_validate_uf_invalid():
    with pytest.raises(ValueError):
        sim._validate_uf("XX", 2020)


def test_validate_uf_year_out_of_range():
    min_year, max_year = sim._YEAR_MIN_UF, sim._YEAR_MAX_UF
    with pytest.raises(ValueError):
        sim._validate_uf("SP", min_year - 1)
    with pytest.raises(ValueError):
        sim._validate_uf("SP", max_year + 1)


def test_list_files_filters(monkeypatch):
    sample = ["DOSP2020.dbc", "DOBA2021.dbc", "README.txt"]

    monkeypatch.setattr(sim._ftp, "list_files", lambda d: sample)

    all_files = sim.list_files()
    assert all_files == sample

    sp_files = sim.list_files("SP")
    assert sp_files == ["DOSP2020.dbc"]


def test_list_special_filters(monkeypatch):
    sample = ["DOEXT24.dbc", "DOFET24.dbc", "OTHER.txt"]
    monkeypatch.setattr(sim._ftp, "list_files", lambda d: sample)

    all_files = sim.list_special()
    assert all_files == sample

    ext_files = sim.list_special("EXT")
    assert ext_files == ["DOEXT24.dbc"]


def test_download_docs_invalid():
    with pytest.raises(ValueError):
        sim.download_docs("not-a-file")


def test_download_docs_all(monkeypatch, tmp_path):
    dummy = tmp_path / "doc.zip"
    monkeypatch.setattr(
        sim, "_download_file", lambda ftp_dir, name, dest, force: dummy
    )

    result = sim.download_docs()
    assert isinstance(result, list)
    assert all(isinstance(p, Path) for p in result)
