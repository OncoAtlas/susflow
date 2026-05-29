# SUSFlow

Biblioteca Python moderna para download, análise e engenharia de dados dos sistemas públicos de informação do DATASUS. Esta versão traduz a documentação principal para Português do Brasil.

Documentação em inglês: [README principal](../../README.md)

## Conteúdo

- Documentação dos módulos em `docs/pt-br/` e resumos de padrões FTP
- Código da biblioteca em `susflow/`
- Utilitários em `tools/` para inspeção e mapeamento do FTP

## Links rápidos

- [CNES](./cnes-pt-BR.md) — estabelecimentos de saúde
- [PNI](./pni-pt-BR.md) — imunizações
- [SIM](./sim-pt-BR.md) — mortalidade
- [SINAN](./sinan-pt-BR.md) — doenças de notificação compulsória
- [SINASC](./sinasc-pt-BR.md) — nascidos vivos
- [SIASUS](./siasus-pt-BR.md) — sistema de informações ambulatoriais (SUS)
- [SIHSUS](./sihsus-pt-BR.md) — sistema de informações hospitalares (SUS)
- [Sumário de padrões de FTP](./sumario.md)

## Instalação

Instalação em modo editável durante o desenvolvimento:

```bash
git clone https://github.com/OncoAtlas/susflow.git
cd susflow
python -m venv .venv
. ./.venv/bin/activate
pip install -U pip
pip install -e .
```

Instalação via PyPI (recomendado para a maioria dos usuários):

```bash
pip install susflow
```

Para instalar uma versão específica:

```bash
pip install susflow==0.1.1
```

Dependências de runtime são declaradas em `pyproject.toml`. Dependências comuns para desempenho:

- `pyarrow` ou `fastparquet` (cache Parquet)
- `pandas` (API de DataFrame)

## Uso básico

Cada sistema DATASUS está disponível sob `susflow.systems`. As APIs são leves: `list_files`, `download` e `read` cuidam de descoberta, download e conversão.

Exemplo rápido com `sinasc`:

```python
from susflow.systems import sinasc

# lista arquivos por UF
sinasc.list_files(uf="SP")

# download e retorna um pandas.DataFrame

df = sinasc.read(uf="SP", year=2020)
```

Exemplo com `pni`:

```python
from susflow.systems import pni

df = pni.read(uf="RJ", year=2015)
```

## Comportamento de cache

Por padrão, os downloads são salvos em `~/.susflow/cache/` espelhando a árvore do FTP. Se o arquivo já estiver em cache, a biblioteca reutiliza localmente. Para forçar novo download, use `force=True` nos helpers de download/leitura.

## Orientação de desempenho

- Reduza tipos numéricos e converta strings repetitivas para `category`.
- Converta datasets usados com frequência para Parquet e reutilize o cache local.
- Para conjuntos muito grandes, prefira processar em blocos ou usar DuckDB/Polars para evitar uso excessivo de RAM.

## Ferramentas de desenvolvimento

Recomendamos as seguintes ferramentas para contribuições:

```bash
. ./.venv/bin/activate
pip install -U ruff black isort pytest pytest-mock coverage
ruff .
black --check .
isort --check-only .
pytest -q
```

## Estratégia de testes

- Testes unitários devem simular FTP e IO de arquivos; veja `tests/unit/` para exemplos.
- Testes de integração que acessam FTP real devem ser opt-in e executados manualmente porque dependem de rede.

## Utilitários

`tools/mapear_ftp.py` ajuda a localizar e auditar diretórios do FTP DATASUS quando os caminhos mudam. Ele pode salvar mapas estruturados em `tools/mapas/` para análise offline.

## Contribuindo

Veja [CONTRIBUTING.md](../contributing/CONTRIBUTING.md) para diretrizes de código, testes e fluxo de PR.
Veja [coverage.md](../contributing/coverage.md) para instruções de cobertura de testes.

## Licença

Este projeto está licenciado sob a MIT License — veja `LICENSE`.

## Contato

Issues e pull requests são bem-vindos. Para mudanças maiores, abra uma issue para discutir escopo antes de implementar.
