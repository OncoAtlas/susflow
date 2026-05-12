"""
susflow/config.py
=================
Mapa completo dos sistemas do DATASUS levantado por exploração direta do FTP.
Cada entrada define tudo que a biblioteca precisa para listar e baixar arquivos.

Legenda dos campos:
  ftp_dir       — caminho absoluto no FTP onde ficam os arquivos
  pattern       — padrão do nome de arquivo (use {PREFIX}, {UF}, {YEAR}, {MONTH})
  granularity   — "year" | "month"  (arquivo por ano ou por mês)
  year_digits   — 2 ou 4 dígitos no nome do arquivo
  format        — "dbc" | "dbf" | "zip"  (formato do arquivo no FTP)
  scope         — "uf" | "national"  (arquivo por UF ou dado nacional agregado)
  description   — descrição do sistema
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
# SIM — Sistema de Informações sobre Mortalidade
# ---------------------------------------------------------------------------
#
# Estrutura real confirmada em /dissemin/publicos/SIM/CID10/:
#
#   DOFET/   → categorias especiais (fetal, infantil, materno, causas externas)
#              padrão: DO{TYPE}{YY}.dbc   ex: DOEXT24.dbc, DOINF24.dbc
#              escopo: NACIONAL, granularidade: ANUAL, ano 2 dígitos
#              tipos: EXT (causas externas), FET (fetal), INF (infantil), MAT (materno)
#
#   DBASE/   → NÃO EXISTE (caminho legado documentado incorretamente)
#              Os arquivos por UF estão diretamente em CID10/ ou em subpasta ainda
#              a confirmar. Rodar explorar_sim.py para mapear.
#
# AÇÃO NECESSÁRIA: explorar /dissemin/publicos/SIM/CID10/ para encontrar
# os arquivos DO{UF}{YYYY}.dbc (ex: DOSP2023.dbc).
# ---------------------------------------------------------------------------
SIM = {
    "description": "Sistema de Informações sobre Mortalidade",
    "ftp_base": "/dissemin/publicos/SIM/CID10",

    # Subcategorias especiais — dados nacionais por ano
    "special": {
        "ftp_dir": "/dissemin/publicos/SIM/CID10/DOFET",
        "types": {
            "EXT": "Óbitos por causas externas",
            "FET": "Óbitos fetais",
            "INF": "Óbitos infantis",
            "MAT": "Óbitos maternos",
        },
        # Padrão: DO{TYPE}{YY}.dbc  ex: DOEXT24.dbc
        "pattern":     "DO{TYPE}{YY}.dbc",
        "granularity": "year",
        "year_digits": 2,
        "format":      "dbc",
        "scope":       "national",
        "year_range":  (1996, 2024),
    },

    # Dados por UF — caminho a confirmar com explorar_sim.py
    "uf": {
        "ftp_dir":     "PENDENTE — rodar explorar_sim.py",
        "pattern":     "DO{UF}{YYYY}.dbc",   # ex: DOSP2023.dbc
        "granularity": "year",
        "year_digits": 4,
        "format":      "dbc",
        "scope":       "uf",
    },
}

# ---------------------------------------------------------------------------
# SINASC — Sistema de Informações sobre Nascidos Vivos
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/SINASC/NOV/DNRES/
# Padrão:     DN{UF}{YYYY}.dbc     ex: DNSP2022.dbc
# Cobertura:  1996 → 2022, todas as UFs
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
# SINAN — Sistema de Informações de Agravos de Notificação
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/SINAN/DADOS/FINAIS/
# Padrão:     {DISEASE}BR{YY}.dbc   ex: DENGBR23.dbc
# Escopo: NACIONAL (BR), granularidade ANUAL, ano 2 dígitos
# ---------------------------------------------------------------------------
SINAN = {
    "description": "Sistema de Informações de Agravos de Notificação",
    "ftp_dir":     "/dissemin/publicos/SINAN/DADOS/FINAIS",
    "ftp_dir_prelim": "/dissemin/publicos/SINAN/DADOS/PRELIM",
    "pattern":     "{DISEASE}BR{YY}.dbc",
    "granularity": "year",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "national",

    # Dicionário completo das doenças — código: descrição
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
        "LTAN": "Leishmaniose tegumentar americana",
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
# SIHSUS — Sistema de Informações Hospitalares
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/SIHSUS/200801_/Dados/
# Padrão:     {PREFIX}{UF}{YY}{MM}.dbc   ex: RDSP2301.dbc
# Granularidade: MENSAL, ano 2 dígitos
#
# Prefixos identificados:
#   RD = AIH Reduzida (principal — registro de internação)
#   SP = Serviços Profissionais
#   RJ = AIH Rejeitada
#   ER = AIH com Erro
#   CM = Comunicação de Internação
#   CH = Dados nacionais (BR) — escopo diferente
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
# SIASUS — Sistema de Informações Ambulatoriais
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/SIASUS/200801_/Dados/
# Padrão:     {PREFIX}{UF}{YY}{MM}.dbc   ex: ABAC2501.dbc
# Granularidade: MENSAL, ano 2 dígitos
#
# Prefixos: AB = Produção ambulatorial (BPA — Boletim de Produção Ambulatorial)
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
        "AB": "BPA — Boletim de Produção Ambulatorial (dado principal)",
        "AM": "APAC de Medicamentos",
        "AN": "APAC de Nefrologia",
        "AQ": "APAC de Quimioterapia",
        "AR": "APAC de Radioterapia",
        "BI": "BPA individualizado",
        "PA": "Produção ambulatorial (formato antigo)",
        "PS": "RAAS Psicossocial",
        "SAD": "RAAS Atenção Domiciliar",
    },
}

# ---------------------------------------------------------------------------
# CNES — Cadastro Nacional de Estabelecimentos de Saúde
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/CNES/200508_/Dados/
# Estrutura: um subdiretório por tipo de arquivo (ST, DC, EE, etc.)
# Padrão provável: {TYPE}/{TYPE}{UF}{YY}{MM}.dbc   ex: ST/STSP2501.dbc
# Granularidade: MENSAL
# AÇÃO: os arquivos ficam 2 níveis dentro de Dados/ — explorar um subdir.
# ---------------------------------------------------------------------------
CNES = {
    "description": "Cadastro Nacional de Estabelecimentos de Saúde",
    "ftp_base":    "/dissemin/publicos/CNES/200508_/Dados",
    "granularity": "month",
    "year_digits": 2,
    "format":      "dbc",
    "scope":       "uf",
    "year_range":  (2005, 2025),

    # Subdirs identificados — cada um é um tipo de dado cadastral
    "subtypes": {
        "ST": "Estabelecimentos (dado principal — identificação e localização)",
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
# PNI — Programa Nacional de Imunizações
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/PNI/DADOS/
# Padrão:     DPNI{UF}{YY}.DBF   ex: DPNISP00.DBF
# Formato: DBF (não DBC — já é DBF puro, sem compressão blast)
# Granularidade: ANUAL, ano 2 dígitos
# Cobertura: 1994 → 2019
# ---------------------------------------------------------------------------
PNI = {
    "description": "Programa Nacional de Imunizações",
    "ftp_dir":     "/dissemin/publicos/PNI/DADOS",
    "pattern":     "DPNI{UF}{YY}.DBF",
    "granularity": "year",
    "year_digits": 2,
    "format":      "dbf",   # ATENÇÃO: DBF puro, não DBC — leitura diferente
    "scope":       "uf",
    "year_range":  (1994, 2019),
}

# ---------------------------------------------------------------------------
# IBGE/POP — Estimativas populacionais (denominadores para taxas)
# ---------------------------------------------------------------------------
#
# Confirmado: /dissemin/publicos/IBGE/POP/
# Padrão:     POPBR{YY}.zip   ex: POPBR10.zip
# Formato: ZIP (descomprime para DBF/CSV)
# Cobertura: 1980 → 2012
# ---------------------------------------------------------------------------
IBGE_POP = {
    "description": "Estimativas populacionais IBGE (para cálculo de taxas)",
    "ftp_dir":     "/dissemin/publicos/IBGE/POP",
    "pattern":     "POPBR{YY}.zip",
    "granularity": "year",
    "year_digits": 2,
    "format":      "zip",
    "scope":       "national",
    "year_range":  (1980, 2012),
}

# ---------------------------------------------------------------------------
# Índice geral — facilita iterar sobre todos os sistemas
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