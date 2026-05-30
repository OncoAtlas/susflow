import threading
from functools import partial

import pytest

from susflow.batch import baixar_lote


def test_empty_returns_empty():
    assert baixar_lote([]) == []


def test_results_in_submission_order():
    def task(n):
        return n * 2

    tasks = [partial(task, i) for i in range(5)]
    assert baixar_lote(tasks) == [0, 2, 4, 6, 8]


def test_single_task():
    assert baixar_lote([lambda: "ok"]) == ["ok"]


def test_exception_is_propagated():
    def bad():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        baixar_lote([bad])


def test_exception_in_one_task_still_raises():
    def good():
        return 1

    def bad():
        raise ValueError("fail")

    with pytest.raises(ValueError):
        baixar_lote([good, bad, good])


def test_runs_concurrently():
    barrier = threading.Barrier(3)
    results = []

    def task(n):
        barrier.wait(timeout=2)
        results.append(n)
        return n

    paths = baixar_lote([partial(task, i) for i in range(3)], workers=3)
    assert sorted(paths) == [0, 1, 2]


def test_workers_capped_to_task_count():
    # Should not raise even if workers > len(tasks)
    result = baixar_lote([lambda: 42], workers=100)
    assert result == [42]


def test_accepts_generator():
    def gen():
        for i in range(3):
            yield lambda x=i: x

    assert baixar_lote(gen()) == [0, 1, 2]
