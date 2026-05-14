# susflow/config.py
"""
susflow/config.py
=================
Mapa completo dos sistemas do DATASUS e configurações de motor da biblioteca.
"""

FTP_HOST = "ftp.datasus.gov.br"

# ---------------------------------------------------------------------------
# UFs disponíveis
# ---------------------------------------------------------------------------
UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
    "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
    "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]

# ---------------------------------------------------------------------------
# Agrupamentos Regionais (Para filtros de performance e análise)
# ---------------------------------------------------------------------------
REGIOES = {
    "NORTE": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "NORDESTE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "CENTRO-OESTE": ["DF", "GO", "MS", "MT"],
    "SUDESTE": ["ES", "MG", "RJ", "SP"],
    "SUL": ["PR", "RS", "SC"],
}

# Inverso: permite descobrir a região a partir da UF rapidamente
UF_PARA_REGIAO = {uf: reg for reg, ufs in REGIOES.items() for uf in ufs}

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES DE MOTOR (ENGINE)
# ---------------------------------------------------------------------------
MAX_WORKERS = 5          # Downloads simultâneos no Bulk Load
DEFAULT_ENCODING = "iso-8859-1"

# ---------------------------------------------------------------------------
# DICIONÁRIO DE LEGIBILIDADE (Para o Atlas da Oncologia)
# Mapeia siglas crípticas do DATASUS para nomes claros em português.
# ---------------------------------------------------------------------------
COLUMN_MAPPINGS = {
    # Identificação e Localização
    "MUNIC_RES": "municipio_residencia",
    "CODMUNRES": "municipio_residencia",
    "MUNIC_MOV": "municipio_movimentacao",
    "CNES":      "codigo_cnes",
    
    # Datas e Paciente
    "IDADE":     "idade_paciente",
    "SEXO":      "sexo_paciente",
    "DTINTERNA": "data_internacao",
    "DTOBITO":   "data_obito",
    "DTNASC":    "data_nascimento",
    "DTRECEBIM": "data_recebimento",
    
    # Diagnósticos (CID) e Procedimentos
    "CAUSABAS":   "causa_basica_obito",
    "DIAG_PRINC": "diagnostico_principal",
    "DIAG_SEC":   "diagnostico_secundario",
    "PROC_REA":   "procedimento_realizado",
    
    # Valores e Gestão
    "VAL_TOT":    "valor_total_pago",
    "DIAS_PERM":  "dias_permanencia",
    "CODUFMUN":   "codigo_municipio_ibge",
}

# ---------------------------------------------------------------------------
# MAPEAMENTO DE SISTEMAS (PROVENIÊNCIA E REGRAS DE FTP)
# ---------------------------------------------------------------------------

SIM = {
    "description": "Sistema de Informações sobre Mortalidade",
    "ftp_base": "/dissemin/publicos/SIM/CID10",
    "special": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOFET",
        "types": {"EXT": "Externas", "FET": "Fetais", "INF": "Infantis", "MAT": "Maternos"},
        "pattern": "DO{TYPE}{YY}.dbc",
        "granularity": "year",
        "year_digits": 2,
        "format": "dbc",
        "scope": "national",
        "year_range": (1996, 2024),
    },
    "uf": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DORES",
        "pattern": "DO{UF}{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format": "dbc",
        "scope": "uf",
        "year_range": (1996, 2024),
    },
}

SINASC = {
    "description": "Sistema de Informações sobre Nascidos Vivos",
    "ftp_dir":     "/dissemin/publicos/SINASC/NOV/DNRES",
    "pattern":     "DN{UF}{YYYY}.dbc",
    "granularity": "year",
    "year_digits": 4,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (1996, 2022),
}

SINAN = {
    "description": "Sistema de Informações de Agravos de Notificação",
    "ftp_dir":     "/dissemin/publicos/SINAN/DADOS/FINAIS",
    "ftp_dir_prelim": "/dissemin/publicos/SINAN/DADOS/PRELIM",
    "pattern":     "{DISEASE}BR{YY}.dbc",
    "granularity": "year",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "national",
    "diseases": {
        "DENG": "Dengue", "CHIK": "Chikungunya", "TUBE": "Tuberculose",
        "HANS": "Hanseníase", "CANC": "Câncer relacionado ao trabalho",
        # ... (suas outras doenças mapeadas continuam aqui)
    }
}

SIHSUS = {
    "description": "Sistema de Informações Hospitalares do SUS",
    "ftp_dir":     "/dissemin/publicos/SIHSUS/200801_/Dados",
    "pattern":     "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2008, 2025),
    "prefixes": {
        "RD": "AIH reduzida", "SP": "Serviços profissionais",
    },
}

SIASUS = {
    "description": "Sistema de Informações Ambulatoriais do SUS",
    "ftp_dir":     "/dissemin/publicos/SIASUS/200801_/Dados",
    "pattern":     "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2008, 2025),
}

CNES = {
    "description": "Cadastro Nacional de Estabelecimentos de Saúde",
    "ftp_base":    "/dissemin/publicos/CNES/200508_/Dados",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2005, 2025),
    "subtypes": {
        "ST": "Estabelecimentos", "LT": "Leitos", "PF": "Profissionais",
    },
}

PNI = {
    "description": "Programa Nacional de Imunizações",
    "ftp_dir":     "/dissemin/publicos/PNI/DADOS",
    "pattern":     "DPNI{UF}{YY}.DBF",
    "granularity": "year",
    "year_digits": 2,
    "format":      "dbf",
    "scope":       "uf",
    "year_range":  (1994, 2019),
}

IBGE_POP = {
    "description": "Estimativas populacionais IBGE",
    "ftp_dir":     "/dissemin/publicos/IBGE/POP",
    "pattern":     "POPBR{YY}.zip",
    "granularity": "year",
    "year_digits": 2,
    "format":      "zip",
    "scope":       "national",
    "year_range":  (1980, 2012),
}

# ---------------------------------------------------------------------------
# ÍNDICE GERAL
# ---------------------------------------------------------------------------
ALL_SYSTEMS = {
    "SIM":      SIM,
    "SINASC":   SINASC,
    "SINAN":    SINAN,
    "SIHSUS":   SIHSUS,
    "SIASUS":   SIASUS,
    "CNES":     CNES,
    "PNI":      PNI,
    "IBGE_POP": IBGE_POP,
}