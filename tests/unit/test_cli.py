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

def test_sim_listar(capsys, monkeypatch):
    monkeypatch.setattr("susflow.cli.sim.listar", lambda uf: ["DOSP2022.dbc", "DORJ2022.dbc"])
    run("sim", "listar")
    assert capsys.readouterr().out == "DOSP2022.dbc\nDORJ2022.dbc\n"


def test_sim_listar_uf_filter(monkeypatch):
    captured = {}
    monkeypatch.setattr("susflow.cli.sim.listar", lambda uf: captured.update({"uf": uf}) or [])
    run("sim", "listar", "--uf", "SP")
    assert captured["uf"] == "SP"


def test_sim_baixar(capsys, monkeypatch, tmp_path):
    expected = tmp_path / "DOSP2022.dbc"
    monkeypatch.setattr(
        "susflow.cli.sim.baixar",
        lambda uf, ano, destino, forcar: expected,
    )
    run("sim", "baixar", "SP", "2022")
    assert str(expected) in capsys.readouterr().out


def test_sim_baixar_forcar(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.sim.baixar",
        lambda uf, ano, destino, forcar: captured.update({"forcar": forcar}) or Path("."),
    )
    run("sim", "baixar", "SP", "2022", "--forcar")
    assert captured["forcar"] is True


# ---------------------------------------------------------------------------
# SINASC
# ---------------------------------------------------------------------------

def test_sinasc_listar(capsys, monkeypatch):
    monkeypatch.setattr("susflow.cli.sinasc.listar", lambda uf: ["DNSP2022.dbc"])
    run("sinasc", "listar")
    assert "DNSP2022.dbc" in capsys.readouterr().out


def test_sinasc_baixar(capsys, monkeypatch, tmp_path):
    p = tmp_path / "DNSP2022.dbc"
    monkeypatch.setattr(
        "susflow.cli.sinasc.baixar",
        lambda uf, ano, destino, forcar: p,
    )
    run("sinasc", "baixar", "SP", "2022")
    assert str(p) in capsys.readouterr().out


# ---------------------------------------------------------------------------
# SINAN
# ---------------------------------------------------------------------------

def test_sinan_listar(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sinan.listar",
        lambda doenca, preliminar: ["DENGBR23.dbc"],
    )
    run("sinan", "listar")
    assert "DENGBR23.dbc" in capsys.readouterr().out


def test_sinan_doencas(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sinan.doencas",
        lambda: {"DENG": "Dengue", "CHIK": "Chikungunya"},
    )
    run("sinan", "doencas")
    out = capsys.readouterr().out
    assert "DENG" in out
    assert "Dengue" in out


def test_sinan_baixar_preliminar(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.sinan.baixar",
        lambda doenca, ano, destino, forcar, preliminar: captured.update({"p": preliminar}) or Path("."),
    )
    run("sinan", "baixar", "DENG", "2023", "--preliminar")
    assert captured["p"] is True


# ---------------------------------------------------------------------------
# SIASUS, SIHSUS, CNES, PNI — spot checks
# ---------------------------------------------------------------------------

def test_siasus_baixar(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.siasus.baixar",
        lambda uf, ano, mes, prefixo, destino, forcar: captured.update({"prefixo": prefixo}) or Path("."),
    )
    run("siasus", "baixar", "SP", "2022", "3", "--prefixo", "BI")
    assert captured["prefixo"] == "BI"


def test_sihsus_listar(capsys, monkeypatch):
    monkeypatch.setattr(
        "susflow.cli.sihsus.listar",
        lambda uf, prefixo: ["RDSP2201.dbc"],
    )
    run("sihsus", "listar")
    assert "RDSP2201.dbc" in capsys.readouterr().out


def test_cnes_baixar(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "susflow.cli.cnes.baixar",
        lambda uf, ano, mes, tipo, destino, forcar: captured.update({"tipo": tipo}) or Path("."),
    )
    run("cnes", "baixar", "SP", "2022", "1", "--tipo", "PF")
    assert captured["tipo"] == "PF"


def test_pni_baixar(capsys, monkeypatch, tmp_path):
    p = tmp_path / "DPNISP10.DBF"
    monkeypatch.setattr(
        "susflow.cli.pni.baixar",
        lambda uf, ano, destino, forcar: p,
    )
    run("pni", "baixar", "SP", "2010")
    assert str(p) in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_value_error_prints_to_stderr_and_exits_1(capsys, monkeypatch):
    monkeypatch.setattr("susflow.cli.sim.baixar", lambda *a, **kw: (_ for _ in ()).throw(ValueError("bad year")))
    run("sim", "baixar", "SP", "1800", expect_exit=1)
    assert "bad year" in capsys.readouterr().err


def test_missing_sistema_exits(capsys):
    run(expect_exit=2)
