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
    "AC",
    "AL",
    "AM",
    "AP",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MG",
    "MS",
    "MT",
    "PA",
    "PB",
    "PE",
    "PI",
    "PR",
    "RJ",
    "RN",
    "RO",
    "RR",
    "RS",
    "SC",
    "SE",
    "SP",
    "TO",
]

# ---------------------------------------------------------------------------
# SIM — /dissemin/publicos/SIM/CID10/
#   DORES/  → DO{UF}{YYYY}.dbc      by UF, annual, 4 digits
#   DOFET/  → DO{TYPE}{YY}.dbc      national, annual, 2 digits
#             types: EXT, FET, INF, MAT
# ---------------------------------------------------------------------------
SIM = {
    "description": "Mortality Information System",
    "ftp_base": "/dissemin/publicos/SIM/CID10",
    # Technical documentation and field layouts
    "docs": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOCS",
        "files": {
            "Docs_Tabs_CID10.zip": "Layouts, tables and variable dictionary",
            "Estrutura_do_SIM_2025.pdf": "Current file structure (main reference)",
            "Estrutura_SIM_Anterior.pdf": "Previous structure — required for legacy datasets",
        },
    },
    # Aggregated tabulated data
    "tab": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TAB",
        "files": {
            "OBITOS_CID10_TAB.zip": "Deaths aggregated by ICD-10 (tabulated historical series)",
        },
    },
    # Support tables (ICD-10, municipalities, occupations, countries, UFs)
    "tables": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/TABELAS",
        "files": {
            "CID10.DBF": "International Classification of Diseases — ICD-10",
            "CIDCAP10.DBF": "ICD-10 chapters",
            "CADMUN.DBF": "Municipality registry",
            "CADMUN.xls": "Municipality registry (Excel format)",
            "TABOCUP.DBF": "Occupations table (CBO)",
            "TABPAIS.DBF": "Countries table",
            "TABUF.DBF": "Federative units table",
        },
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
    "special": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOFET",
        "pattern": "DO{TYPE}{YY}.dbc",
        "granularity": "year",
        "year_digits": 2,
        "format": "dbc",
        "scope": "national",
        "year_range": (1996, 2024),
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
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern": "DN{UF}{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format": "dbc",
        "scope": "uf",
        "year_range": (1996, 2022),
    },
    # National aggregate — incomplete series (only 2014–2017 confirmed on FTP)
    "national": {
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern": "DNBR{YYYY}.dbc",
        "granularity": "year",
        "year_digits": 4,
        "format": "dbc",
        "scope": "national",
        "year_range": (2014, 2017),
    },
    # Exception/supplementary files — one-off, not a regular series
    "exceptions": {
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DNRES",
        "pattern": "DNEX{YYYY}.dbc",
        "format": "dbc",
        "note": "One-off files with supplementary records. Confirmed: DNEX2021.dbc.",
    },
    # Technical documentation — exact FTP path to confirm (not mapped yet)
    "docs": {
        "ftp_dir": "/dissemin/publicos/SINASC/NOV/DOCS",
        "files": {
            "Estrutura_SINASC_para_CD.pdf": "File structure (legacy CD-ROM format)",
            "Legislacao_PDF.pdf": "Legislation related to SINASC",
            "NASC98.HLP": "Legacy system help file (1998)",
            "Portaria.pdf": "Regulatory ordinance",
        },
        "note": "FTP path not confirmed — DOCS directory not mapped yet.",
    },
}

