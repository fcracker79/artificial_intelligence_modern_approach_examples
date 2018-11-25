import typing


class Graph:

    def __init__(self):
        self.arch_count = 0
        self.nodes = set()
        self.archs = dict()  # type: typing.Dict[str, typing.Set[str]]
        self.costs = dict()  # type: typing.Dict[str, int]

    def add_arch(self, node1, node2, cost: int=1):
        self.arch_count += 1
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.archs.setdefault(node1, set()).add(node2)
        self.archs.setdefault(node2, set()).add(node1)
        self.costs[','.join(sorted((node1, node2)))] = cost

    def get_cost(self, node1: str, node2: str) -> int:
        return self.costs[','.join(sorted((node1, node2)))]

    def get_children(self, node):
        return self.archs.get(node, [])


Node = typing.NamedTuple(
        'Node',
        (
            ('state', typing.Any),
            ('parent', typing.Optional['Node']),
            # ('operator', 'Boh'),
            ('depth', int),
            ('cost', int),
        )
    )


Solution = typing.NamedTuple(
    'Solution',
    (
        ('nodes', typing.List[Node]),
        ('score', int),
        ('iterations', int)
    )
)

QueuingFunction = typing.NewType(
    'QueuingFunction',
    typing.Callable[[typing.Deque[Node], typing.Sequence[Node]], typing.Deque[Node]]
)
