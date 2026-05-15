from susflow import config

def test_config_ufs_count():
    """Ensures all 27 UFs are present."""
    assert len(config.UFS) == 27

def test_regioes_mapping():
    """Validates that all config UFs are mapped to some region."""
    all_mapped_ufs = []
    for ufs in config.REGIOES.values():
        all_mapped_ufs.extend(ufs)
    
    assert set(all_mapped_ufs) == set(config.UFS)

def test_system_year_ranges():
    """Validates that year ranges are logical."""
    for sys_name, sys_info in config.ALL_SYSTEMS.items():
        # Check whether year_range exists at the uf level or globally
        target = sys_info.get("uf") or sys_info
        if "year_range" in target:
            start, end = target["year_range"]
            assert start < end
            assert start >= 1970