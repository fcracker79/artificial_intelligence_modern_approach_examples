import time
import typing

from ai.search_tree.eight_queens.chessboard import CHESSBOARD_SIZE
from ai.search_tree.eight_queens.graph import Queen
from ai.search_tree.node_expansion import expand_children
from ai.search_tree.search_tree import SearchTree, goal_conditional_function
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
    if not solution:
        print('NO SUCH SOLUTION')
        return
    print('Score:', solution.score)
    print('Iterations:', solution.iterations)
    print('Best path:', '\n\t'.join(map(_str_node, solution.nodes)))


def print_algo(name: str, graph: Graph, from_node: str, to_node: str, queuing_function: QueuingFunction):
    start = time.time()
    solution, _ = SearchTree(graph, from_node, expand_children, queuing_function, goal_conditional_function(to_node)).solve()
    stop = time.time()
    print_solution(name, solution)
    print('Elapsed time', stop - start)


def print_queens_positions(queens: typing.List[int]):
    print(' ', '_' * (CHESSBOARD_SIZE * 2 + 1), sep='')
    for i in range(CHESSBOARD_SIZE):
        print(
            '|',
            ' '.join('Q' if queens[i] == j else '*' for j in range(CHESSBOARD_SIZE)),
            '|')
    print(' ', '-' * (CHESSBOARD_SIZE * 2 + 1), '\n', sep='')


def print_queens(queens: typing.List[Queen]):
    print_queens_positions(list(map(lambda d: d.position, queens)))
