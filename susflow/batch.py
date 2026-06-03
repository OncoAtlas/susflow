"""
susflow/batch.py
================
Concurrent download utility.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def download_batch(
    tasks: Iterable[Callable[[], T]],
    workers: int = 4,
) -> list[T]:
    """Download multiple files concurrently.

    Each task must be a zero-argument callable that performs one download and
    returns its result (typically a Path).  Build tasks with functools.partial
    or lambdas:

        from functools import partial
        import susflow.systems.sim as sim

        paths = download_batch([
            partial(sim.download, "SP", 2022),
            partial(sim.download, "RJ", 2022),
            partial(sim.download, "MG", 2022),
        ])

    Results are returned in the same order as the input tasks.
    The first exception (in submission order) is re-raised after all tasks
    complete.

    workers : max concurrent threads (default 4).
              Tune downward if the FTP server rejects too many connections.
    """
    tasks = list(tasks)
    if not tasks:
        return []
    with ThreadPoolExecutor(max_workers=min(workers, len(tasks))) as pool:
        futures = [pool.submit(fn) for fn in tasks]
    return [f.result() for f in futures]
