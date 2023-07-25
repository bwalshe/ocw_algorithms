#include <cstddef>
#include <iostream>
#include <iterator>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>

class Graph {
public:
  class BreadthFirstIterator {
    using iterator_category = std::input_iterator_tag;
    using value_type = int;
    using pointer = int *;
    using reference = int &;

  private:
    std::set<int> _frountier;
    std::set<int> _next_frountier;
    int _v;
    const Graph *_g;
    static BreadthFirstIterator END;

    BreadthFirstIterator() : _v(-1) {}

  public:
    BreadthFirstIterator(int start, const Graph &g) : _v(start), _g(&g) {
      _frountier.insert(g.edges.at(start).begin(), g.edges.at(start).end());
    }

    static BreadthFirstIterator end() { return BreadthFirstIterator(); }
    BreadthFirstIterator &operator++() {
      if (_frountier.size() == 0) {
        _v = -1;
        return *this;
      }
      _v = *_frountier.begin();
      _frountier.erase(_v);
      auto neighbours = _g->edges.find(_v);
      if (neighbours != _g->edges.end())
        _next_frountier.insert(neighbours->second.begin(),
                               neighbours->second.end());
      if (_frountier.empty()) {
        _frountier.swap(_next_frountier);
        _next_frountier.clear();
      }
      return *this;
    }

    BreadthFirstIterator operator++(int) {
      BreadthFirstIterator tmp = *this;
      ++(*this);
      return tmp;
    }

    int operator*() { return _v; }
    friend bool operator==(BreadthFirstIterator const &a,
                           BreadthFirstIterator const &b) {
      if (&a == &b)
        return true;
      return a._v == b._v;
    }
    friend bool operator!=(BreadthFirstIterator const &a,
                           BreadthFirstIterator const &b) {
      return !(a == b);
    }
  };

  using breadth_first = BreadthFirstIterator;
  std::unordered_set<int> vertices;
  std::unordered_map<int, std::vector<int>> edges;

  Graph &add_edge(int source, int dest) {
    vertices.insert(source);
    edges[source].push_back(dest);
    return *this;
  }

  BreadthFirstIterator depth_first_start(int start) const {
    return BreadthFirstIterator(start, *this);
  }

  BreadthFirstIterator depth_first_end() const { return breadth_first::end(); }
};

int main(int argc, char **argv) {
  Graph g;
  g.add_edge(1, 2)
      .add_edge(1, 5)
      .add_edge(2, 6)
      .add_edge(6, 3)
      .add_edge(3, 7)
      .add_edge(4, 7);

  for (auto v : g.vertices) {
    std::cout << v << ":\n";
    for (auto dest : g.edges[v]) {
      std::cout << "\t" << dest << std::endl;
    }
  }

  std::cout << "Depth First:" << std::endl;
  for (Graph::breadth_first v = g.depth_first_start(1);
       v != Graph::breadth_first::end(); ++v) {
    std::cout << *v << std::endl;
  }
}
