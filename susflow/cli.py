"""
susflow/cli.py
==============
Command-line interface for susflow.
"""

import argparse
import sys
from pathlib import Path

from .systems import cnes, ibge_pop, pni, siasus, sihsus, sim, sinan, sinasc


def _dest_force(p):
    p.add_argument(
        "--destination",
        metavar="DIR",
        type=Path,
        default=None,
        help="destination folder (default: cache)",
    )
    p.add_argument(
        "--force", action="store_true", help="re-download even if already cached"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="susflow",
        description="Download DATASUS public health data.",
    )
    subs = parser.add_subparsers(dest="system", metavar="SYSTEM", required=True)

    # ------------------------------------------------------------------
    # SIM — Mortality Information System
    # ------------------------------------------------------------------
    sim_p = subs.add_parser("sim", help="Mortality Information System")
    sim_a = sim_p.add_subparsers(dest="action", required=True)

    p = sim_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None, help="filter by state (e.g. SP)")
    p.set_defaults(func=_sim_list)

    p = sim_a.add_parser("download", help="download DO{UF}{YYYY}.dbc")
    p.add_argument("uf", help="state code (e.g. SP)")
    p.add_argument("year", type=int, help="4-digit year")
    _dest_force(p)
    p.set_defaults(func=_sim_download)

    # ------------------------------------------------------------------
    # SINASC — Live Births
    # ------------------------------------------------------------------
    sinasc_p = subs.add_parser("sinasc", help="Live Births Information System")
    sinasc_a = sinasc_p.add_subparsers(dest="action", required=True)

    p = sinasc_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.set_defaults(func=_sinasc_list)

    p = sinasc_a.add_parser("download", help="download DN{UF}{YYYY}.dbc")
    p.add_argument("uf")
    p.add_argument("year", type=int)
    _dest_force(p)
    p.set_defaults(func=_sinasc_download)

    # ------------------------------------------------------------------
    # SINAN — Notifiable Diseases
    # ------------------------------------------------------------------
    sinan_p = subs.add_parser("sinan", help="Notifiable Diseases Information System")
    sinan_a = sinan_p.add_subparsers(dest="action", required=True)

    p = sinan_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--disease", default=None, help="filter by disease code")
    p.add_argument("--preliminary", action="store_true")
    p.set_defaults(func=_sinan_list)

    p = sinan_a.add_parser("diseases", help="list all disease codes")
    p.set_defaults(func=_sinan_diseases)

    p = sinan_a.add_parser("download", help="download {DISEASE}BR{YY}.dbc")
    p.add_argument("disease", help="disease code (e.g. DENG)")
    p.add_argument("year", type=int)
    p.add_argument("--preliminary", action="store_true")
    _dest_force(p)
    p.set_defaults(func=_sinan_download)

    # ------------------------------------------------------------------
    # SIASUS — Outpatient
    # ------------------------------------------------------------------
    siasus_p = subs.add_parser("siasus", help="Outpatient Information System (SUS)")
    siasus_a = siasus_p.add_subparsers(dest="action", required=True)

    p = siasus_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--prefix", default="PA", help="file prefix (default: PA)")
    p.set_defaults(func=_siasus_list)

    p = siasus_a.add_parser("download", help="download {PREFIX}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("year", type=int)
    p.add_argument("month", type=int)
    p.add_argument("--prefix", default="PA")
    _dest_force(p)
    p.set_defaults(func=_siasus_download)

    # ------------------------------------------------------------------
    # SIHSUS — Hospital Admissions
    # ------------------------------------------------------------------
    sihsus_p = subs.add_parser("sihsus", help="Hospital Admissions Information System")
    sihsus_a = sihsus_p.add_subparsers(dest="action", required=True)

    p = sihsus_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--prefix", default="RD", help="file prefix (default: RD)")
    p.set_defaults(func=_sihsus_list)

    p = sihsus_a.add_parser("download", help="download {PREFIX}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("year", type=int)
    p.add_argument("month", type=int)
    p.add_argument("--prefix", default="RD")
    _dest_force(p)
    p.set_defaults(func=_sihsus_download)

    # ------------------------------------------------------------------
    # CNES — Health Establishments
    # ------------------------------------------------------------------
    cnes_p = subs.add_parser("cnes", help="National Registry of Health Establishments")
    cnes_a = cnes_p.add_subparsers(dest="action", required=True)

    p = cnes_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.add_argument("--type", default="ST", dest="type_", help="subtype (default: ST)")
    p.set_defaults(func=_cnes_list)

    p = cnes_a.add_parser("download", help="download {TYPE}{UF}{YY}{MM}.dbc")
    p.add_argument("uf")
    p.add_argument("year", type=int)
    p.add_argument("month", type=int)
    p.add_argument("--type", default="ST", dest="type_")
    _dest_force(p)
    p.set_defaults(func=_cnes_download)

    # ------------------------------------------------------------------
    # PNI — Immunization
    # ------------------------------------------------------------------
    pni_p = subs.add_parser("pni", help="National Immunization Program")
    pni_a = pni_p.add_subparsers(dest="action", required=True)

    p = pni_a.add_parser("list", help="list available files on FTP")
    p.add_argument("--uf", default=None)
    p.set_defaults(func=_pni_list)

    p = pni_a.add_parser("download", help="download DPNI{UF}{YY}.DBF")
    p.add_argument("uf")
    p.add_argument("year", type=int)
    _dest_force(p)
    p.set_defaults(func=_pni_download)

    # ------------------------------------------------------------------
    # IBGE — Population Estimates (POP)
    # ------------------------------------------------------------------
    ibge_p = subs.add_parser("ibge", help="IBGE Population Estimates")
    ibge_a = ibge_p.add_subparsers(dest="action", required=True)

    p = ibge_a.add_parser("list", help="list available files on FTP")
    p.set_defaults(func=_ibge_list)

    p = ibge_a.add_parser("download", help="download POPBR{YY}.zip")
    p.add_argument("year", type=int, help="4-digit year (e.g. 2000)")
    _dest_force(p)
    p.set_defaults(func=_ibge_download)

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


def _sim_list(args):
    for f in sim.list_files(args.uf):
        print(f)


def _sim_download(args):
    print(
        sim.download(args.uf, args.year, destination=args.destination, force=args.force)
    )


def _sinasc_list(args):
    for f in sinasc.list_files(args.uf):
        print(f)


def _sinasc_download(args):
    print(
        sinasc.download(
            args.uf, args.year, destination=args.destination, force=args.force
        )
    )


def _sinan_list(args):
    for f in sinan.list_files(args.disease, preliminary=args.preliminary):
        print(f)


def _sinan_diseases(args):
    for code, desc in sinan.diseases().items():
        print(f"{code:<10} {desc}")


def _sinan_download(args):
    print(
        sinan.download(
            args.disease,
            args.year,
            destination=args.destination,
            force=args.force,
            preliminary=args.preliminary,
        )
    )


def _siasus_list(args):
    for f in siasus.list_files(args.uf, prefix=args.prefix):
        print(f)


def _siasus_download(args):
    print(
        siasus.download(
            args.uf,
            args.year,
            args.month,
            prefix=args.prefix,
            destination=args.destination,
            force=args.force,
        )
    )


def _sihsus_list(args):
    for f in sihsus.list_files(args.uf, prefix=args.prefix):
        print(f)


def _sihsus_download(args):
    print(
        sihsus.download(
            args.uf,
            args.year,
            args.month,
            prefix=args.prefix,
            destination=args.destination,
            force=args.force,
        )
    )


def _cnes_list(args):
    for f in cnes.list_files(args.uf, type_=args.type_):
        print(f)


def _cnes_download(args):
    print(
        cnes.download(
            args.uf,
            args.year,
            args.month,
            type_=args.type_,
            destination=args.destination,
            force=args.force,
        )
    )


def _pni_list(args):
    for f in pni.list_files(args.uf):
        print(f)


def _pni_download(args):
    print(
        pni.download(args.uf, args.year, destination=args.destination, force=args.force)
    )


def _ibge_list(args):
    for f in ibge_pop.list_files():
        print(f)


def _ibge_download(args):
    print(
        ibge_pop.download(args.year, destination=args.destination, force=args.force)
    )
