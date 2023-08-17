from typing import Iterable, Iterator, TypeVar, Generic, Tuple, Set
from fibonacci_heap import FibHeap
import math

T = TypeVar("T")


class Graph(Generic[T]):
    def __init__(self, edges: Iterable[Tuple[T, T, int]]):
        self._weights = {(a, b): w for a, b, w in edges}
        self._edges = {}
        for a, b, w in edges:
            self._edges[a] = self._edges.get(a, set()) | {b}
        self._vertices = set(a for a, _, _ in edges) | set(b for _, b, _ in edges)

    @property
    def edges(self) -> Iterator[Tuple[T, T]]:
        yield from self._weights.keys()

    @property
    def vertices(self) -> Iterator[T]:
        yield from self._vertices

    def neighbours(self, n: T) -> Set[T]:
        return self._edges.get(n, set())

    def weight(self, a: T, b: T) -> int:
        return self._weights[(a, b)]


def dijkstra(graph: Graph[T], start: T) -> Set[Tuple[T, int]]:
    for a, b in graph.edges:
        if graph.weight(a, b) < 0:
            raise ValueError(f"Edge ({a},{b}) has weight {graph.weight(a, b)}, but Dijkstra's algorithm "
                             "requires that all edge weights be greater than zero.")

    queue: FibHeap = FibHeap()
    nodes = dict()
    for v in graph.vertices:
        if v != start:
            nodes[v] = queue.insert(math.inf, (v, None))
    nodes[start] = queue.insert(0, (start, None))
    distances = set()
    while len(queue) > 0:
        u = queue.extract_min()
        n = u.value[0]
        d = u.key
        distances.add((n, d))
        for neighbour in graph.neighbours(n):
            v = nodes[neighbour]
            w = graph.weight(n, v.value[0])
            if v.key > d + w:
                queue.decrease_key(v, d + w)
    return distances


def test_dijkstra():
    graph = Graph([(1, 2, 2), (1, 3, 1), (2, 4, 1), (3, 4, 1), (4, 5, 2)])
    assert dijkstra(graph, 1) == {(1, 0), (2, 2), (3, 1), (4, 2), (5, 4)}

    graph = Graph([("s", "t", 10), ("s", "y", 5), ("t", "x", 1), ("t", "y", 2),
                   ("y", "t", 3), ("y", "x", 9), ("y", "z", 2), ("z", "s", 7),
                   ("z", "x", 6)])
    assert dijkstra(graph, "s") == {("s", 0), ("t", 8), ("x", 9), ("y", 5), ("z", 7)}