# ---------------------------------------------------------------------------
# SINAN — /dissemin/publicos/SINAN/DADOS/
#   FINAIS/{DISEASE}BR{YY}.dbc    consolidated data
#   PRELIM/{DISEASE}BR{YY}.dbc    preliminary data
#   DOCS/                         technical documentation (path to confirm)
# ---------------------------------------------------------------------------
SINAN = {
    "description": "Notifiable Diseases Information System",
    "ftp_dir": "/dissemin/publicos/SINAN/DADOS/FINAIS",
    "ftp_dir_prelim": "/dissemin/publicos/SINAN/DADOS/PRELIM",
    "pattern": "{DISEASE}BR{YY}.dbc",
    "granularity": "year",
    "year_digits": 2,
    "format": "dbc",
    "scope": "national",
    "diseases": {
        "ACBI": "Venomous animal accident",
        "ACGR": "Serious occupational accident",
        "ANIM": "Animal accident (other)",
        "ANTR": "Anthrax",
        "BOTU": "Botulism",
        "CANC": "Work-related cancer",
        "CHAG": "Chagas disease",
        "CHIK": "Chikungunya",
        "COLE": "Cholera",
        "COQU": "Whooping cough (Pertussis)",
        "DCRJ": "Creutzfeldt-Jakob disease",
        "DENG": "Dengue",
        "DERM": "Occupational dermatosis",
        "DIFT": "Diphtheria",
        "ESPO": "Sporotrichosis",
        "ESQU": "Schistosomiasis",
        "FMAC": "Spotted fever (Rickettsia)",
        "FTIF": "Typhoid fever",
        "HANS": "Leprosy (Hansen's disease)",
        "HANT": "Hantavirus",
        "IEXO": "Exogenous poisoning",
        "LEIV": "Visceral leishmaniasis",
        "LEPT": "Leptospirosis",
        "LERD": "Work-related musculoskeletal disorder (RSI/WMSD)",
        "LTA": "American tegumentary leishmaniasis",
        "MALA": "Malaria",
        "MENI": "Meningitis",
        "MENT": "Work-related mental disorder",
        "NTRA": "Noma (Cancrum oris)",
        "PAIR": "Noise-induced hearing loss",
        "PEST": "Plague",
        "PFAN": "Acute flaccid paralysis / Poliomyelitis",
        "PNEU": "Pneumoconiosis",
        "RAIV": "Human rabies",
        "ROTA": "Rotavirus",
        "SDTA": "Foodborne disease outbreak",
        "TETA": "Accidental tetanus",
        "TETN": "Neonatal tetanus",
        "TOXC": "Congenital toxoplasmosis",
        "TOXG": "Gestational toxoplasmosis",
        "TRAC": "Trachoma",
        "TUBE": "Tuberculosis",
        "VIOL": "Domestic / sexual / self-inflicted violence",
        "ZIKA": "Zika virus",
    },
    # Technical documentation — FTP path to confirm (not mapped yet)
    "docs": {
        "ftp_dir": "/dissemin/publicos/SINAN/DOCS",
        "files": {
            "Docs_TAB_SINAN.zip": "Layouts, tables and variable dictionary for all conditions",
            "POP_I_Acesso_a_Microdados_5.pdf": "Guide to accessing SINAN microdata",
            "POP_II_Descompactacao_expansao_conversao_3.pdf": "Guide to decompress and convert .dbc files",
            "POP_III_Instalacao_do_tabulador_TabWin_3.pdf": "Installation guide for TabWin (official tabulator)",
            "Nota_Tecnica_Doenca_de_Creutzfeldt-Jakob(DCJ).pdf": "Technical note — Creutzfeldt-Jakob disease",
            "Nota_Tecnica_Intoxicacao_Exogena.pdf": "Technical note — Exogenous poisoning",
            "Nota_Tecnica_Rotavirus.pdf": "Technical note — Rotavirus",
            "Nota_Tecnica_Surtos_de_DTA.pdf": "Technical note — Foodborne disease outbreaks",
            "Nota_Tecnica_Toxoplasmose.pdf": "Technical note — Toxoplasmosis",
        },
        "note": "FTP path not confirmed — DOCS directory not mapped yet.",
    },
}

# ---------------------------------------------------------------------------
# SIHSUS — /dissemin/publicos/SIHSUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    by UF, monthly, 2 digits
#   Main prefix: RD (Reduced AIH — hospitalization record)
#   Exception: CH and CM use fixed BR (national scope), not {UF}
# ---------------------------------------------------------------------------
SIHSUS = {
    "description": "Hospital Information System of SUS",
    "ftp_dir": "/dissemin/publicos/SIHSUS/200801_/Dados",
    "ftp_dir_old": "/dissemin/publicos/SIHSUS/199201_200712",
    "pattern": "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format": "dbc",
    "scope": "uf",
    "year_range": (2008, 2026),
    "prefixes": {
        "RD": "Reduced AIH (hospitalizations — main record)",
        "SP": "Professional services",
        "RJ": "Rejected AIH",
        "ER": "AIH with error",
    },
    # CH and CM use fixed BR scope — pattern: {PREFIX}BR{YY}{MM}.dbc
    "national_prefixes": {
        "CH": "National header (aggregated data)",
        "CM": "Movement report",
    },
}

