import itertools
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    if n < 1:
        raise ValueError("n must be at least 1")

    iterator = iter(iterable)

    while True:
        batch = tuple(islice(iterator, n))
        if not batch:
            return
        yield batch


if __name__ == "__main__":
    assert list(batched([1, 2, 3, 4, 5, 6, 7], 3)) == [(1, 2, 3), (4, 5, 6), (7,)]
    assert list(batched((letter for letter in "abcde"), 2)) == [("a", "b"), ("c", "d"), ("e",)]
    assert list(batched([], 3)) == []
    assert list(batched(range(10), 4)) == list(itertools.batched(range(10), 4))

    try:
        list(batched([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
