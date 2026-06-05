 # Sumário de padrões de arquivos do DATASUS (FTP)

 Base: `ftp.datasus.gov.br`

 ## 1. SIM – Sistema de Informação sobre Mortalidade

 **Caminho base:** `/dissemin/publicos/SIM/CID10/`

 | Subpasta  | Padrão                                             | Descrição                                                   | Exemplo                        |
 | --------- | -------------------------------------------------- | ----------------------------------------------------------- | ------------------------------ |
 | `DOFET`   | `DOEXT<AA>.DBC`                                    | Óbitos de adultos – formato estendido (AA = ano, 2 dígitos) | `DOEXT00.DBC`, `DOEXT23.DBC`   |
 | `DOFET`   | `DOFET<AA>.DBC`                                    | Óbitos fetais – formato reduzido                            | `DOFET00.dbc`, `DOFET23.dbc`   |
 | `DOFET`   | `DOINF<AA>.DBC`                                    | Óbitos infantis (0‑1 ano)                                   | `DOINF00.DBC`, `DOINF23.dbc`   |
 | `DOFET`   | `DOMAT<AA>.DBC`                                    | Óbitos maternos                                             | `DOMAT00.DBC`, `DOMAT23.dbc`   |
 | `DOFET`   | `DOREXT<AA>.DBC`                                   | Óbitos de residentes em outras UFs? (arquivos pequenos)     | `DOREXT13.dbc`, `DOREXT23.dbc` |
 | `DORES`   | `DO<UF><AAAA>.DBC`                                 | Óbitos por UF + ano completo (4 dígitos)                    | `DOAC2000.dbc`, `DOBR2024.dbc` |
 | `DORES`   | `DO<UF><AA>.DBC`                                   | Óbitos por UF + ano (2 dígitos – primeiros anos)            | `DOAC1996.dbc`                 |
 | `DOCS`    | `Docs_Tabs_CID10.zip`, `Estrutura_do_SIM_2025.pdf` | Documentação, layouts e manuais                             |                                |
 | `TAB`     | `OBITOS_CID10_TAB.zip`, `CNVS_CID10_v2019.rar`     | Dados agregados e tabelas auxiliares                        |                                |
 | `TABELAS` | `CID10.DBF`, `TABUF.DBF`, `CADMUN.DBF`             | Tabelas de apoio (CID10, UF, municípios)                    |                                |

 ## 2. SINASC – Sistema de Informação sobre Nascidos Vivos

 **Caminho base:** `/dissemin/publicos/SINASC/NOV/DNRES/`

 | Padrão             | Descrição                                          | Exemplo                                            |
 | ------------------ | -------------------------------------------------- | -------------------------------------------------- |
 | `DN<UF><AAAA>.DBC` | Nascidos vivos por UF + ano (4 dígitos)            | `DNAC1996.DBC`, `DNRJ2022.dbc`                     |
 | `DN<UF><AA>.DBC`   | Nascidos vivos por UF + ano (2 dígitos)            | `DNAC96.DBC` (não aparece no seu mapa mas é comum) |
 | `DNBR<AAAA>.DBC`   | Nascidos vivos – Brasil (agregado nacional)        | `DNBR2014.dbc`                                     |
 | `DNEX<AAAA>.dbc`   | Exceções / dados suplementares (arquivos pequenos) | `DNEX2021.dbc`                                     |

 _Observação: Os primeiros anos usavam dois dígitos; a partir de 2000 passaram a usar quatro._

 ## 3. SINAN – Sistema de Informação de Agravos de Notificação

 **Caminho base:** `/dissemin/publicos/SINAN/DADOS/` (subpastas `FINAIS/` e `PRELIM/`)

 ### Padrão geral:

 - Dados finais: `FINAIS/<AGRAVO><UF><AA>.DBC` ou `<AGRAVO>BR<AA>.DBC`
 - Dados preliminares: `PRELIM/<AGRAVO><UF><AA>.DBC` (mesma estrutura)

 ### Principais agravos (prefixos):

 | Prefixo | Agravo                                    | Exemplo        |
 | ------- | ----------------------------------------- | -------------- |
 | `ACBI`  | Acidente de trabalho com vínculo          | `ACBIBR07.dbc` |
 | `ACGR`  | Acidente de trabalho grave                | `ACGRBR07.dbc` |
 | `ANIM`  | Animais peçonhentos                       | `ANIMBR07.dbc` |
 | `ANTR`  | Antraz (Carbúnculo)                       | `ANTRBR07.dbc` |
 | `BOTU`  | Botulismo                                 | `BOTUBR07.dbc` |
 | `CANC`  | Câncer (notificação)                      | `CANCBR07.dbc` |
 | `CHAG`  | Doença de Chagas                          | `CHAGBR00.dbc` |
 | `CHIK`  | Chikungunya                               | `CHIKBR15.dbc` |
 | `COQU`  | Coqueluche                                | `COQUBR07.dbc` |
 | `DENG`  | Dengue                                    | `DENGBR00.dbc` |
 | `DERM`  | Dermatoses ocupacionais                   | `DERMBR06.dbc` |
 | `DIFT`  | Difteria                                  | `DIFTBR07.dbc` |
 | `ESQU`  | Esquistossomose                           | `ESQUBR07.dbc` |
 | `FMAC`  | Febre Maculosa                            | `FMACBR07.dbc` |
 | `FTIF`  | Febre Tifoide                             | `FTIFBR07.dbc` |
 | `HANS`  | Hanseníase                                | `HANSBR01.dbc` |
 | `HANT`  | Hantavirose                               | `HANTBR00.dbc` |
 | `IEXO`  | Intoxicação exógena (outros)              | `IEXOBR06.dbc` |
 | `LEIV`  | Leishmaniose visceral                     | `LEIVBR00.dbc` |
 | `LEPT`  | Leptospirose                              | `LEPTBR00.dbc` |
 | `LTA`   | Leishmaniose tegumentar americana         | `LTANBR00.dbc` |
 | `MALA`  | Malária                                   | `MALABR04.dbc` |
 | `MENI`  | Meningite                                 | `MENIBR07.dbc` |
 | `MENT`  | Meningite (outros?)                       | `MENTBR06.dbc` |
 | `NTRA`  | N特拉 – Intoxicação por agrotóxicos?      | `NTRABR10.dbc` |
 | `PAIR`  | Paralisia flácida aguda                   | `PAIRBR06.dbc` |
 | `PEST`  | Peste                                     | `PESTBR07.dbc` |
 | `PFAN`  | Febre amarela (pan)                       | `PFANBR07.dbc` |
 | `PNEU`  | Pneumonia (SAR)                           | `PNEUBR06.dbc` |
 | `RAIV`  | Raiva humana                              | `RAIVBR07.dbc` |
 | `ROTA`  | Rotavírus                                 | `ROTABR09.dbc` |
 | `SDTA`  | Síndrome da toxemia da gestação? (outros) | `SDTABR07.dbc` |
 | `TETA`  | Tétano acidental                          | `TETABR07.dbc` |
 | `TOXC`  | Intoxicação por cádmio? (específico)      | `TOXCBR19.dbc` |
 | `TRAC`  | Tracoma                                   | `TRACBR09.dbc` |
 | `TUBE`  | Tuberculose                               | `TUBEBR01.dbc` |
 | `VIOL`  | Violência doméstica e outras              | `VIOLBR09.dbc` |
 | `ZIKA`  | Zika vírus                                | `ZIKABR16.dbc` |

 _Nota: `UF` pode ser `BR` (Brasil) ou a sigla do estado (ex: `SP`, `RJ`)._

 ## 4. SIH/SIHSUS – Sistema de Informações Hospitalares

 **Caminho base:** `/dissemin/publicos/SIHSUS/200801_/Dados/`

 ### Padrões de nome (mais comuns):

 | Padrão               | Descrição                                                   | Exemplo                   |
 | -------------------- | ----------------------------------------------------------- | ------------------------- |
 | `RD<UF><AA><MM>.dbc` | **Resumo de Internação** – principal arquivo de internações | `RDSP0801.dbc` (2008/jan) |
 | `ER<UF><AA><MM>.dbc` | Complemento de serviços profissionais (ER)                  | `ERSP0801.dbc`            |
 | `SP<UF><AA><MM>.dbc` | Complemento (serviços profissionais – antigo)               | `SPAC0801.dbc`            |
 | `RJ<UF><AA><MM>.dbc` | Complemento – aparece para vários estados                   | `RJSP0801.dbc`            |
 | `CHBR<AA><MM>.dbc`   | Cabeçalho? (arquivos pequenos)                              | `CHBR1901.dbc`            |
 | `CMBR<AA><MM>.dbc`   | Complemento? (arquivos pequenos)                            | `CMBR1901.dbc`            |

 **Observação:** `<AA>` = dois últimos dígitos do ano; `<MM>` = mês (01 a 12).

 ## 5. SIA/SIASUS – Sistema de Informações Ambulatoriais

 **Caminho base:** `/dissemin/publicos/SIASUS/200801_/Dados/`

 | Padrão                | Descrição                                                                         | Exemplo                        |
 | --------------------- | --------------------------------------------------------------------------------- | ------------------------------ |
 | `AB<UF><AA><MM>.dbc`  | **Produção ambulatorial** (APAC, BPA, etc.) – arquivo principal                   | `ABSP0801.dbc`, `ABAC2501.dbc` |
 | `ACF<UF><AA><MM>.dbc` | Autorização de procedimentos de alto custo / complexidade                         | `ACFAL1408.dbc`                |
 | `PA<UF><AA><MM>.dbc`  | Outro formato de produção ambulatorial (não aparece no seu mapeamento, mas comum) | `PASPB0801.dbc`                |

 **Estrutura do nome:**

 - `AB`, `PA`, `ACF` = tipo de arquivo
 - `UF` = sigla do estado (ex: `SP`, `RJ`, `BR`)
 - `AA` = ano (dois últimos dígitos)
 - `MM` = mês

 ## 6. Outros padrões complementares

 ### Arquivos de documentação e layout

 - Geralmente estão nas subpastas `DOCS/` ou `TABELAS/` dentro de cada sistema.
 - Extensões: `.pdf`, `.zip`, `.rar`, `.DBF`.

 ### Tabelas de apoio

 - **UF:** `TABUF.DBF`
 - **Municípios:** `CADMUN.DBF` ou `Tabela-de-Municipios-informacoes.pdf`
 - **CID10:** `CID10.DBF`
 - **CID10 capítulos:** `CIDCAP10.DBF`
 - **CBO (ocupações):** `TABOCUP.DBF`
 - **Países:** `TABPAIS.DBF`

 ## IBGE – Estimativas Populacionais (IBGE)

