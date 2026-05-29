# CONTRIBUTING.md

Obrigado pelo interesse em contribuir com o SUSFlow. Este documento explica o fluxo de trabalho preferido, o estilo de código, as expectativas de testes e dicas para fazer uma contribuição bem-sucedida.

## Começando

1. Faça um fork do repositório e crie uma branch para o seu trabalho:

```bash
git clone https://github.com/seu-usuario/susflow.git
cd susflow
git checkout -b feat/sua-funcionalidade
```

2. Crie um ambiente virtual e instale as dependências de desenvolvimento:

```bash
python -m venv .venv
. ./.venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

## Estilo & linters

- Estilo de código: siga o formato do `black`.
- Ordenação de imports: use o `isort`.
- Verificações estáticas: usamos `ruff` para linting.

Execute todas as verificações localmente antes de abrir um PR:

```bash
ruff .
isort --check-only .
black --check .
```

## Testes

- Os testes unitários devem ser adicionados em `tests/unit/` e evitam chamadas de rede, fazendo mock de FTP e IO de arquivos.
- Os testes de integração que exigem acesso à rede (FTP ao vivo) devem ficar em `tests/integration/` e serem marcados como opcionais. Não os execute na CI por padrão.

Exemplo de execução de testes:

```bash
pytest -q
coverage run -m pytest
coverage report -m
```

## Mensagens de commit & PRs

- Mantenha os commits focados e atômicos.
- Escreva descrições de PR claras explicando as mudanças e a motivação.
- Vincule issues relacionadas e inclua screenshots ou exemplos de saída quando aplicável.

## Mudanças de API

Evite quebrar a API pública sempre que possível. Se uma mudança de API for necessária:

- Abra uma issue descrevendo a motivação e o plano de migração.
- Mantenha a API antiga como depreciada por pelo menos uma release, com avisos claros.

## Documentação

- Atualize `docs/` para qualquer mudança de comportamento ou API.
- Mantenha os exemplos em `README.md` e `docs/` precisos.

## Segurança

Se descobrir um problema de segurança, reporte-o de forma privada abrindo uma issue e marcando-a como sensível. Não divulgue problemas de segurança publicamente até que eles sejam corrigidos.

## Obrigado

Agradecemos suas contribuições. Mantenha um tom amigável e construtivo nas discussões e revisões de código.
