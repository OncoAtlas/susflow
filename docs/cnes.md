# CNES — Cadastro Nacional de Estabelecimentos de Saúde

Base FTP: `ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/`

---

## Tipos de dados disponíveis

| Tipo | Função | Retorno | Descrição |
|------|--------|---------|-----------|
| Por UF | `ler(uf, ano, mes)` | `DataFrame` | Dados cadastrais de um subtipo para uma UF |
| Por UF | `baixar(uf, ano, mes)` | `Path` | Arquivo `.dbc` bruto |

---

## Subtipos disponíveis

**Padrão de arquivo:** `{TYPE}/{TYPE}{UF}{YY}{MM}.dbc`  
**Granularidade:** mensal / por UF  

> O arquivo fica dentro de um subdiretório com o mesmo nome do subtipo:  
> ex: `ST/STSP2501.dbc` → estabelecimentos de SP, janeiro de 2025.

```python
from susflow.systems import cnes

# ver todos os subtipos disponíveis
print(cnes.subtipos())

# Estabelecimentos — subtipo padrão
df = cnes.ler(uf="SP", ano=2025, mes=1)
df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="ST")

# outros subtipos
df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="PF")   # profissionais
df = cnes.ler(uf="RJ", ano=2024, mes=6, tipo="LT")   # leitos
df = cnes.ler(uf="MG", ano=2023, mes=3, tipo="EQ")   # equipamentos

# só baixar
path = cnes.baixar(uf="SP", ano=2025, mes=1)
path = cnes.baixar(uf="SP", ano=2025, mes=1, tipo="PF")

# listar arquivos disponíveis
cnes.listar()                       # todos os ST
cnes.listar(uf="SP")                # ST de SP
cnes.listar(uf="SP", tipo="PF")     # profissionais de SP
```

### Subtipos ativos

| Tipo | Arquivo exemplo | Conteúdo | Cobertura |
|------|----------------|----------|-----------|
| `ST` | `STSP2501.dbc` | **Estabelecimentos** — identificação, localização, tipo | 2005–2026 |
| `PF` | `PFSP2501.dbc` | **Profissionais de saúde** — vínculos e CBO | 2005–2026 |
| `DC` | `DCSP2501.dbc` | Dados complementares do estabelecimento | 2005–2026 |
| `EQ` | `EQSP2501.dbc` | Equipamentos disponíveis | 2005–2026 |
| `SR` | `SRSP2501.dbc` | Serviços especializados ofertados | 2005–2026 |
| `LT` | `LTSP0510.dbc` | Leitos (SUS e não-SUS) | 2005–2026 |
| `HB` | `HBSP0703.dbc` | Habilitações e certificações | 2007–2026 |
| `EF` | `EFSP0703.dbc` | Centros cirúrgicos e obstétricos | 2007–2026 |
| `EP` | `EPSP0704.dbc` | Equipes de saúde (eSF, eAP, etc.) | 2007–2026 |
| `RC` | `RCSP0703.dbc` | Regras contratuais | 2007–2026 |
| `IN` | `INSP0711.dbc` | Incentivos financeiros | 2007–2026 |
| `GM` | `GMSP1407.dbc` | Gestão e metas | 2014–2026 |

### Subtipos encerrados (ainda disponíveis no FTP)

| Tipo | Arquivo exemplo | Conteúdo | Cobertura | Observação |
|------|----------------|----------|-----------|------------|
| `EE` | `EESP0703.dbc` | Equipamentos e produções | 2007–2019 | Encerrado em dez/2019 |

---

## Principais variáveis por subtipo

### ST — Estabelecimentos

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `CNES` | str | Código CNES (identificador único) |
| `CODUFMUN` | str | Código IBGE do município |
| `REGSAUDE` | str | Região de saúde |
| `MICR_REG` | str | Microrregião de saúde |
| `DISTRSAN` | str | Distrito sanitário |
| `DISTRADM` | str | Distrito administrativo |
| `TPGESTAO` | str | Tipo de gestão (M=municipal, E=estadual, D=dupla) |
| `PF_PJ` | str | Pessoa física ou jurídica |
| `CPF_CNPJ` | str | CPF ou CNPJ |
| `NIV_DEP` | str | Nível de dependência |
| `CNPJ_MAN` | str | CNPJ da mantenedora |
| `ESFERA_A` | str | Esfera administrativa |
| `ATIVIDAD` | str | Atividade de ensino/pesquisa |
| `RETENCAO` | str | Tipo de retenção |
| `NATUREZA` | str | Natureza jurídica |
| `CLIENTEL` | str | Clientela atendida |
| `TP_UNID` | str | Tipo de unidade |
| `TURNO_AT` | str | Turno de atendimento |
| `NIV_HIER` | str | Nível hierárquico |
| `TERCEIRO` | str | Indicador de terceirização |
| `COMPETEN` | str | Competência (AAAAMM) |

### PF — Profissionais

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `CNES` | str | Código CNES do estabelecimento |
| `CBO` | str | Código CBO da ocupação |
| `NOMEPROF` | str | Nome do profissional |
| `CNS_PROF` | str | CNS do profissional |
| `CONSELHO` | str | Conselho profissional |
| `REGISTRO` | str | Número de registro no conselho |
| `VINCULAC` | str | Tipo de vínculo |
| `SUBVINCUL` | str | Subtipo de vínculo |
| `TP_SUS` | str | Atende pelo SUS |
| `COMPETEN` | str | Competência (AAAAMM) |

### LT — Leitos

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `CNES` | str | Código CNES do estabelecimento |
| `TP_LEITO` | str | Tipo de leito |
| `CODLEITO` | str | Código do leito |
| `QT_EXIST` | str | Quantidade existente |
| `QT_CONTR` | str | Quantidade contratada (SUS) |
| `QT_SUS` | str | Quantidade SUS |
| `COMPETEN` | str | Competência (AAAAMM) |

---

## Fluxo recomendado

```
1. Explorar o que existe
   print(cnes.subtipos())              ← todos os subtipos e descrições
   cnes.listar(uf="SP")                ← arquivos ST de SP disponíveis
   cnes.listar(uf="SP", tipo="PF")     ← profissionais de SP

2. Baixar os dados
   df = cnes.ler(uf="SP", ano=2025, mes=1)              ← estabelecimentos
   df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="PF")   ← profissionais
   df = cnes.ler(uf="SP", ano=2025, mes=1, tipo="LT")   ← leitos

3. Combinar meses em série histórica
   import pandas as pd
   dfs = [cnes.ler(uf="SP", ano=2024, mes=m) for m in range(1, 13)]
   df_ano = pd.concat(dfs, ignore_index=True)
```

---

## Notas

- Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
- O ano usa **2 dígitos** e o mês **2 dígitos com zero à esquerda**: `STSP2501.dbc` = SP, janeiro de 2025.
- O arquivo fica dentro de um subdiretório com o mesmo nome do subtipo — isso é tratado automaticamente pela biblioteca.
- Cada subtipo tem sua própria cobertura temporal. Tentar baixar `EE` para 2022 levanta erro com a cobertura correta (2007–2019).
- `ST` e `PF` são os subtipos mais usados: `ST` para análises de distribuição de estabelecimentos, `PF` para análises de força de trabalho em saúde.
- O campo `CNES` é a chave de cruzamento entre todos os subtipos — use-o para enriquecer `ST` com dados de `LT`, `EQ`, `PF`, etc.
- Para cruzar municípios com nomes, use `CADMUN.DBF` disponível no SIM (`sim.baixar_tabelas("CADMUN.DBF")`).
