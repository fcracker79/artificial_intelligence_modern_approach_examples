import collections
import itertools

from sortedcontainers import SortedList

from ai.search_tree.common_types import QueuingFunction, Fringe, Children


def breadth_first(queue: Fringe, nodes: Children) -> Fringe:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


def depth_first(queue: Fringe, nodes: Children) -> Fringe:
    return collections.deque(itertools.chain(queue, nodes))


def uniform_cost(queue: Fringe, nodes: Children) -> Fringe:
    if isinstance(queue, SortedList):
        queue.update(nodes)
        return queue
    return SortedList(itertools.chain(nodes, queue), key=lambda d: -d.cost)


def limited(depth_limit: int, queuing_function: QueuingFunction):
    def _f(queue: Fringe, nodes: Children) -> Fringe:
        return collections.deque(
            filter(lambda d: d.depth <= depth_limit, queuing_function(queue, nodes))
        )
    return _f


def depth_limited_first(depth_limit: int):
    return limited(depth_limit, depth_first)
