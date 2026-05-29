# SUSFlow

Biblioteca Python moderna para download, análise e engenharia de dados dos sistemas públicos de informação do DATASUS. Esta versão traduz a documentação principal para Português do Brasil.

Instalação
-
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

Uso básico
-
Exemplo rápido com `sinasc`:

```python
from susflow.systems import sinasc
sinasc.listar(uf="SP")
df = sinasc.ler(uf="SP", ano=2020)
```

Cache
-
Downloads são salvos em `~/.susflow/cache/` espelhando a árvore do FTP. Use `forcar=True` para forçar re-download.

Dicas de desempenho
-
- Converta colunas repetitivas para `category`.
- Salve resultados processados em Parquet para reutilização.

Contribuindo
-
Leia `CONTRIBUTING.md` para orientações sobre testes, estilo e fluxo de PR.

Licença
-
MIT
