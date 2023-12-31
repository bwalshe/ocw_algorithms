from typing import Any, Protocol, TypeVar, Generic, Optional
from collections.abc import Iterator
from abc import abstractmethod

C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


class Node(Generic[C]):
    def __init__(self, key: C, value: Any = None, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = self
        self.right = self
        self.mark = False

        self.children = CircularList()

    def add_child(self, new_child):
        self.children.insert(new_child)
        new_child.parent = self

    @property
    def degree(self):
        return len(self.children)

    def __str__(self):
        return "(" + str(self.key) + ": [" + ", ".join(str(c) for c in self.children) + "])"


def insert_node(double_ended: Node[C], node: Node[C]):
    if node is None:
        return
    next_node = double_ended.right
    double_ended.right = node
    node.left = double_ended
    node.right = next_node
    next_node.left = node


def iterate_double_ended(double_ended: Node[C], count: int) -> Iterator[Node[C]]:
    if double_ended is None:
        return
    n = double_ended
    for _ in range(count):
        yield n
        n = n.right


def remove(node: Node):
    left = node.left
    right = node.right
    left.right = right
    right.left = left
    node.left = node
    node.right = node


class CircularList(Generic[C]):
    def __init__(self, start: Node[C] = None):
        self._start: Node | None = start
        self._size = 0
        if start:
            self.insert(start)

    def __len__(self) -> int:
        return self._size

    @property
    def any_element(self) -> Node[C]:
        return self._start

    def insert(self, n: Node[C]) -> None:
        if self._start is None:
            self._start = n
            self._start.right = n
            self._start.left = n
        else:
            insert_node(self._start, n)
        self._size += 1

    def remove(self, n: Node[C]) -> None:
        if self._size == 0:
            raise IndexError("remove from empty list")
        if n is self._start:
            self._start = self._start.right
        remove(n)
        self._size -= 1
        if self._size == 0:
            self._start = None

    def __iter__(self) -> Iterator[Node[C]]:
        yield from iterate_double_ended(self._start, self._size)

    def drain(self) -> Iterator[Node[C]]:
        n = self.any_element
        while n:
            self.remove(n)
            n_next = self.any_element
            yield n
            n = n_next

    def __str__(self) -> str:
        return "[" + ", ".join(str(n) for n in self) + "]"


class FibHeap(Generic[C]):
    def __init__(self):
        self._roots = CircularList()
        self._min = None
        self._size = 0

    def insert(self, key: C, val=None) -> Node[C]:
        node = Node(key, val)
        self._roots.insert(node)
        if self._min is None or node.key < self._min.key:
            self._min = node
        self._size += 1
        return node

    def union(self, other: "FibHeap[C]") -> None:
        """
        Mutates this object so that it contains all elements from the other heap
        """
        for node in other._roots:
            self._roots.insert(node)
        self._size += other._size
        if not self._min or (other._min and other._min.key < self._min.key):
            self._min = other._min

    def __len__(self) -> int:
        return self._size

    @property
    def min(self) -> Optional[Node[C]]:
        if self._min:
            return self._min

    def extract_min(self) -> Node[C]:
        z = self._min
        if z is not None:
            self._roots.remove(z)
            for child in z.children.drain():
                self._roots.insert(child)
                child.parent = None
            if len(self._roots) == 0:
                self._min = None
            else:
                self._min = self._roots.any_element
                self._consolidate()
            self._size -= 1
            return z

    def _consolidate(self):
        A = {}
        for w in self._roots.drain():
            x = w
            d = w.degree
            while d in A:
                y = A.get(d)
                if y is x:
                    del A[d]
                    continue
                if x.key > y.key:
                    x, y = y, x
                x.add_child(y)
                y.mark = False
                del A[d]
                d += 1
            A[d] = x
        self._min = None
        for n in A.values():
            self._roots.insert(n)
            if self._min is None or n.key < self._min.key:
                self._min = n

    def decrease_key(self, x: Node[C], k: int):
        if k > x.key:
            raise RuntimeError(f"Cannot change key from {x.key} to {k}"
                               "New key must be lower than existing one.")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self._min.key:
            self._min = x

    def delete_node(self, x: Node) -> None:
        self.decrease_key(x, self.min.key - 1)
        self.extract_min()

    def _cut(self, x: Node, y: Node):
        y.children.remove(x)
        self._roots.insert(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y: Node):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def __str__(self):
        return str(self._roots)


def test_list_insert():
    def expect_list(vals):
        assert list(n.key for n in iterate_double_ended(l1, len(vals))) == list(vals)

    l1 = Node("a")
    expect_list("a")
    b = Node("b")
    insert_node(l1, b)
    expect_list("ab")
    insert_node(l1, Node("c"))
    expect_list("acb")


def test_list_remove():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    insert_node(a, b)
    insert_node(b, c)
    assert [n.key for n in iterate_double_ended(a, 3)] == list("abc")
    remove(b)
    assert [n.key for n in iterate_double_ended(a, 2)] == list("ac")
    remove(c)
    assert [n.key for n in iterate_double_ended(a, 1)] == list("a")
    insert_node(a, c)
    assert [n.key for n in iterate_double_ended(a, 2)] == list("ac")


def test_circular_list_iterate_and_remove():
    l = CircularList()
    l.insert(Node(0))
    l.insert(Node(2))
    l.insert(Node(1))

    i = 0
    for n in l.drain():
        assert n.key == i
        i += 1


def test_node_children():
    chars = "ABCD"
    root = Node("Not used")
    for c in chars:
        root.add_child(Node(c))

    children = [n.key for n in root.children]
    assert set(children) == set(chars)


def test_insert():
    heap = FibHeap()
    expect(heap, 0, None)

    heap.insert(0)
    expect(heap, 1, 0)

    heap.insert(1)
    expect(heap, 2, 0)

    heap.insert(-1)
    expect(heap, 3, -1)


def test_merge():
    h1 = FibHeap()
    expect(h1, 0, None)
    h1.union(FibHeap())
    expect(h1, 0, None)

    h2 = FibHeap()
    h2.insert(1)
    h1.union(h2)
    expect(h1, 1, 1)

    h1.union(FibHeap())
    expect(h1, 1, 1)


def test_extract_min():
    size = 10
    heap = FibHeap()

    def drain_and_test():
        for i in range(size):
            assert len(heap) == size - i
            x = heap.extract_min().key
            assert x == i

    for i in range(size):
        heap.insert(i)
    drain_and_test()
    assert len(heap) == 0

    for i in reversed(range(size)):
        heap.insert(i)
    drain_and_test()
    assert len(heap) == 0


def expect(heap, size, minimum):
    assert len(heap) == size
    if size == 0:
        assert heap.min is None
    else:
        assert heap.min.key == minimum


def test_decrease_key():
    h = FibHeap()
    for i in range(10):
        h.insert(i)

    n1 = h.insert(100)
    n2 = h.insert(100)

    assert h.min.key == 0

    h.decrease_key(n1, -1)
    h.decrease_key(n2, -2)

    assert h.extract_min().key == -2
    assert h.extract_min().key == -1
    assert h.extract_min().key == 0


def test_delete_node():
    count = 10
    h = FibHeap()
    last = None
    for i in range(count):
        last = h.insert(i)

    h.delete_node(last)

    remaining = []
    while len(h) > 0:
        remaining.append(h.extract_min().key)

    assert remaining == list(range(count - 1))
