from typing import Protocol
from functools import cache
import pytest


class EditCost(Protocol):
    def delete(self, char: str) -> float:
        pass

    def add(self, char: str) -> float:
        pass

    def exchange(self, a: str, b: str) -> float:
        pass


class DefaultEditCost:
    @staticmethod
    def delete(char) -> float:
        return 1.0

    @staticmethod
    def add(char) -> float:
        return 2.0

    @staticmethod
    def exchange(a, b) -> float:
        if a == b:
            return 0.0
        return 1.0


@cache
def distance_cached(s1: str, s2: str, cost: EditCost) -> float:
    if s1 == s2:
        return 0
    if s1 == "":
        return sum(cost.add(c) for c in s2)
    if s2 == "":
        return sum(cost.delete(c) for c in s1)
    delete = cost.delete(s1[0]) + distance_cached(s1[1:], s2, cost)
    add = cost.add(s2[0]) + distance_cached(s1, s2[1:], cost)
    exchange = cost.exchange(s1[0], s2[0]) + distance_cached(s1[1:], s2[1:], cost)
    return min(delete, add, exchange)


def distance_topological(s1: str, s2: str, cost: EditCost) -> float:
    big_num = 10 ** 8
    l1, l2 = len(s1), len(s2)
    table = []
    for _ in range(len(s1)):
        table.append([0] * len(s2))

    def get_cached(i, j):
        if i < l1 and j < l2:
            return table[i][j]
        return big_num

    for i, c1 in reversed(list(enumerate(s1))):
        for j, c2 in reversed(list(enumerate(s2))):
            if i == l1 - 1 and j == l2 - 1:
                continue
            add = cost.add(c2) + get_cached(i,j + 1)
            delete = cost.delete(c1) + get_cached(i + 1, j)
            swap = cost.exchange(c1, c2) + get_cached(i + 1, j + 1)
            table[i][j] = min(add, delete, swap)

    return table[0][0]


@pytest.mark.parametrize("distance", [distance_cached, distance_topological])
def test_distance(distance):
    assert distance("a", "a", DefaultEditCost) == 0
    assert distance("aa", "a", DefaultEditCost) == 1
    assert distance("aaa", "aba", DefaultEditCost) == 1
    assert distance("a", "aa", DefaultEditCost) == 2
    assert distance("this is kind of a long string", "this is kind o a long string", DefaultEditCost) == 1
