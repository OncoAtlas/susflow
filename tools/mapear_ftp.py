"""
tools/mapear_ftp.py
===================
Map the DATASUS FTP directory structure.

Usage:
    python mapear_ftp.py                   # print to stdout
    python mapear_ftp.py --salvar          # save to mapas/mapa_ftp_<timestamp>.txt
    python mapear_ftp.py --salvar --quiet  # save without printing
    python mapear_ftp.py --profundo        # descend MAX_PROF_PADRAO + 1 levels
    python mapear_ftp.py --alvo /dissemin/publicos/SINAN/DADOS  # specific path
"""

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

FTP_HOST = "ftp.datasus.gov.br"

# Folder where generated .txt files will be saved (relative to this script)
PASTA_SAIDA = "mapas"

# Default recursion depth for subdirectories
MAX_PROF_PADRAO = 1

# Paths explored when no --alvo is passed (v1 systems)
ALVOS_PADRAO = [
    "/dissemin/publicos/SIM/CID10",
    "/dissemin/publicos/SINASC/NOV/DNRES",
    "/dissemin/publicos/SINAN/DADOS",
    "/dissemin/publicos/SIHSUS/200801_/Dados",
    "/dissemin/publicos/SIASUS/200801_/Dados",
    "/dissemin/publicos/CNES/200508_/Dados",
    "/dissemin/publicos/PNI/DADOS",
    "/dissemin/publicos/IBGE/POP",
]

# ---------------------------------------------------------------------------

import argparse
from datetime import datetime
from ftplib import FTP
from pathlib import Path


def nova_conexao() -> FTP:
    """Open a fresh FTP connection. Reconnecting per target avoids the '200 Type set to A' bug."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def listar_pasta(
    ftp: FTP,
    caminho: str,
    linhas: list[str],
    profundidade: int = 0,
    max_prof: int = MAX_PROF_PADRAO,
) -> None:
    try:
        ftp.cwd(caminho)
        itens: list[str] = []
        ftp.retrlines("LIST", itens.append)

        subdirs = []
        for linha in itens:
            eh_dir = "<DIR>" in linha
            nome = linha.split("<DIR>")[-1].strip() if eh_dir else linha.split()[-1]
            indent = "  " * profundidade

            if eh_dir:
                subdirs.append(nome)
                linhas.append(f"{indent}DIR  {caminho}/{nome}/")
            else:
                partes = linha.split()
                tam = partes[2] if len(partes) > 3 else "?"
                linhas.append(f"{indent}FILE {tam:>12}  {caminho}/{nome}")

        if profundidade < max_prof:
            for sub in subdirs:
                listar_pasta(
                    ftp, f"{caminho}/{sub}", linhas, profundidade + 1, max_prof
                )
                ftp.cwd(caminho)

    except Exception as e:
        linhas.append("  " * profundidade + f"ERRO {caminho}: {e}")


def mapear(
    alvos: list[str],
    max_prof: int = MAX_PROF_PADRAO,
    imprimir: bool = True,
    salvar: bool = False,
) -> list[str]:
    todas: list[str] = [
        f"DATASUS FTP Map — {FTP_HOST}",
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Max depth: {max_prof}",
        "",
    ]

    for caminho in alvos:
        todas.extend(["", "=" * 70, f"PASTA: {caminho}", "=" * 70])

        if imprimir:
            print(f"\nConnecting → {caminho} ...")

        ftp = nova_conexao()
        listar_pasta(ftp, caminho, todas, max_prof=max_prof)
        ftp.quit()

        if imprimir:
            print("  ✓ done")

    if imprimir:
        print("\n" + "\n".join(todas))

    if salvar:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta = Path(__file__).parent / PASTA_SAIDA
        pasta.mkdir(exist_ok=True)
        destino = pasta / f"mapa_ftp_{ts}.txt"
        destino.write_text("\n".join(todas), encoding="utf-8")
        print(f"\nSaved to: {destino}")

    return todas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map the DATASUS FTP.")
    parser.add_argument("--salvar", action="store_true", help="Save result to .txt")
    parser.add_argument("--quiet", action="store_true", help="Do not print to terminal")
    parser.add_argument(
        "--profundo",
        action="store_true",
        help=f"Descend {MAX_PROF_PADRAO + 1} levels instead of {MAX_PROF_PADRAO}",
    )
    parser.add_argument(
        "--alvo", action="append", help="Specific FTP path (repeatable)"
    )
    args = parser.parse_args()

    mapear(
        alvos=args.alvo or ALVOS_PADRAO,
        max_prof=MAX_PROF_PADRAO + 1 if args.profundo else MAX_PROF_PADRAO,
        imprimir=not args.quiet,
        salvar=args.salvar,
    )
