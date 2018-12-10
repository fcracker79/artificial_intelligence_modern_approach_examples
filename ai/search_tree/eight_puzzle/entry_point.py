import typing

from ai.search_tree.common_types import Node
from ai.search_tree.eight_puzzle.puzzle import PuzzleGraph, Puzzle
from ai.search_tree.print_tools import print_solution
from ai.search_tree.queuing_functions import uniform_cost, limited
from ai.search_tree.search_tree import SearchTree


def entry_point():
    def _expand_function(node: Node, st: SearchTree) -> typing.Iterable[Node]:
        return list(st.get_children(node))

    def _conditional_function(node: Node, _: typing.Sequence[Node]) -> bool:
        return node.state.correct

    # puzzle = Puzzle(positions=[1, 2, 3, 8, 0, 4, 7, 6, 5])
    # puzzle = Puzzle(positions=[0, 2, 3, 1, 8, 4, 7, 6, 5])
    # puzzle = Puzzle(positions=[1, 2, 3, 4, 5, 6, 8, 7, 0])
    # puzzle = Puzzle(positions=[8, 5, 3, 4, 0, 2, 7, 6, 1])
    puzzle = Puzzle(positions=[1, 2, 3, 8, 0, 4, 7, 6, 5])
    puzzle.shuffle(100)
    # puzzle = Puzzle(positions=[3, 4, 5, 2, 1, 8, 7, 6, 0])
    p = PuzzleGraph(root=puzzle)
    print(p.root)
    search_tree = SearchTree(
        p, p.root,
        _expand_function,
        limited(30, uniform_cost),
        _conditional_function,
        solutions=1,
        skip_duplicate_states=True
    )
    solution, all_solutions = search_tree.solve()
    print_solution('Best solution', solution)


if __name__ == '__main__':
    entry_point()
