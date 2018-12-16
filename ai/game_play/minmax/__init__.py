import typing

from ai.search_tree.common_types import Node

NodeWithScore = typing.NamedTuple(
    'NodeWithScore',
    (('node', Node), ('score', float), ('best_move', int), ('steps_to_best_move', int))
)

ScoreFunction = typing.NewType('ScoreFunction', typing.Callable[[Node], float])
CutoffFunction = typing.NewType('CutoffFunction', typing.Callable[[typing.Sequence[Node]], typing.Iterator[Node]])
