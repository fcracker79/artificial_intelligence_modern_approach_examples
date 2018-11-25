import time
import typing

from ai.search_tree.node_expansion import expand_children
from ai.search_tree.search_tree import SearchTree
from ai.search_tree.common_types import Graph, QueuingFunction, Solution, Node

_LENGTH = 80


def header(t: str):
    stars = '*' * ((_LENGTH - len(t) - 2) // 2)
    final_stars = stars if len(stars) * 2 + 2 + len(t) == _LENGTH else stars + '*'
    print(stars, t, final_stars, sep=' ')


def _str_node(node: Node) -> str:
    # noinspection PyProtectedMember
    return 'Node(state={state}, depth={depth}, cost={cost})'.format(**node._asdict())


def print_solution(name: str, solution: typing.Optional[Solution]):
    header(name)
    print('Score:', solution.score)
    print('Iterations:', solution.iterations)
    print('Best path:', '\n\t'.join(map(_str_node, solution.nodes)))


def print_algo(name: str, graph: Graph, from_node: str, to_node: str, queuing_function: QueuingFunction):
    start = time.time()
    solution = SearchTree(graph, from_node, to_node, expand_children, queuing_function).solve()
    stop = time.time()
    print_solution(name, solution)
    print('Elapsed time', stop - start)
