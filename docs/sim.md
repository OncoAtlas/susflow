# SIM — Sistema de Informações sobre Mortalidade

Base FTP: `ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/`

---

## Tipos de dados disponíveis

| Tipo | Função | Retorno | Descrição |
|------|--------|---------|-----------|
| Por UF | `ler(uf, ano)` | `DataFrame` | Óbitos registrados em uma UF, por ano |
| Por UF | `baixar(uf, ano)` | `Path` | Arquivo `.dbc` bruto da UF |
| Especial | `ler_especial(tipo, ano)` | `DataFrame` | Óbitos nacionais por categoria (EXT/FET/INF/MAT) |
| Especial | `baixar_especial(tipo, ano)` | `Path` | Arquivo `.dbc` bruto da categoria |
| Documentação | `baixar_docs(arquivo?)` | `Path / list[Path]` | Layouts, estrutura e dicionário de variáveis |
| Tabelas de apoio | `baixar_tabelas(arquivo?)` | `Path / list[Path]` | CID-10, municípios, ocupações, países, UFs |
| Dados tabulados | `baixar_tab(arquivo?)` | `Path / list[Path]` | Óbitos agregados por CID-10 (série histórica) |

---

## Dados por UF — `DORES/`

**Padrão de arquivo:** `DO{UF}{YYYY}.dbc`  
**Cobertura:** 1996–2024, todas as 27 UFs  
**Granularidade:** anual / por UF

```python
from susflow.systems import sim

df = sim.ler(uf="SP", ano=2023)
path = sim.baixar(uf="RJ", ano=2022)
arquivos = sim.listar(uf="MG")
```

### Principais variáveis do DataFrame

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `DTOBITO` | str | Data do óbito (DDMMAAAA) |
| `CAUSABAS` | str | Causa básica do óbito (CID-10) |
| `SEXO` | str | Sexo (1=Masc, 2=Fem, 9=Ignorado) |
| `IDADE` | str | Idade codificada (ver dicionário) |
| `CODMUNRES` | str | Código IBGE do município de residência |
| `CODMUNOCI` | str | Código IBGE do município de ocorrência |
| `ESTCIV` | str | Estado civil |
| `ESC` | str | Escolaridade |
| `OCUP` | str | Ocupação (CBO) |
| `RACACOR` | str | Raça/cor |
| `LOCOCOR` | str | Local de ocorrência (hospital, domicílio, etc.) |
| `ASSISTMED` | str | Assistência médica recebida |
| `ATESTANTE` | str | Tipo de atestante |
| `CIRCOBITO` | str | Circunstância do óbito |
| `ACIDTRAB` | str | Acidente de trabalho |
| `FONTE` | str | Fonte da informação |
| `TPMORTEOCO` | str | Tipo de morte |
| `CAUSABAS_O` | str | Causa básica original (antes de correção) |
| `UFINFORM` | str | UF informante |

> Para a lista completa de variáveis e seus códigos, baixe `Estrutura_do_SIM_2025.pdf` ou `Docs_Tabs_CID10.zip`.

---

## Dados especiais — `DOFET/`

**Padrão de arquivo:** `DO{TIPO}{YY}.dbc`  
**Cobertura:** 1996–2024, escopo nacional  
**Granularidade:** anual / nacional

| Tipo | Arquivo exemplo | Conteúdo |
|------|----------------|----------|
| `EXT` | `DOEXT24.dbc` | Óbitos por causas externas (acidentes, homicídios, suicídios) |
| `FET` | `DOFET24.dbc` | Óbitos fetais |
| `INF` | `DOINF24.dbc` | Óbitos infantis (0–1 ano) |
| `MAT` | `DOMAT24.dbc` | Óbitos maternos |

```python
df = sim.ler_especial(tipo="EXT", ano=2023)
df = sim.ler_especial(tipo="MAT", ano=2022)

path = sim.baixar_especial(tipo="INF", ano=2024)
arquivos = sim.listar_especial(tipo="FET")
```

---

## Documentação técnica — `DOCS/`

