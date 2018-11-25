from ai.search_tree.common_types import Graph


def create_example_graph(add_costs: bool=False) -> Graph:
    g = Graph()
    g.add_arch('Arad', 'Zerind', add_costs and 1 or 1)
    g.add_arch('Arad', 'Timsoara', add_costs and 2 or 1)
    g.add_arch('Arad', 'Sibiu', add_costs and 3 or 1)
    g.add_arch('Zerind', 'Oradea', add_costs and 1 or 1)
    g.add_arch('Oradea', 'Sibiu', add_costs and 4 or 1)
    g.add_arch('Timsoara', 'Lugoj', add_costs and 2 or 1)
    g.add_arch('Lugoj', 'Mehadia', add_costs and 1 or 1)
    g.add_arch('Mehadia', 'Dobreta', add_costs and 1 or 1)
    g.add_arch('Dobreta', 'Craovia', add_costs and 2 or 1)
    g.add_arch('Craovia', 'Rimnicu Vilcea', add_costs and 3 or 1)
    g.add_arch('Craovia', 'Pitesti', add_costs and 3 or 1)
    g.add_arch('Rimnicu Vilcea', 'Sibiu', add_costs and 1 or 1)
    g.add_arch('Rimnicu Vilcea', 'Pitesti', add_costs and 2 or 1)
    g.add_arch('Sibiu', 'Faragas', add_costs and 2 or 1)
    g.add_arch('Faragas', 'Bucharest', add_costs and 5 or 1)
    g.add_arch('Pitesti', 'Bucharest', add_costs and 3 or 1)
    g.add_arch('Bucharest', 'Giurgiu', add_costs and 2 or 1)
    g.add_arch('Bucharest', 'Urziceni', add_costs and 1 or 1)
    g.add_arch('Urziceni', 'Hisrova', add_costs and 2 or 1)
    g.add_arch('Urziceni', 'Vaslui', add_costs and 4 or 1)
    g.add_arch('Hisrova', 'Eforie', add_costs and 2 or 1)
    g.add_arch('Vaslui', 'Iasi', add_costs and 2 or 1)
    g.add_arch('Iasi', 'Neamt', add_costs and 2 or 1)
    return g
