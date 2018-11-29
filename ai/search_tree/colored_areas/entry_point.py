import time
import typing

from ai.search_tree.colored_areas.colored_areas import ColoredArea
from ai.search_tree.colored_areas.example import example
from ai.search_tree.common_types import Node
from ai.search_tree.queuing_functions import depth_first
from ai.search_tree.search_tree import SearchTree

if __name__ == '__main__':
    start = time.time()

    colored_areas = example

    def _conditional_function(node: Node, _: typing.Sequence[Node]) -> bool:
        return node.depth == colored_areas.areas_count - 1

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

    c = 0
    for color in colored_areas.colors:
        search_tree = SearchTree(
            colored_areas, ColoredArea('area0', color),
            _expand_function,
            depth_first, _conditional_function)
        _, all_solutions = search_tree.solve()
        for i, d in enumerate(all_solutions):
            print(', '.join(map(lambda d: '{}: {}'.format(d.state.area, d.state.color), d.nodes)))
            c += 1

    print('Total with graph: {} ({} sec)'.format(c, time.time() - start))
