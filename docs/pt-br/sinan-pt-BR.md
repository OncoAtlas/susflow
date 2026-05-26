 # SINAN — Sistema de Informações de Agravos de Notificação

 Base FTP: `ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/`

 ---

 ## Tipos de dados disponíveis

 | Tipo | Função | Retorno | Descrição |
 |------|--------|---------|-----------|
 | Dados finais | `ler(doenca, ano)` | `DataFrame` | Microdados consolidados do agravo |
 | Dados finais | `baixar(doenca, ano)` | `Path` | Arquivo `.dbc` bruto (dados finais) |
 | Dados preliminares | `ler(doenca, ano, preliminar=True)` | `DataFrame` | Dados ainda não consolidados |
 | Dados preliminares | `baixar(doenca, ano, preliminar=True)` | `Path` | Arquivo `.dbc` bruto (preliminar) |
 | Documentação | `baixar_docs(arquivo?)` | `Path / list[Path]` | Layouts, dicionário e notas técnicas |

 ---

 ## Dados de agravos — `DADOS/FINAIS/` e `DADOS/PRELIM/`

 **Padrão de arquivo:** `{DOENÇA}BR{YY}.dbc`  
 **Escopo:** nacional (BR)  
 **Granularidade:** anual, ano com 2 dígitos

 ```python
 from susflow.systems import sinan

 # ver todas as doenças disponíveis
 print(sinan.doencas())   # {código: descrição}

 # dados finais
 df = sinan.ler(doenca="DENG", ano=2023)
 df = sinan.ler(doenca="TUBE", ano=2022)

 # dados preliminares do ano corrente
 df = sinan.ler(doenca="DENG", ano=2024, preliminar=True)

 # só baixar o arquivo
 path = sinan.baixar(doenca="CHIK", ano=2023)
 path = sinan.baixar(doenca="HANS", ano=2022, preliminar=True)

 # listar arquivos disponíveis
 sinan.listar(doenca="DENG")
 sinan.listar(preliminar=True)
 ```

 ---

 ## Agravos disponíveis

 | Código | Agravo | Cobertura (finais) |
 |--------|--------|--------------------|
 | `ACBI` | Acidente por animal peçonhento | 2006–2019 |
 | `ACGR` | Acidente de trabalho grave | 2006–2019 |
 | `ANIM` | Acidente por animal (outros) | 2007–2022 |
 | `ANTR` | Antraz (Carbúnculo) | 2006–2023 |
 | `BOTU` | Botulismo | 2007–2023 |
 | `CANC` | Câncer relacionado ao trabalho | 2007–2019 |
 | `CHAG` | Doença de Chagas | 2000–2022 |
 | `CHIK` | Chikungunya | 2015–2024 |
 | `COLE` | Cólera | 2007–2022 |
 | `COQU` | Coqueluche | 2007–2024 |
 | `DCRJ` | Doença de Creutzfeldt-Jakob | 2007–2022 |
 | `DENG` | Dengue | 2000–2024 |
 | `DERM` | Dermatose ocupacional | 2006–2019 |
 | `DIFT` | Difteria | 2007–2023 |
 | `ESPO` | Esporotricose | 2013–2022 |
 | `ESQU` | Esquistossomose | 2007–2019 |
 | `FMAC` | Febre maculosa | 2007–2021 |
 | `FTIF` | Febre tifoide | 2007–2023 |
 | `HANS` | Hanseníase | 2001–2023 |
 | `HANT` | Hantavirose | 1999–2024 |
 | `IEXO` | Intoxicação exógena | 2006–2022 |
 | `LEIV` | Leishmaniose visceral | 2000–2024 |
 | `LEPT` | Leptospirose | 2000–2024 |
 | `LERD` | LER/DORT | 2006–2019 |
 | `LTA`  | Leishmaniose tegumentar americana | 2000–2024 |
 | `MALA` | Malária | 2004–2022 |
 | `MENI` | Meningite | 2007–2022 |
 | `MENT` | Transtorno mental relacionado ao trabalho | 2006–2019 |
 | `NTRA` | Noma (Cancrum oris) | 2010–2021 |
 | `PAIR` | Perda auditiva induzida por ruído | 2006–2019 |
 | `PEST` | Peste | 2007–2024 |
 | `PFAN` | Paralisia flácida aguda / Poliomielite | 2007–2019 |
 | `PNEU` | Pneumoconiose | 2006–2019 |
 | `RAIV` | Raiva humana | 2007–2023 |
 | `ROTA` | Rotavírus | 2009–2024 |
 | `SDTA` | Surto de doença transmitida por alimento | 2007–2018 |
 | `TETA` | Tétano acidental | 2007–2023 |
 | `TETN` | Tétano neonatal | 2014–2021 |
 | `TOXC` | Toxoplasmose congênita | 2019–2023 |
 | `TOXG` | Toxoplasmose gestacional | 2019–2023 |
 | `TRAC` | Tracoma | 2009–2021 |
 | `TUBE` | Tuberculose | 2001–2019 |
 | `VIOL` | Violência doméstica / sexual / autoprovocada | 2009–2024 |
 | `ZIKA` | Zika vírus | 2016–2024 |

 > Dados preliminares disponíveis para anos mais recentes — use `preliminar=True`.  
 > A cobertura exata por agravo varia. Use `sinan.listar(doenca="CÓDIGO")` para confirmar os anos disponíveis.

 ---

 ## Variáveis comuns a todos os agravos

 | Variável | Tipo | Descrição |
 |----------|------|-----------|
 | `DT_NOTIFIC` | str | Data de notificação (AAAA-MM-DD) |
 | `DT_SIN_PRI` | str | Data dos primeiros sintomas |
 | `SEM_NOT` | str | Semana epidemiológica de notificação |
 | `NU_ANO` | str | Ano de notificação |
 | `ID_MUNICIP` | str | Código IBGE do município de notificação |
 | `ID_REGIONA` | str | Código da regional de saúde |
 | `ID_UNIDADE` | str | Código da unidade de saúde notificante |
 | `NU_IDADE_N` | str | Idade codificada (1º dígito = unidade) |
 | `CS_SEXO` | str | Sexo (M=Masculino, F=Feminino, I=Ignorado) |
 | `CS_RACA` | str | Raça/cor |
 | `CS_ESCOL_N` | str | Escolaridade |
 | `SG_UF_NOT` | str | UF de notificação |
 | `ID_MN_RESI` | str | Código IBGE do município de residência |
 | `SG_UF` | str | UF de residência |
 | `CLASSI_FIN` | str | Classificação final do caso |
 | `CRITERIO` | str | Critério de confirmação |
 | `EVOLUCAO` | str | Evolução do caso (cura, óbito, etc.) |
 | `DT_ENCERRA` | str | Data de encerramento do caso |

 > Cada agravo possui variáveis específicas adicionais. Consulte `Docs_TAB_SINAN.zip` para o dicionário completo por agravo.

 ---

 ## Documentação técnica — `DOCS/`

 > **Atenção:** o caminho FTP deste diretório ainda não foi confirmado por mapeamento direto. Se o download falhar, rode `python tools/mapear_ftp.py --alvo /dissemin/publicos/SINAN` para localizar o diretório correto.

 | Arquivo | Descrição | Quando usar |
 |---------|-----------|-------------|
 | `Docs_TAB_SINAN.zip` | Layouts e dicionário de variáveis de todos os agravos | Referência principal para entender os campos |
 | `POP_I_Acesso_a_Microdados_5.pdf` | Guia de acesso aos microdados | Primeiro passo para novos usuários |
 | `POP_II_Descompactacao_expansao_conversao_3.pdf` | Guia de descompactação e conversão dos `.dbc` | Referência para processamento manual |
 | `POP_III_Instalacao_do_tabulador_TabWin_3.pdf` | Guia de instalação do TabWin | Uso do tabulador oficial do DATASUS |
 | `Nota_Tecnica_Doenca_de_Creutzfeldt-Jakob(DCJ).pdf` | Nota técnica — Doença de Creutzfeldt-Jakob | Análise do agravo DCRJ |
 | `Nota_Tecnica_Intoxicacao_Exogena.pdf` | Nota técnica — Intoxicação Exógena | Análise do agravo IEXO |
 | `Nota_Tecnica_Rotavirus.pdf` | Nota técnica — Rotavírus | Análise do agravo ROTA |
 | `Nota_Tecnica_Surtos_de_DTA.pdf` | Nota técnica — Surtos de DTA | Análise do agravo SDTA |
 | `Nota_Tecnica_Toxoplasmose.pdf` | Nota técnica — Toxoplasmose | Análise dos agravos TOXC e TOXG |

 ```python
 # ver o que está disponível
 print(sinan.listar_docs())

 # baixar o dicionário principal (referência para todos os agravos)
 path = sinan.baixar_docs("Docs_TAB_SINAN.zip")

 # baixar nota técnica de um agravo específico
 path = sinan.baixar_docs("Nota_Tecnica_Intoxicacao_Exogena.pdf")

 # baixar os guias de acesso a microdados
 path = sinan.baixar_docs("POP_I_Acesso_a_Microdados_5.pdf")

 # baixar todos de uma vez
 paths = sinan.baixar_docs()

 # salvar em pasta específica
 path = sinan.baixar_docs("Docs_TAB_SINAN.zip", destino="/meus/dados/sinan")
 ```

 ---

 ## Fluxo recomendado

 ```
 1. Explorar o que existe
    print(sinan.doencas())              ← lista todos os agravos disponíveis
    sinan.listar(doenca="DENG")         ← anos disponíveis para dengue
    sinan.listar(preliminar=True)       ← dados preliminares disponíveis

 2. Baixar os dados
    df = sinan.ler(doenca="DENG", ano=2023)              ← dados finais
    df = sinan.ler(doenca="DENG", ano=2024, preliminar=True)  ← preliminar

 3. Baixar referências para entender os campos
    sinan.baixar_docs("Docs_TAB_SINAN.zip")              ← dicionário completo
    sinan.baixar_docs("Nota_Tecnica_Rotavirus.pdf")      ← nota do agravo específico
 ```

 ---

 ## Notas

 - Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
 - O ano no nome do arquivo usa **2 dígitos**: `DENGBR23.dbc` = dados de 2023.
 - O campo `NU_IDADE_N` usa codificação própria: o 1º dígito indica a unidade (1=horas, 2=dias, 3=meses, 4=anos) e os 2 seguintes o valor.
 - `CLASSI_FIN` classifica o caso: 1=Confirmado, 2=Descartado, 3=Inconclusivo (varia por agravo).
 - Dados preliminares (`PRELIM/`) são atualizados continuamente e podem diferir dos finais. Use dados finais para análises históricas.
 - Alguns agravos têm cobertura histórica curta (ex: CHIK desde 2015, ZIKA desde 2016) por serem doenças emergentes.
 - Para cruzar municípios com nomes, use `CADMUN.DBF` disponível no SIM (`sim.baixar_tabelas("CADMUN.DBF")`).
