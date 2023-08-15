package org.example.tree;


import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.IntStream;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.*;

public class BinaryTreeTest {

    @Test
    public void testBinaryTreeInsert() {
        List<Integer> expected = IntStream.range(0, 10)
                .boxed()
                .toList();
        BinaryTree<Integer, Integer> tree = new BinaryTree<>();
        assertThat(tree.size(), equalTo(0));
        for(int i: expected) {
            tree.insert(i, i);
        }
        assertThat(tree.size(), equalTo(expected.size()));
        List<Integer> actual = new ArrayList<>();
        tree.walk(actual::add);
        assertThat(actual, equalTo(expected));

        tree = new BinaryTree<>();
        var itr = expected.listIterator(expected.size());
        while (itr.hasPrevious()){
            var i = itr.previous();
            tree.insert(i, i);
        }
        actual = new ArrayList<>();
        tree.walk(actual::add);
        assertThat(actual, equalTo(expected));
    }

    @Test
    public void testBinaryTreeSearch() {
        BinaryTree<Integer, Boolean> tree = new BinaryTree<>();
        for(int i = 0; i < 10; ++i) {
            tree.insert(2 * i, false);
        }

        tree.insert(3, true);

        assertThat(tree.search(3).data, is(true));
        assertThat(tree.search(4).data, is(false));
        assertThat(tree.search(5).data, is(nullValue()));
    }

}
