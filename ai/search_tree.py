import collections
import itertools
import sys
import time
import typing


class Graph:

    def __init__(self):
        self.arch_count = 0
        self.nodes = set()
        self.archs = dict()  # type: typing.Dict[str, typing.Set[str]]
        self.costs = dict()  # type: typing.Dict[str, int]

    def add_arch(self, node1, node2, cost: int=1):
        self.arch_count += 1
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.archs.setdefault(node1, set()).add(node2)
        self.archs.setdefault(node2, set()).add(node1)
        self.costs[','.join(sorted((node1, node2)))] = cost

    def get_cost(self, node1: str, node2: str) -> int:
        return self.costs[','.join(sorted((node1, node2)))]

    def get_children(self, node):
        return self.archs.get(node, [])


def _create_example_graph(add_costs: bool=False) -> Graph:
    g = Graph()
    g.add_arch('Arad', 'Zerind', add_costs and 1 or 1)
    g.add_arch('Arad', 'Timsoara', add_costs and 2 or 1)
    g.add_arch('Arad', 'Sibiu', add_costs and 3 or 1)
    g.add_arch('Zerind', 'Oradea', add_costs and 1 or 1)
    g.add_arch('Oradea', 'Sibiu', add_costs and 4 or 1)
    g.add_arch('Timsoara', 'Lugoj', add_costs and 2 or 1)
    g.add_arch('Lugoj', 'Mehadia', add_costs and 1 or 1)
    g.add_arch('Mehadia', 'Dobreta', add_costs and 1 or 1)
    g.add_arch('Dobreta', 'Craovia', add_costs and 2 or 1)
    g.add_arch('Craovia', 'Rimnicu Vilcea', add_costs and 3 or 1)
    g.add_arch('Craovia', 'Pitesti', add_costs and 3 or 1)
    g.add_arch('Rimnicu Vilcea', 'Sibiu', add_costs and 1 or 1)
    g.add_arch('Rimnicu Vilcea', 'Pitesti', add_costs and 2 or 1)
    g.add_arch('Sibiu', 'Faragas', add_costs and 2 or 1)
    g.add_arch('Faragas', 'Bucharest', add_costs and 5 or 1)
    g.add_arch('Pitesti', 'Bucharest', add_costs and 3 or 1)
    g.add_arch('Bucharest', 'Giurgiu', add_costs and 2 or 1)
    g.add_arch('Bucharest', 'Urziceni', add_costs and 1 or 1)
    g.add_arch('Urziceni', 'Hisrova', add_costs and 2 or 1)
    g.add_arch('Urziceni', 'Vaslui', add_costs and 4 or 1)
    g.add_arch('Hisrova', 'Eforie', add_costs and 2 or 1)
    g.add_arch('Vaslui', 'Iasi', add_costs and 2 or 1)
    g.add_arch('Iasi', 'Neamt', add_costs and 2 or 1)
    return g


Node = typing.NamedTuple(
        'Node',
        (
            ('state', typing.Any),
            ('parent', typing.Optional['Node']),
            # ('operator', 'Boh'),
            ('depth', int),
            ('cost', int),
        )
    )
Solution = typing.NamedTuple(
    'Solution',
    (
        ('nodes', typing.List[Node]),
        ('score', int),
        ('iterations', int)
    )
)

QueuingFunction = typing.NewType(
    'QueuingFunction',
    typing.Callable[[typing.Deque[Node], typing.Sequence[Node]], typing.Deque[Node]]
)


ExpandFunction = typing.NewType('ExpandFunction', typing.Callable[[Node, 'SearchTree'], typing.Iterable[Node]])


