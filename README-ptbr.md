# susflow

> Biblioteca Python de alta performance para extrair, converter e padronizar dados do DATASUS — a plataforma de dados públicos do Ministério da Saúde do Brasil.

**🇺🇸 [Read in English](README.md)**

---

## Visão Geral

`susflow` automatiza todo o pipeline do DATASUS: descoberta de arquivos em servidores FTP legados, conversão do formato proprietário `.dbc`, remoção de duplicatas e entrega de dados prontos para análise em formato Parquet — tudo com uma única chamada de função.

### Por que usar o susflow?

| Desafio | Solução susflow |
|---------|----------------|
| Arquivos `.dbc` não abrem no Mac/Linux | Conversão DBC → Parquet transparente via `pyreaddbc` + DuckDB |
| Nomes de colunas crípticos (`CAUSABAS`, `DTINTERNA`) | Renomeação automática para nomes legíveis (`causa_basica_obito`, `data_internacao`) |
| Codificação ISO-8859-1 / Mojibake | Corrigido para UTF-8 em toda leitura |
| Linhas duplicadas em arquivos legados | Removidas automaticamente durante a conversão |
| Downloads repetidos desperdiçam tempo | Cache local particionado — re-execuções são instantâneas |
| Estruturas FTP diferentes por sistema | API unificada `load()` para todos os sistemas |

---

## Estrutura do Repositório

```
.
├── README.md                        # Documentação principal (inglês)
├── README-ptbr.md                   # Este arquivo (português)
├── CONTRIBUTING.md                  # Como adicionar sistemas e rodar os testes
├── CONTEXT.md                       # Contexto estratégico e filosófico da lib
├── pyproject.toml                   # Configurações de build e dependências
├── setup.py                         # Script de instalação legado/compatibilidade
│
├── docs/
│   ├── CHANGELOG_REFACTOR.md        # Histórico de refatorações
│   └── MIGRATION_RATIONALE.md       # Decisões arquiteturais
│
├── susflow/
│   ├── __init__.py
│   ├── config.py                    # O "cérebro": mapas de FTP, mapeamentos de colunas, lista de UFs
│   ├── ftp.py                       # Camada de rede: downloads resilientes com retry/backoff
│   ├── cache.py                     # Gestão de caminhos locais para arquivos baixados
│   ├── reader.py                    # Suporte para leitura local (.zip, .dbf)
│   │
│   ├── core/
│   │   ├── cleaner.py               # Renomeação de colunas, enriquecimento de municípios, CID, datas
│   │   ├── specialties.py           # Filtros clínicos especializados (ex: Oncologia CID C00–D48)
│   │   ├── synchronization.py       # BacktrackingEngine: encontra o mês mais recente consistente no FTP
│   │   └── validator.py             # Valida UF, faixa de anos e granularidade contra as regras do config
│   │
│   ├── parsers/
│   │   └── converter.py             # DBC/DBF → Parquet via DuckDB + Polars (dedup + ZSTD)
│   │
│   ├── resources/
│   │   ├── territory.py             # Mapa de municípios IBGE (código 7 dígitos → 6 dígitos, com cache)
│   │   └── municipios_br.parquet    # Cache local de geolocalização
│   │
│   ├── storage/
│   │   └── local_lake.py            # Construtor de caminhos Hive-particionados para o lago local
│   │
│   └── systems/                     # Interface do usuário — um arquivo por sistema do DATASUS
│       ├── base.py                  # generic_load() e generic_bulk_load() — o motor universal
│       ├── sim.py                   # SIM: Sistema de Informações sobre Mortalidade
│       ├── sinasc.py                # SINASC: Nascidos Vivos
│       ├── sinan.py                 # SINAN: Agravos de Notificação
│       ├── sih.py                   # SIHSUS: Sistema de Informações Hospitalares (AIH)
│       ├── cnes.py                  # CNES: Cadastro de Estabelecimentos de Saúde
│       └── sia.py                   # SIASUS: Sistema de Informações Ambulatoriais
│
└── tests/                           # Suite de testes unitários e de integração
```

**Layout do Lago Local** (criado automaticamente no primeiro uso):

