import time
import typing

from ai.search_tree.common_types import Node
from ai.search_tree.eight_queens import brute_force
from ai.search_tree.eight_queens.chessboard import CHESSBOARD_SIZE, Chessboard
from ai.search_tree.eight_queens.graph import ChessboardGraph, Queen
from ai.search_tree.print_tools import print_queens
from ai.search_tree.queuing_functions import depth_first
from ai.search_tree.search_tree import SearchTree

if __name__ == '__main__':
    start = time.time()
    solutions = len(brute_force.brute_force())
    elapsed_bf = time.time() - start

    start = time.time()
    chessboard = Chessboard()

    def _conditional_function(node: Node, _: typing.Sequence[Node]) -> bool:
        return node.depth == 7

    def _expand_function(node: Node, st: SearchTree) -> typing.Iterable[Node]:
        children = list(st.get_children(node))
        parents = []
        for parent in st.get_parents(node):
            parents.insert(0, parent.state)
        parents.append(node.state)
        return list(
            filter(
                lambda child: not chessboard.any_queen_eat(
                    list(map(lambda cur_node: cur_node.position, parents + [child.state]))),
                children
            )
        )

    c = 0
    for j in range(CHESSBOARD_SIZE):
        search_tree = SearchTree(
            ChessboardGraph(), Queen(0, j),
            _expand_function,
            depth_first, _conditional_function)
        _, all_solutions = search_tree.solve()
        for i, d in enumerate(all_solutions):
            print_queens(list(map(lambda cur_solution: cur_solution.state, d.nodes)))
            c += 1

    print('Total brute force: {} ({} sec)'.format(solutions, elapsed_bf))
    print('Total with graph: {} ({} sec)'.format(c, time.time() - start))
