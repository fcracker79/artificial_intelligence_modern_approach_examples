import time

from ai.search_tree.colored_areas.algo import create_conditional_function, create_expand_function
from ai.search_tree.colored_areas.colored_areas import ColoredArea
from ai.search_tree.colored_areas.example import example
from ai.search_tree.queuing_functions import depth_first
from ai.search_tree.search_tree import SearchTree


def entry_point():
    start = time.time()

    colored_areas = example

    c = 0
    for color in colored_areas.colors:
        search_tree = SearchTree(
            colored_areas, ColoredArea('area0', color),
            create_expand_function(example),
            depth_first, create_conditional_function(example))
        _, all_solutions = search_tree.solve()
        for i, d in enumerate(all_solutions):
            print(', '.join(map(lambda d: '{}: {}'.format(d.state.area, d.state.color), d.nodes)))
            c += 1

    print('Total with graph: {} ({} sec)'.format(c, time.time() - start))


if __name__ == '__main__':
    entry_point()
