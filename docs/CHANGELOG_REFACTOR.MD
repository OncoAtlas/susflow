## Objetivo
Unificar a lógica de download, conversão e cache em uma interface única (`generic_load`), eliminando duplicidade de código nos módulos de sistemas (CNES, SIM, SIH, etc).

## Nova arquitetura: `generic_load`
A lógica foi centralizada em `susflow/systems/base.py`. Agora, os módulos em `systems/` funcionam apenas como configuradores de caminhos.

### Fluxo de operação:
1. **Identificação**: Monta o nome do arquivo baseado em `table`, `uf`, `year` e `month`.
2. **Cache**: Verifica no `local_lake` se o `.parquet` já existe.
3. **Extração**: Caso não exista, baixa o `.dbc` do FTP usando o `sub_dir` fornecido.
4. **Transformação**: Converte o `.dbc` para `.parquet` via DuckDB (corrigindo encoding Latin-1).
5. **Carga**: Retorna um Polars DataFrame.

---

## PROBLEMA ATUAL:
Durante os testes de integração, o sistema **SINASC** apresentou erro `550 (Path not found)`.

### Descobertas:
- **Inconsistência de Diretório**: Diferente de outros sistemas, o SINASC alterna entre `1994_/Dados` e `1996_/Dados`.
- **Case Sensitivity**: O servidor FTP do DATASUS é sensível a maiúsculas. Em alguns anos a pasta é `Dados`, em outros `DADOS`.
- **Estrutura de Subpastas**: Ao contrário do CNES, o SINASC frequentemente coloca o arquivo `DNPB...` diretamente na pasta `Dados`, sem a subpasta intermediária `/DN/`.

### Solução Aplicada:
- O `sub_dir` agora deve ser passado completo pelo módulo do sistema.
- A `generic_load` foi simplificada para não presumir subpastas extras, permitindo que cada sistema defina seu caminho exato.

---

## Mudanças por Arquivo

| Arquivo | Mudança Principal |
| :--- | :--- |
| `systems/base.py` | Criação da `generic_load` e padronização da montagem de URL FTP. |
| `systems/cnes.py` | Refatorado para usar `base.py` e restauração da função `load_latest`. |
| `systems/sim.py` | Migrado para Polars/DuckDB via `generic_load`. |
| `systems/sinasc.py` | Ajuste do `sub_dir` para `1994_/Dados` para maior compatibilidade. |
| `ftp.py` | Implementação da função `existe()` para suporte ao Backtracking. |

### Atualização: Estrutura de Dados e Performance (Hive Partitioning)
**Objetivo**: Implementar o padrão "Hive Partitioning" para permitir o *Partition Pruning*, reduzindo drasticamente o uso de RAM e tempo de IO em análises regionais.

#### Mudanças Estruturais:
1. **Hierarquia de Pastas**: Migração do modelo flat para `SISTEMA/TABELA/year=YYYY/uf=XX/data.parquet`.
2. **Inteligência Geográfica**: Integração do `config.REGIOES` para permitir cargas em lote por blocos federativos (ex: Norte, Nordeste).
3. **Enriquecimento Territorial**: Implementação de cache local para municípios (IBGE) em `resources/`, permitindo tradução offline de códigos para nomes de cidades.

#### Melhorias de Performance:
- **Partition Pruning**: O Polars agora ignora diretórios físicos que não atendem aos filtros de `year` ou `uf`.
- **Lazy Evaluation**: Introdução do `scan_system()` para processamento de múltiplos anos/estados sem saturação de memória.