import collections
import itertools
import typing

from ai.search_tree.common_types import Node


def breadth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    queue.extend(nodes)
    return queue


def depth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


def uniform_cost(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(sorted(itertools.chain(nodes, queue), key=lambda d: d.cost))


def depth_limited_first(depth_limit: int):
    def _f(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
        return collections.deque(
            filter(lambda d: d.depth <= depth_limit, depth_first(queue, nodes))
        )
    return _f