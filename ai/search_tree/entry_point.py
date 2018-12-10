import random

from ai.search_tree import example
from ai.search_tree.algo import iterative_deepening_search
from ai.search_tree.example import create_example_graph
from ai.search_tree.print_tools import header, print_algo
from ai.search_tree.queuing_functions import uniform_cost, breadth_first, depth_first, depth_limited_first


def _run_algos_random_graph(add_costs: bool):
    header('WITH COSTS' if add_costs else 'WITHOUT COSTS')
    # g = create_example_graph(add_costs=add_costs)
    g = example.create_big_graph(30, 30, add_costs=add_costs)
    node_list = list(g.nodes)
    from_node = node_list[random.randint(0, len(node_list) - 1)]
    to_node = node_list[random.randint(0, len(node_list) - 1)]
    print_algo('BREADTH FIRST', g, from_node, to_node, breadth_first)
    print_algo('DEPTH FIRST', g, from_node, to_node, depth_first)
    print_algo('UNIFORM COST', g, from_node, to_node, uniform_cost)
    print_algo('DEPTH FIRST LIMIT 3', g, from_node, to_node, depth_limited_first(3))
    iterative_deepening_search(g, from_node, to_node)


def _run_algos_romania(add_costs: bool):
    from_node, to_node = 'Arad', 'Bucharest'
    header('WITH COSTS' if add_costs else 'WITHOUT COSTS')
    g = create_example_graph(add_costs=add_costs)
    print_algo('BREADTH FIRST', g, from_node, to_node, breadth_first)
    print_algo('DEPTH FIRST', g, from_node, to_node, depth_first)
    print_algo('UNIFORM COST', g, from_node, to_node, uniform_cost)
    print_algo('DEPTH FIRST LIMIT 3', g, from_node, to_node, depth_limited_first(3))
    iterative_deepening_search(g, from_node, to_node)


def entry_point():
    _run_algos_romania(False)
    _run_algos_romania(True)


if __name__ == '__main__':
    entry_point()
