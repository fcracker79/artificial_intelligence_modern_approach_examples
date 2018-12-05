import typing

from ai.search_tree.common_types import Node
from ai.search_tree.eight_puzzle.puzzle import PuzzleGraph, Puzzle
from ai.search_tree.print_tools import print_solution
from ai.search_tree.queuing_functions import depth_first, uniform_cost, breadth_first, depth_limited_first, \
    limited
from ai.search_tree.search_tree import SearchTree


def entry_point():
    def _expand_function(node: Node, st: SearchTree) -> typing.Iterable[Node]:
        return list(st.get_children(node))

    def _conditional_function(node: Node, path: typing.Sequence[Node]) -> bool:
        return node.state.correct

    puzzle = Puzzle()
    # Can't find solution for this
    # puzzle.positions = [1, 2, 3, 4, 5, 6, 8, 7, 0]
    puzzle.positions = [8, 5, 3, 4, 0, 2, 6, 7, 1]
    puzzle.empty_slot = puzzle.positions.index(0)
    p = PuzzleGraph(root=puzzle)
    print(p.root)
    search_tree = SearchTree(
        p, p.root,
        _expand_function,
        depth_first,
        _conditional_function,
        solutions=1
    )
    solution, all_solutions = search_tree.solve()
    print_solution('Best solution', solution)


if __name__ == '__main__':
    entry_point()
