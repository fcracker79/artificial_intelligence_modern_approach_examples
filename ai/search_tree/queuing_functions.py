import collections
import itertools
import typing

from ai.search_tree.common_types import Node, QueuingFunction


def breadth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


def depth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(
        itertools.chain(queue, nodes)
    )


def uniform_cost(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(sorted(breadth_first(queue, nodes), reverse=True, key=lambda d: d.cost))


def limited(depth_limit: int, queuing_function: QueuingFunction):
    def _f(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
        return collections.deque(
            filter(lambda d: d.depth <= depth_limit, queuing_function(queue, nodes))
        )
    return _f


def depth_limited_first(depth_limit: int):
    return limited(depth_limit, depth_first)
