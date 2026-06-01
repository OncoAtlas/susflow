import pytest

from susflow.systems import cnes


def test_validate_subtype_invalid():
    with pytest.raises(ValueError):
        cnes._validate_subtype("ZZ")


def test_validate_month_and_uf_and_year():
    with pytest.raises(ValueError):
        cnes._validate("ST", "XX", 2020, 1)
    with pytest.raises(ValueError):
        cnes._validate("ST", "SP", 2020, 13)


def test_file_name_and_ftp_dir():
    name = cnes._file_name("ST", "SP", 2025, 1)
    assert name.endswith("2501.dbc")
    assert cnes._ftp_dir("ST").endswith("/ST")


def test_list_files_filters(monkeypatch):
    sample = ["STSP2501.dbc", "STRJ2501.dbc", "OTHER.txt"]
    monkeypatch.setattr(cnes._ftp, "list_files", lambda d: sample)

    all_files = cnes.list_files()
    assert all_files == sample

    sp_files = cnes.list_files("SP")
    assert sp_files == ["STSP2501.dbc"]