**Caminho base:** `/dissemin/publicos/IBGE/POP/`

| Padrão           | Descrição                                      | Exemplo          |
| ---------------- | ---------------------------------------------- | ---------------- |
| `POPBR<AA>.zip`  | Estimativas populacionais – Brasil (nacional, ano com 2 dígitos) | `POPBR00.zip`, `POPBR12.zip` |

**Cobertura:** 1980–2012 (anual, apenas nacional)

**Observações:**
- Arquivos ZIP contendo um .DBC/.DBF com contagens populacionais (por faixas etárias, sexo etc.).
- Use `ibge_pop.read(ano)` ou `download(ano)` (via `susflow.systems.ibge_pop` ou CLI `susflow ibge`).
- Sem quebra por estado (UF) — agregado nacional apenas.

---

## 7. Dicas para consulta e uso

 - **Prefixo é a chave**: identifique o sistema pelo prefixo do nome (ex: `DO` = SIM, `DN` = SINASC, `RD`/`ER` = SIH, `AB` = SIA).
 - **Ano**: a maioria usa dois dígitos até 1999, depois quatro dígitos ou dois+dois (ano+mês).
 - **UF**: `BR` = Brasil; siglas de dois caracteres para os estados.
 - **Extensão `.dbc`** → arquivo compactado (DBF + compressão proprietária). Use `dbc2dbf` ou bibliotecas como `pysus`.
 - **Arquivos preliminares**: em `SINAN/DADOS/PRELIM/` – dados ainda não consolidados.
 - **Arquivos finais**: em `FINAIS/` (SINAN) ou nos diretórios raiz dos sistemas.

 ## 8. Exemplos de consulta por sistema

 | Quero...                                                  | Padrão a procurar                    | Caminho típico                             |
 | --------------------------------------------------------- | ------------------------------------ | ------------------------------------------ |
 | Óbitos do Rio de Janeiro em 2023                          | `DORJ2023.DBC`                       | `/dissemin/publicos/SIM/CID10/DORES/`      |
 | Nascidos vivos de São Paulo, 2022                         | `DNSP2022.dbc`                       | `/dissemin/publicos/SINASC/NOV/DNRES/`     |
 | Dengue no Brasil, 2020 (final)                            | `DENGBR20.dbc` (ou `DENGBR2020.dbc`) | `/dissemin/publicos/SINAN/DADOS/FINAIS/`   |
 | Internações hospitalares de Minas Gerais, janeiro de 2019 | `RDMG1901.dbc`                       | `/dissemin/publicos/SIHSUS/200801_/Dados/` |
 | Produção ambulatorial do Ceará, dezembro de 2021          | `ABCE2112.dbc`                       | `/dissemin/publicos/SIASUS/200801_/Dados/` |

 ---

 _Última atualização: 2026-05-13 (com base no mapeamento fornecido)._  
 _Para novos sistemas ou alterações, consulte o diretório FTP diretamente ou a documentação oficial do DATASUS._
