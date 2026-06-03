from pathlib import Path

import pytest

from susflow.cli import main


def run(*argv, expect_exit=None):
    if expect_exit is not None:
        with pytest.raises(SystemExit) as exc:
            main(list(argv))
        assert exc.value.code == expect_exit
        return None
    main(list(argv))


# ---------------------------------------------------------------------------
# SIM
# ---------------------------------------------------------------------------

def test_sim_list(capsys, monkeypatch):
    monkeypatch.setattr("susflow.cli.sim.list_files", lambda uf: ["DOSP2022.dbc", "DORJ2022.dbc"])
    run("sim", "list")
    assert capsys.readouterr().out == "DOSP2022.dbc\nDORJ2022.dbc\n"


def test_sim_list_uf_filter(monkeypatch):
    captured = {}
    monkeypatch.setattr("susflow.cli.sim.list_files", lambda uf: captured.update({"uf": uf}) or [])
    run("sim", "list", "--uf", "SP")
    assert captured["uf"] == "SP"


def test_sim_download(capsys, monkeypatch, tmp_path):
    expected = tmp_path / "DOSP2022.dbc"
    monkeypatch.setattr(
        "susflow.cli.sim.download",
        lambda uf, year, destination, force: expected,
    )
    run("sim", "download", "SP", "2022")
    assert str(expected) in capsys.readouterr().out


def test_sim_download_force(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.sim.download",
        lambda uf, year, destination, force: captured.update({"force": force}) or Path("."),
    )
    run("sim", "download", "SP", "2022", "--force")
    assert captured["force"] is True


# ---------------------------------------------------------------------------
# SINASC
# ---------------------------------------------------------------------------

def test_sinasc_list(capsys, monkeypatch):
    monkeypatch.setattr("susflow.cli.sinasc.list_files", lambda uf: ["DNSP2022.dbc"])
    run("sinasc", "list")
    assert "DNSP2022.dbc" in capsys.readouterr().out


def test_sinasc_download(capsys, monkeypatch, tmp_path):
    p = tmp_path / "DNSP2022.dbc"
    monkeypatch.setattr(
        "susflow.cli.sinasc.download",
        lambda uf, year, destination, force: p,
    )
    run("sinasc", "download", "SP", "2022")
    assert str(p) in capsys.readouterr().out


# ---------------------------------------------------------------------------
# SINAN
# ---------------------------------------------------------------------------

def test_sinan_list(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sinan.list_files",
        lambda disease, preliminary: ["DENGBR23.dbc"],
    )
    run("sinan", "list")
    assert "DENGBR23.dbc" in capsys.readouterr().out


def test_sinan_diseases(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sinan.diseases",
        lambda: {"DENG": "Dengue", "CHIK": "Chikungunya"},
    )
    run("sinan", "diseases")
    out = capsys.readouterr().out
    assert "DENG" in out
    assert "Dengue" in out


def test_sinan_download_preliminary(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.sinan.download",
        lambda disease, year, destination, force, preliminary: captured.update({"p": preliminary}) or Path("."),
    )
    run("sinan", "download", "DENG", "2023", "--preliminary")
    assert captured["p"] is True


# ---------------------------------------------------------------------------
# SIASUS, SIHSUS, CNES, PNI — spot checks
# ---------------------------------------------------------------------------

def test_siasus_download(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.siasus.download",
        lambda uf, year, month, prefix, destination, force: captured.update({"prefix": prefix}) or Path("."),
    )
    run("siasus", "download", "SP", "2022", "3", "--prefix", "BI")
    assert captured["prefix"] == "BI"


def test_sihsus_list(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sihsus.list_files",
        lambda uf, prefix: ["RDSP2201.dbc"],
    )
    run("sihsus", "list")
    assert "RDSP2201.dbc" in capsys.readouterr().out


def test_cnes_download(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.cnes.download",
        lambda uf, year, month, type_, destination, force: captured.update({"type_": type_}) or Path("."),
    )
    run("cnes", "download", "SP", "2022", "1", "--type", "PF")
    assert captured["type_"] == "PF"


def test_pni_download(capsys, monkeypatch, tmp_path):
    p = tmp_path / "DPNISP10.DBF"
    monkeypatch.setattr(
        "susflow.cli.pni.download",
        lambda uf, year, destination, force: p,
    )
    run("pni", "download", "SP", "2010")
    assert str(p) in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_value_error_prints_to_stderr_and_exits_1(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sim.download",
        lambda *a, **kw: (_ for _ in ()).throw(ValueError("bad year")),
    )
    run("sim", "download", "SP", "1800", expect_exit=1)
    assert "bad year" in capsys.readouterr().err


def test_missing_system_exits(capsys):
    run(expect_exit=2)
