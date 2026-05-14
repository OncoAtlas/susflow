from susflow import config

def test_config_ufs_count():
    """Garante que todas as 27 UFs estão presentes."""
    assert len(config.UFS) == 27

def test_regioes_mapping():
    """Valida se todas as UFs do config estão mapeadas em alguma região."""
    all_mapped_ufs = []
    for ufs in config.REGIOES.values():
        all_mapped_ufs.extend(ufs)
    
    assert set(all_mapped_ufs) == set(config.UFS)

def test_system_year_ranges():
    """Valida se os ranges de anos são lógicos."""
    for sys_name, sys_info in config.ALL_SYSTEMS.items():
        # Verifica se existe year_range no nível uf ou geral
        target = sys_info.get("uf") or sys_info
        if "year_range" in target:
            start, end = target["year_range"]
            assert start < end
            assert start >= 1970