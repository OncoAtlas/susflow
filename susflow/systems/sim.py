# susflow/systems/sim.py
from .. import config as _cfg
from .base import generic_load, generic_bulk_load

"""Loads SIM data (mortality)."""

def load(uf: str, year: int, **kwargs):
    conf = _cfg.SIM["uf"] # Pega as regras do SIM no config
    return generic_load(
        system="SIM",
        sub_dir=conf["ftp_dir"],
        table="DO",
        uf=uf,
        year=year,
        **kwargs
    )

def load_bulk(ufs: list, year: int, **kwargs):
    conf = _cfg.SIM["uf"]
    return generic_bulk_load(
        system="SIM",
        sub_dir=conf["ftp_dir"],
        table="DO",
        ufs=ufs,
        year=year,
        max_workers=_cfg.MAX_WORKERS, # Usa o limite definido no config
        **kwargs
    )