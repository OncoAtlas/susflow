"""
susflow/config.py
=================
Metadados de todos os sistemas do DATASUS.

Campos de cada sistema:
  ftp_dir       — caminho absoluto no FTP
  pattern       — padrão do nome ({UF}, {YYYY}, {YY}, {PREFIX}, {DISEASE}, {TYPE})
  granularity   — "year" | "month"
  year_digits   — 2 ou 4
  format        — "dbc" | "dbf" | "zip"
  scope         — "uf" | "national"
  year_range    — (ano_inicio, ano_fim) inclusive
"""

FTP_HOST = "ftp.datasus.gov.br"

UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
    "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
    "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]

# ---------------------------------------------------------------------------
# SIM — /dissemin/publicos/SIM/CID10/
#   DORES/  → DO{UF}{YYYY}.dbc      por UF, anual, 4 dígitos
#   DOFET/  → DO{TYPE}{YY}.dbc      nacional, anual, 2 dígitos
#             tipos: EXT, FET, INF, MAT
# ---------------------------------------------------------------------------
SIM = {
    "description": "Sistema de Informações sobre Mortalidade",
    "ftp_base":    "/dissemin/publicos/SIM/CID10",

    # Documentação técnica e layouts de campos
    "docs": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOCS",
        "arquivos": {
            "Docs_Tabs_CID10.zip":       "Layouts, tabelas e dicionário de variáveis",
            "Estrutura_do_SIM_2025.pdf": "Estrutura atual dos arquivos (referência principal)",
            "Estrutura_SIM_Anterior.pdf": "Estrutura anterior — necessária para bases legadas",
        },
    },

    # Dados agregados tabulados
    "tab": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TAB",
        "arquivos": {
            "OBITOS_CID10_TAB.zip": "Óbitos agregados por CID-10 (série histórica tabulada)",
        },
    },

    # Tabelas de apoio (CID-10, municípios, ocupações, países, UFs)
    "tabelas": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TABELAS",
        "arquivos": {
            "CID10.DBF":      "Classificação Internacional de Doenças — CID-10",
            "CIDCAP10.DBF":   "Capítulos do CID-10",
            "CADMUN.DBF":     "Cadastro de municípios",
            "CADMUN.xls":     "Cadastro de municípios (formato Excel)",
            "TABOCUP.DBF":    "Tabela de ocupações (CBO)",
            "TABPAIS.DBF":    "Tabela de países",
            "TABUF.DBF":      "Tabela de unidades federativas",
        },
    },

    "uf": {
        "ftp_dir":     "/dissemin/publicos/SIM/CID10/DORES",
        "pattern":     "DO{UF}{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format":      "dbc",
        "scope":       "uf",
        "year_range":  (1996, 2024),
    },

    "special": {
        "ftp_dir":     "/dissemin/publicos/SIM/CID10/DOFET",
        "pattern":     "DO{TYPE}{YY}.dbc",
        "granularity": "year",
        "year_digits": 2,
        "format":      "dbc",
        "scope":       "national",
        "year_range":  (1996, 2024),
        "types": {
            "EXT": "Óbitos por causas externas",
            "FET": "Óbitos fetais",
            "INF": "Óbitos infantis",
            "MAT": "Óbitos maternos",
        },
    },
}

# ---------------------------------------------------------------------------
# SINASC — /dissemin/publicos/SINASC/NOV/DNRES/
#   DN{UF}{YYYY}.dbc    por UF, anual, 4 dígitos
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# SINAN — /dissemin/publicos/SINAN/DADOS/
#   FINAIS/{DISEASE}BR{YY}.dbc    dados consolidados
#   PRELIM/{DISEASE}BR{YY}.dbc    dados preliminares
# ---------------------------------------------------------------------------
SINAN = {
    "description":    "Sistema de Informações de Agravos de Notificação",
    "ftp_dir":        "/dissemin/publicos/SINAN/DADOS/FINAIS",
    "ftp_dir_prelim": "/dissemin/publicos/SINAN/DADOS/PRELIM",
    "pattern":        "{DISEASE}BR{YY}.dbc",
    "granularity":    "year",
    "year_digits":    2,
    "format":         "dbc",
    "scope":          "national",
    "diseases": {
        "ACBI": "Acidente por animal peçonhento",
        "ACGR": "Acidente de trabalho grave",
        "ANIM": "Acidente por animal (outros)",
        "ANTR": "Antraz (Carbúnculo)",
        "BOTU": "Botulismo",
        "CANC": "Câncer relacionado ao trabalho",
        "CHAG": "Doença de Chagas",
        "CHIK": "Chikungunya",
        "COLE": "Cólera",
        "COQU": "Coqueluche",
        "DCRJ": "Doença de Creutzfeldt-Jakob",
        "DENG": "Dengue",
        "DERM": "Dermatose ocupacional",
        "DIFT": "Difteria",
        "ESPO": "Esporotricose",
        "ESQU": "Esquistossomose",
        "FMAC": "Febre maculosa",
        "FTIF": "Febre tifoide",
        "HANS": "Hanseníase",
        "HANT": "Hantavirose",
        "IEXO": "Intoxicação exógena",
        "LEIV": "Leishmaniose visceral",
        "LEPT": "Leptospirose",
        "LERD": "LER/DORT",
        "LTA":  "Leishmaniose tegumentar americana",
        "MALA": "Malária",
        "MENI": "Meningite",
        "MENT": "Transtorno mental relacionado ao trabalho",
        "NTRA": "Noma (Cancrum oris)",
        "PAIR": "Perda auditiva induzida por ruído",
        "PEST": "Peste",
        "PFAN": "Paralisia flácida aguda / Poliomielite",
        "PNEU": "Pneumoconiose",
        "RAIV": "Raiva humana",
        "ROTA": "Rotavírus",
        "SDTA": "Surto de doença transmitida por alimento",
        "TETA": "Tétano acidental",
        "TETN": "Tétano neonatal",
        "TOXC": "Toxoplasmose congênita",
        "TOXG": "Toxoplasmose gestacional",
        "TRAC": "Tracoma",
        "TUBE": "Tuberculose",
        "VIOL": "Violência doméstica / sexual / autoprovocada",
        "ZIKA": "Zika vírus",
    },
}

