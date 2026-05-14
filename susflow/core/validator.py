from datetime import datetime
import logging
from .. import config as _cfg

logger = logging.getLogger(__name__)

def validate_params(system: str, uf: str, year: int, month: int = 0):
    """
    Validador dinâmico que consulta o config.py para garantir integridade.
    """
    system = system.upper()
    uf = uf.upper()
    now = datetime.now()

    # 1. Validação de UF (usando a lista mestre do config)
    if uf not in _cfg.UFS:
        raise ValueError(f"❌ UF '{uf}' inválida. UFs aceitas: {', '.join(_cfg.UFS)}")

    # 2. Busca as regras do sistema no config
    sys_map = _cfg.ALL_SYSTEMS.get(system)
    if not sys_map:
        logger.warning(f"⚠️ Sistema {system} não mapeado no config. Usando validação genérica.")
        min_year = 1990
        is_monthly = month > 0
    else:
        # Pega o range de anos real definido no seu mapeamento
        # Nota: Alguns sistemas no seu config têm o range dentro de subchaves (ex: SIM['uf'])
        target_config = sys_map.get("uf") if "uf" in sys_map else sys_map
        min_year, max_year = target_config.get("year_range", (1990, now.year))
        is_monthly = target_config.get("granularity") == "month"

    # 3. Validação de cronologia (passado e futuro)
    if year < min_year:
        raise ValueError(f"❌ {system}: Dados disponíveis apenas a partir de {min_year}.")
    
    if year > now.year:
        raise ValueError(f"❌ O ano {year} ainda não está disponível.")

    # 4. Validação de Mês e Periodicidade
    if is_monthly:
        if month < 1 or month > 12:
            raise ValueError(f"❌ {system} é MENSAL. Informe um mês entre 1 e 12.")
    else:
        if month != 0:
            logger.info(f"ℹ️ {system} é ANUAL. O mês {month} será ignorado.")
            month = 0 # Normaliza para anual

    # 5. Validação de Disponibilidade Real (Lag do DATASUS)
    # Evita que o usuário tente baixar o mês atual ou anterior que ainda não subiu
    if year == now.year and is_monthly:
        lag = 2 # Meses de atraso médio do DATASUS
        if (now.month - month) < lag:
            logger.warning(f"⚠️ Dados de {month}/{year} podem ainda não estar no FTP (Publicação preliminar).")

    return uf, year, month