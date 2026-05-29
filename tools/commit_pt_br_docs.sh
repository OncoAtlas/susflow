#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

commit_group() {
    local message="$1"
    shift

    if [[ $# -eq 0 ]]; then
        echo "Nenhum arquivo alvo para: $message"
        return 0
    fi

    git add -A -- "$@"

    if git diff --cached --quiet -- "$@"; then
        echo "Nenhuma alteração para: $message"
        return 0
    fi

    git commit -m "$message"
    echo "Commit criado: $message"
}

commit_group "docs: refresh root README" README.md

commit_group "docs: migrate documentation structure to new English layout" \
    docs/cnes.md \
    docs/pni.md \
    docs/siasus.md \
    docs/sihsus.md \
    docs/sim.md \
    docs/sinan.md \
    docs/sinasc.md \
    docs/summary.md \
    docs/contributing/CONTRIBUTING.md \
    docs/contributing/coverage.md \
    docs/en/ \
    CONTRIBUTING.md

commit_group "docs(pt-br): add Portuguese contributor docs" \
    docs/pt-br/CONTRIBUTING.md \
    docs/pt-br/coverage.md \
    docs/pt-br/README.md

commit_group "chore: add documentation commit helper" tools/commit_pt_br_docs.sh

printf '\nStatus final:\n'
git status --short
