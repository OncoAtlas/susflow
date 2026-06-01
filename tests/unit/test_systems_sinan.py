import pytest

from susflow.systems import sinan


def test_validate_invalid_disease():
    with pytest.raises(ValueError):
        sinan._validate("UNKNOWN", 2020)


def test_validate_year_out_of_range():
    with pytest.raises(ValueError):
        sinan._validate("DENG", 1990)


def test_file_name():
    assert sinan._file_name("DENG", 2023) == "DENGBR23.dbc"


def test_list_files_filters(monkeypatch):
    sample = ["DENGBR23.dbc", "CHIKBR23.dbc", "README.txt"]
    monkeypatch.setattr(sinan._ftp, "list_files", lambda d: sample)

    all_files = sinan.list_files()
    assert all_files == sample

    deng_files = sinan.list_files("DENG")
    assert deng_files == ["DENGBR23.dbc"]


def test_download_uses_cache_if_exists(monkeypatch, tmp_path):
    local = tmp_path / "DENGBR23.dbc"
    local.write_text("x")

    monkeypatch.setattr(sinan._cache, "local_path", lambda path, destination: local)

    monkeypatch.setattr(
        sinan._ftp,
        "download",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("ftp called")),
    )

    result = sinan.download("DENG", 2023)
    assert result == local


def test_download_invalid_disease(monkeypatch):
    with pytest.raises(ValueError):
        sinan.download("XXXX", 2023)
