from susflow import config
from susflow.systems import cnes, siasus, sihsus


def test_sinan_has_diseases_and_pattern():
    # config contains SINAN metadata
    assert "DENG" in config.SINAN["diseases"]


def test_sihsus_and_siasus_have_prefixes():
    # modules expose prefix listing functions
    p1 = sihsus.prefixos()
    assert isinstance(p1, dict)
    pn = sihsus.prefixos_nacionais()
    assert isinstance(pn, dict)

    p2 = siasus.prefixos()
    assert isinstance(p2, dict)


def test_cnes_pattern_and_subtypes():
    # config has CNES metadata and module exposes subtypes
    assert "pattern" in config.CNES
    s = cnes.subtipos()
    assert isinstance(s, dict)
    assert "ST" in s


def test_pni_format_dbf():
    assert config.PNI["format"] == "dbf"