class SearchTree:
    def __init__(
            self, graph: Graph, root: str, goal: str,
            expand_function: ExpandFunction,
            queuing_function: QueuingFunction):
        self.graph, self.root, self.goal = graph, root, goal
        self.queuing_function = queuing_function
        self.nodes = collections.deque()
        self.nodes.append(Node(root, None, 0, 0))
        self._expand_function = expand_function
        self.iterations = 0

    def log(self, *a, **kw):
        pass
        # print(*a, **kw)

    def get_children(self, node: Node) -> typing.Iterable[Node]:
        children = self.graph.get_children(node.state)
        self.iterations += len(children)
        return map(
            lambda d: Node(d, node, node.depth + 1, node.cost + self.graph.get_cost(node.state, d)),
            children
        )

    def solve(self) -> typing.Optional[Solution]:
        self.iterations = 0
        best_solution, best_score = None, sys.maxsize
        while self.nodes:
            node = self.nodes.pop()  # type: Node
            # Note:
            # Without this simple optimization, depth-first and breadth-first compare well in terms of performances.
            # With this optimization, depth-first is sligthly faster.
            if node.cost > best_score:
                continue
            path = list(self.get_parents(node))[::-1]
            self.log('Current path', node, path)
            self.log('Nodes', self.nodes)
            if node.state == self.goal:
                if node.cost < best_score:
                    self.log(node)
                    best_solution, best_score = path + [node], node.cost
                    self.log(best_solution)
                continue
            children = self._expand_function(node, self)
            parent_states = set(map(lambda d: d.state, path))
            self.log('children', node, children)
            children = list(filter(lambda d: d.state not in parent_states, children))
            self.log('children cleaned', children)
            self.nodes = self.queuing_function(self.nodes, children)
            node in self.nodes and self.nodes.remove(node)

        return Solution(best_solution, best_score, self.iterations) if best_solution else None

    @classmethod
    def get_parents(cls, node: Node):
        while node.parent:
            node = node.parent
            yield node


def _expand_children(node: Node, search_tree: SearchTree) -> typing.Iterable[Node]:
    return search_tree.get_children(node)


def _expand_at_level(level: int):
    def _f(node: Node, search_tree: SearchTree) -> typing.Iterable[Node]:
        nodes_to_expand = [node]
        while nodes_to_expand:
            node_to_expand = nodes_to_expand.pop()
            if node_to_expand.depth == level:
                yield node_to_expand
            elif node_to_expand.depth < level:
                nodes_to_expand.extend(_expand_children(node_to_expand, search_tree))
    return _f


def _breadth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    queue.extend(nodes)
    return queue


def _depth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


def _uniform_cost(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(sorted(itertools.chain(nodes, queue), key=lambda d: d.cost))


def _depth_limited_first(depth_limit: int):
    def _f(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
        return collections.deque(
            filter(lambda d: d.depth <= depth_limit, _depth_first(queue, nodes))
        )
    return _f


_LENGTH = 80


def _header(t: str):
    stars = '*' * ((_LENGTH - len(t) - 2) // 2)
    final_stars = stars if len(stars) * 2 + 2 + len(t) == _LENGTH else stars + '*'
    print(stars, t, final_stars, sep=' ')


def _str_node(node: Node) -> str:
    return 'Node(state={state}, depth={depth}, cost={cost})'.format(**node._asdict())


def _print_solution(name: str, solution: typing.Optional[Solution]):
    _header(name)
    print('Score:', solution.score)
    print('Iterations:', solution.iterations)
    print('Best path:', '\n\t'.join(map(_str_node, solution.nodes)))


def _print_algo(name: str, graph: Graph, from_node: str, to_node: str, queuing_function: QueuingFunction):
    start = time.time()
    solution = SearchTree(graph, from_node, to_node, _expand_children, queuing_function).solve()
    stop = time.time()
    _print_solution(name, solution)
    print('Elapsed time', stop - start)


def _iterative_deepening_search(graph: Graph, from_node: str, to_node: str):
    start = time.time()
    best_solution = None  # type: Solution
    iterations = 0
    for max_depth in range(len(graph.nodes)):
        if best_solution and len(best_solution.nodes) <= max_depth:
            break
        search_tree = SearchTree(graph, from_node, to_node, _expand_at_level(max_depth), _depth_first)
        solution = search_tree.solve()
        iterations += search_tree.iterations
        if not solution:
            continue
        if not best_solution or solution.score < best_solution.score:
            best_solution = solution
    solution = Solution(nodes=best_solution.nodes, score=best_solution.score, iterations=iterations)
    stop = time.time()
    _print_solution('Iterative deepening search', solution)
    print('Elapsed time', stop - start)


def _run_algos(add_costs: bool):
    from_node, to_node = 'Arad', 'Bucharest'
    _header('WITH COSTS' if add_costs else 'WITHOUT COSTS')
    g = _create_example_graph(add_costs=add_costs)
    _print_algo('BREADTH FIRST', g, from_node, to_node, _breadth_first)
    _print_algo('DEPTH FIRST', g, from_node, to_node, _depth_first)
    _print_algo('UNIFORM COST', g, from_node, to_node, _uniform_cost)
    _print_algo('DEPTH FIRST LIMIT 3', g, from_node, to_node, _depth_limited_first(3))
    _iterative_deepening_search(g, from_node, to_node)


def _run():
    _run_algos(False)
    _run_algos(True)


if __name__ == '__main__':
    _run()
