class Node:
    def __init__(self, value, parent=None):
        self.key = value
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


def insert_node(double_ended: Node, node: Node):
    if node is None:
        return
    next_node = double_ended.right
    double_ended.right = node
    node.left = double_ended
    node.right = next_node
    next_node.left = node


def iterate_double_ended(double_ended: Node, count: int):
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


class CircularList:
    def __init__(self, start: Node = None):
        self._start: Node | None = start
        self._size = 0
        if start:
            self.insert(start)

    def __len__(self):
        return self._size

    @property
    def any_element(self) -> Node:
        return self._start

    def insert(self, n):
        if self._start is None:
            self._start = n
            self._start.right = n
            self._start.left = n
        else:
            insert_node(self._start, n)
        self._size += 1

    def remove(self, n):
        if self._size == 0:
            raise IndexError("remove from empty list")
        if n is self._start:
            self._start = self._start.right
        remove(n)
        self._size -= 1
        if self._size == 0:
            self._start = None

    def __iter__(self):
        yield from iterate_double_ended(self._start, self._size)

    def drain(self):
        n = self.any_element
        while n:
            self.remove(n)
            n_next = self.any_element
            yield n
            n = n_next

    def __str__(self):
        return "[" + ", ".join(str(n) for n in self) + "]"


class FibHeap:
    def __init__(self):
        self._roots = CircularList()
        self._min = None
        self._size = 0

    def insert(self, val):
        node = Node(val)
        self._roots.insert(node)
        if self._min is None or node.key < self._min.key:
            self._min = node
        self._size += 1

    def union(self, other: "FibHeap"):
        for node in other._roots:
            self._roots.insert(node)
        self._size += other._size
        if not self._min or (other._min and other._min.key < self._min.key):
            self._min = other._min

    def __len__(self):
        return self._size

    @property
    def min(self):
        if self._min:
            return self._min.key

    def extract_min(self):
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
            return z.key

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
            x = heap.extract_min()
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
    assert heap.min == minimum
