package org.example.tree;


import java.util.function.Consumer;

public class BinaryTree<K extends Comparable<K>, D> {
    private final BinaryNode<K, D> _nil;
    private BinaryNode<K, D> _root;
    private int _size;

    public BinaryTree() {
        _nil = new BinaryNode<>(null, null, null);
        _nil.parent = _nil;
        _nil.left = _nil;
        _nil.right = _nil;
        _root = _nil;
        _size = 0;
    }


    public BinaryNode<K, D> insert(K key, D item) {
        BinaryNode<K, D> z = new BinaryNode<>(key, item, _nil);
        BinaryNode<K, D> y = _nil;
        BinaryNode<K, D> x = _root;
        while (x != _nil) {
            y = x;
            if (z.key.compareTo(x.key) < 0) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        z.parent = y;
        if (y == _nil) {
            _root = z;
        } else if (z.key.compareTo(y.key) < 0) {
            y.left = z;
        } else {
            y.right = z;
        }
        ++_size;
        z.isRed = true;
        insertFixUp(z);
        return z;
    }

    public int size() {
        return _size;
    }

    public void walk(Consumer<D> visitor) {
        inorderWalk(visitor, _root);
    }

    private void inorderWalk(Consumer<D> visitor, BinaryNode<K, D> node) {
        if (node != _nil) {
            inorderWalk(visitor, node.left);
            visitor.accept(node.data);
            inorderWalk(visitor, node.right);
        }
    }

    public BinaryNode<K, D> search(K key) {
        var x = _root;
        while (x != _nil) {
            var comp = key.compareTo(x.key);
            if (comp == 0) {
                return x;
            } else if (key.compareTo(x.key) < 0) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        return x;
    }

    private void leftRotate(BinaryNode<K, D> x) {
        var y = x.right;
        x.right = y.left;
        if (y.left != _nil) {
            y.left.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == _nil) {
            _root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    private void rightRotate(BinaryNode<K, D> x) {
        var y = x.left;
        x.left = y.right;
        if (y.right != _nil) {
            y.right.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == _nil) {
            _root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    private void insertFixUp(BinaryNode<K, D> z) {
        while (z.parent.isRed) {
            if (z.parent == z.parent.parent.left) {
                var y = z.parent.parent.right;
                if (y.isRed) {
                    z.parent.isRed = false;
                    y.isRed = false;
                    z.parent.parent.isRed = true;
                    z = z.parent.parent;
                } else {
                    if (z == z.parent.right) {
                        z = z.parent;
                        leftRotate(z);
                    }
                    z.parent.isRed = false;
                    z.parent.parent.isRed = true;
                    rightRotate(z.parent.parent);
                }
            } else {
                var y = z.parent.parent.left;
                if (y.isRed) {
                    z.parent.isRed = false;
                    y.isRed = false;
                    z.parent.parent.isRed = true;
                    z = z.parent.parent;
                } else {
                    if (z == z.parent.left) {
                        z = z.parent;
                        rightRotate(z);
                    }
                    z.parent.isRed = false;
                    z.parent.parent.isRed = true;
                    leftRotate(z.parent.parent);
                }
            }
        }
        _root.isRed = false;
    }

    public int height() {
        return nodeHeight(_root);
    }

    private int nodeHeight(BinaryNode<K, D> x) {
        if (x == _nil) {
            return 0;
        }
        var leftHeight = nodeHeight(x.left);
        var rightHeight = nodeHeight(x.right);
        return 1 + Math.max(leftHeight, rightHeight);
    }
}
