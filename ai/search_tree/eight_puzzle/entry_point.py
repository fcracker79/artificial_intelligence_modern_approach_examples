import typing

from ai.search_tree.common_types import Node
from ai.search_tree.eight_puzzle.puzzle import PuzzleGraph
from ai.search_tree.print_tools import print_solution
from ai.search_tree.queuing_functions import breadth_first, depth_first
from ai.search_tree.search_tree import SearchTree

if __name__ == '__main__':
    def _expand_function(node: Node, st: SearchTree) -> typing.Iterable[Node]:
        return list(st.get_children(node))

    def _conditional_function(node: Node, path: typing.Sequence[Node]) -> bool:
        return node.state.correct

    p = PuzzleGraph()
    search_tree = SearchTree(
        p, p.root,
        _expand_function,
        depth_first,
        _conditional_function
    )
    solution, all_solutions = search_tree.solve()
    print_solution('Best solution', solution)
