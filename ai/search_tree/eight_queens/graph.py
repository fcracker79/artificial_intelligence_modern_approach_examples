import typing

from ai.search_tree.common_types import GenericGraph
from ai.search_tree.eight_queens.chessboard import CHESSBOARD_SIZE

Queen = typing.NamedTuple(
    'Queen',
    (
        ('queen_number', int),
        ('position', int)
    )
)


class ChessboardGraph(GenericGraph[Queen]):
    def get_cost(self, node1: Queen, node2: Queen):
        return 1

    def get_children(self, node: Queen) -> typing.Sequence[Queen]:
        return [Queen(node.queen_number + 1, i) for i in range(CHESSBOARD_SIZE)]