Arquivos disponíveis para download (não lidos como DataFrame):

| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| `Docs_Tabs_CID10.zip` | Layouts completos, tabelas e dicionário de variáveis | Referência principal para entender os campos |
| `Estrutura_do_SIM_2025.pdf` | Estrutura atual dos arquivos | Bases de 2010 em diante |
| `Estrutura_SIM_Anterior.pdf` | Estrutura anterior dos arquivos | **Necessário para bases legadas (antes de 2010)** |

```python
# ver o que está disponível
print(sim.listar_docs())

# baixar um documento específico
path = sim.baixar_docs("Estrutura_do_SIM_2025.pdf")
path = sim.baixar_docs("Estrutura_SIM_Anterior.pdf")  # para bases antigas

# baixar todos de uma vez
paths = sim.baixar_docs()

# salvar em pasta específica
path = sim.baixar_docs("Docs_Tabs_CID10.zip", destino="/meus/dados/sim")
```

---

## Tabelas de apoio — `TABELAS/`

Tabelas de referência usadas para decodificar os campos dos DataFrames:

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `CID10.DBF` | DBF | Classificação Internacional de Doenças — CID-10 (códigos e descrições) |
| `CIDCAP10.DBF` | DBF | Capítulos do CID-10 |
| `CADMUN.DBF` | DBF | Cadastro de municípios brasileiros (código IBGE, nome, UF) |
| `CADMUN.xls` | Excel | Cadastro de municípios (formato Excel) |
| `TABOCUP.DBF` | DBF | Tabela de ocupações — CBO |
| `TABPAIS.DBF` | DBF | Tabela de países |
| `TABUF.DBF` | DBF | Tabela de unidades federativas |

```python
# ver o que está disponível
print(sim.listar_tabelas())

# baixar uma tabela específica
path = sim.baixar_tabelas("CID10.DBF")
path = sim.baixar_tabelas("CADMUN.DBF")

# baixar todas de uma vez
paths = sim.baixar_tabelas()
```

---

## Dados tabulados — `TAB/`

Dados já agregados, úteis para análises sem precisar processar os microdados:

| Arquivo | Conteúdo |
|---------|----------|
| `OBITOS_CID10_TAB.zip` | Série histórica de óbitos agregados por CID-10 |

```python
print(sim.listar_tab())

path = sim.baixar_tab("OBITOS_CID10_TAB.zip")
paths = sim.baixar_tab()  # baixa todos
```

---

## Fluxo recomendado

```
1. Explorar o que existe
   sim.listar(uf="SP")
   sim.listar_especial()

2. Baixar os dados
   df = sim.ler(uf="SP", ano=2023)          ← microdados por UF
   df = sim.ler_especial(tipo="MAT", ano=2022)  ← dados nacionais especiais

3. Baixar referências para decodificar os campos
   sim.baixar_tabelas("CID10.DBF")
   sim.baixar_tabelas("CADMUN.DBF")

4. Consultar a estrutura dos campos (se necessário)
   sim.baixar_docs("Estrutura_do_SIM_2025.pdf")
   sim.baixar_docs("Estrutura_SIM_Anterior.pdf")  ← para anos anteriores a 2010
```

---

## Notas

- Arquivos `.dbc` são DBF comprimidos com o algoritmo proprietário **blast** (PKWARE). A biblioteca descomprime automaticamente via `pyreaddbc`.
- O campo `IDADE` usa codificação própria do DATASUS: o primeiro dígito indica a unidade (1=horas, 2=dias, 3=meses, 4=anos) e os dois seguintes o valor.
- Municípios são identificados pelo código IBGE de 6 dígitos (`CODMUNRES`, `CODMUNOCI`). Use `CADMUN.DBF` para cruzar com nomes.
- Causas de óbito seguem o CID-10. Use `CID10.DBF` para obter as descrições dos códigos.
- Para bases anteriores a 2010, a estrutura dos campos pode diferir — consulte `Estrutura_SIM_Anterior.pdf`.