```
data_lake/
├── SIM/DO/year=2022/uf=PB/data.parquet
├── SIHSUS/RD/year=2023/month=03/uf=SP/data.parquet
├── CNES/ST/year=2024/month=01/uf=RJ/data.parquet
└── _temp/                           # Área temporária de download (limpa automaticamente)
```

---

## Instalação

```bash
pip install susflow
```

**Requisitos:** Python 3.10+, DuckDB, Polars, pyreaddbc

---

## Primeiros Passos

### Mortalidade (SIM)

```python
from susflow.systems import sim

# Carrega óbitos da Paraíba em 2022
df = sim.load(uf="PB", year=2022)
print(df.head())
# Colunas: causa_basica_obito, data_obito, municipio_residencia, sexo_paciente ...
```

### Internações (SIHSUS)

```python
from susflow.systems import sih

# Mês único
df = sih.load(uf="SP", year=2023, month=3, table="RD")

# Ano completo em paralelo (12 meses, até 5 downloads simultâneos)
df_ano = sih.load_year(uf="SP", year=2023)
```

### Agravos de Notificação (SINAN)

```python
from susflow.systems import sinan

df_dengue = sinan.load(agravo="DENG", uf="CE", year=2023)
df_tb     = sinan.load(agravo="TUBE", uf="AM", year=2022)
```

### Nascidos Vivos (SINASC)

```python
from susflow.systems import sinasc

df = sinasc.load(uf="RJ", year=2021)
```

### CNES — sempre o mês mais recente disponível

```python
from susflow.systems import cnes

# O BacktrackingEngine varre o FTP de trás para frente até encontrar
# o mês mais recente onde a tabela solicitada já foi publicada
df_estab = cnes.load_latest(table="ST", uf="MG")
```

### Carga em lote — múltiplos estados em paralelo

```python
from susflow.systems import sim

nordeste = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
df_nordeste = sim.load_bulk(ufs=nordeste, year=2022)
```

### Filtro de Oncologia (CID C00–D48)

```python
from susflow.systems import sim
from susflow.core import specialties

df = sim.load(uf="SP", year=2022)
df_cancer = specialties.filter_oncology(df, cid_column="causa_basica_obito")
```

### Varredura lazy do lago local (zero RAM até o `.collect()`)

```python
from susflow.systems.base import scan_system
import polars as pl

lazy = scan_system("SIM", "DO")
resultado = lazy.filter(pl.col("year") == 2022).collect()
```

### Carregar uma região inteira

```python
from susflow.systems.base import load_region

df_sul = load_region("SIM", "DO", region_name="SUL", year=2022)
# Opções de region_name: "NORTE", "NORDESTE", "CENTRO-OESTE", "SUDESTE", "SUL"
```

---

## Arquitetura em Diagrama

```
Usuário chama sim.load(uf, year)
        │
        ▼
validator.validate_params()       ← verifica UF, faixa de anos e granularidade (config.py)
        │
        ▼
local_lake.get_path()             ← monta o caminho Hive-particionado no cache local
        │
   ┌────┴────┐
   │ em cache?│
   └────┬────┘
    Sim │                    Não
        ▼                    ▼
  converter.load_as_df()   ftp.baixar()              ← download resiliente com retry/backoff
        │                  converter.to_parquet()    ← DBC → DBF → DuckDB → Polars (dedup + ZSTD)
        │                         │
        └──────────┬───────────────┘
                   ▼
        cleaner.apply_standard_clean()    ← renomear + municípios + descrições CID + datas
                   │
                   ▼
             pl.DataFrame  ✓
```

---

## Referência de Configuração

Todas as regras dos sistemas vivem em `config.py`. Constantes principais:

| Constante | Finalidade |
|-----------|-----------|
| `UFS` | Todos os 27 códigos de estado brasileiros válidos |
| `REGIOES` | Agrupamento de estados por região (Norte, Nordeste, etc.) |
| `UF_PARA_REGIAO` | Busca reversa: UF → nome da região |
| `COLUMN_MAPPINGS` | Colunas crípticas do DATASUS → nomes legíveis em snake_case |
| `MAX_WORKERS` | Concorrência de downloads paralelos (padrão: 5) |
| `ALL_SYSTEMS` | Registro de todos os sistemas suportados e suas regras de FTP |

---

## Contribuindo

Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para um guia passo a passo sobre como adicionar novos sistemas e rodar a suite de testes.

---

## Licença

MIT