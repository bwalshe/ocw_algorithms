package org.example.tree;


import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.IntStream;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;

public class BinaryTreeTest {

    @Test
    public void testBinaryTreeInsert() {
        List<Integer> expected = IntStream.range(0, 10)
                .boxed()
                .toList();
        BinaryTree<Integer> tree = new BinaryTree<>();
        assertThat(tree.size(), equalTo(0));
        for(int i: expected) {
            tree.insert(i);
        }
        assertThat(tree.size(), equalTo(expected.size()));
        List<Integer> actual = new ArrayList<>();
        tree.walk(actual::add);
        assertThat(actual, equalTo(expected));

        tree = new BinaryTree<>();
        var itr = expected.listIterator(expected.size());
        while (itr.hasPrevious()){
            tree.insert(itr.previous());
        }
        actual = new ArrayList<>();
        tree.walk(actual::add);
        assertThat(actual, equalTo(expected));
    }

}