# ---------------------------------------------------------------------------
# SIASUS — /dissemin/publicos/SIASUS/200801_/Dados/
#   {PREFIX}{UF}{YY}{MM}.dbc    by UF, monthly, 2 digits
#   Main prefix: PA (Outpatient Production)
# ---------------------------------------------------------------------------
SIASUS = {
    "description": "Outpatient Information System of SUS",
    "ftp_dir": "/dissemin/publicos/SIASUS/200801_/Dados",
    "ftp_dir_old": "/dissemin/publicos/SIASUS/199407_200712",
    "pattern": "{PREFIX}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format": "dbc",
    "scope": "uf",
    "year_range": (2008, 2026),
    "prefixes": {
        "PA": ("Outpatient Production (BPA)", 2008, 2026),
        "BI": ("Individualized BPA", 2008, 2026),
        "AD": ("APAC — Miscellaneous Reports", 2008, 2026),
        "AM": ("APAC — Medications", 2008, 2026),
        "AMP": ("APAC — Standardized Medications", 2020, 2026),
        "AQ": ("APAC — Chemotherapy", 2008, 2026),
        "AR": ("APAC — Radiotherapy", 2008, 2026),
        "ACF": ("APAC — Arteriovenous Fistula Construction", 2014, 2026),
        "ATD": ("APAC — Dialysis Treatment", 2014, 2026),
        "PS": ("RAAS — Psychosocial Care", 2013, 2026),
        "AB": ("APAC — Post-Bariatric Surgery Follow-up (new)", 2025, 2026),
        "ABO": ("APAC — Post-Bariatric Surgery Follow-up (legacy)", 2015, 2018),
        "AN": ("APAC — Nephrology (discontinued, replaced by ATD)", 2008, 2014),
        "SAD": ("RAAS — Home Care (discontinued)", 2013, 2015),
    },
}

# ---------------------------------------------------------------------------
# CNES — /dissemin/publicos/CNES/200508_/Dados/
#   {TYPE}/{TYPE}{UF}{YY}{MM}.dbc    by UF, monthly, 2 digits
#   File is 2 levels inside Dados/: e.g. ST/STSP2501.dbc
#   Main subtype: ST (Health Facilities)
# ---------------------------------------------------------------------------
CNES = {
    "description": "National Registry of Health Facilities",
    "ftp_base": "/dissemin/publicos/CNES/200508_/Dados",
    "pattern": "{TYPE}/{TYPE}{UF}{YY}{MM}.dbc",
    "granularity": "month",
    "year_digits": 2,
    "format": "dbc",
    "scope": "uf",
    "subtypes": {
        "ST": ("Health facilities (main record)", 2005, 2026),
        "PF": ("Healthcare professionals", 2005, 2026),
        "DC": ("Complementary data", 2005, 2026),
        "EQ": ("Equipment", 2005, 2026),
        "SR": ("Specialized services", 2005, 2026),
        "LT": ("Hospital beds", 2005, 2026),
        "HB": ("Accreditations", 2007, 2026),
        "EF": ("Surgical and obstetric centers", 2007, 2026),
        "EP": ("Health teams", 2007, 2026),
        "RC": ("Contractual rules", 2007, 2026),
        "IN": ("Incentives", 2007, 2026),
        "GM": ("Management and targets", 2014, 2026),
        "EE": ("Equipment and production (discontinued)", 2007, 2019),
    },
}

# ---------------------------------------------------------------------------
# PNI — /dissemin/publicos/PNI/DADOS/
#   DPNI{UF}{YY}.DBF    by UF, annual, 2 digits
#   Plain DBF format (no blast compression) — use dbfread, not pyreaddbc
# ---------------------------------------------------------------------------
PNI = {
    "description": "National Immunization Program",
    "ftp_dir": "/dissemin/publicos/PNI/DADOS",
    "pattern": "DPNI{UF}{YY}.DBF",
    "granularity": "year",
    "year_digits": 2,
    "format": "dbf",
    "scope": "uf",
    "year_range": (1994, 2019),
}

# ---------------------------------------------------------------------------
# IBGE/POP — /dissemin/publicos/IBGE/POP/
#   POPBR{YY}.zip    national, annual, 2 digits
# ---------------------------------------------------------------------------
IBGE_POP = {
    "description": "IBGE Population Estimates",
    "ftp_dir": "/dissemin/publicos/IBGE/POP",
    "pattern": "POPBR{YY}.zip",
    "granularity": "year",
    "year_digits": 2,
    "format": "zip",
    "scope": "national",
    "year_range": (1980, 2012),
}

ALL_SYSTEMS = {
    "SIM": SIM,
    "SINASC": SINASC,
    "SINAN": SINAN,
    "SIHSUS": SIHSUS,
    "SIASUS": SIASUS,
    "CNES": CNES,
    "PNI": PNI,
    "IBGE_POP": IBGE_POP,
}