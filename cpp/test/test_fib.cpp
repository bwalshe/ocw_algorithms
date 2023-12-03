#include "fibheap.h"
#include <algorithm>
#include <gtest/gtest.h>
#include <vector>

TEST(TestFibHeap, TestPeek) {
  FibHeap<int> heap;
  EXPECT_EQ(heap.size(), 0);
  heap.insert(10);
  EXPECT_EQ(heap.size(), 1);
  EXPECT_EQ(heap.peek_min(), std::move(10));
  heap.insert(1);
  EXPECT_EQ(heap.size(), 2);
  EXPECT_EQ(heap.peek_min(), 1);
  heap.insert(100);
  EXPECT_EQ(heap.size(), 3);
  EXPECT_EQ(heap.peek_min(), 1);
  heap.insert(-1);
  EXPECT_EQ(heap.size(), 4);
  EXPECT_EQ(heap.peek_min(), -1);
}

TEST(TestFibHeap, TestExtractMin) {
  std::vector<int> input{5, 3, 6, 1, 4};
  std::vector<int> expected{input};
  std::sort(expected.begin(), expected.end());
  FibHeap<int> heap;
  for (auto i : input)
    heap.insert(i);

  EXPECT_EQ(heap.size(), input.size());
  for (auto i : expected)
    EXPECT_EQ(heap.extract_min(), i);
  EXPECT_EQ(heap.size(), 0);
}
