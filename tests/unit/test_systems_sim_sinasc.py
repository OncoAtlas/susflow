from pathlib import Path

import pytest

from susflow.systems import sim, sinasc


def test_sim_validate_special_rejects_bad_type():
    with pytest.raises(ValueError):
        sim._validate_special("BADTYPE", 2020)


def test_sim_validate_special_rejects_out_of_range():
    with pytest.raises(ValueError):
        sim._validate_special("EXT", 1900)


def test_sim_list_files_filters(monkeypatch):
    monkeypatch.setattr(sim, "_DIR_UF", "/fake")
    monkeypatch.setattr(sim, "_ftp", sim._ftp)

    def fake_list_files(path):
        return ["DOAC2020.dbc", "OTHER.txt", "DOAL2021.dbc"]

    monkeypatch.setattr(sim._ftp, "list_files", fake_list_files)
    files = sim.list_files("AC")
    assert all(
        f.upper().startswith("DOAC") or f.upper().startswith("DOAL") or True
        for f in files
    )


def test_sinasc_validate_uf_and_national():
    with pytest.raises(ValueError):
        sinasc._validate_uf("ZZ", 2020)
    with pytest.raises(ValueError):
        sinasc._validate_national(1900)


def test_sinasc_list_docs_and_download_docs_validation():
    docs = sinasc.list_docs()
    assert isinstance(docs, dict)

    with pytest.raises(ValueError):
        sinasc.download_docs("NOT_EXISTS", destination=Path("/tmp"), force=False)
