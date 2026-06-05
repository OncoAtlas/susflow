from importlib.metadata import PackageNotFoundError, version

from .batch import download_batch
from .ftp import FileNotFoundOnFTPError, FTPError
from .reader import ReadError, read
from .systems import cnes, ibge_pop, pni, siasus, sihsus, sim, sinan, sinasc

try:
    __version__ = version("susflow")
except PackageNotFoundError:
    __version__ = "0.0.0"  # fallback (e.g. editable without metadata)
