import collections
import sys
import typing

from ai.search_tree.common_types import Node, QueuingFunction, Solution, GenericGraph, ElementType

ExpandFunction = typing.NewType('ExpandFunction', typing.Callable[[Node, 'SearchTree'], typing.Iterable[Node]])
ConditionalFunction = typing.NewType('ConditionalFunction', typing.Callable[[Node, typing.Sequence[Node]], bool])


def goal_conditional_function(goal) -> ConditionalFunction:
    def _f(node: Node, path: typing.Sequence[Node]) -> bool:
        return node.state == goal
    return _f


class SearchTree(typing.Generic[ElementType]):
    def __init__(
            self, graph: GenericGraph[ElementType], root: ElementType,
            expand_function: ExpandFunction,
            queuing_function: QueuingFunction,
            conditional_function: ConditionalFunction):
        self.graph, self.root = graph, root
        self.queuing_function = queuing_function
        self.nodes = collections.deque()
        self.nodes.append(Node(root, None, 0, 0))
        self._expand_function = expand_function
        self._conditional_function = conditional_function
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

    def solve(self) -> typing.Tuple[typing.Optional[Solution], typing.Sequence[Solution]]:
        all_solutions = []
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
            if self._conditional_function(node, path):
                all_solutions.append(Solution(path + [node], node.cost, self.iterations))
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

        return \
            (Solution(best_solution, best_score, self.iterations), all_solutions)\
            if best_solution else (None, [])

    @classmethod
    def get_parents(cls, node: Node):
        while node.parent:
            node = node.parent
            yield node
