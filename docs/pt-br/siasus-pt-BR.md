 # SIASUS — Sistema de Informações Ambulatoriais do SUS

 Base FTP: `ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/`

 ---

 ## Tipos de dados disponíveis

 | Tipo | Função | Retorno | Descrição |
 |------|--------|---------|-----------|
 | Por UF | `read(uf, year, month)` | `DataFrame` | Microdados ambulatoriais de uma UF |
 | Por UF | `download(uf, year, month)` | `Path` | Arquivo `.dbc` bruto |

 ---

 ## Prefixos disponíveis

 **Padrão de arquivo:** `{PREFIX}{UF}{YY}{MM}.dbc`  
 **Granularidade:** mensal / por UF

 ```python
 from susflow.systems import siasus

 # ver todos os prefixos disponíveis
 print(siasus.prefixes())

 # Produção Ambulatorial — prefixo padrão
 df = siasus.read(uf="SP", year=2023, month=1)
 df = siasus.read(uf="SP", year=2023, month=1, prefix="PA")

 # outros prefixos
 df = siasus.read(uf="SP", year=2023, month=1, prefix="AQ")   # quimioterapia
 df = siasus.read(uf="RJ", year=2023, month=6, prefix="ATD")  # diálise

 # só baixar
 path = siasus.download(uf="SP", year=2023, month=1)
 path = siasus.download(uf="MG", year=2023, month=3, prefix="AM")

 # listar arquivos disponíveis
 siasus.list_files()                         # todos os PA
 siasus.list_files(uf="SP")                  # PA de SP
 siasus.list_files(uf="SP", prefix="AQ")    # quimioterapia de SP
 ```

 ### Prefixos ativos

 | Prefixo | Arquivo exemplo | Conteúdo | Cobertura |
 |---------|----------------|----------|-----------|
 | `PA` | `PASP2301.dbc` | **Produção Ambulatorial (BPA)** — dado principal | 2008–2026 |
 | `BI` | `BISP2301.dbc` | BPA Individualizado | 2008–2026 |
 | `AD` | `ADSP2301.dbc` | APAC de Laudos Diversos | 2008–2026 |
 | `AM` | `AMSP2301.dbc` | APAC de Medicamentos | 2008–2026 |
 | `AMP` | `AMPSP2301.dbc` | APAC de Medicamentos Padronizados | 2020–2026 |
 | `AQ` | `AQSP2301.dbc` | APAC de Quimioterapia | 2008–2026 |
 | `AR` | `ARSP2301.dbc` | APAC de Radioterapia | 2008–2026 |
 | `ACF` | `ACFSP1408.dbc` | APAC Confecção de Fístula Arteriovenosa | 2014–2026 |
 | `ATD` | `ATDSP1408.dbc` | APAC Tratamento Dialítico | 2014–2026 |
 | `PS` | `PSSP1305.dbc` | RAAS Psicossocial | 2013–2026 |
 | `AB` | `ABSP2501.dbc` | APAC Acompanhamento Pós Cirurgia Bariátrica (novo) | 2025–2026 |

 ### Prefixos encerrados (ainda disponíveis no FTP)

 | Prefixo | Arquivo exemplo | Conteúdo | Cobertura | Observação |
 |---------|----------------|----------|-----------|------------|
 | `ABO` | `ABOSP1502.dbc` | APAC Pós Cirurgia Bariátrica (legado) | 2015–2018 | Substituído por `AB` |
 | `AN` | `ANSP0801.dbc` | APAC de Nefrologia | 2008–2014 | Substituído por `ATD` |
 | `SAD` | `SADSP1307.dbc` | RAAS Atenção Domiciliar | 2013–2015 | Encerrado |

 > A validação de ano respeita a cobertura individual de cada prefixo. Tentar baixar `AN` para 2020 levanta erro.

 ---

 ## Diferença entre PA e BI

 - `PA` (BPA Consolidado) — cada linha representa o total de procedimentos realizados por um estabelecimento em um mês. Dado agregado.
 - `BI` (BPA Individualizado) — cada linha representa um atendimento individual. Dado de microdados com identificação do paciente.

 Para análises individuais (perfil de pacientes, trajetória de cuidado), use `BI`. Para análises de produção por estabelecimento, use `PA`.

 ---

 ## Diferença entre AM e AMP

 - `AM` — APAC de Medicamentos (todos os medicamentos do componente especializado)
 - `AMP` — APAC de Medicamentos Padronizados (subconjunto específico, disponível a partir de 2020)

 ---

 ## Principais variáveis do DataFrame (PA — Produção Ambulatorial)

 | Variável | Tipo | Descrição |
 |----------|------|-----------|
 | `PA_CODUNI` | str | Código CNES do estabelecimento |
 | `PA_GESTAO` | str | Código da gestão |
 | `PA_CONDIC` | str | Condição de atendimento |
 | `PA_UFMUN` | str | Código IBGE do município |
 | `PA_REGCT` | str | Registro contratual |
 | `PA_INCOUT` | str | Incremento outros |
 | `PA_INCURG` | str | Incremento urgência |
 | `PA_TPUPS` | str | Tipo de UPS |
 | `PA_TIPPRE` | str | Tipo de prestador |
 | `PA_MN_IND` | str | Modalidade/natureza |
 | `PA_CNPJCPF` | str | CNPJ/CPF do estabelecimento |
 | `PA_CNPJMNT` | str | CNPJ mantenedora |
 | `PA_CNPJ_CC` | str | CNPJ contrato |
 | `PA_MVM` | str | Mês/ano de movimento (AAAAMM) |
 | `PA_CMP` | str | Mês/ano de competência (AAAAMM) |
 | `PA_PROC_ID` | str | Código do procedimento (SIGTAP) |
 | `PA_TPFIN` | str | Tipo de financiamento |
 | `PA_SUBFIN` | str | Subfonte de financiamento |
 | `PA_NIVCPL` | str | Nível de complexidade |
 | `PA_DOCORIG` | str | Documento de origem |
 | `PA_AUTORIZ` | str | Número de autorização |
 | `PA_CNSMED` | str | CNS do profissional |
 | `PA_CBOCOD` | str | CBO do profissional |
 | `PA_MOTSAI` | str | Motivo de saída |
 | `PA_OBITO` | str | Indicador de óbito |
 | `PA_ENCERR` | str | Indicador de encerramento |
 | `PA_PERMAN` | str | Indicador de permanência |
 | `PA_ALTA` | str | Indicador de alta |
 | `PA_TRANSF` | str | Indicador de transferência |
 | `PA_QTDPRO` | str | Quantidade produzida |
 | `PA_QTDAPR` | str | Quantidade aprovada |
 | `PA_VALPRO` | float | Valor produzido (R$) |
 | `PA_VALAPR` | float | Valor aprovado (R$) |

 > Para o dicionário completo de variáveis por prefixo, consulte a documentação oficial do DATASUS (SIGTAP).

 ---

 ## Fluxo recomendado

 ```
 1. Explorar o que existe
    print(siasus.prefixes())             ← todos os prefixos e descrições
    siasus.list_files(uf="SP")               ← arquivos PA de SP disponíveis
    siasus.list_files(uf="SP", prefix="AQ") ← quimioterapia de SP

 2. Baixar os dados
    df = siasus.read(uf="SP", year=2023, month=1)              ← produção ambulatorial
    df = siasus.read(uf="SP", year=2023, month=1, prefix="AQ") ← quimioterapia

 3. Combinar meses em série histórica
    import pandas as pd
    dfs = [siasus.read(uf="SP", year=2023, month=m) for m in range(1, 13)]
    df_ano = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notas

 - Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
 - O ano usa **2 dígitos** e o mês **2 dígitos com zero à esquerda**: `PASP2301.dbc` = SP, janeiro de 2023.
 - Cada prefixo tem sua própria cobertura temporal. A validação de ano é feita por prefixo — tentar baixar `AN` para 2020 levanta erro com a cobertura correta.
 - `PA` é o arquivo mais volumoso — estados grandes (SP, RJ, MG) podem ter centenas de MB por mês.
 - Procedimentos são identificados pelo código SIGTAP (`PA_PROC_ID`). Consulte a tabela SIGTAP para descrições.
 - Para cruzar municípios com nomes, use `CADMUN.DBF` disponível no SIM (`sim.download_tables("CADMUN.DBF")`).
 - Para cruzar estabelecimentos com dados cadastrais, use o CNES.
