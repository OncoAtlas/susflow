# Test coverage — how to run and generate reports

This file explains how to run the test suite with coverage and generate reports locally (the CI already runs coverage and enforces a minimum threshold).

Commands

1. Create and activate a virtual environment, install the package and test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e . || pip install .
pip install coverage pytest pytest-mock
```

2. Run tests under coverage and show a terminal summary:

```bash
coverage run -m pytest -q
coverage report -m
```

3. Generate an HTML report for local inspection:

```bash
coverage html
# then open htmlcov/index.html in your browser
```

4. Produce an XML report (useful for CI integrations like Codecov):

```bash
coverage xml -o coverage.xml
```

Integration tests

Integration tests are placed under `tests/integration/` and are skipped by default. To run them locally set the environment variable:

```bash
export RUN_INTEGRATION=true
coverage run -m pytest tests/integration -q
coverage report -m
```

CI notes

- The repository CI (`.github/workflows/ci.yml`) runs `coverage run -m pytest` and fails the job if coverage is below the threshold (`--fail-under=70`).
- If you want coverage uploaded to a service such as Codecov, add a step to the workflow that uploads `coverage.xml` using the official Codecov action and provide the `CODECOV_TOKEN` secret.

If you want, I can add a `coverage` make target or a small script to simplify these commands. 
