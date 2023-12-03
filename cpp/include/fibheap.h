#include <cmath>
#include <list>
#include <memory>
#include <vector>

template <typename T> class FibHeap {
  struct Node {
    Node *parent;
    std::list<Node> children;

    Node(const T &_val) : val(_val), parent(nullptr) {}
    Node(const Node &other) = delete;
    Node(Node &&other) noexcept : val(other.val), parent(other.parent) {
      std::swap(children, other.children);
    }
    T val;
    int degree() { return children.size(); }
    bool mark = false;
  };

  using NodeItr = typename std::list<Node>::iterator;
  std::list<Node> roots;
  NodeItr min{roots.begin()};

  int _size;

  void link(Node *x, Node *y) {
    y->parent = x;
    x->children.push_back(std::move(*y));
  }

  void consolodate() {
    std::vector<Node *> degrees(size(), nullptr);
    for (NodeItr w = roots.begin(); w != roots.end(); ++w) {
      auto degree = w->degree();
      auto *x = &(*w);
      while (degrees[degree] != nullptr) {
        auto *y = degrees[degree];
        if (x->val > y->val)
          std::swap(x, y);
        link(x, y);
        degrees[degree] = nullptr;
        ++degree;
      }
      degrees[degree] = x;
    }

    std::list<Node> new_roots;
    min = new_roots.begin();

    for (auto *node : degrees) {
      if (node) {
        bool new_min = (min == new_roots.end() || node->val < min->val);
        new_roots.push_front(std::move(*node));
        if (new_min)
          min = new_roots.begin();
      }
    }
    std::swap(roots, new_roots);
  }

public:
  FibHeap() : _size(0) {}

  void insert(const T &value) {
    roots.push_front(Node{value});
    if (min == roots.end() || min->val > roots.front().val) {
      min = roots.begin();
    }
    ++_size;
  }

  T &peek_min() { return min->val; }

  T extract_min() {
    T val{std::move(min->val)};
    for (auto &node : roots)
      node.parent = nullptr;
    roots.splice(roots.end(), min->children);
    roots.erase(min);
    min = roots.begin();
    consolodate();
    --_size;
    return val;
  }

  int size() { return _size; }
};
