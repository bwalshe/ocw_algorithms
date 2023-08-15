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
}
