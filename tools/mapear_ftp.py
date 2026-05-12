"""
tools/mapear_ftp.py
===================
Mapeia a estrutura de diretórios do FTP do DATASUS e lista os arquivos
encontrados em cada caminho alvo.

Uso:
    python mapear_ftp.py                  # imprime na tela
    python mapear_ftp.py --salvar         # salva em mapa_ftp_<timestamp>.txt
    python mapear_ftp.py --salvar --quiet # salva sem imprimir

Flags:
    --salvar   Salva o resultado em arquivo .txt
    --quiet    Suprime a impressão no terminal (só faz sentido com --salvar)
    --profundo Desce mais um nível de subdiretórios (mais lento)
    --alvo     Caminho FTP específico a explorar (pode repetir)
               Ex: --alvo /dissemin/publicos/SIM/CID10

Exemplos:
    python mapear_ftp.py --alvo /dissemin/publicos/SINAN/DADOS --salvar
    python mapear_ftp.py --profundo --salvar --quiet
"""

import argparse
from datetime import datetime
from ftplib import FTP
from pathlib import Path

FTP_HOST = "ftp.datasus.gov.br"

# Caminhos explorados por padrão (v1 da biblioteca)
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


def nova_conexao() -> FTP:
    """Abre uma conexão FTP limpa. Reconectar por alvo evita o bug '200 Type set to A'."""
    ftp = FTP()
    ftp.connect(FTP_HOST, 21)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def listar_pasta(ftp: FTP, caminho: str, linhas: list[str], profundidade: int = 0, max_prof: int = 1) -> None:
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
                listar_pasta(ftp, f"{caminho}/{sub}", linhas, profundidade + 1, max_prof)
                ftp.cwd(caminho)

    except Exception as e:
        linhas.append("  " * profundidade + f"ERRO {caminho}: {e}")


def mapear(alvos: list[str], max_prof: int = 1, imprimir: bool = True, salvar: bool = False) -> list[str]:
    todas: list[str] = [
        f"Mapa FTP DATASUS — {FTP_HOST}",
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Profundidade máxima: {max_prof}",
        "",
    ]

    for caminho in alvos:
        cabecalho = [
            "",
            "=" * 70,
            f"PASTA: {caminho}",
            "=" * 70,
        ]
        todas.extend(cabecalho)

        if imprimir:
            print(f"\nConectando → {caminho} ...")

        ftp = nova_conexao()
        listar_pasta(ftp, caminho, todas, max_prof=max_prof)
        ftp.quit()

        if imprimir:
            print("  ✓ concluído")

    if imprimir:
        print("\n" + "\n".join(todas))

    if salvar:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = Path(__file__).parent / f"mapa_ftp_{ts}.txt"
        destino.write_text("\n".join(todas), encoding="utf-8")
        print(f"\nSalvo em: {destino}")

    return todas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mapeia o FTP do DATASUS.")
    parser.add_argument("--salvar",  action="store_true", help="Salva resultado em .txt")
    parser.add_argument("--quiet",   action="store_true", help="Não imprime no terminal")
    parser.add_argument("--profundo", action="store_true", help="Desce 2 níveis em vez de 1")
    parser.add_argument("--alvo",    action="append",     help="Caminho FTP específico (repetível)")
    args = parser.parse_args()

    alvos    = args.alvo or ALVOS_PADRAO
    max_prof = 2 if args.profundo else 1
    imprimir = not args.quiet

    mapear(alvos=alvos, max_prof=max_prof, imprimir=imprimir, salvar=args.salvar)
