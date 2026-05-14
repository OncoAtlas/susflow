System Context: susflow (Python Library)
1. Overview
susflow is a high-performance Python library designed to bridge the gap between researchers and the cryptic, legacy Data Lake of the Brazilian Ministry of Health (DATASUS). It automates the entire pipeline: from discovering files on legacy FTP servers to providing a clean, analysis-ready Local Data Lake in Parquet format.
2. Core Philosophy
•	High Performance: Uses DuckDB for ultra-fast extraction of legacy formats and Polars for memory-efficient data manipulation.
•	Offline-first: Every file downloaded or converted is stored in a structured local lake (Hive-partitioned), ensuring that subsequent analyses are instant.
•	Standardization: It maps cryptic columns (e.g., CAUSABAS) to human-readable names (basic_cause_of_death) and standardizes encodings (from ISO-8859-1 to UTF-8).
•	Internationalization: Built with an English core (code/docs) while maintaining domain-specific Portuguese context where necessary (e.g., Brazilian municipality names).
3. Technical Architecture
The library is organized into specialized layers:
A. Transport & Infrastructure (ftp.py, local_lake.py)
•	Manages connections to ftp.datasus.gov.br.
•	Implements resilient downloads with retries and backoff.
•	Organizes the data lake using Hive partitioning: data_lake/SYSTEM/TABLE/year=YYYY/month=MM/uf=XX/data.parquet.
B. Parsing & Conversion (reader.py, converter.py)
•	Legacy Support: Handles .dbc (proprietary compressed DBF), .dbf, and .zip files.
•	Hybrid Engine: Uses pyreaddbc for decompression, DuckDB's st_read for fast DBF ingestion, and Polars for final optimization and ZSTD compression.
C. Validation & Intelligence (validator.py, synchronization.py, config.py)
•	Metadata-Driven: A centralized config.py acts as the "source of truth" for directory paths and column mappings.
•	Backtracking Engine: A smart synchronization tool that scans the FTP to find the most recent consistent data available across multiple tables (essential for systems like CNES).
D. System Wrappers (systems/)
•	Simplified entry points for end-users: sim.load(), sih.load(), sinan.load(), etc.
•	Each system inherits from a base.py loader that orchestrates the full pipeline: Validate -> Download -> Convert -> Clean.
4. Key Features
•	Parallel Loading: generic_bulk_load allows downloading and processing multiple states or years simultaneously using ThreadPoolExecutor.
•	Automatic Enrichment: Integrates with the IBGE API to fetch and cache municipality maps, automatically mapping 7-digit codes to the 6-digit standard used by DATASUS.
•	Clinical Intelligence: Built-in filters for specialized domains like Oncology (filtering ICD-10 codes C00-D48).
5. Technical Stack
•	Languages: Python 3.10+
•	Database Engine: DuckDB (for DBF/DBC parsing)
•	DataFrames: Polars (Primary), Pandas (Support)
•	Networking: ftplib, requests
•	Compression: ZSTD (Parquet)
6. Challenges the Library Solves
•	Complexity: DATASUS uses different directory structures for each system (some by year, some by month, some with prefix variations).
•	Format: .dbc is a non-standard format that is difficult to open on modern OSs (Mac/Linux).
•	Duplicates: Legacy files often contain duplicated rows which are automatically removed during the susflow conversion process.
•	Encoding: Corrects the common "Mojibake" issues found in Brazilian public data.

```
.
├── CONTEXT.md               # Contexto estratégico e filosófico da lib
├── CONTRIBUTING.md          # Guia para novos desenvolvedores (como adicionar sistemas)
├── README.md                # Página principal (Instalação e Quick Start)
├── docs/                    # Documentação técnica profunda e histórico de mudanças
│   ├── CHANGELOG_REFACTOR.MD
│   └── MIGRATION_RATIONALE.md
├── pyproject.toml           # Configurações de build e dependências (DuckDB, Polars)
├── setup.py                 # Script de instalação legado/compatibilidade
├── susflow/                 # Código-fonte principal
│   ├── __init__.py
│   ├── cache.py             # Gestão de caminhos locais para arquivos baixados
│   ├── config.py            # O "Cérebro": Mapas de FTP, colunas e UFs
│   ├── core/                # Lógica de processamento e inteligência
│   │   ├── cleaner.py       # Tradução de colunas e limpeza de tipos de dados
│   │   ├── specialties.py   # Filtros clínicos especializados (ex: Oncologia)
│   │   ├── synchronization.py # Motor de busca por dados mais recentes (Backtracking)
│   │   └── validator.py     # Validador de anos, meses e UFs permitidas
│   ├── ftp.py               # Camada de rede: Downloads resilientes do DATASUS
│   ├── parsers/             # Transformação de formatos
│   │   └── converter.py     # Motor de conversão DBC -> Parquet via DuckDB
│   ├── reader.py            # Suporte para leitura de arquivos locais (.zip, .dbf)
│   ├── resources/           # Dados de referência
│   │   ├── territory.py     # Gestão do dicionário de municípios (API IBGE)
│   │   └── municipios_br.parquet # Cache local de geolocalização
│   ├── storage/             # Infraestrutura de persistência
│   │   └── local_lake.py    # Implementação do Data Lake (Hive Partitioning)
│   └── systems/             # Interface do Usuário (Sistemas do DATASUS)
│       ├── base.py          # Carregador genérico (Engine de Bulk Load)
│       ├── cnes.py          # Sistema de estabelecimentos
│       ├── sih.py           # Sistema hospitalar (AIH)
│       ├── sim.py           # Sistema de mortalidade
│       ├── sinan.py         # Doenças de notificação
│       └── sinasc.py        # Nascimentos
└── tests/                   # Suite de testes (Unitários e Integração)
```