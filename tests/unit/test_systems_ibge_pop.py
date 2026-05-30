import pandas as pd
import pytest

from susflow import cache as _cache
from susflow import config
from susflow.systems import ibge_pop


def test_nome_correto():
    assert ibge_pop._nome(1995) == "POPBR95.zip"
    assert ibge_pop._nome(2000) == "POPBR00.zip"
    assert ibge_pop._nome(2012) == "POPBR12.zip"
    assert ibge_pop._nome(1980) == "POPBR80.zip"


def test_validar_rejeita_fora_do_intervalo():
    with pytest.raises(ValueError, match="out of range"):
        ibge_pop._validar(1979)
    with pytest.raises(ValueError, match="out of range"):
        ibge_pop._validar(2013)


def test_validar_aceita_limites():
    ibge_pop._validar(1980)
    ibge_pop._validar(2012)


def test_baixar_usa_cache_quando_arquivo_existe(tmp_path, monkeypatch):
    local = tmp_path / "POPBR95.zip"
    local.write_bytes(b"dummy")
    monkeypatch.setattr(_cache, "caminho_local", lambda *a, **k: local)

    resultado = ibge_pop.baixar(1995, destino=tmp_path)
    assert resultado == local


def test_baixar_forca_download_quando_forcar(tmp_path, monkeypatch):
    local = tmp_path / "POPBR95.zip"
    local.write_bytes(b"dummy")
    downloaded = {}

    monkeypatch.setattr(_cache, "caminho_local", lambda *a, **k: local)
    monkeypatch.setattr(ibge_pop._ftp, "baixar", lambda *a, **k: downloaded.update({"called": True}) or local)

    ibge_pop.baixar(1995, destino=tmp_path, forcar=True)
    assert downloaded.get("called")


def test_ler_retorna_dataframe(tmp_path, monkeypatch):
    fake_path = tmp_path / "POPBR95.zip"
    fake_path.write_bytes(b"dummy")
    expected = pd.DataFrame({"POPULACAO": [1000]})

    monkeypatch.setattr(ibge_pop, "baixar", lambda *a, **k: fake_path)
    monkeypatch.setattr(ibge_pop, "_ler", lambda p: expected)

    result = ibge_pop.ler(1995)
    assert result.equals(expected)


def test_config_ibge_pop_integro():
    assert config.IBGE_POP["ftp_dir"] == "/dissemin/publicos/IBGE/POP"
    assert config.IBGE_POP["format"] == "zip"
    assert config.IBGE_POP["scope"] == "national"
    assert "IBGE_POP" in config.ALL_SYSTEMS
