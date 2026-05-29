from susflow import config
from susflow.systems import cnes, siasus, sihsus


def test_sinan_has_diseases_and_pattern():
    assert "DENG" in config.SINAN["diseases"]


def test_sihsus_and_siasus_have_prefixes():
    p1 = sihsus.prefixes()
    assert isinstance(p1, dict)
    pn = sihsus.national_prefixes()
    assert isinstance(pn, dict)

    p2 = siasus.prefixes()
    assert isinstance(p2, dict)


def test_cnes_pattern_and_subtypes():
    assert "pattern" in config.CNES
    s = cnes.subtypes()
    assert isinstance(s, dict)
    assert "ST" in s


def test_pni_format_dbf():
    assert config.PNI["format"] == "dbf"