# ---------------------------------------------------------------------------
# SIHSUS — /dissemin/publicos/SIHSUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    por UF, mensal, 2 dígitos
#   Prefixo principal: RD (AIH Reduzida — registro de internação)
# ---------------------------------------------------------------------------
SIHSUS = {
    "description": "Sistema de Informações Hospitalares do SUS",
    "ftp_dir":     "/dissemin/publicos/SIHSUS/200801_/Dados",
    "ftp_dir_old": "/dissemin/publicos/SIHSUS/199201_200712",
    "pattern":     "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2008, 2025),
    "prefixes": {
        "RD": "AIH reduzida (internações — dado principal)",
        "SP": "Serviços profissionais",
        "RJ": "AIH rejeitada",
        "ER": "AIH com erro",
        "CM": "Comunicação de movimento",
        "CH": "Dados nacionais agregados",
    },
}

# ---------------------------------------------------------------------------
# SIASUS — /dissemin/publicos/SIASUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    por UF, mensal, 2 dígitos
#   Prefixo principal: AB (BPA — Boletim de Produção Ambulatorial)
# ---------------------------------------------------------------------------
SIASUS = {
    "description": "Sistema de Informações Ambulatoriais do SUS",
    "ftp_dir":     "/dissemin/publicos/SIASUS/200801_/Dados",
    "ftp_dir_old": "/dissemin/publicos/SIASUS/199407_200712",
    "pattern":     "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2008, 2025),
    "prefixes": {
        "AB":  "BPA — Boletim de Produção Ambulatorial (dado principal)",
        "AM":  "APAC de Medicamentos",
        "AN":  "APAC de Nefrologia",
        "AQ":  "APAC de Quimioterapia",
        "AR":  "APAC de Radioterapia",
        "BI":  "BPA individualizado",
        "PA":  "Produção ambulatorial (formato antigo)",
        "PS":  "RAAS Psicossocial",
        "SAD": "RAAS Atenção Domiciliar",
    },
}

# ---------------------------------------------------------------------------
# CNES — /dissemin/publicos/CNES/200508_/Dados/
#   {TYPE}/{TYPE}{UF}{YY}{MM}.dbc    por UF, mensal, 2 dígitos
#   Subtype principal: ST (Estabelecimentos)
# ---------------------------------------------------------------------------
CNES = {
    "description": "Cadastro Nacional de Estabelecimentos de Saúde",
    "ftp_base":    "/dissemin/publicos/CNES/200508_/Dados",
    "pattern":     "{TYPE}/{TYPE}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2005, 2025),
    "subtypes": {
        "ST": "Estabelecimentos (dado principal)",
        "DC": "Dados complementares",
        "EE": "Equipamentos",
        "EF": "Centros cirúrgicos / obstétricos",
        "EP": "Equipes de saúde",
        "EQ": "Equipamentos e produções",
        "GM": "Gestão e metas",
        "HB": "Habilitações",
        "IN": "Incentivos",
        "LT": "Leitos",
        "PF": "Profissionais",
        "RC": "Regras contratuais",
        "SR": "Serviços especializados",
    },
}

# ---------------------------------------------------------------------------
# PNI — /dissemin/publicos/PNI/DADOS/
#   DPNI{UF}{YY}.DBF    por UF, anual, 2 dígitos
#   Formato DBF puro (sem compressão blast) — usar dbfread, não pyreaddbc
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# IBGE/POP — /dissemin/publicos/IBGE/POP/
#   POPBR{YY}.zip    nacional, anual, 2 dígitos
# ---------------------------------------------------------------------------
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
