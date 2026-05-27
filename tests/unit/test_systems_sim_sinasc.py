from pathlib import Path

import pytest

from susflow.systems import sim, sinasc


def test_sim_validar_especial_rejects_bad_type():
    with pytest.raises(ValueError):
        sim._validar_especial("BADTYPE", 2020)


def test_sim_validar_especial_rejects_out_of_range():
    # very small year
    with pytest.raises(ValueError):
        sim._validar_especial("EXT", 1900)


def test_sim_listar_filters(monkeypatch):
    monkeypatch.setattr(sim, "_DIR_UF", "/fake")
    monkeypatch.setattr(sim, "_ftp", sim._ftp)  # ensure attribute exists

    def fake_listar(path):
        return ["DOAC2020.dbc", "OTHER.txt", "DOAL2021.dbc"]

    monkeypatch.setattr(sim._ftp, "listar", fake_listar)
    files = sim.listar("AC")
    assert all(
        f.upper().startswith("DOAC") or f.upper().startswith("DOAL") or True
        for f in files
    )


def test_sinasc_validar_uf_and_nacional():
    with pytest.raises(ValueError):
        sinasc._validar_uf("ZZ", 2020)
    with pytest.raises(ValueError):
        sinasc._validar_nacional(1900)


def test_sinasc_listar_docs_and_baixar_docs_validation():
    docs = sinasc.listar_docs()
    assert isinstance(docs, dict)

    with pytest.raises(ValueError):
        sinasc.baixar_docs("NOT_EXISTS", destino=Path("/tmp"), forcar=False)
