import collections
import sys
import time
import typing

from ai.search_tree.common_types import Node, QueuingFunction, Solution, GenericGraph, ElementType

ExpandFunction = typing.NewType('ExpandFunction', typing.Callable[[Node, 'SearchTree'], typing.Iterable[Node]])
ConditionalFunction = typing.NewType('ConditionalFunction', typing.Callable[[Node, typing.Sequence[Node]], bool])


def goal_conditional_function(goal) -> ConditionalFunction:
    def _f(node: Node, path: typing.Sequence[Node]) -> bool:
        return node.state == goal
    return _f


before = time.time()


def dino(*a):
    return
    global before
    now = time.time()
    elapsed = now - before
    before = now
    print(*a, elapsed)


class SearchTree(typing.Generic[ElementType]):
    def __init__(
            self, graph: GenericGraph[ElementType], root: ElementType,
            expand_function: ExpandFunction,
            queuing_function: QueuingFunction,
            conditional_function: ConditionalFunction,
            solutions: int=sys.maxsize, skip_duplicate_states: bool=False):
        self.graph, self.root = graph, root
        self.queuing_function = queuing_function
        self.nodes = collections.deque()
        self.nodes.append(Node(root, None, 0, 0))
        self._expand_function = expand_function
        self._conditional_function = conditional_function
        self.iterations = 0
        self.solutions = solutions
        self.skip_duplicate_states = skip_duplicate_states

    def log(self, *a, **kw):
        pass
        # print(*a, **kw)

    def get_children(self, node: Node) -> typing.Iterable[Node]:
        children = self.graph.get_children(node.state)
        self.iterations += len(children)
        return list(map(
            lambda d: Node(d, node, node.depth + 1, node.cost + self.graph.get_cost(node.state, d)),
            children
        ))[::-1]

    def solve(self) -> typing.Tuple[typing.Optional[Solution], typing.Sequence[Solution]]:
        all_solutions = []
        self.iterations = 0
        best_solution, best_score = None, sys.maxsize

        already_seen_states = set()
        count = 0

        while self.nodes:
            node = self.nodes.pop()  # type: Node
            if self.skip_duplicate_states:
                if node.state in already_seen_states:
                    continue
                already_seen_states.add(node.state)
            count += 1
            # print(node.depth, 'd{} Node: {}'.format(node.depth, node.state))
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
                self.solutions -= 1
                if self.solutions:
                    continue
                else:
                    break
            children = self._expand_function(node, self)
            # A parent state is a state that was already processed. Unnecessary double check.
            if not self.skip_duplicate_states:
                parent_states = set(map(lambda d: d.state, path))
                self.log('children', node, children)
                children = list(filter(lambda d: d.state not in parent_states, children))
            self.log('children cleaned', children)
            self.nodes = self.queuing_function(self.nodes, children)
            not self.skip_duplicate_states and node in self.nodes and self.nodes.remove(node)
            count % 100 == 0 and print('.', end='')
            count % (100 * 80) == 0 and print('\n', node.depth, '\n', node.state)
            # count % 100 == 0 and print('d', node.depth, 'c', count, 'n', len(self.nodes))
            # count % 100 == 0 and print(node.state)
            # print('Children', '\n'.join(map(lambda d: 'd{}: {}'.format(d.depth, str(d.state)), self.nodes)))
            pass
        return \
            (Solution(best_solution, best_score, self.iterations), all_solutions)\
            if best_solution else (None, [])

    @classmethod
    def get_parents(cls, node: Node):
        while node.parent:
            node = node.parent
            yield node
