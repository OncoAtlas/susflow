"""
susflow/cli.py
==============
Command-line interface for susflow.
"""

import argparse
import sys
from pathlib import Path

from .systems import cnes, pni, siasus, sihsus, sim, sinan, sinasc


def _dest_forcar(p):
    p.add_argument("--destino", metavar="DIR", type=Path, default=None,
                   help="destination folder (default: cache)")
    p.add_argument("--forcar", action="store_true",
                   help="re-download even if already cached")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="susflow",
        description="Download DATASUS public health data.",
    )
    subs = parser.add_subparsers(dest="sistema", metavar="SISTEMA", required=True)

    # ------------------------------------------------------------------
    # SIM — Mortality Information System
    # ------------------------------------------------------------------
    sim_p = subs.add_parser("sim", help="Mortality Information System")
    sim_a = sim_p.add_subparsers(dest="acao", required=True)

    p = sim_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None, help="filter by state (e.g. SP)")
    p.set_defaults(func=_sim_listar)

    p = sim_a.add_parser("baixar", help="download DO{UF}{YYYY}.dbc")
    p.add_argument("uf", help="state code (e.g. SP)")
    p.add_argument("ano", type=int, help="4-digit year")
    _dest_forcar(p)
    p.set_defaults(func=_sim_baixar)

    # ------------------------------------------------------------------
    # SINASC — Live Births
    # ------------------------------------------------------------------
    sinasc_p = subs.add_parser("sinasc", help="Live Births Information System")
    sinasc_a = sinasc_p.add_subparsers(dest="acao", required=True)

    p = sinasc_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.set_defaults(func=_sinasc_listar)

    p = sinasc_a.add_parser("baixar", help="download DN{UF}{YYYY}.dbc")
    p.add_argument("uf")
    p.add_argument("ano", type=int)
    _dest_forcar(p)
    p.set_defaults(func=_sinasc_baixar)

    # ------------------------------------------------------------------
    # SINAN — Notifiable Diseases
    # ------------------------------------------------------------------
    sinan_p = subs.add_parser("sinan", help="Notifiable Diseases Information System")
    sinan_a = sinan_p.add_subparsers(dest="acao", required=True)

    p = sinan_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--doenca", default=None, help="filter by disease code")
    p.add_argument("--preliminar", action="store_true")
    p.set_defaults(func=_sinan_listar)

    p = sinan_a.add_parser("doencas", help="list all disease codes")
    p.set_defaults(func=_sinan_doencas)

    p = sinan_a.add_parser("baixar", help="download {DISEASE}BR{YY}.dbc")
    p.add_argument("doenca", help="disease code (e.g. DENG)")
    p.add_argument("ano", type=int)
    p.add_argument("--preliminar", action="store_true")
    _dest_forcar(p)
    p.set_defaults(func=_sinan_baixar)

    # ------------------------------------------------------------------
    # SIASUS — Outpatient
    # ------------------------------------------------------------------
    siasus_p = subs.add_parser("siasus", help="Outpatient Information System (SUS)")
    siasus_a = siasus_p.add_subparsers(dest="acao", required=True)

    p = siasus_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--prefixo", default="PA", help="file prefix (default: PA)")
    p.set_defaults(func=_siasus_listar)

    p = siasus_a.add_parser("baixar", help="download {PREFIX}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("ano", type=int)
    p.add_argument("mes", type=int)
    p.add_argument("--prefixo", default="PA")
    _dest_forcar(p)
    p.set_defaults(func=_siasus_baixar)

    # ------------------------------------------------------------------
    # SIHSUS — Hospital Admissions
    # ------------------------------------------------------------------
    sihsus_p = subs.add_parser("sihsus", help="Hospital Admissions Information System")
    sihsus_a = sihsus_p.add_subparsers(dest="acao", required=True)

    p = sihsus_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--prefixo", default="RD", help="file prefix (default: RD)")
    p.set_defaults(func=_sihsus_listar)

    p = sihsus_a.add_parser("baixar", help="download {PREFIX}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("ano", type=int)
    p.add_argument("mes", type=int)
    p.add_argument("--prefixo", default="RD")
    _dest_forcar(p)
    p.set_defaults(func=_sihsus_baixar)

    # ------------------------------------------------------------------
    # CNES — Health Establishments
    # ------------------------------------------------------------------
    cnes_p = subs.add_parser("cnes", help="National Registry of Health Establishments")
    cnes_a = cnes_p.add_subparsers(dest="acao", required=True)

    p = cnes_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--tipo", default="ST", help="subtype (default: ST)")
    p.set_defaults(func=_cnes_listar)

    p = cnes_a.add_parser("baixar", help="download {TYPE}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("ano", type=int)
    p.add_argument("mes", type=int)
    p.add_argument("--tipo", default="ST")
    _dest_forcar(p)
    p.set_defaults(func=_cnes_baixar)

    # ------------------------------------------------------------------
    # PNI — Immunization
    # ------------------------------------------------------------------
    pni_p = subs.add_parser("pni", help="National Immunization Program")
    pni_a = pni_p.add_subparsers(dest="acao", required=True)

    p = pni_a.add_parser("listar", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.set_defaults(func=_pni_listar)

    p = pni_a.add_parser("baixar", help="download DPNI{UF}{YY}.DBF")
    p.add_argument("uf")
    p.add_argument("ano", type=int)
    _dest_forcar(p)
    p.set_defaults(func=_pni_baixar)

    # ------------------------------------------------------------------
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def _sim_listar(args):
    for f in sim.listar(args.uf):
        print(f)


def _sim_baixar(args):
    print(sim.baixar(args.uf, args.ano, destino=args.destino, forcar=args.forcar))


def _sinasc_listar(args):
    for f in sinasc.listar(args.uf):
        print(f)


def _sinasc_baixar(args):
    print(sinasc.baixar(args.uf, args.ano, destino=args.destino, forcar=args.forcar))


def _sinan_listar(args):
    for f in sinan.listar(args.doenca, preliminar=args.preliminar):
        print(f)


def _sinan_doencas(args):
    for code, desc in sinan.doencas().items():
        print(f"{code:<10} {desc}")


def _sinan_baixar(args):
    print(sinan.baixar(
        args.doenca, args.ano,
        destino=args.destino, forcar=args.forcar, preliminar=args.preliminar,
    ))


def _siasus_listar(args):
    for f in siasus.listar(args.uf, prefixo=args.prefixo):
        print(f)


def _siasus_baixar(args):
    print(siasus.baixar(
        args.uf, args.ano, args.mes,
        prefixo=args.prefixo, destino=args.destino, forcar=args.forcar,
    ))


def _sihsus_listar(args):
    for f in sihsus.listar(args.uf, prefixo=args.prefixo):
        print(f)


def _sihsus_baixar(args):
    print(sihsus.baixar(
        args.uf, args.ano, args.mes,
        prefixo=args.prefixo, destino=args.destino, forcar=args.forcar,
    ))


def _cnes_listar(args):
    for f in cnes.listar(args.uf, tipo=args.tipo):
        print(f)


def _cnes_baixar(args):
    print(cnes.baixar(
        args.uf, args.ano, args.mes,
        tipo=args.tipo, destino=args.destino, forcar=args.forcar,
    ))


def _pni_listar(args):
    for f in pni.listar(args.uf):
        print(f)


def _pni_baixar(args):
    print(pni.baixar(args.uf, args.ano, destino=args.destino, forcar=args.forcar))
