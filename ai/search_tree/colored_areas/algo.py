import typing

from ai.search_tree.colored_areas.colored_areas import ColoredAreas
from ai.search_tree.common_types import Node
from ai.search_tree.search_tree import SearchTree, ExpandFunction, ConditionalFunction


def create_conditional_function(colored_areas: ColoredAreas) -> ConditionalFunction:
    def _conditional_function(node: Node, _: typing.Sequence[Node]) -> bool:
        return node.depth == colored_areas.areas_count - 1
    return _conditional_function


def create_expand_function(colored_areas: ColoredAreas) -> ExpandFunction:
    def _expand_function(node: Node, st: SearchTree) -> typing.Iterable[Node]:
        children = list(st.get_children(node))

        parent_colors = dict()
        for parent in st.get_parents(node):
            parent_colors[parent.state.area] = parent.state.color
        parent_colors[node.state.area] = node.state.color
        return list(
            filter(
                lambda child: child.state.area not in parent_colors and all(
                    x not in parent_colors or parent_colors[x] != child.state.color
                    for x in colored_areas.adiacencies[child.state.area]),
                children
            )
        )
    return _expand_function
