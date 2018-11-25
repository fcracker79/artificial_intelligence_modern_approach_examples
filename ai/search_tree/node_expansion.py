import typing

from ai.search_tree.search_tree import SearchTree
from ai.search_tree.common_types import Node


def expand_children(node: Node, search_tree: SearchTree) -> typing.Iterable[Node]:
    return search_tree.get_children(node)


def expand_at_level(level: int):
    # Returns all children that have depth == level.
    def _f(node: Node, search_tree: SearchTree) -> typing.Iterable[Node]:
        nodes_to_expand = [node]
        while nodes_to_expand:
            node_to_expand = nodes_to_expand.pop()
            if node_to_expand.depth == level:
                yield node_to_expand
            elif node_to_expand.depth < level:
                nodes_to_expand.extend(expand_children(node_to_expand, search_tree))
    return _f
