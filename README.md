# SUSFlow

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Formato de Saída](https://img.shields.io/badge/output-pandas.DataFrame-orange.svg)](#)

Biblioteca Python moderna para automação, download e engenharia de dados dos sistemas de informação do DATASUS. O susflow abstrai de forma transparente o protocolo FTP governamental, gerencia cache local, lida com a descompressão de arquivos proprietários .dbc e entrega dados limpos diretamente em estruturas do Pandas.

---

## Sumário de Documentação Técnica

Os guias detalhados sobre layouts de arquivos, variáveis específicas e regras de cada sistema de informação estão localizados na pasta /docs. Navegue diretamente por aqui:

- [**CNES** — Cadastro Nacional de Estabelecimentos de Saúde](./docs/cnes.md)
- [**PNI** — Programa Nacional de Imunizações](./docs/pni.md)
- [**SIM** — Sistema de Informações sobre Mortalidade](./docs/sim.md)
- [**SINAN** — Sistema de Informação de Agravos de Notificação](./docs/sinan.md)
- [**SINASC** — Sistema de Informações sobre Nascidos Vivos](./docs/sinasc.md)
- [**SIASUS** — Sistema de Informações Ambulatoriais do SUS](./docs/siasus.md) (Em breve)
- [**SIHSUS** — Sistema de Informações Hospitalares do SUS](./docs/sihsus.md) (Em breve)

---

## Instalação

Como o projeto está em desenvolvimento ativo, instale em modo editável (-e):

```bash
git clone [https://github.com/seu-usuario/susflow.git](https://github.com/seu-usuario/susflow.git)
cd susflow
pip install -e .

```

### Requisitos Base

- pandas (Manipulação de dados)
- pyreaddbc (Motor de descompressão do algoritmo BLAST)
- dbfread (Leitor nativo de estruturas DBF)
- pyarrow / fastparquet (Opcional, altamente recomendado para cache de alta performance)

---

## Como Usar (Exemplos Rápidos)

### 1. SINASC — Nascidos Vivos

```python
from susflow.systems import sinasc

# Listar arquivos disponíveis no servidor FTP
sinasc.listar(uf="PB")

# Baixar e carregar diretamente em um DataFrame pronto para análise
df_sinasc = sinasc.ler(uf="SP", ano=2022)

```

### 2. PNI — Imunizações (Formato DBF Puro)

```python
from susflow.systems import pni

# Cobertura histórica anual por UF (1994 a 2019)
df_pni = pni.ler(uf="RJ", ano=2015)

```

### 3. CNES — Estabelecimentos de Saúde (Granularidade Mensal)

```python
from susflow.systems import cnes

# Leitura mensal parametrizada por tipo de tabela (ex: "ST" = Estabelecimentos)
df_cnes = cnes.ler(uf="MG", ano=2022, mes=5, tipo="ST")

```

---

## Gerenciamento de Cache Inteligente

Para evitar sobrecarregar o servidor do DATASUS e acelerar seus scripts, o susflow implementa um cache local persistente em ~/.susflow/cache/, espelhando fielmente a árvore de diretórios do FTP original:

```text
~/.susflow/cache/
└── dissemin/publicos/
    ├── SINASC/NOV/DNRES/DNSP2022.dbc
    ├── PNI/DADOS/DPNISP15.DBF
    └── CNES/200508_/Dados/ST/STPB2201.dbc

```

- **Validação:** Se o arquivo solicitado já existir no diretório local, a biblioteca pula o download e faz a leitura imediata.
- **Sobrescrita:** Para atualizar dados preliminares ou forçar uma nova cópia do servidor, utilize o parâmetro forcar=True:

```python
df = sinasc.ler(uf="BA", ano=2023, forcar=True)

```

---

## Dicas de Desempenho e Memória

Bases de dados de saúde pública do Brasil podem ser massivas, frequentemente congelando ou travando o Jupyter Notebook se não tratadas corretamente. Siga as boas práticas abaixo:

1. **Otimização de Tipos (Downcasting):** Converta colunas de strings altamente repetitivas (como códigos de UF, Sexo ou Municípios) para o tipo category do Pandas. Reduza tipos de inteiros int64 genéricos para int16 ou int8 no seu pipeline. Isso pode reduzir o consumo de RAM em até 80%.
2. **Transição de Formato de Longo Prazo:** Arquivos .DBF e .DBC são extremamente lentos para leitura analítica. Após efetuar o primeiro pni.ler() ou cnes.ler(), salve o DataFrame resultante em formato Parquet:

```python
df.to_parquet("meus_dados.parquet", compression="snappy")

```

3. **Ajuste do Jupyter IOPub:** Se o seu Jupyter travar ao exibir ou processar DataFrames massivos, inicialize-o via terminal expandindo os limites de taxa de dados:

```bash
jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10

```

---

## Escopo e Mapeamento dos Sistemas

### v1 — Matriz de Implementação Atual

| Sistema                                             | Sigla      | Granularidade    | Formato | Status    |
| --------------------------------------------------- | ---------- | ---------------- | ------- | --------- |
| Sistema de Informações sobre Nascidos Vivos         | **SINASC** | Anual / Por UF   | .dbc    | Concluído |
| Sistema de Informações sobre Mortalidade (Geral)    | **SIM**    | Anual / Por UF   | .dbc    | Concluído |
| Sistema de Informações sobre Mortalidade (Especial) | **SIM**    | Anual / Nacional | .dbc    | Concluído |
| Sistema de Informação de Agravos de Notificação     | **SINAN**  | Anual / Nacional | .dbc    | Concluído |
| Cadastro Nacional de Estabelecimentos de Saúde      | **CNES**   | Mensal / Por UF  | .dbc    | Concluído |
| Programa Nacional de Imunizações                    | **PNI**    | Anual / Por UF   | .dbf    | Concluído |
| Sistema de Informações Hospitalares                 | **SIHSUS** | Mensal / Por UF  | .dbc    | Planejado |
| Sistema de Informações Ambulatoriais                | **SIASUS** | Mensal / Por UF  | .dbc    | Planejado |

---

## Engenharia Reversa do Fluxo de Dados

```text
 ┌───────────────────────┐
 │  FTP DATASUS (.dbc)   │  <- Arquivo compactado no servidor público
 └──────────┬────────────┘
            │  (Susflow faz o download & valida cache)
            ▼
 ┌───────────────────────┐
 │ Descompressão BLAST   │  <- Traduz .dbc para .dbf estruturado em Python puro
 └──────────┬────────────┘
            │  (Motor de parsing do reader)
            ▼
 ┌───────────────────────┐
 │   Pandas DataFrame    │  <- Pronto para análise, gráficos e ML
 └───────────────────────┘

```

---

## Ferramentas de Mapeamento (Diretório tools/)

O DATASUS frequentemente altera de forma silenciosa os caminhos ou padrões de nomenclatura de arquivos no FTP. A pasta tools/ contém scripts utilitários robustos para varredura e auditoria desses diretórios:

```bash
# Mapear e atualizar de forma automática os caminhos base da v1
python tools/mapear_ftp.py

# Executar mapeamento silencioso salvando o log estruturado em json/csv
python tools/mapear_ftp.py --salvar --quiet

# Auditar uma árvore de diretórios específica no FTP profundo
python tools/mapear_ftp.py --alvo /dissemin/publicos/SINAN/DADOS --profundo

```

---

Desenvolvido para simplificar a pesquisa epidemiológica e a ciência de dados em saúde no Brasil. Contribuições e pull requests são bem-vindos!
