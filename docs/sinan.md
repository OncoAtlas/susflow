 # SINAN — Notifiable Diseases Information System

 FTP base: `ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/`

 ---

 ## Available data types

 | Type | Function | Returns | Description |
 |------|----------|---------|-------------|
 | Final data | `read(disease, year)` | `DataFrame` | Consolidated microdata for the disease |
 | Final data | `download(disease, year)` | `Path` | Raw `.dbc` file (final data) |
 | Preliminary data | `read(disease, year, preliminary=True)` | `DataFrame` | Data not yet consolidated |
 | Preliminary data | `download(disease, year, preliminary=True)` | `Path` | Raw `.dbc` file (preliminary) |
 | Documentation | `download_docs(file?)` | `Path / list[Path]` | Layouts, dictionary and technical notes |

 ---

 ## Disease data — `DADOS/FINAIS/` and `DADOS/PRELIM/`

 **File pattern:** `{DOENÇA}BR{YY}.dbc`  
 **Scope:** national (BR)  
 **Granularity:** annual, year with 2 digits

 ```python
 from susflow.systems import sinan

 # list all available diseases
 print(sinan.diseases())   # {code: description}

 # final data
 df = sinan.read(disease="DENG", year=2023)
 df = sinan.read(disease="TUBE", year=2022)

 # preliminary data for the current year
 df = sinan.read(disease="DENG", year=2024, preliminary=True)

 # download only the file
 path = sinan.download(disease="CHIK", year=2023)
 path = sinan.download(disease="HANS", year=2022, preliminary=True)

 # list available files
 sinan.list_files(disease="DENG")
 sinan.list_files(preliminary=True)
 ```

 ---

 ## Available diseases

 | Code | Disease | Coverage (finals) |
 |------|---------|-------------------|
 | `ACBI` | Animal envenomation accident | 2006–2019 |
 | `ACGR` | Severe occupational accident | 2006–2019 |
 | `ANIM` | Animal-related accident (others) | 2007–2022 |
 | `ANTR` | Anthrax | 2006–2023 |
 | `BOTU` | Botulism | 2007–2023 |
 | `CANC` | Work-related cancer | 2007–2019 |
 | `CHAG` | Chagas disease | 2000–2022 |
 | `CHIK` | Chikungunya | 2015–2024 |
 | `COLE` | Cholera | 2007–2022 |
 | `COQU` | Pertussis | 2007–2024 |
 | `DCRJ` | Creutzfeldt-Jakob disease | 2007–2022 |
 | `DENG` | Dengue | 2000–2024 |
 | `DERM` | Occupational dermatitis | 2006–2019 |
 | `DIFT` | Diphtheria | 2007–2023 |
 | `ESPO` | Sporotrichosis | 2013–2022 |
 | `ESQU` | Schistosomiasis | 2007–2019 |
 | `FMAC` | Spotted fever | 2007–2021 |
 | `FTIF` | Typhoid fever | 2007–2023 |
 | `HANS` | Leprosy | 2001–2023 |
 | `HANT` | Hantavirus | 1999–2024 |
 | `IEXO` | Exogenous intoxication | 2006–2022 |
 | `LEIV` | Visceral leishmaniasis | 2000–2024 |
 | `LEPT` | Leptospirosis | 2000–2024 |
 | `LERD` | Repetitive strain injuries (RSI) | 2006–2019 |
 | `LTA`  | American cutaneous leishmaniasis | 2000–2024 |
 | `MALA` | Malaria | 2004–2022 |
 | `MENI` | Meningitis | 2007–2022 |
 | `MENT` | Mental disorder related to work | 2006–2019 |
 | `NTRA` | Noma (Cancrum oris) | 2010–2021 |
 | `PAIR` | Noise-induced hearing loss | 2006–2019 |
 | `PEST` | Plague | 2007–2024 |
 | `PFAN` | Acute flaccid paralysis / Poliomyelitis | 2007–2019 |
 | `PNEU` | Pneumoconiosis | 2006–2019 |
 | `RAIV` | Human rabies | 2007–2023 |
 | `ROTA` | Rotavirus | 2009–2024 |
 | `SDTA` | Foodborne disease outbreak | 2007–2018 |
 | `TETA` | Accidental tetanus | 2007–2023 |
 | `TETN` | Neonatal tetanus | 2014–2021 |
 | `TOXC` | Congenital toxoplasmosis | 2019–2023 |
 | `TOXG` | Gestational toxoplasmosis | 2019–2023 |
 | `TRAC` | Trachoma | 2009–2021 |
 | `TUBE` | Tuberculosis | 2001–2019 |
 | `VIOL` | Domestic/sexual/self-inflicted violence | 2009–2024 |
 | `ZIKA` | Zika virus | 2016–2024 |

 > Preliminary data are available for recent years — use `preliminar=True`.
 > Exact coverage varies by disease. Use `sinan.listar(doenca="CODE")` to confirm available years.

 ---

 ## Variables common to all diseases

 | Variable | Type | Description |
 |----------|------|-------------|
 | `DT_NOTIFIC` | str | Notification date (YYYY-MM-DD) |
 | `DT_SIN_PRI` | str | Onset date of first symptoms |
 | `SEM_NOT` | str | Epidemiological week of notification |
 | `NU_ANO` | str | Year of notification |
 | `ID_MUNICIP` | str | IBGE code of notification municipality |
 | `ID_REGIONA` | str | Health region code |
 | `ID_UNIDADE` | str | Notifying health unit code |
 | `NU_IDADE_N` | str | Encoded age (1st digit = unit) |
 | `CS_SEXO` | str | Sex (M=Male, F=Female, I=Ignored) |
 | `CS_RACA` | str | Race/color |
 | `CS_ESCOL_N` | str | Education |
 | `SG_UF_NOT` | str | Notification UF |
 | `ID_MN_RESI` | str | IBGE code of residence municipality |
 | `SG_UF` | str | Residence UF |
 | `CLASSI_FIN` | str | Final case classification |
 | `CRITERIO` | str | Confirmation criterion |
 | `EVOLUCAO` | str | Case outcome (recovered, death, etc.) |
 | `DT_ENCERRA` | str | Case closing date |

 > Each disease has specific additional variables. See `Docs_TAB_SINAN.zip` for the full dictionary per disease.

 ---

 ## Technical documentation — `DOCS/`

 > **Note:** the FTP path for this directory has not been fully confirmed by direct mapping. If download fails, run `python tools/mapear_ftp.py --alvo /dissemin/publicos/SINAN` to locate the correct directory.

 | File | Description | When to use |
 |------|-------------|-------------|
 | `Docs_TAB_SINAN.zip` | Layouts and variable dictionary for all diseases | Main reference to understand fields |
 | `POP_I_Acesso_a_Microdados_5.pdf` | Guide to access microdata | First step for new users |
 | `POP_II_Descompactacao_expansao_conversao_3.pdf` | Guide to decompress and convert `.dbc` | Reference for manual processing |
 | `POP_III_Instalacao_do_tabulador_TabWin_3.pdf` | Guide to install TabWin | Use of DATASUS official tabulator |
 | `Nota_Tecnica_Doenca_de_Creutzfeldt-Jakob(DCJ).pdf` | Technical note — Creutzfeldt-Jakob disease | DCRJ analysis |
 | `Nota_Tecnica_Intoxicacao_Exogena.pdf` | Technical note — Exogenous intoxication | IEXO analysis |
 | `Nota_Tecnica_Rotavirus.pdf` | Technical note — Rotavirus | ROTA analysis |
 | `Nota_Tecnica_Surtos_de_DTA.pdf` | Technical note — DTA outbreaks | SDTA analysis |
 | `Nota_Tecnica_Toxoplasmose.pdf` | Technical note — Toxoplasmosis | TOXC and TOXG analysis |

 ```python
 # see what's available
 print(sinan.list_docs())

 # download the main dictionary (reference for all diseases)
 path = sinan.download_docs("Docs_TAB_SINAN.zip")

 # download a technical note for a specific disease
 path = sinan.download_docs("Nota_Tecnica_Intoxicacao_Exogena.pdf")

 # download microdata access guides
 path = sinan.download_docs("POP_I_Acesso_a_Microdados_5.pdf")

 # download all at once
 paths = sinan.download_docs()

 # save to a specific folder
 paths = sinan.download_docs("Docs_TAB_SINAN.zip", destination="/my/data/sinan")
 ```

 ---

 ## Recommended workflow

 ```
 1. Explore what's available
    print(sinan.diseases())                 ← lists all available diseases
    sinan.list_files(disease="DENG")        ← available years for dengue
    sinan.list_files(preliminary=True)      ← preliminary data available

 2. Download data
    df = sinan.read(disease="DENG", year=2023)                       ← final data
    df = sinan.read(disease="DENG", year=2024, preliminary=True)     ← preliminary

 3. Download references to understand the fields
    sinan.download_docs("Docs_TAB_SINAN.zip")              ← full dictionary
    sinan.download_docs("Nota_Tecnica_Rotavirus.pdf")      ← specific disease note
 ```

 ---

 ## Notes

 - `.dbc` files are DBF files compressed with the proprietary **blast** (PKWARE) algorithm. The library decompresses them automatically via `pyreaddbc`.
 - The year in the filename uses **2 digits**: `DENGBR23.dbc` = 2023 data.
 - The `NU_IDADE_N` field uses a custom encoding: the 1st digit indicates the unit (1=hours, 2=days, 3=months, 4=years) and the next 2 digits the value.
 - `CLASSI_FIN` classifies the case: 1=Confirmed, 2=Discarded, 3=Inconclusive (varies by disease).
 - Preliminary data (`PRELIM/`) are updated continuously and may differ from final data. Use final data for historical analyses.
 - Some diseases have short historical coverage (e.g. CHIK since 2015, ZIKA since 2016) because they are emerging diseases.
 - To map municipalities to names, use `CADMUN.DBF` available in SIM (`sim.download_tables("CADMUN.DBF")`).