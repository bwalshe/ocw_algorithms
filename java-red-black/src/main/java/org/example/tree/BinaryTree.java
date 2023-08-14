package org.example.tree;


import java.util.function.Consumer;

public class BinaryTree<T extends Comparable<T>> {
    private final BinaryNode<T> _nil;
    private BinaryNode<T> _root;
    private int _size;

    public BinaryTree() {
        _nil = new BinaryNode<>(null, null);
        _nil.parent = _nil;
        _nil.left = _nil;
        _nil.right = _nil;
        _root = _nil;
        _size = 0;
    }


    public BinaryNode<T> insert(T item) {
        BinaryNode<T> z = new BinaryNode<>(item, _nil);
        BinaryNode<T> y = _nil;
        BinaryNode<T> x = _root;
        while (x != _nil) {
            y = x;
            if (z.data.compareTo(x.data) < 0) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        z.parent = y;
        if (y == _nil) {
            _root = z;
        } else if (z.data.compareTo(y.data) < 0) {
            y.left = z;
        } else {
            y.right = z;
        }
        ++_size;
        return z;
    }

    public int size() {
        return _size;
    }

    public void walk(Consumer<T> visitor) {
        inorderWalk(visitor, _root);
    }

    private void inorderWalk(Consumer<T> visitor, BinaryNode<T> node) {
        if (node != _nil) {
            inorderWalk(visitor, node.left);
            visitor.accept(node.data);
            inorderWalk(visitor, node.right);
        }
    }
}
