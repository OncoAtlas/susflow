CONTRIBUTING.md
================

Thank you for your interest in contributing to SUSFlow. This document explains the preferred workflow, code style, testing expectations and tips for making a successful contribution.

Getting started
-
1. Fork the repository and create a branch for your work:

```bash
git clone https://github.com/your-user/susflow.git
cd susflow
git checkout -b feat/your-feature
```

2. Create a virtual environment and install developer dependencies:

```bash
python -m venv .venv
. ./.venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

Style & linters
-
- Code style: follow `black` formatting.
- Import ordering: use `isort`.
- Static checks: we use `ruff` for linting.

Run all checks locally before opening a PR:

```bash
ruff .
isort --check-only .
black --check .
```

Testing
-
- Unit tests must be added under `tests/unit/` and should avoid network calls by mocking FTP and file IO.
- Integration tests that require network access (live FTP) should be under `tests/integration/` and marked as optional. Do not run them in CI by default.

Example of running tests:

```bash
pytest -q
coverage run -m pytest
coverage report -m
```

Commit messages & PRs
-
- Keep commits focused and atomic.
- Write clear PR descriptions explaining the changes and motivation.
- Link related issues and include screenshots or example outputs if applicable.

API changes
-
Avoid breaking public APIs whenever possible. If an API change is necessary:

- Open an issue describing the rationale and migration plan.
- Keep old API as deprecated for at least one release with clear warnings.

Documentation
-
- Update `docs/` for any behavior or API changes.
- Keep examples in `README.md` and `docs/` accurate.

Security
-
If you discover a security issue, please report it privately by opening an issue and marking it as sensitive. Do not disclose security issues publicly until they are patched.

Thank you
-
We appreciate your contributions. Maintain a friendly, constructive tone in discussions and code reviews.
