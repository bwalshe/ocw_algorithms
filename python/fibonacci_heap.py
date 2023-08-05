from dataclasses import dataclass


class Node:
    def __init__(self, value, parent=None):
        self.key = value
        self.degree = 0
        self.parent = parent
        self.left = self
        self.right = self
        self.mark = False

        self._child = None

    def add_child(self, value):
        new_node = Node(value, self)
        if self._child is None:
            self._child = new_node
        else:
            insert_node(self._child, new_node)

    def children(self):
        yield from iterate_double_ended(self._child)

    def __str__(self):
        return "(" + str(self.key) + ": [" + ", ".join(str(c) for c in self.children()) + "])"


def insert_node(double_ended: Node, node: Node):
    if node is None:
        return
    start = node
    end = node.left
    next_node = double_ended.right
    double_ended.right = start
    start.left = double_ended
    end.right = next_node
    next_node.left = end


def iterate_double_ended(double_ended: Node):
    if double_ended is None:
        return
    start = double_ended
    yield start
    n = start.right
    while n is not start:
        yield n
        n = n.right


def remove(node: Node):
    left = node.left
    right = node.right
    left.right = right
    right.left = left
    node.left = node
    node.right = node


class FibHeap:
    def __init__(self):
        self._roots = None
        self._min = None
        self._size = 0

    def insert(self, val):
        node = Node(val)
        if self._min is None:
            self._roots = node
            self._min = node
        else:
            insert_node(self._roots, node)
            if node.key < self._min.key:
                self._min = node
        self._size += 1

    def union(self, other: "FibHeap"):
        if self._roots:
            insert_node(self._roots, other._roots)
        else:
            self._roots = other._roots
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
            if z is z.right:
                self._roots = None
            else:
                self._roots = z.right
                remove(z)
            for child in list(z.children()):
                remove(child)
                if self._roots is None:
                    self._roots = child
                else:
                    insert_node(self._roots, child)
                child.parent = None
            if self._roots is None:
                self._min = None
            else:
                self._min = self._roots
                self._consolidate()
            self._size -= 1
            return z.key

    def _consolidate(self):
        A = {}
        for w in list(iterate_double_ended(self._roots)):
            x = w
            d = w.degree
            while d in A:
                y = A.get(d)
                if y is x:
                    del A[d]
                    continue
                if x.key > y.key:
                    x, y = y, x
                self._fib_heap_link(y, x)
                del A[d]
                d += 1
            A[d] = x
        self._min = None
        for n in A.values():
            remove(n)
            if self._min is None:
                self._roots = n
                self._min = n
            else:
                insert_node(self._roots, n)
                if n.key < self._min.key:
                    self._min = n

    @staticmethod
    def _fib_heap_link(y, x):
        remove(y)
        if x._child == None:
            x._child = y
        else:
            insert_node(x._child, y)
        y.parent = x
        y.mark = False
        x.degree += 1

    def __str__(self):
        return "\n".join(str(r) for r in iterate_double_ended(self._roots))


def test_list_insert():
    def expect_list(vals):
        assert list(n.key for n in iterate_double_ended(l1)) == list(vals)

    l1 = Node("a")
    expect_list("a")
    b = Node("b")
    insert_node(l1, b)
    expect_list("ab")
    insert_node(l1, Node("c"))
    expect_list("acb")
    l2 = Node("d")
    insert_node(l2, Node("e"))
    insert_node(l1, l2)
    expect_list("adecb")
    insert_node(b, Node("f"))
    expect_list("adecbf")


def test_list_remove():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    insert_node(a, b)
    insert_node(b, c)
    assert [n.key for n in iterate_double_ended(a)] == list("abc")
    remove(b)
    assert [n.key for n in iterate_double_ended(a)] == list("ac")
    remove(c)
    assert [n.key for n in iterate_double_ended(a)] == list("a")
    insert_node(a, c)
    assert [n.key for n in iterate_double_ended(a)] == list("ac")


def test_node_children():
    chars = "ABCD"
    root = Node("Not used")
    for c in chars:
        root.add_child(c)

    children = [n.key for n in root.children()]
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
