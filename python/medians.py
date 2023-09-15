from random import randint, shuffle
from typing import Sequence, TypeVar, Protocol
from collections.abc import MutableSequence
from itertools import islice

import pytest

T = TypeVar("T")
CT = TypeVar("CT", bound="Comparable")


class Comparable(Protocol[T]):
    def __lt__(self, other: T) -> bool:
        pass

    def __eq__(self, other: T) -> bool:
        pass


class PartitionFn(Protocol[CT]):
    def __call__(self, items: MutableSequence[CT], start: int, end: int) -> int:
        pass


def minimum(items: Sequence[CT]) -> CT:
    min_seen = None
    for i in items:
        if min_seen is None or i < min_seen:
            min_seen = i
    return min_seen


def select(items: MutableSequence[CT],
           rank: int,
           partition_fn: PartitionFn[CT]) -> CT:
    def go(start, end, i):
        if start == end:
            return items[start]
        q = partition_fn(items, start, end)
        k = q - start + 1
        if k == i:
            return items[q]
        elif i < k:
            return go(start, q - 1, i)
        return go(q + 1, end, i - k)

    return go(0, len(items) - 1, rank)


def partition(items: MutableSequence[CT], start: int, end: int) -> int:
    pivot = items[end]
    i = start - 1
    for j in range(start, end):
        if items[j] < pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[end] = items[end], items[i + 1]
    return i + 1


def random_partition(items: MutableSequence[CT], start: int, end: int) -> int:
    i = randint(start, end - 1)
    items[end], items[i] = items[i], items[end]
    return partition(items, start, end)


def median_partition(items: MutableSequence[CT], start: int, end: int) -> int:
    medians = []
    i = start
    while i < end:
        group = islice(items, i, min(i + 5, end + 1))
        group = sorted(group)
        medians.append(group[(len(group) - 1) // 2])
        i += 5
    pivot = select(medians, len(medians) // 2, median_partition)
    for i in range(start, end):
        if items[i] == pivot:
            items[i], items[end] = items[end], items[i]
            break
    if items[end] != pivot:
        raise RuntimeError("pivot not found.")
    return partition(items, start, end)


def test_minimum():
    vals = list(range(10))
    expected = min(vals)
    assert minimum(vals) == expected
    vals.reverse()
    assert minimum(vals) == expected
    assert minimum([]) is None


def test_partition():
    vals = list(range(10))
    for i in range(len(vals)):
        vals.sort()
        vals[i] = vals[-1]
        vals[-1] = i
        assert partition(vals, 0, len(vals) - 1) == i


@pytest.mark.parametrize("pfn", [partition, random_partition, median_partition])
def test_randomised_select(pfn):
    vals = list(range(103))
    for i in vals:
        shuffle(vals)
        assert select(vals, i + 1, pfn) == i
