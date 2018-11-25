import binascii
import os
import random
import typing

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


def _generate_hex_node() -> str:
    return binascii.hexlify(os.urandom(16)).decode()


def create_big_graph(
        nodes: int, archs: int, node_generator: typing.Callable[[], str]=_generate_hex_node,
        add_costs: typing.Optional[bool]=None,
        cost_generator: typing.Optional[typing.Callable[[str, str], int]]=None) -> Graph:
    if add_costs is None and cost_generator is None:
        raise ValueError('Please specify either \'add_costs\' or \'cost_generator\'')
    g = Graph()
    nodes = [node_generator() for _ in range(nodes)]
    for _ in range(archs):
        node1, node2 = nodes[random.randint(0, len(nodes) - 1)], nodes[random.randint(0, len(nodes) - 1)]
        cost = cost_generator and cost_generator(node1, node2) or (add_costs and random.randint(1, len(nodes)) or 1)
        g.add_arch(node1, node2, cost)
    return g
