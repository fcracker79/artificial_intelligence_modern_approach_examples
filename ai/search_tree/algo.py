import time

from ai.search_tree.node_expansion import expand_at_level
from ai.search_tree.print_tools import print_solution
from ai.search_tree.queuing_functions import depth_first
from ai.search_tree.search_tree import SearchTree
from ai.search_tree.common_types import Graph, Solution


def iterative_deepening_search(graph: Graph, from_node: str, to_node: str):
    start = time.time()
    best_solution = None  # type: Solution
    iterations = 0
    for max_depth in range(len(graph.nodes)):
        if best_solution and len(best_solution.nodes) <= max_depth:
            break
        search_tree = SearchTree(graph, from_node, to_node, expand_at_level(max_depth), depth_first)
        solution = search_tree.solve()
        iterations += search_tree.iterations
        if not solution:
            continue
        if not best_solution or solution.score < best_solution.score:
            best_solution = solution
    solution = Solution(nodes=best_solution.nodes, score=best_solution.score, iterations=iterations)
    stop = time.time()
    print_solution('Iterative deepening search', solution)
    print('Elapsed time', stop - start)
