"""
tests/teste_download.py
=======================
Teste end-to-end: baixa um arquivo real de cada sistema implementado
e valida que o DataFrame retornado tem dados.

Requer conexão com a internet (acessa ftp.datasus.gov.br).

Uso:
    python tests/teste_download.py
    python tests/teste_download.py --sistema sinasc
    python tests/teste_download.py --sistema sim
    python tests/teste_download.py --sistema sinan
"""

import argparse
import sys
import traceback

import pandas as pd

# ── helpers ────────────────────────────────────────────────────────────────

def ok(msg: str) -> None:
    print(f"  ✅ {msg}")

def falhou(msg: str, erro: Exception) -> None:
    print(f"  ❌ {msg}")
    traceback.print_exc()

def cabecalho(titulo: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print(f"{'─' * 50}")

def checar_df(df: pd.DataFrame, label: str) -> None:
    assert isinstance(df, pd.DataFrame), "retorno não é DataFrame"
    assert len(df) > 0,                  "DataFrame vazio"
    assert len(df.columns) > 0,          "DataFrame sem colunas"
    ok(f"{label} → {len(df):,} linhas × {len(df.columns)} colunas")


# ── testes por sistema ──────────────────────────────────────────────────────

def testar_sinasc() -> bool:
    cabecalho("SINASC — Nascidos Vivos")
    from susflow.systems import sinasc
    passou = True

    # listar
    try:
        arquivos = sinasc.listar(uf="SP")
        assert len(arquivos) > 0
        ok(f"listar(uf='SP') → {len(arquivos)} arquivos")
    except Exception as e:
        falhou("listar()", e); passou = False

    # ler (ano pequeno = arquivo menor = download mais rápido)
    try:
        df = sinasc.ler(uf="AC", ano=1996)
        checar_df(df, "ler(uf='AC', ano=1996)")
    except Exception as e:
        falhou("ler()", e); passou = False

    # cache: segunda chamada não deve bater no FTP
    try:
        df2 = sinasc.ler(uf="AC", ano=1996)
        checar_df(df2, "ler() — cache hit")
    except Exception as e:
        falhou("ler() cache", e); passou = False

    # validação de parâmetros
    try:
        sinasc.baixar(uf="XX", ano=2022)
        print("  ❌ deveria ter levantado ValueError para UF inválida")
        passou = False
    except ValueError:
        ok("ValueError para UF inválida")

    try:
        sinasc.baixar(uf="SP", ano=1800)
        print("  ❌ deveria ter levantado ValueError para ano inválido")
        passou = False
    except ValueError:
        ok("ValueError para ano fora do intervalo")

    return passou


def testar_sim() -> bool:
    cabecalho("SIM — Mortalidade")
    from susflow.systems import sim
    passou = True

    # por UF
    try:
        arquivos = sim.listar(uf="AC")
        assert len(arquivos) > 0
        ok(f"listar(uf='AC') → {len(arquivos)} arquivos")
    except Exception as e:
        falhou("listar()", e); passou = False

    try:
        df = sim.ler(uf="AC", ano=1996)
        checar_df(df, "ler(uf='AC', ano=1996)")
    except Exception as e:
        falhou("ler() por UF", e); passou = False

    # especial (DOFET)
    try:
        arquivos_esp = sim.listar_especial(tipo="MAT")
        assert len(arquivos_esp) > 0
        ok(f"listar_especial(tipo='MAT') → {len(arquivos_esp)} arquivos")
    except Exception as e:
        falhou("listar_especial()", e); passou = False

    try:
        df_esp = sim.ler_especial(tipo="MAT", ano=2000)
        checar_df(df_esp, "ler_especial(tipo='MAT', ano=2000)")
    except Exception as e:
        falhou("ler_especial()", e); passou = False

    # validações
    try:
        sim.baixar_especial(tipo="ZZZ", ano=2020)
        print("  ❌ deveria ter levantado ValueError para tipo inválido")
        passou = False
    except ValueError:
        ok("ValueError para tipo especial inválido")

    return passou


def testar_sinan() -> bool:
    cabecalho("SINAN — Agravos de Notificação")
    from susflow.systems import sinan
    passou = True

    # dicionário de doenças
    try:
        d = sinan.doencas()
        assert len(d) > 0
        ok(f"doencas() → {len(d)} doenças mapeadas")
    except Exception as e:
        falhou("doencas()", e); passou = False

    # listar
    try:
        arquivos = sinan.listar(doenca="DENG")
        assert len(arquivos) > 0
        ok(f"listar(doenca='DENG') → {len(arquivos)} arquivos")
    except Exception as e:
        falhou("listar()", e); passou = False

    # ler (tuberculose — arquivo menor)
    try:
        df = sinan.ler(doenca="TUBE", ano=2007)
        checar_df(df, "ler(doenca='TUBE', ano=2007)")
    except Exception as e:
        falhou("ler()", e); passou = False

    # validações
    try:
        sinan.baixar(doenca="INVALIDA", ano=2020)
        print("  ❌ deveria ter levantado ValueError para doença inválida")
        passou = False
    except ValueError:
        ok("ValueError para doença inválida")

    return passou


# ── main ────────────────────────────────────────────────────────────────────

SISTEMAS = {
    "sinasc": testar_sinasc,
    "sim":    testar_sim,
    "sinan":  testar_sinan,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Teste end-to-end do susflow.")
    parser.add_argument("--sistema", choices=list(SISTEMAS), help="Testar apenas um sistema")
    args = parser.parse_args()

    alvos = {args.sistema: SISTEMAS[args.sistema]} if args.sistema else SISTEMAS

    resultados = {}
    for nome, fn in alvos.items():
        resultados[nome] = fn()

    print(f"\n{'═' * 50}")
    print("  Resultado final")
    print(f"{'═' * 50}")
    tudo_ok = True
    for nome, passou in resultados.items():
        status = "✅ passou" if passou else "❌ falhou"
        print(f"  {nome.upper():<10} {status}")
        if not passou:
            tudo_ok = False

    sys.exit(0 if tudo_ok else 1)
