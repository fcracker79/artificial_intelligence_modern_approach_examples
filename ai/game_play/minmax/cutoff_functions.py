import typing

from ai.game_play.minmax import CutoffFunction
from ai.search_tree.common_types import Node


def max_depth(depth: int) -> CutoffFunction:
    def _f(nodes: typing.Sequence[Node]) -> typing.Iterator[Node]:
        return filter(lambda d: d.depth <= depth, nodes)
    return _f
