"""
susflow/batch.py
================
Concurrent download utility.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def baixar_lote(
    tarefas: Iterable[Callable[[], T]],
    workers: int = 4,
) -> list[T]:
    """Download multiple files concurrently.

    Each task must be a zero-argument callable that performs one download and
    returns its result (typically a Path).  Build tasks with functools.partial
    or lambdas:

        from functools import partial
        import susflow.systems.sim as sim

        paths = baixar_lote([
            partial(sim.baixar, "SP", 2022),
            partial(sim.baixar, "RJ", 2022),
            partial(sim.baixar, "MG", 2022),
        ])

    Results are returned in the same order as the input tasks.
    The first exception (in submission order) is re-raised after all tasks
    complete.

    workers : max concurrent threads (default 4).
              Tune downward if the FTP server rejects too many connections.
    """
    tarefas = list(tarefas)
    if not tarefas:
        return []
    with ThreadPoolExecutor(max_workers=min(workers, len(tarefas))) as pool:
        futures = [pool.submit(fn) for fn in tarefas]
    return [f.result() for f in futures]
