package org.example.tree;

public class BinaryNode<T> {
    T data;
    BinaryNode<T> left;
    BinaryNode<T> right;

    BinaryNode<T> parent;

    BinaryNode(T value, BinaryNode<T> nil) {
        data = value;
        left = nil;
        right = nil;
        parent = nil;
    }
}
