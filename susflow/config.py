"""
susflow/config.py
=================
Metadata for all DATASUS systems.

Fields for each system:
    ftp_dir       — absolute path on the FTP
    pattern       — name pattern ({UF}, {YYYY}, {YY}, {PREFIX}, {DISEASE}, {TYPE})
    granularity   — "year" | "month"
    year_digits   — 2 or 4
    format        — "dbc" | "dbf" | "zip"
    scope         — "uf" | "national"
    year_range    — (start_year, end_year) inclusive
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
    "description": "Mortality Information System",
    "ftp_base":    "/dissemin/publicos/SIM/CID10",

    # Technical documentation and field layouts
    "docs": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOCS",
        "arquivos": {
            "Docs_Tabs_CID10.zip":       "Layouts, tables and variable dictionary",
            "Estrutura_do_SIM_2025.pdf": "Current file structure (main reference)",
            "Estrutura_SIM_Anterior.pdf": "Previous structure — needed for legacy datasets",
        },
    },

    # Aggregated tabulated data
    "tab": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TAB",
        "arquivos": {
            "OBITOS_CID10_TAB.zip": "Deaths aggregated by ICD-10 (tabulated historical series)",
        },
    },

    # Support tables (ICD-10, municipalities, occupations, countries, UFs)
    "tabelas": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TABELAS",
        "arquivos": {
            "CID10.DBF":      "International Classification of Diseases — ICD-10",
            "CIDCAP10.DBF":   "ICD-10 chapters",
            "CADMUN.DBF":     "Municipality registry",
            "CADMUN.xls":     "Municipality registry (Excel format)",
            "TABOCUP.DBF":    "Occupations table (CBO)",
            "TABPAIS.DBF":    "Countries table",
            "TABUF.DBF":      "Federative units table",
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
            "EXT": "Deaths by external causes",
            "FET": "Fetal deaths",
            "INF": "Infant deaths",
            "MAT": "Maternal deaths",
        },
    },
}

# ---------------------------------------------------------------------------
# SINASC — /dissemin/publicos/SINASC/NOV/
#   DNRES/  → DN{UF}{YYYY}.dbc      by UF, annual, 4 digits
#   DNRES/  → DNBR{YYYY}.dbc        national aggregate (2014–2017 only)
#   DNRES/  → DNEX{YYYY}.dbc        exceptions/supplementary (one-off, e.g. 2021)
#   DOCS/   → technical documentation  (path to confirm — not mapped yet)
# ---------------------------------------------------------------------------
SINASC = {
    "description": "Live Births Information System",

    "uf": {
        "ftp_dir":     "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern":     "DN{UF}{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format":      "dbc",
        "scope":       "uf",
        "year_range":  (1996, 2022),
    },

    # National aggregate — incomplete series (only 2014–2017 confirmed on FTP)
    "nacional": {
        "ftp_dir":     "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern":     "DNBR{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format":      "dbc",
        "scope":       "national",
        "year_range":  (2014, 2017),
    },

    # Exception/supplementary files — one-off, not a regular series
    "excecoes": {
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern": "DNEX{YYYY}.dbc",
        "format":  "dbc",
        "nota":    "One-off files with supplementary records. Confirmed: DNEX2021.dbc.",
    },

    # Technical documentation — exact FTP path to confirm (not mapped yet)
    "docs": {
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DOCS",
        "arquivos": {
            "Estrutura_SINASC_para_CD.pdf": "File structure (legacy CD-ROM format)",
            "Legislacao_PDF.pdf":           "Legislation related to SINASC",
            "NASC98.HLP":                   "Legacy system help file (1998)",
            "Portaria.pdf":                 "Regulatory ordinance",
        },
        "nota": "FTP path not confirmed — DOCS directory not mapped yet.",
    },
}

# ---------------------------------------------------------------------------
# SINAN — /dissemin/publicos/SINAN/DADOS/
#   FINAIS/{DISEASE}BR{YY}.dbc    dados consolidados
#   PRELIM/{DISEASE}BR{YY}.dbc    dados preliminares
#   DOCS/                         documentação técnica (caminho a confirmar)
# ---------------------------------------------------------------------------
SINAN = {
    "description":    "Notifiable Diseases Information System",
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

    # Technical documentation — FTP path to confirm (not mapped yet)
    "docs": {
        "ftp_dir": "/dissemin/publicos/SINAN/DOCS",
        "arquivos": {
            "Docs_TAB_SINAN.zip":                              "Layouts, tables and variable dictionary for all conditions",
            "POP_I_Acesso_a_Microdados_5.pdf":                 "Guide to access SINAN microdata",
            "POP_II_Descompactacao_expansao_conversao_3.pdf":  "Guide to decompress and convert .dbc files",
            "POP_III_Instalacao_do_tabulador_TabWin_3.pdf":    "Installation guide for TabWin (official tabulator)",
            "Nota_Tecnica_Doenca_de_Creutzfeldt-Jakob(DCJ).pdf": "Technical note — Creutzfeldt-Jakob disease",
            "Nota_Tecnica_Intoxicacao_Exogena.pdf":            "Technical note — Exogenous poisoning",
            "Nota_Tecnica_Rotavirus.pdf":                      "Technical note — Rotavirus",
            "Nota_Tecnica_Surtos_de_DTA.pdf":                  "Technical note — Foodborne disease outbreaks",
            "Nota_Tecnica_Toxoplasmose.pdf":                   "Technical note — Toxoplasmosis",
        },
        "nota": "FTP path not confirmed — DOCS directory not mapped yet.",
    },
}

# ---------------------------------------------------------------------------
# SIHSUS — /dissemin/publicos/SIHSUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    by UF, monthly, 2 digits
#   Main prefix: RD (Reduced AIH — hospitalization record)
#   Exception: CH and CM use fixed BR (national scope), not {UF}
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
    "year_range":  (2008, 2026),
    "prefixes": {
        "RD": "AIH reduzida (internações — dado principal)",
        "SP": "Serviços profissionais",
        "RJ": "AIH rejeitada",
        "ER": "AIH com erro",
    },
    # CH e CM usam BR fixo — padrão: {PREFIX}BR{YY}{MM}.dbc
    "prefixes_nacionais": {
        "CH": "Cabeçalho nacional (dados agregados)",
        "CM": "Comunicação de movimento",
    },
}

# ---------------------------------------------------------------------------
# SIASUS — /dissemin/publicos/SIASUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    por UF, mensal, 2 dígitos
#   Prefixo principal: PA (Produção Ambulatorial)
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
    "year_range":  (2008, 2026),
    "prefixes": {
        "PA":  ("Produção Ambulatorial (BPA)",                          2008, 2026),
        "BI":  ("BPA Individualizado",                                  2008, 2026),
        "AD":  ("APAC de Laudos Diversos",                              2008, 2026),
        "AM":  ("APAC de Medicamentos",                                 2008, 2026),
        "AMP": ("APAC de Medicamentos Padronizados",                    2020, 2026),
        "AQ":  ("APAC de Quimioterapia",                                2008, 2026),
        "AR":  ("APAC de Radioterapia",                                 2008, 2026),
        "ACF": ("APAC Confecção de Fístula Arteriovenosa",              2014, 2026),
        "ATD": ("APAC Tratamento Dialítico",                            2014, 2026),
        "PS":  ("RAAS Psicossocial",                                    2013, 2026),
        "AB":  ("APAC Acompanhamento Pós Cirurgia Bariátrica (novo)",   2025, 2026),
        "ABO": ("APAC Acompanhamento Pós Cirurgia Bariátrica (legado)", 2015, 2018),
        "AN":  ("APAC de Nefrologia (encerrado, substituído por ATD)",  2008, 2014),
        "SAD": ("RAAS Atenção Domiciliar (encerrado)",                  2013, 2015),
    },
}

# ---------------------------------------------------------------------------
# CNES — /dissemin/publicos/CNES/200508_/Dados/
#   {TYPE}/{TYPE}{UF}{YY}{MM}.dbc    por UF, mensal, 2 dígitos
#   Arquivo fica 2 níveis dentro de Dados/: ex. ST/STSP2501.dbc
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
    "subtypes": {
        "ST": ("Estabelecimentos (dado principal)",          2005, 2026),
        "PF": ("Profissionais de saúde",                    2005, 2026),
        "DC": ("Dados complementares",                      2005, 2026),
        "EQ": ("Equipamentos",                              2005, 2026),
        "SR": ("Serviços especializados",                   2005, 2026),
        "LT": ("Leitos",                                    2005, 2026),
        "HB": ("Habilitações",                             2007, 2026),
        "EF": ("Centros cirúrgicos e obstétricos",          2007, 2026),
        "EP": ("Equipes de saúde",                          2007, 2026),
        "RC": ("Regras contratuais",                        2007, 2026),
        "IN": ("Incentivos",                                2007, 2026),
        "GM": ("Gestão e metas",                            2014, 2026),
        "EE": ("Equipamentos e produções (encerrado)",      2007, 2019),
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
