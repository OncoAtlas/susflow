## 1. Mudança de paradigma: Data-First
A principal mudança é que o usuário final não deve gerenciar arquivos.
- **Antes:** O foco era o método `baixar()` que retornava um `Path`.
- **Depois:** O foco é o método `load()` que retorna um `DataFrame` (Pandas ou Polars).

O download e o parsing tornam-se **detalhes de implementação**. Se o dado não existe localmente, a biblioteca o providencia de forma transparente.

## 2. Parquet como camada de cache otimizada
Por motivos de performance, abandonamos o uso de arquivos temporários e leitura repetida de DBC/DBF.
- **Armazenamento:** Todo arquivo baixado (.dbc/.dbf) é imediatamente convertido para `.parquet` no cache local.
- **Vantagem:** O Parquet preserva tipos de dados, permite leitura seletiva de colunas (importante para equipamentos oncológicos) e é drasticamente mais rápido que o parsing de DBC.

## 3. O Motor de sincronização (consistência temporal)
Precisamos de consistência dos dados, então:
- A biblioteca implementa um motor de **backtracking**.
- Exemplo: Para o CNES, a `load()` só entrega o mês `202603` se **ambas** as tabelas `ST` (estabelecimentos) e `EQ` (equipamentos) estiverem disponíveis para esse mês. Se uma faltar, a biblioteca retrocede automaticamente para o mês anterior.

## 4. Mapeamento de arquitetura

| Componente Antigo | Novo Componente | Nova Responsabilidade |
| :--- | :--- | :--- |
| `ftp.py` | `transport/ftp.py` | Agora inclui `discovery` para checagem rápida de existência sem baixar. |
| `reader.py` | `parsers/converter.py` | Converte DBC/DBF diretamente para Parquet usando DuckDB/PyReadDBC. |
| `cache.py` | `storage/local_lake.py` | Gerencia a estrutura de diretórios do "Data Lake" local. |
| `sim.py`, `cnes.py` | `systems/*.py` | Interfaces que expõem a função `load()` e perfis (ex: `load_oncology`). |

## 5. Próximos Passos na Implementação
1. Refatorar o `ftp.py` para suportar o motor de descoberta.
2. Criar o `converter.py` integrando DuckDB para geração de Parquet.
3. Implementar a lógica de `load()` no CNES com o backtracking de consistência.

---