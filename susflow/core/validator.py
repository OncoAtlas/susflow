from datetime import datetime
import logging
from .. import config as _cfg

logger = logging.getLogger(__name__)

def validate_params(system: str, uf: str, year: int, month: int = 0):
    """
    Dynamic validator that consults config.py to ensure integrity.
    """
    system = system.upper()
    uf = uf.upper()
    now = datetime.now()

    # 1. UF validation (using the master list from config)
    if uf not in _cfg.UFS:
        raise ValueError(f"❌ UF '{uf}' inválida. UFs aceitas: {', '.join(_cfg.UFS)}")

    # 2. Fetch system rules from config
    sys_map = _cfg.ALL_SYSTEMS.get(system)
    if not sys_map:
        logger.warning(f"⚠️ Sistema {system} não mapeado no config. Usando validação genérica.")
        min_year = 1990
        is_monthly = month > 0
    else:
        # Get the actual year range defined in the mapping
        # Note: some systems in config keep the range inside nested keys (e.g. SIM['uf'])
        target_config = sys_map.get("uf") if "uf" in sys_map else sys_map
        min_year, max_year = target_config.get("year_range", (1990, now.year))
        is_monthly = target_config.get("granularity") == "month"

    # 3. Chronology validation (past and future)
    if year < min_year:
        raise ValueError(f"❌ {system}: Dados disponíveis apenas a partir de {min_year}.")
    
    if year > now.year:
        raise ValueError(f"❌ O ano {year} ainda não está disponível.")

    # 4. Month and periodicity validation
    if is_monthly:
        if month < 1 or month > 12:
            raise ValueError(f"❌ {system} é MENSAL. Informe um mês entre 1 e 12.")
    else:
        if month != 0:
            logger.info(f"ℹ️ {system} é ANUAL. O mês {month} será ignorado.")
            month = 0 # Normalize to annual

    # 5. Real availability validation (DATASUS lag)
    # Prevents the user from trying to download the current or previous month before publication
    if year == now.year and is_monthly:
        lag = 2 # Average DATASUS delay in months
        if (now.month - month) < lag:
            logger.warning(f"⚠️ Dados de {month}/{year} podem ainda não estar no FTP (Publicação preliminar).")

    return uf, year, month