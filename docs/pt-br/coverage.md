# Cobertura de testes — como executar e gerar relatórios

Este arquivo explica como executar a suíte de testes com cobertura e gerar relatórios localmente (a CI já executa cobertura e impõe um limite mínimo).

## Comandos

1. Crie e ative um ambiente virtual, instale o pacote e as dependências de teste (o extra `dev` inclui coverage, pytest etc.):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

2. Execute os testes com cobertura e mostre o resumo no terminal:

```bash
coverage run -m pytest -q
coverage report -m
```

3. Gere um relatório HTML para inspeção local:

```bash
coverage html
# então abra htmlcov/index.html no navegador
```

4. Gere um relatório XML (útil para integrações de CI, como Codecov):

```bash
coverage xml -o coverage.xml
```

## Testes de integração

Os testes de integração ficam em `tests/integration/` e são ignorados por padrão. Para executá-los localmente, defina a variável de ambiente:

```bash
export RUN_INTEGRATION=true
coverage run -m pytest tests/integration -q
coverage report -m
```

## Notas da CI

- A CI do repositório (`.github/workflows/ci.yml`) executa `coverage run -m pytest`, gera `coverage.xml` e falha o job se a cobertura ficar abaixo do limite (`--fail-under=75`).
- Removemos o upload automático para Codecov da CI; se quiser publicar cobertura em um serviço externo, adicione uma etapa explícita de upload e forneça o token necessário como secret do repositório.

## PRs de autofix/formatting

- A CI inclui um job `autofix` que cria um PR de formatação usando `peter-evans/create-pull-request`. O workflow agora cria uma branch única por execução e a remove após o merge para evitar colisões com execuções anteriores.

Se quiser, posso adicionar um alvo `coverage` no make ou um script pequeno para simplificar esses comandos.
