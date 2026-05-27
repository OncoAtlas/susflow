from susflow import config


def test_ftp_host_and_ufs():
    assert isinstance(config.FTP_HOST, str)
    assert "SP" in config.UFS


def test_all_systems_contains_sim():
    assert "SIM" in config.ALL_SYSTEMS
