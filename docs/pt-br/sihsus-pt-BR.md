 # SIHSUS — Sistema de Informações Hospitalares do SUS

 Base FTP: `ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/`

 ---

 ## Tipos de dados disponíveis

 | Tipo | Função | Retorno | Descrição |
 |------|--------|---------|-----------|
 | Por UF | `ler(uf, ano, mes)` | `DataFrame` | Microdados de internações de uma UF |
 | Por UF | `baixar(uf, ano, mes)` | `Path` | Arquivo `.dbc` bruto por UF |
 | Nacional | `ler_nacional(ano, mes)` | `DataFrame` | Dados nacionais agregados (CH ou CM) |
 | Nacional | `baixar_nacional(ano, mes)` | `Path` | Arquivo `.dbc` nacional |

 ---

 ## Dados por UF

 **Padrão de arquivo:** `{PREFIX}{UF}{YY}{MM}.dbc`  
 **Cobertura:** 2008–2026, todas as 27 UFs  
 **Granularidade:** mensal

 ```python
 from susflow.systems import sihsus

 # ver prefixos disponíveis
 print(sihsus.prefixos())

 # AIH Reduzida — dado principal (prefixo padrão: RD)
 df = sihsus.ler(uf="SP", ano=2023, mes=1)
 df = sihsus.ler(uf="RJ", ano=2022, mes=12)

 # outros prefixos
 df = sihsus.ler(uf="MG", ano=2023, mes=6, prefixo="SP")  # serviços profissionais
 df = sihsus.ler(uf="BA", ano=2023, mes=3, prefixo="RJ")  # AIH rejeitada

 # só baixar o arquivo
 path = sihsus.baixar(uf="SP", ano=2023, mes=1)
 path = sihsus.baixar(uf="SP", ano=2023, mes=1, prefixo="ER")

 # listar arquivos disponíveis
 sihsus.listar()                        # todos os RD
 sihsus.listar(uf="SP")                 # RD de SP
 sihsus.listar(uf="SP", prefixo="SP")   # serviços profissionais de SP
 ```

 ### Prefixos por UF

 | Prefixo | Arquivo exemplo | Conteúdo |
 |---------|----------------|----------|
 | `RD` | `RDSP2301.dbc` | **AIH Reduzida — dado principal** (registro de internação) |
 | `SP` | `SPSP2301.dbc` | Serviços profissionais complementares |
 | `RJ` | `RJSP2301.dbc` | AIH rejeitada (não aprovada para pagamento) |
 | `ER` | `ERSP2301.dbc` | AIH com erro de preenchimento |

 ---

 ## Dados nacionais (CH e CM)

 **Padrão de arquivo:** `{PREFIX}BR{YY}{MM}.dbc`  
 **Escopo:** nacional (BR fixo — não há versão por UF)

 ```python
 # ver prefixos nacionais
 print(sihsus.prefixos_nacionais())

 # cabeçalho nacional (prefixo padrão: CH)
 df = sihsus.ler_nacional(ano=2023, mes=1)
 path = sihsus.baixar_nacional(ano=2023, mes=1)

 # comunicação de movimento
 df = sihsus.ler_nacional(ano=2023, mes=1, prefixo="CM")

 # listar disponíveis
 sihsus.listar_nacional()               # CH (padrão)
 sihsus.listar_nacional(prefixo="CM")   # CM
 ```

 ### Prefixos nacionais

 | Prefixo | Arquivo exemplo | Conteúdo |
 |---------|----------------|----------|
 | `CH` | `CHBR2301.dbc` | Cabeçalho nacional — dados agregados de referência |
 | `CM` | `CMBR2301.dbc` | Comunicação de movimento hospitalar |

 ---

 ## Principais variáveis do DataFrame (AIH Reduzida — RD)

 | Variável | Tipo | Descrição |
 |----------|------|-----------|
 | `N_AIH` | str | Número da AIH |
 | `DT_INTER` | str | Data de internação (AAAAMM DD) |
 | `DT_SAIDA` | str | Data de saída |
 | `DIAG_PRINC` | str | Diagnóstico principal (CID-10) |
 | `DIAG_SECUN` | str | Diagnóstico secundário (CID-10) |
 | `PROC_REA` | str | Procedimento realizado |
 | `PROC_SOLIC` | str | Procedimento solicitado |
 | `VAL_TOT` | float | Valor total da AIH (R$) |
 | `VAL_UTI` | float | Valor de UTI |
 | `QT_DIARIAS` | str | Quantidade de diárias |
 | `MORTE` | str | Indicador de óbito (0=não, 1=sim) |
 | `SEXO` | str | Sexo do paciente |
 | `IDADE` | str | Idade do paciente |
 | `MUNIC_RES` | str | Código IBGE do município de residência |
 | `MUNIC_MOV` | str | Código IBGE do município de atendimento |
 | `CNES` | str | Código CNES do estabelecimento |
 | `GESTAO` | str | Tipo de gestão (municipal/estadual) |
 | `COMPLEX` | str | Complexidade do atendimento |
 | `INSTRU` | str | Instrução do paciente |
 | `CID_ASSO` | str | CID associado |
 | `CID_MORTE` | str | CID da causa de morte |
 | `NATUREZA` | str | Natureza jurídica do estabelecimento |
 | `RUBRICA` | str | Rubrica orçamentária |

 -> Para o dicionário completo de variáveis, consulte a documentação oficial do DATASUS.

 ---

 ## Fluxo recomendado

 ```
 1. Explorar o que existe
    sihsus.listar(uf="SP")              ← arquivos RD de SP disponíveis
    sihsus.listar_nacional()            ← arquivos CH nacionais

 2. Baixar os dados
    df = sihsus.ler(uf="SP", ano=2023, mes=1)       ← internações SP jan/2023
    df = sihsus.ler_nacional(ano=2023, mes=1)        ← cabeçalho nacional

 3. Combinar meses em série histórica
    import pandas as pd
    dfs = [sihsus.ler(uf="SP", ano=2023, mes=m) for m in range(1, 13)]
    df_ano = pd.concat(dfs, ignore_index=True)
 ```

 ---

 ## Notas

 - Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
 - O ano no nome do arquivo usa **2 dígitos** e o mês usa **2 dígitos com zero à esquerda**: `RDSP2301.dbc` = SP, janeiro de 2023.
 - Os arquivos `RD` são os microdados principais — cada linha é uma internação (AIH).
 - `SP`, `RJ` e `ER` são complementares ao `RD` e compartilham o campo `N_AIH` para cruzamento.
 - `CH` e `CM` têm escopo nacional (`BR`) e não existem por UF.
 - Arquivos grandes: `RD` de estados populosos (SP, RJ, MG) podem ter dezenas de MB por mês.
 - Para cruzar municípios com nomes, use `CADMUN.DBF` disponível no SIM (`sim.baixar_tabelas("CADMUN.DBF")`).
 - Para cruzar estabelecimentos com dados cadastrais, use o CNES.
