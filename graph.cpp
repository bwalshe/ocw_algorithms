#include <cstddef>
#include <iostream>
#include <iterator>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

template <typename T> class Graph {
public:
  class BreadthFirstIterator {
    using iterator_category = std::input_iterator_tag;
    using value_type = T;
    using pointer = T *;
    using reference = T &;

  private:
    std::set<int> _seen;
    std::set<int> _frountier;
    std::set<int> _next_frountier;
    size_t _v;
    size_t _depth;
    const Graph *_g;

    BreadthFirstIterator(const Graph *g) : _v{g->vertices.size()} {}

    static BreadthFirstIterator end(const Graph *g) {
      return BreadthFirstIterator(g);
    }

  public:
    BreadthFirstIterator(size_t start, const Graph *g) : _v(start), _g(g) {
      auto i = g->edges.at(start);
      _next_frountier.insert(i.begin(), i.end());
    }

    BreadthFirstIterator begin() const { return *this; }

    BreadthFirstIterator end() const { return end(this->_g); }

    BreadthFirstIterator &operator++() {
      if (_frountier.empty() && !_next_frountier.empty()) {
        _frountier.swap(_next_frountier);
        _next_frountier.clear();
        ++_depth;
      }
      if (_frountier.size() == 0) {
        _v = _g->vertices.size();
        return *this;
      }
      _v = *_frountier.begin();
      _frountier.erase(_v);
      auto neighbours = _g->edges.find(_v);
      if (neighbours != _g->edges.end())
        for (auto n : neighbours->second) {
          if (!_seen.count(n)) {
            _seen.insert(n);
            _next_frountier.insert(n);
          }
        }
      return *this;
    }

    BreadthFirstIterator operator++(int) {
      BreadthFirstIterator tmp = *this;
      ++(*this);
      return tmp;
    }

    const T &operator*() const { return _g->vertices.at(_v); }

    int depth() const { return _depth; }

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

  std::vector<T> vertices;
  std::unordered_map<size_t, std::vector<size_t>> edges;

  size_t add_vertex(const T &value) {
    size_t i = vertices.size();
    vertices.push_back(value);
    return i;
  }

  int add_vertex(T &&value) {
    int i = vertices.size();
    vertices.push_back(std::move(value));
    return i;
  }

  Graph &add_edge(size_t source, size_t dest) {
    edges[source].push_back(dest);
    return *this;
  }

  BreadthFirstIterator breadth_first(size_t start) const {
    return BreadthFirstIterator(start, this);
  }
};

int main(int argc, char **argv) {
  using string_graph = Graph<std::string>;

  string_graph g;
  for (int i = 0; i < 7; ++i) {
    g.add_vertex(std::string(1, 'a' + i));
  }
  g.add_edge(0, 1)
      .add_edge(0, 4)
      .add_edge(1, 5)
      .add_edge(5, 2)
      .add_edge(1, 6)
      .add_edge(3, 6);

  std::cout << "Depth First:" << std::endl;
  for (auto &v : g.breadth_first(0)) {
    std::cout << v << std::endl;
  }
}
