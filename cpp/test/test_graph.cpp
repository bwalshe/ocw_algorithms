#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <string>
#include <vector>

#include "graph.h"

using ::testing::AnyOf;
using ::testing::ElementsAre;

TEST(TestGraph, TestDepthFirst) {
  using string_graph = Graph<std::string>;

  string_graph g;
  for (int i = 0; i < 7; ++i) {
    g.add_vertex(std::string(1, 'a' + i));
  }
  g.add_edge(0, 1)
      .add_edge(0, 4)
      .add_edge(1, 5)
      .add_edge(5, 2)
      .add_edge(4, 6)
      .add_edge(3, 6);

  EXPECT_EQ(g.vertices.size(), 7);

  std::vector<std::string> inorder;
  for (auto &v : g.breadth_first(0)) {
    inorder.push_back(v);
  }
  EXPECT_THAT(inorder, AnyOf(ElementsAre("a", "b", "e", "f", "g", "c"),
                             ElementsAre("a", "e", "b", "f", "g", "c")));
}
