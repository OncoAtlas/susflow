import pytest

from susflow.systems import cnes


def test_validar_subtipo_invalid():
    with pytest.raises(ValueError):
        cnes._validar_subtipo("ZZ")


def test_validar_month_and_uf_and_year():
    with pytest.raises(ValueError):
        cnes._validar("ST", "XX", 2020, 1)
    with pytest.raises(ValueError):
        cnes._validar("ST", "SP", 2020, 13)


def test_nome_and_ftp_dir():
    name = cnes._nome("ST", "SP", 2025, 1)
    assert name.endswith("2501.dbc")
    assert cnes._ftp_dir("ST").endswith("/ST")


def test_listar_filters(monkeypatch):
    sample = ["STSP2501.dbc", "STRJ2501.dbc", "OTHER.txt"]
    monkeypatch.setattr(cnes._ftp, "listar", lambda d: sample)

    all_files = cnes.listar()
    assert all_files == sample

    sp_files = cnes.listar("SP")
    assert sp_files == ["STSP2501.dbc"]
