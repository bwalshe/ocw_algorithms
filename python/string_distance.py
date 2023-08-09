from typing import Protocol
from functools import cache


class EditCost(Protocol):
    def delete(self, char: str) -> int:
        pass

    def add(self, char: str) -> int:
        pass

    def exchange(self, a: str, b: str) -> int:
        pass


class DefaultEditCost:
    @staticmethod
    def delete(char):
        return 1

    @staticmethod
    def add(char):
        return 2

    @staticmethod
    def exchange(a, b):
        if a == b:
            return 0
        return 1


@cache
def distance_cached(s1: str, s2: str, cost: EditCost) -> int:
    if s1 == s2:
        return 0
    if s1 == "" or s2 == "":
        remaining = s1 if s2 == "" else s2
        return sum(cost.add(c) for c in remaining)
    delete1 = cost.delete(s1[0]) + distance_cached(s1[1:], s2, cost)
    delete2 = cost.delete(s2[0]) + distance_cached(s1, s2[1:], cost)
    add1 = cost.add(s1[0]) + distance_cached(s1, s2[1:], cost)
    add2 = cost.add(s2[0]) + distance_cached(s1[1:], s2, cost)
    exchange = cost.exchange(s1[0], s2[0]) + distance_cached(s1[1:], s2[1:], cost)
    return min(delete1, delete2, add1, add2, exchange)


def test_distance():
    assert distance_cached("a", "a", DefaultEditCost) == 0
    assert distance_cached("aaa", "aba", DefaultEditCost) == 1
    assert distance_cached("a", "aa", DefaultEditCost) == 1
    assert distance_cached("this is kind of a long string", "this is kind o a long string", DefaultEditCost) == 1
