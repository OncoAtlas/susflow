# IBGE — Estimativas Populacionais

**Base FTP:** `/dissemin/publicos/IBGE/POP/`

---

## Tipos de dados disponíveis

| Tipo     | Função               | Retorna     | Descrição                                        |
| -------- | -------------------- | ----------- | ------------------------------------------------ |
| nacional | `read(ano, engine=..., parquet=...)` | `DataFrame` (ou tabela do engine) | Estimativas populacionais do Brasil por ano      |
| nacional | `download(year)`     | `Path`      | Arquivo `.zip` bruto com as estimativas          |

---

> **Parâmetros comuns para `read()`:**
> - `engine="pandas" | "polars" | "pyarrow"`
> - `parquet=True` — cache sidecar Parquet

## Dados anuais nacionais

**Padrão de arquivo:** `POPBR{YY}.zip` (sufixo de ano com 2 dígitos)

**Cobertura:** 1980–2012

**Granularidade:** anual / apenas nacional (sem quebra por estado ou município)

```python
from susflow.systems import ibge_pop

# Baixa (se necessário) e retorna um DataFrame (pandas ou outro engine)
df = ibge_pop.read(2000)

# Baixa apenas o arquivo ZIP bruto
path = ibge_pop.download(1995)

# Lista arquivos disponíveis
files = ibge_pop.list_files()
```

Os arquivos ZIP contêm um único `.DBC` (ou `.DBF`) com contagens populacionais, geralmente detalhadas por faixas etárias, sexo e outras características demográficas para o ano de referência.

Para descrições detalhadas das variáveis, consulte os metadados originais do IBGE ou inspecione as colunas do DataFrame retornado.

**Nota:** Este sistema fornece apenas dados em nível nacional. Para dados populacionais por estado ou município, consulte outras fontes do IBGE ou sistemas do DATASUS.
