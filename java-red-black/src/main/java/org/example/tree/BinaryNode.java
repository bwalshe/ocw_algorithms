package org.example.tree;

public class BinaryNode<K, D> {
    K key;
    D data;
    BinaryNode<K, D> left;
    BinaryNode<K, D> right;

    BinaryNode<K, D> parent;

    boolean isRed;

    BinaryNode(K key, D value, BinaryNode<K, D> nil) {
        this.key = key;
        data = value;
        left = nil;
        right = nil;
        parent = nil;
        isRed = false;
    }

}
